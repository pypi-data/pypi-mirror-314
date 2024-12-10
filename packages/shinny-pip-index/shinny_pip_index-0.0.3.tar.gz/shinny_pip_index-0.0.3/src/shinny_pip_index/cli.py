import argparse
import logging
import subprocess
import sys

from .server import run


def app():
    parser = argparse.ArgumentParser(
        prog='shinny-pip',
        description='simple pip index for shinny-cd private package',
        add_help=False,
    )
    parser.add_argument('install')  # positional argument
    parser.add_argument('-i', '--index-url')
    install, args = parser.parse_known_intermixed_args()
    assert install.install == "install", f"unsupported command: {install}"
    # 如果用户使用了 -- 分隔符， 那么可能会匹配到 positional 的 -v 和 --verbose 参数
    if "-v" in args or "--verbose" in args:
        logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
    port = run()
    subprocess.check_call(
        [sys.executable, "-m", "pip", "install"] + args + ["--index-url", f"http://localhost:{port}"])
