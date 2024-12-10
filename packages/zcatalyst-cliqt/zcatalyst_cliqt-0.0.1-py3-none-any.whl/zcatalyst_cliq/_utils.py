import os
import requests
from os import path
from pathlib import Path
from .error import CatalystError
from . import _constants as Constants


def get_function_root() -> str:
    home_dir = path.join(Path.home(), './')
    fn_root = find_func_root(home_dir, path.dirname(path.abspath(__file__)))
    if not fn_root:
        raise CatalystError(
            'Unable to get the function root', 2
        )
    os.environ['X_ZC_FUNCTION_ROOT'] = fn_root
    return fn_root


def find_func_root(home_dir, cur_dir):
    if os.getenv('X_ZC_FUNCTION_ROOT'):
        return os.getenv('X_ZC_FUNCTION_ROOT')
    if path.exists(path.join(cur_dir, Constants.CONFIG_JSON)):
        return cur_dir
    if path.normpath(cur_dir) == home_dir:
        return None
    return find_func_root(home_dir, path.join(cur_dir, '../'))


def send_request(method, url, **kwargs):
    return requests.request(
        method,
        url,
        headers={
            'User-Agent': Constants.USER_AGENT
        },
        **kwargs
    )
