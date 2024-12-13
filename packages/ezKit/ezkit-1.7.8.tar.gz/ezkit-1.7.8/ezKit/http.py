import json

import requests
from loguru import logger

from . import utils


def download(
    request: dict,
    file: dict,
    chunks: bool = False,
    iter_content: dict | None = None,
    echo: bool = False,
    info: str = None,
    debug: bool = False
) -> bool:
    "下载文件"

    if utils.v_true(request, dict):
        request_arguments = {'method': 'GET', 'stream': True, **request}
    else:
        return False

    if utils.v_true(file, dict):
        file_arguments = {'mode': 'wb', **file}
    else:
        return False

    if utils.v_true(iter_content, dict):
        iter_content_arguments = {'chunk_size': 1024, **iter_content}
    else:
        iter_content_arguments = {'chunk_size': 1024}

    info = f'下载 {info}' if utils.v_true(info, str) else f'下载'

    try:

        logger.info(f'{info} ......') if utils.v_true(echo, bool) else next

        response = requests.request(**request_arguments)

        with open(**file_arguments) as _file:

            if utils.v_true(chunks, bool):
                for _chunk in response.iter_content(**iter_content_arguments):
                    _file.write(_chunk)
            else:
                _file.write(response.content)

        logger.success(f'{info} [成功]') if utils.v_true(echo, bool) else next

        return True

    except Exception as e:
        logger.exception(e) if debug is True else next
        logger.error(f'{info} [失败]') if utils.v_true(echo, bool) else next
        return False


def response_json(
    data: any = None,
    debug: bool = False,
    **kwargs
) -> str:
    """解决字符编码问题: ensure_ascii=False"""
    try:
        return json.dumps(data, default=str, ensure_ascii=False, sort_keys=True, **kwargs)
    except Exception as e:
        logger.exception(e) if debug is True else next
        return None
