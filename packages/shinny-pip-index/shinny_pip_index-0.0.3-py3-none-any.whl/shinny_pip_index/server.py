import itertools
import json
import logging
import os
import pathlib
import re
import string
import threading
from collections import defaultdict
from functools import partial
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import List, Dict
from urllib.parse import urljoin

import oss2

logger = logging.getLogger("shinny-pip-index.server")


def distribution_package_name_normalize(name: str) -> str:
    # https://packaging.python.org/en/latest/specifications/binary-distribution-format/#escaping-and-unicode
    # 注意这个标准和pypi的normalize不同，pypi的normalize最终替换字符是'-'，而不是'_'
    return re.sub(r"[-_.]+", "_", name).lower()


def local_version_normalize(version: str) -> str:
    # https://packaging.python.org/en/latest/specifications/version-specifiers/#local-version-segments
    return version.replace('-', '.').replace('_', '.').lower()


def find_shinny_cd_projects(bucket: oss2.Bucket) -> Dict[str, List[str]]:
    """
    查找 shinny cd 项目并按照规范返回符合的项目
    :return:
    """
    services: Dict[str, List[str]] = defaultdict(list)
    # 列举fun文件夹下的文件与子文件夹名称，不列举子文件夹下的文件
    for obj in oss2.ObjectIteratorV2(bucket, prefix='', delimiter='/', max_keys=1000):
        service = obj.key.split('/')[0]
        service_normalized = distribution_package_name_normalize(service)
        services[service_normalized].append(service)
    logger.debug(f"Found services: {services}")
    return services


# define a class to handle the request
# this class will inherit from BaseHTTPRequestHandler
# and override the do_GET method
# this method will meet the requirements of the pypi json-based-simple-api-for-python-package-indexes
class ShinnyIndexRequestHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, services: Dict[str, List[str]], bucket: oss2.Bucket, public_index: str, **kwargs):
        self.services = services
        self.bucket = bucket
        self.public_index = public_index
        super().__init__(*args, **kwargs)

    def do_GET(self):
        # get the package name and version from the request
        # pip 会进行normalize，全小写字母，下划线转换为短横线
        pkg_name = self.path.split('/')[1]
        files = self.check_shinny_cd_projects(pkg_name)
        if not files:
            # exact package name not found
            self.redirect_to_public_index()
            return

        # set the response code to 200
        self.send_response(200)
        # set the response headers
        self.send_header('Content-type', 'application/vnd.pypi.simple.v1+json')
        self.end_headers()

        result = {
            "meta": {
                "api-version": "1.0"
            },
            "name": pkg_name,
            "files": files,
        }
        logger.debug(f"Response: {result}")
        self.wfile.write(json.dumps(result).encode())

    def redirect_to_public_index(self):
        self.send_response(302)
        # self.public_index 必须以 / 结尾
        self.send_header('Location', urljoin(self.public_index, self.path.lstrip('/')))
        self.end_headers()

    def check_shinny_cd_projects(self, name: str) -> List[Dict[str, str]]:
        """
        查找 shinny cd 项目并按照规范返回符合的项目
        :return:
        """
        name = distribution_package_name_normalize(name)
        pkg_names = set()
        pkg_name_parts = name.split('_')
        for i in range(len(pkg_name_parts)):
            pkg_names.add('_'.join(pkg_name_parts[:i + 1]))
        # reverse alphabet order, for example: [otg_sim_dag, otg_sim, otg]
        for service in sorted(list(pkg_names & self.services.keys()), reverse=True):
            logger.debug(f"Request: {self.path}, service: {service}")
            files = self.get_packages(service, name)
            if files:
                return files
        return []

    def get_packages(self, service: str, name: str) -> List[Dict[str, str]]:
        """
        获取指定服务的指定包版本信息
        :param service: 服务名称
        :param name: sdist包名称
        :return: pypi标注的包信息
        """
        # 列举 "<service>/" 文件夹下所有对象
        files = []
        # make sure the package name is normalized
        package_name = distribution_package_name_normalize(name)
        folders = self.services[service]
        logger.debug(f"Searching for package: {package_name} in {','.join(folders)}")
        for obj in itertools.chain.from_iterable(oss2.ObjectIteratorV2(self.bucket, prefix=f'{service_folder}/', max_keys=1000) for service_folder in folders):
            filename = pathlib.Path(obj.key).name
            path_parts = obj.key.split('/')
            if len(path_parts) < 3:
                # skip irrelevant objects
                continue

            # 允许所有符合python版本规范的版本号
            python_version_regex = r'([1-9][0-9]*!)?(0|[1-9][0-9]*)(\.(0|[1-9][0-9]*))*((a|b|rc)(0|[1-9][0-9]*))?(\.post(0|[1-9][0-9]*))?(\.dev(0|[1-9][0-9]*))?'
            # try extract branch/commit or tag from obj.key
            commit = path_parts[2] if len(path_parts[2]) == 7 and all(c in string.hexdigits for c in path_parts[2]) else None
            tag_version = path_parts[1] if re.fullmatch(rf'^{python_version_regex}$', path_parts[1]) else None
            if tag_version and not commit:
                # tag
                # 预防branch名称符合tag规范 （代码库内文件夹名称符合commit特征的可能性较低）
                file_prefix_pattern = re.compile(
                    rf"^{re.escape(package_name)}-{re.escape(tag_version)}.*\.(tar\.gz|whl)$")
            elif commit:
                # branch/commit
                local_version = local_version_normalize(f"{path_parts[1]}.{path_parts[2]}")
                file_prefix_pattern = re.compile(
                    rf"^{re.escape(package_name)}-{python_version_regex}\+{re.escape(local_version)}.*\.(tar\.gz|whl)$")
            else:
                # skip irrelevant objects
                continue

            if re.fullmatch(file_prefix_pattern, filename):
                logger.debug(f"Found package: {filename}")
                files.append({
                    "filename": filename,
                    "url": urljoin("https://shinny-cd.oss-cn-shanghai-internal.aliyuncs.com/", obj.key),
                    "hashes": {},
                })
        return files


# define a function to start the server
def run(port=0) -> int:
    """
    启动临时index server
    考虑到extra index也需要响应所有的请求，因此需要提前预载service信息，bypass公有库的请求
    :return:
    """
    try:
        shinny_cd = oss2.Bucket(oss2.AnonymousAuth(), 'oss-cn-shanghai-internal.aliyuncs.com', 'shinny-cd')
        services = find_shinny_cd_projects(shinny_cd)
    except Exception:
        # log the error and set shinny_cd to None
        # all package requests will be redirected to the public index
        logger.error(f"Failed to load shinny-cd projects", exc_info=True)
        logger.warning("All requests will be redirected to the public index")
        shinny_cd = None
        services = {}
    server_address = ('localhost', port)
    # get the public index url
    public_index = os.getenv('SHINNY_PIP_INDEX_URL', 'http://mirrors.cloud.aliyuncs.com/pypi/simple/')
    # using partial to pass the services to the handler class constructor
    handler_class = partial(ShinnyIndexRequestHandler, services=services, bucket=shinny_cd, public_index=public_index)
    server = ThreadingHTTPServer(server_address, handler_class)
    logger.info(f'Starting server on {server.server_name}:{server.server_port}')
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()
    return server.server_port
