from typing import Callable

from . import bottle, utils


def enable_cors(fn: Callable) -> Callable:
    """
    Bottle CORS
    """
    """
    参考文档:
    - https://stackoverflow.com/a/17262900
    - https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Access-Control-Allow-Headers
    - https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Access-Control-Allow-Methods
    - https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Access-Control-Allow-Origin
    """
    def cors(*args, **kwargs):
        bottle.response.headers['Access-Control-Allow-Headers'] = '*'
        bottle.response.headers['Access-Control-Allow-Methods'] = '*'
        bottle.response.headers['Access-Control-Allow-Origin'] = '*'
        if bottle.request.method != 'OPTIONS':
            return fn(*args, **kwargs)
    return cors

def request_json() -> dict | None:
    """
    Bottle Request JSON
    """
    try:
        data: dict = bottle.request.json
        if utils.v_true(data, dict):
            return data
        else:
            return None
    except:
        return None
