"""
Python Utils
"""
import csv
import datetime
import hashlib
import json
import os
import subprocess
import time
import tomllib
from copy import deepcopy
from multiprocessing import Pool, Process
from multiprocessing.pool import ThreadPool
from pathlib import Path
from shutil import rmtree
from threading import Thread
from typing import Any, Callable, List, Optional, Union
from urllib.parse import ParseResult, urlparse
from uuid import uuid4

from loguru import logger

# --------------------------------------------------------------------------------------------------


# None Type
NoneType = type(None)


# --------------------------------------------------------------------------------------------------


def v_true(
    v_instance: Any,
    v_type: Any = None,
    true_list: list | tuple | set | str | None = None,
    false_list: list | tuple | set | str | None = None,
    debug: bool = False
) -> bool:
    """
    检查变量类型以及变量是否为 True

    常见类型:

        Boolean     bool            False
        Numbers     int/float       0/0.0
        String      str             ""
        List        list/tuple/set  []/()/{}
        Dictionary  dict            {}

    函数使用 callable(func) 判断
    """

    try:

        if isinstance(v_instance, v_type):

            if all(
                [
                    true_list is not None,
                    false_list is None,
                    isinstance(true_list, (list, tuple, set, str))
                ]
            ):
                return v_instance in true_list

            if all(
                [
                    true_list is None,
                    false_list is not None,
                    isinstance(false_list, (list, tuple, set, str))
                ]
            ):
                return v_instance not in false_list

            if all(
                [
                    true_list is not None,
                    false_list is not None,
                    isinstance(true_list, (list, tuple, set, str)),
                    isinstance(false_list, (list, tuple, set, str))
                ]
            ):
                return (v_instance in true_list) and (v_instance not in false_list)

            return v_instance not in [False, None, 0, 0.0, '', (), [], {*()}, {*[]}, {*{}}, {}]

        return False

    except Exception as e:
        if v_true(debug, bool):
            logger.exception(e)
        return False


# --------------------------------------------------------------------------------------------------


def os_environ(
    name: str,
    value: Any = None,
    debug: bool = False
) -> Any:
    """
    系统变量

    伪全局变量
    Python 没有全局变量, 多个文件无法调用同一个变量.
    为了解决这个问题, 将变量设置为系统变量, 从而实现多个文件调用同一个变量.
    """
    try:

        # 变量名添加一个前缀, 防止和系统中其它变量名冲突
        _variable_name = f'PYTHON_VARIABLE_{name}'

        if value is None:

            _data = os.environ.get(_variable_name)

            # 判断是否有数据
            if _data:
                try:
                    # 如果环境变量有值, 使用 json.loads() 解析
                    parsed_data = json.loads(_data)
                    return parsed_data
                except json.JSONDecodeError:
                    return None
            else:
                return None

        _data = json.dumps(value)
        os.environ[_variable_name] = _data

        return value

    except Exception as e:
        if v_true(debug, bool):
            logger.exception(e)
        return None


# --------------------------------------------------------------------------------------------------


def mam_of_numbers(
    numbers: list | tuple,
    dest_type: str | None = None,
    debug: bool = False
) -> tuple[int | float, int | float, int | float] | tuple[None, None, None]:
    """
    (maximum, average, minimum)

    返回一组数字中的 最大值(maximum), 平均值(average), 最小值(minimum)
    numbers 数字列表 (仅支持 list 和 tuple, 不支 set)
    dest_type 目标类型 (将数字列表中的数字转换成统一的类型)
    """

    try:
        _numbers = deepcopy(numbers)
        match True:
            case True if dest_type == 'float':
                _numbers = [float(i) for i in numbers]
            case True if dest_type == 'int':
                _numbers = [int(i) for i in numbers]
        _num_max = max(_numbers)
        _num_avg = sum(_numbers) / len(_numbers)
        _num_min = min(_numbers)
        return _num_max, _num_avg, _num_min
    except Exception as e:
        if v_true(debug, bool):
            logger.exception(e)
        return None, None, None


# --------------------------------------------------------------------------------------------------


def step_number_for_split_equally(
    integer: int,
    split_equally_number: int,
    debug: bool = False
) -> int | None:
    """
    step number for split equally

    平分数字的步长

      integer 数字
      split_equally_number 平分 integer 的数字

    示例:

        [1, 2, 3, 4, 5, 6, 7, 8, 9]

        分成 2 份 -> [[1, 2, 3, 4, 5], [6, 7, 8, 9]]        -> 返回 5
        分成 3 份 -> [[1, 2, 3], [4, 5, 6], [7, 8, 9]]      -> 返回 3
        分成 4 份 -> [[1, 2, 3], [4, 5], [6, 7], [8, 9]]    -> 返回 3
        分成 5 份 -> [[1, 2], [3, 4], [5, 6], [7, 8], [9]]  -> 返回 2
    """
    try:
        if integer % split_equally_number == 0:
            return int(integer / split_equally_number)
        return int(integer / split_equally_number) + 1
    except Exception as e:
        if v_true(debug, bool):
            logger.exception(e)
        return None


# --------------------------------------------------------------------------------------------------


def division(
    dividend: int | float,
    divisor: int | float,
    debug: bool = False
) -> float | None:
    """Division"""
    try:
        return dividend / divisor
    except Exception as e:
        if v_true(debug, bool):
            logger.exception(e)
        return None


def divisor_1000(
    dividend: int | float,
    debug: bool = False
) -> float | None:
    """Division (divisor: 1000)"""
    # 除法, 除以 1000
    try:
        return dividend / 1000
    except Exception as e:
        if v_true(debug, bool):
            logger.exception(e)
        return None


def divisor_1024(
    dividend: int | float,
    debug: bool = False
) -> float | None:
    """Division (divisor: 1024)"""
    # 除法, 除以 1024
    try:
        return dividend / 1024
    except Exception as e:
        if v_true(debug, bool):
            logger.exception(e)
        return None


def divisor_square_1000(
    dividend: int | float,
    debug: bool = False
) -> float | None:
    """Division (divisor: 1000*1000)"""
    try:
        return dividend / (1000 * 1000)
    except Exception as e:
        if v_true(debug, bool):
            logger.exception(e)
        return None


def divisor_square_1024(
    dividend: int | float,
    debug: bool = False
) -> float | None:
    """Division (divisor: 1024*1024)"""
    try:
        return dividend / (1024 * 1024)
    except Exception as e:
        if v_true(debug, bool):
            logger.exception(e)
        return None


# --------------------------------------------------------------------------------------------------


def check_file_type(
    file_object: str,
    file_type: str,
    debug: bool = False
) -> bool:
    """
    check file type

    检查文件类型

        file_object 文件对象
        file_type 文件类型
    """
    try:

        _file_path = Path(file_object)

        match True:
            case True if _file_path.exists() is False:
                result = False
            case True if file_type == 'absolute' and _file_path.is_absolute() is True:
                result = True
            case True if file_type == 'block_device' and _file_path.is_block_device() is True:
                result = True
            case True if file_type == 'dir' and _file_path.is_dir() is True:
                result = True
            case True if file_type == 'fifo' and _file_path.is_fifo() is True:
                result = True
            case True if file_type == 'file' and _file_path.is_file() is True:
                result = True
            case True if file_type == 'mount' and _file_path.is_mount() is True:
                result = True
            case True if file_type == 'relative_to' and _file_path.is_relative_to() is True:
                result = True
            case True if file_type == 'reserved' and _file_path.is_reserved() is True:
                result = True
            case True if file_type == 'socket' and _file_path.is_socket() is True:
                result = True
            case True if file_type == 'symlink' and _file_path.is_symlink() is True:
                result = True
            case _:
                result = False

        return result

    except Exception as e:
        if v_true(debug, bool):
            logger.exception(e)
        return False


# --------------------------------------------------------------------------------------------------


def list_sort(
    data: list,
    deduplication: bool = False,
    debug: bool = False,
    **kwargs
) -> list | None:
    """list sort"""
    # 列表排序, 示例: list_sort(['1.2.3.4', '2.3.4.5'], key=inet_aton)
    # 参考文档:
    #     https://stackoverflow.com/a/4183538
    #     https://blog.csdn.net/u013541325/article/details/117530957
    try:

        # from ipaddress import ip_address
        # _ips = [str(i) for i in sorted(ip_address(ip.strip()) for ip in ips)]
        # 注意: list.sort() 是直接改变 list, 不会返回 list

        # 拷贝数据, 去重, 排序, 返回
        _data = deepcopy(data)
        if deduplication is True:
            _data = list(set(_data))
        _data.sort(**kwargs)
        return _data

    except Exception as e:
        if v_true(debug, bool):
            logger.exception(e)
        return None


def list_dict_sorted_by_key(
    data: list | tuple,
    key: str,
    debug: bool = False,
    **kwargs
) -> list | None:
    """list dict sorted by key"""
    # 列表字典排序
    # 参考文档: https://stackoverflow.com/a/73050
    try:
        _data = deepcopy(data)
        return sorted(_data, key=lambda x: x[key], **kwargs)
    except Exception as e:
        if v_true(debug, bool):
            logger.exception(e)
        return None


def list_split(
    data: list,
    number: int,
    equally: bool = False,
    debug: bool = False
) -> list | None:
    """list split"""
    # 列表分割
    #
    # 默认: 将 list 以 number个元素为一个list 分割
    #
    #     data = [1, 2, 3, 4, 5, 6, 7]
    #
    #     list_split(data, 2) -> 将 data 以 2个元素为一个 list 分割
    #     [[1, 2], [3, 4], [5, 6], [7]]
    #
    #     list_split(data, 3) -> 将 data 以 3个元素为一个 list 分割
    #     [[1, 2, 3], [4, 5, 6], [7]]
    #
    # equally 为 True 时, 将 data 平均分成 number 份
    #
    #     data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]
    #
    #     list_split_equally(data, 5) -> 将 data 平均分成 5 份
    #     [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16], [17, 18, 19]]
    #
    #     list_split_equally(data, 6) -> 将 data 平均分成 6 份
    #     [[1, 2, 3, 4], [5, 6, 7], [8, 9, 10], [11, 12, 13], [14, 15, 16], [17, 18, 19]]
    #
    #     list_split_equally(data, 7) -> 将 data 平均分成 7 份
    #     [[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12], [13, 14, 15], [16, 17], [18, 19]]

    try:

        # 数据拷贝
        _data_object = deepcopy(data)

        # 数据长度
        _data_length = len(_data_object)

        # 数据平分后的结果
        _data_result = []

        _step_number: Optional[int] = None

        if v_true(debug, bool):
            logger.info(f"data object: {_data_object}")
            logger.info(f"data length: {_data_length}")

        if _data_length < number:
            if v_true(debug, bool):
                logger.error('number must greater than data length')
            return None

        if _data_length == number:

            _data_result = [[i] for i in _data_object]

        else:

            if equally is True:

                _step_number = step_number_for_split_equally(_data_length, number, debug=debug)

                if v_true(debug, bool):
                    logger.info(f"step number: {_step_number}")

                if _data_length % number == 0:

                    index_number_list = list(range(0, _data_length, number))

                    if v_true(debug, bool):
                        logger.info(f"index number list: {index_number_list}")

                    for index_number in index_number_list:

                        if v_true(debug, bool):
                            logger.info(f"index: {index_number}, data: {_data_object[index_number:index_number + number]}")

                        _data_result.append(deepcopy(_data_object[index_number:index_number + number]))

                else:

                    # 前一部分
                    if _step_number is not None:
                        previous_end_number = (_data_length % number) * _step_number
                        previous_index_number_list = list(range(0, previous_end_number, _step_number))
                        for index_number in previous_index_number_list:
                            _data_result.append(deepcopy(_data_object[index_number:index_number + _step_number]))

                        # 后一部分
                        next_number_list = list(range(previous_end_number, _data_length, _step_number - 1))
                        for index_number in next_number_list:
                            _data_result.append(deepcopy(_data_object[index_number:index_number + (_step_number - 1)]))

            else:

                for index_number in list(range(0, _data_length, number)):
                    _data_result.append(deepcopy(_data_object[index_number:index_number + number]))

        return _data_result

    except Exception as e:
        if v_true(debug, bool):
            logger.exception(e)
        return None


def list_print_by_step(
    data: list,
    number: int,
    separator: str | None = None,
    debug: bool = False
) -> bool:
    """
    list print by step

    列表按照 步长 和 分隔符 有规律的输出
    """
    try:

        _data_list = list_split(data, number, debug=debug)

        if _data_list is None:
            return False

        for _item in _data_list:
            print(*_item, sep=separator)

        return True

    except Exception as e:
        if v_true(debug, bool):
            logger.exception(e)
        return False


def list_remove_list(
    original: list,
    remove: list,
    debug: bool = False
) -> list | None:
    """List remove List"""
    try:
        _original = deepcopy(original)
        _remove = deepcopy(remove)
        return [i for i in _original if i not in _remove]
    except Exception as e:
        if v_true(debug, bool):
            logger.exception(e)
        return None


def list_merge(
    data: list,
    debug: bool = False
) -> list | None:
    """list merge"""
    # 合并 List 中的 List 为一个 List
    try:
        _results = []
        for i in deepcopy(data):
            _results += i
        return _results
    except Exception as e:
        if v_true(debug, bool):
            logger.exception(e)
        return None


def list_to_file(
    data: list,
    file: str,
    encoding: str = 'utf-8-sig',
    debug: bool = False
) -> bool:
    """list to file"""
    try:
        with open(file, 'w', encoding=encoding) as _file:
            for line in data:
                _file.write(f"{line}\n")
        return True
    except Exception as e:
        if v_true(debug, bool):
            logger.exception(e)
        return False

def list_to_csvfile(
    data: list,
    file: str,
    fields: list | None = None,
    encoding: str = 'utf-8-sig',
    debug: bool = False,
    **kwargs
) -> bool:
    """list to csvfile"""
    try:
        with open(file, 'w', encoding=encoding) as _file:
            # CRLF replaced by LF
            # https://stackoverflow.com/a/29976091
            outcsv = csv.writer(_file, lineterminator=os.linesep, **kwargs)
            if v_true(fields, list) and fields is not None:
                outcsv.writerow(fields)
            outcsv.writerows(data)
        return True
    except Exception as e:
        if v_true(debug, bool):
            logger.exception(e)
        return False

def range_zfill(
    start: int,
    stop: int,
    step: int,
    width: int,
    debug: bool = False
) -> list | None:
    """range zfill"""
    # 生成长度相同的字符串的列表
    # 示例: range_zfill(8, 13, 1, 2) => ['08', '09', '10', '11', '12']
    # 生成 小时 列表: range_zfill(0, 24, 1, 2)
    # 生成 分钟和秒 列表: range_zfill(0, 60, 1, 2)
    # https://stackoverflow.com/a/733478
    # the zfill() method to pad a string with zeros
    try:
        return [str(i).zfill(width) for i in range(start, stop, step)]
    except Exception as e:
        if v_true(debug, bool):
            logger.exception(e)
        return None


# --------------------------------------------------------------------------------------------------


def dict_remove_key(
    data: dict,
    key: str,
    debug: bool = False
) -> None | dict:
    """dict remove key"""
    try:
        data_copy: dict = deepcopy(data)
        data_copy.pop(key)
        return data_copy
    except Exception as e:
        if v_true(debug, bool):
            logger.exception(e)
        return None

def dict_to_file(
    data: dict,
    file: str,
    encoding: str = 'utf-8-sig',
    debug: bool = False,
    **kwargs
) -> bool:
    """dict to file"""
    try:
        with open(file, 'w', encoding=encoding) as _file:
            json.dump(obj=data, fp=_file, indent=4, sort_keys=True, **kwargs)
        return True
    except Exception as e:
        if v_true(debug, bool):
            logger.exception(e)
        return False


def dict_nested_update(
    data: dict,
    key: str,
    value: Any,
    debug: bool = False
) -> bool:
    """dict nested update"""
    # dictionary nested update
    # https://stackoverflow.com/a/58885744
    try:

        if not v_true(data, dict, debug=debug):
            return False

        for _k, _v in data.items():
            # callable() 判断是非为 function
            if (key is not None and key == _k) or (callable(key) is True and key == _k):
                if callable(value) is True:
                    data[_k] = value()
                else:
                    data[_k] = value
            elif isinstance(_v, dict) is True:
                dict_nested_update(_v, key, value)
            elif isinstance(_v, list) is True:
                for _o in _v:
                    if isinstance(_o, dict):
                        dict_nested_update(_o, key, value)
            else:
                pass

        return True

    except Exception as e:
        if v_true(debug, bool):
            logger.exception(e)
        return False


# --------------------------------------------------------------------------------------------------


def filename(
    file: str,
    split: str = '.',
    debug: bool = False
) -> str | None:
    """filename"""
    # 获取文件名称
    # https://stackoverflow.com/questions/678236/how-do-i-get-the-filename-without-the-extension-from-a-path-in-python
    # https://stackoverflow.com/questions/4152963/get-name-of-current-script-in-python
    try:

        if v_true(debug, bool):
            logger.info(f"file: {file}")
            logger.info(f"split: {split}")

        _basename = str(os.path.basename(file))

        if v_true(debug, bool):
            logger.info(f"basename: {_basename}")

        _index_of_split = _basename.index(split)

        if v_true(debug, bool):
            logger.info(f"index of split: {_index_of_split}")
            logger.info(f"filename: {_basename[:_index_of_split]}")

        return _basename[:_index_of_split]

    except Exception as e:
        if v_true(debug, bool):
            logger.exception(e)
        return None


def filehash(
    file: str,
    sha: str = 'md5',
    debug: bool = False
) -> str | None:
    """filehash"""
    # 获取文件Hash
    # 参考文档:
    #     https://stackoverflow.com/a/59056837
    #     https://stackoverflow.com/questions/22058048/hashing-a-file-in-python
    try:
        with open(file, "rb") as _file:
            match True:
                case True if sha == 'sha1':
                    file_hash = hashlib.sha1()
                case True if sha == 'sha224':
                    file_hash = hashlib.sha224()
                case True if sha == 'sha256':
                    file_hash = hashlib.sha256()
                case True if sha == 'sha384':
                    file_hash = hashlib.sha384()
                case True if sha == 'sha512':
                    file_hash = hashlib.sha512()
                case True if sha == 'sha3_224':
                    file_hash = hashlib.sha3_224()
                case True if sha == 'sha3_256':
                    file_hash = hashlib.sha3_256()
                case True if sha == 'sha3_384':
                    file_hash = hashlib.sha3_384()
                case True if sha == 'sha3_512':
                    file_hash = hashlib.sha3_512()
                # case True if sha == 'shake_128':
                #     file_hash = hashlib.shake_128()
                # case True if sha == 'shake_256':
                #     file_hash = hashlib.shake_256()
                case _:
                    file_hash = hashlib.md5()
            # 建议设置为和 block size 相同的值, 多数系统默认为 4096, 可使用 stat 命令查看
            # stat / (IO Block)
            # stat -f / (Block size)
            while chunk := _file.read(4096):
                file_hash.update(chunk)
            return file_hash.hexdigest()
    except Exception as e:
        if v_true(debug, bool):
            logger.exception(e)
        return None


def filesize(
    file: str,
    debug: bool = False
) -> int | None:
    """filesize"""
    # 获取文件大小
    try:
        return os.path.getsize(file)
    except Exception as e:
        if v_true(debug, bool):
            logger.exception(e)
        return None


# --------------------------------------------------------------------------------------------------


# def resolve_path() -> str | None:
#     """resolve path"""
#     # 获取当前目录名称
#     return str(Path().resolve())


# def parent_path(
#     path: str,
#     debug: bool = False,
#     **kwargs
# ) -> str | None:
#     """获取父目录名称"""
#     try:
#         return str(Path(path, **kwargs).parent.resolve()) if v_true(path, str, debug=debug) else None
#     except Exception as e:
#         if v_true(debug, bool):
#             logger.exception(e)
#         return None


def realpath(
    path: str,
    debug: bool = False,
    **kwargs
) -> str | None:
    """获取对象真实路径"""
    try:
        # if v_true(debug, bool):
        #     logger.info(f"path: {path}")
        # return os.path.realpath(path, **kwargs)
        if v_true(path, str, debug=debug) is False:
            return None
        return str(Path(path, **kwargs).resolve())
    except Exception as e:
        if v_true(debug, bool):
            logger.exception(e)
        return None


def current_dir(
    path: str,
    debug: bool = False,
    **kwargs
) -> str | None:
    """获取对象所在目录"""
    try:
        if v_true(path, str, debug=debug) is False:
            return None
        return str(Path(path, **kwargs).parent.resolve())
    except Exception as e:
        if v_true(debug, bool):
            logger.exception(e)
        return None


def parent_dir(
    path: str,
    debug: bool = False,
    **kwargs
) -> str | None:
    """获取对象所在目录的父目录"""
    try:
        if v_true(path, str, debug=debug) is False:
            return None
        return str(Path(path, **kwargs).parent.parent.resolve())
    except Exception as e:
        if v_true(debug, bool):
            logger.exception(e)
        return None


# --------------------------------------------------------------------------------------------------


def retry(
    times: int,
    func: Callable,
    debug: bool = False,
    **kwargs
):
    """重试"""
    # 函数传递参数: https://stackoverflow.com/a/803632
    # callable() 判断类型是非为函数: https://stackoverflow.com/a/624939
    try:
        _num = 0
        while True:
            # 重试次数判断 (0 表示无限次数, 这里条件使用 > 0, 表示有限次数)
            if times > 0:
                _num += 1
                if _num > times:
                    return
            # 执行函数
            try:
                return func(**kwargs)
            except Exception as e:
                if v_true(debug, bool):
                    logger.exception(e)
                logger.success('retrying ...')
                continue
            # break
    except Exception as e:
        if v_true(debug, bool):
            logger.exception(e)


# --------------------------------------------------------------------------------------------------

# 日期时间有两种: UTC datetime (UTC时区日期时间) 和 Local datetime (当前时区日期时间)
#
# Unix Timestamp 仅为 UTC datetime 的值
#
# 但是, Local datetime 可以直接转换为 Unix Timestamp, UTC datetime 需要先转换到 UTC TimeZone 再转换为 Unix Timestamp
#
# 相反, Unix Timestamp 可以直接转换为 UTC datetime, 要获得 Local datetime, 需要再将 UTC datetime 转换为 Local datetime
#
#     https://stackoverflow.com/a/13287083
#     https://stackoverflow.com/a/466376
#     https://stackoverflow.com/a/7999977
#     https://stackoverflow.com/a/3682808
#     https://stackoverflow.com/a/63920772
#     https://www.geeksforgeeks.org/how-to-remove-timezone-information-from-datetime-object-in-python/
#
# pytz all timezones
#
#     https://stackoverflow.com/a/13867319
#     https://stackoverflow.com/a/15692958
#
#     import pytz
#     pytz.all_timezones
#     pytz.common_timezones
#     pytz.timezone('US/Eastern')
#
# timezone
#
#     https://stackoverflow.com/a/39079819
#     https://stackoverflow.com/a/1681600
#     https://stackoverflow.com/a/4771733
#     https://stackoverflow.com/a/63920772
#     https://toutiao.io/posts/sin4x0/preview
#
# 其它:
#
#     dt.replace(tzinfo=timezone.utc).astimezone(tz=None)
#
#     (dt.replace(tzinfo=timezone.utc).astimezone(tz=None)).strftime(format)
#     datetime.fromisoformat((dt.replace(tzinfo=timezone.utc).astimezone(tz=None)).strftime(format))
#     string_to_datetime((dt.replace(tzinfo=timezone.utc).astimezone(tz=None)).strftime(format), format)
#
#     datetime.fromisoformat(time.strftime(format, time.gmtime(dt)))


def date_to_datetime(
    date_object: datetime.datetime,
    debug: bool = False
) -> datetime.datetime | None:
    """'日期'转换为'日期时间'"""
    # https://stackoverflow.com/a/1937636
    try:
        return datetime.datetime.combine(date_object, datetime.datetime.min.time())
    except Exception as e:
        if v_true(debug, bool):
            logger.exception(e)
        return None


def datetime_to_date(
    datetime_instance: datetime.datetime,
    debug: bool = False
) -> datetime.date | None:
    """'日期时间'转换为'日期'"""
    # https://stackoverflow.com/a/3743240
    try:
        return datetime_instance.date()
    except Exception as e:
        if v_true(debug, bool):
            logger.exception(e)
        return None


def local_timezone():
    """获取当前时区"""
    return datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo


def datetime_now(
        debug: bool = False,
        **kwargs
) -> datetime.datetime | None:
    """获取当前日期和时间"""
    _utc = kwargs.pop("utc", False)
    try:
        return datetime.datetime.utcnow() if _utc is True else datetime.datetime.now(**kwargs)
    except Exception as e:
        if v_true(debug, bool):
            logger.exception(e)
        return None


def datetime_offset(
    datetime_instance: datetime.datetime,
    debug: bool = False,
    **kwargs
) -> datetime.datetime | None:
    """
    获取 '向前或向后特定日期时间' 的日期和时间

    类型: weeks, days, hours, minutes, seconds, microseconds, milliseconds
    """
    _utc = kwargs.pop("utc", False)
    try:
        if isinstance(datetime_instance, datetime.datetime):
            return datetime_instance + datetime.timedelta(**kwargs)
        return datetime.datetime.utcnow() + datetime.timedelta(**kwargs) if _utc is True else datetime.datetime.now() + datetime.timedelta(**kwargs)
    except Exception as e:
        if v_true(debug, bool):
            logger.exception(e)
        return None


def datetime_to_string(
    datetime_instance: datetime.datetime,
    string_format: str = '%Y-%m-%d %H:%M:%S',
    debug: bool = False
) -> str | None:
    """'日期时间'转换为'字符串'"""
    try:
        return datetime.datetime.strftime(datetime_instance, string_format) if isinstance(datetime_instance, datetime.datetime) is True else None
    except Exception as e:
        if v_true(debug, bool):
            logger.exception(e)
        return None


def datetime_to_timestamp(
    datetime_instance: datetime.datetime,
    utc: bool = False,
    debug: bool = False
) -> int | None:
    """
    Datatime 转换为 Unix Timestamp
    Local datetime 可以直接转换为 Unix Timestamp
    UTC datetime 需要先替换 timezone 再转换为 Unix Timestamp
    """
    try:
        if isinstance(datetime_instance, datetime.datetime):
            return int(datetime_instance.replace(tzinfo=datetime.timezone.utc).timestamp()) if utc is True else int(datetime_instance.timestamp())
        return None
    except Exception as e:
        if v_true(debug, bool):
            logger.exception(e)
        return None


def datetime_local_to_timezone(
    datetime_instance: datetime.datetime,
    tz: datetime.timezone = datetime.timezone.utc,
    debug: bool = False
) -> datetime.datetime | None:
    """
    Local datetime to TimeZone datetime (默认转换为 UTC datetime)
    replace(tzinfo=None) 移除结尾的时区信息
    """
    try:
        if isinstance(datetime_instance, datetime.datetime) is True:
            return (datetime.datetime.fromtimestamp(datetime_instance.timestamp(), tz=tz)).replace(tzinfo=None)
        else:
            return None
    except Exception as e:
        if v_true(debug, bool):
            logger.exception(e)
        return None


def datetime_utc_to_timezone(
    datetime_instance: datetime.datetime,
    tz: Any = datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo,
    debug: bool = False
) -> datetime.datetime | None:
    """
    UTC datetime to TimeZone datetime (默认转换为 Local datetime)
    replace(tzinfo=None) 移除结尾的时区信息
    """
    try:
        if isinstance(datetime_instance, datetime.datetime) is True:
            return datetime_instance.replace(tzinfo=datetime.timezone.utc).astimezone(tz).replace(tzinfo=None)
        else:
            return None
    except Exception as e:
        if v_true(debug, bool):
            logger.exception(e)
        return None


def timestamp_to_datetime(
    timestamp: int,
    tz: datetime.timezone = datetime.timezone.utc,
    debug: bool = False
) -> datetime.datetime | None:
    """Unix Timestamp 转换为 Datatime"""
    try:
        return (datetime.datetime.fromtimestamp(timestamp, tz=tz)).replace(tzinfo=None) if v_true(timestamp, int, debug=debug) else None
    except Exception as e:
        if v_true(debug, bool):
            logger.exception(e)
        return None


def datetime_string_to_datetime(
    datetime_string: str,
    datetime_format: str = '%Y-%m-%d %H:%M:%S',
    debug: bool = False
) -> datetime.datetime | None:
    """datetime string to datetime"""
    try:
        return datetime.datetime.strptime(datetime_string, datetime_format) if v_true(datetime_string, str, debug=debug) else None
    except Exception as e:
        if v_true(debug, bool):
            logger.exception(e)
        return None


def datetime_string_to_timestamp(
    datetime_string: str,
    datetime_format: str = '%Y-%m-%d %H:%M:%S',
    debug: bool = False
) -> int | None:
    """datetime string to timestamp"""
    try:
        return int(time.mktime(time.strptime(datetime_string, datetime_format))) if v_true(datetime_string, str, debug=debug) else None
    except Exception as e:
        if v_true(debug, bool):
            logger.exception(e)
        return None


def datetime_object(
    date_time: datetime.datetime,
    debug: bool = False
) -> dict | None:
    """datetime object"""
    try:
        return {
            'date': date_time.strftime("%Y-%m-%d"),
            'time': date_time.strftime("%H:%M:%S"),
            'datetime_now': date_time.strftime("%Y-%m-%d %H:%M:%S"),
            'datetime_minute': date_time.strftime("%Y-%m-%d %H:%M:00"),
            'datetime_hour': date_time.strftime("%Y-%m-%d %H:00:00"),
            'datetime_zero': date_time.strftime('%Y-%m-%d 00:00:00')
        }
    except Exception as e:
        if v_true(debug, bool):
            logger.exception(e)
        return None


# --------------------------------------------------------------------------------------------------


# run_cmd = bash('echo ok', universal_newlines=True, stdout=PIPE)
#
# if run_cmd != None:
#     returncode = run_cmd.returncode
#     outputs = run_cmd.stdout.splitlines()
#     print(returncode, type(returncode))
#     print(outputs, type(outputs))
#
# # echo 'echo ok' > /tmp/ok.sh
# run_script = bash('/tmp/ok.sh', file=True, universal_newlines=True, stdout=PIPE)
#
# if run_script != None:
#     returncode = run_script.returncode
#     outputs = run_script.stdout.splitlines()
#     print(returncode, type(returncode))
#     print(outputs, type(outputs))


def shell(
    command: str,
    isfile: bool = False,
    sh_shell: str = '/bin/bash',
    sh_option: str | None = None,
    debug: bool = False,
    **kwargs
) -> subprocess.CompletedProcess | None:
    """run shell command or script"""
    try:
        match True:
            case True if not check_file_type(sh_shell, 'file', debug=debug):
                return None
            case True if v_true(sh_shell, str, debug=debug) and v_true(command, str, debug=debug):
                if isfile is True:
                    if sh_option is None:
                        return subprocess.run([sh_shell, command], **kwargs, check=False)
                    return subprocess.run([sh_shell, sh_option, command], **kwargs, check=False)
                if sh_option is None:
                    sh_option = '-c'
                return subprocess.run([sh_shell, sh_option, command], **kwargs, check=False)
            case _:
                return None
    except Exception as e:
        if v_true(debug, bool):
            logger.exception(e)
        return None


# --------------------------------------------------------------------------------------------------


def json_file_parser(
    file: str,
    debug: bool = False
) -> dict | None:
    """JSON File Parser"""
    try:
        if check_file_type(file, 'file', debug=debug):
            with open(file, encoding="utf-8") as json_raw:
                json_dict = json.load(json_raw)
            return json_dict
        if v_true(debug, bool):
            logger.error(f"No such file: {file}")
        return None
    except Exception as e:
        if v_true(debug, bool):
            logger.exception(e)
        return None

# json_raw = '''
# {
#     "markdown.preview.fontSize": 14,
#     "editor.minimap.enabled": false,
#     "workbench.iconTheme": "vscode-icons",
#     "http.proxy": "http://127.0.0.1:1087"
# }
# '''
#
# print(json_sort(json_raw))
#
# {
#     "editor.minimap.enabled": false,
#     "http.proxy": "http://127.0.0.1:1087",
#     "markdown.preview.fontSize": 14,
#     "workbench.iconTheme": "vscode-icons"
# }


def json_sort(
    string: str,
    debug: bool = False,
    **kwargs
) -> str | None:
    """JSON Sort"""
    try:
        return json.dumps(json.loads(string), indent=4, sort_keys=True, **kwargs) if v_true(string, str, debug=debug) else None
    except Exception as e:
        if v_true(debug, bool):
            logger.exception(e)
        return None


# --------------------------------------------------------------------------------------------------


def delete_files(
    files: Union[str, List],
    debug: bool = False
) -> bool:
    """删除文件"""
    try:

        if isinstance(files, str) and check_file_type(files, 'file', debug=debug):

            os.remove(files)
            if v_true(debug, bool):
                logger.success(f'deleted file: {files}')
            return True

        if v_true(files, list, debug=debug):

            for _file in files:

                if v_true(_file, str, debug=debug) and check_file_type(_file, 'file', debug=debug):
                    try:
                        os.remove(_file)
                        logger.success(f'deleted file: {_file}')
                    except Exception as e:
                        logger.error(f'error file: {_file} {e}')
                else:
                    logger.error(f'error file: {_file}')

            return True

        if v_true(debug, bool):
            logger.error(f'error file: {files}')

        return False

    except Exception as e:
        if v_true(debug, bool):
            logger.exception(e)
        return False


def delete_directory(
    directory: Union[str, List],
    debug: bool = False
) -> bool:
    """
    delete directory

    https://docs.python.org/3/library/os.html#os.rmdir

        os.rmdir(path, *, dir_fd=None)

    Remove (delete) the directory path.

    If the directory does not exist or is not empty, an FileNotFoundError or an OSError is raised respectively.

    In order to remove whole directory trees, shutil.rmtree() can be used.

    https://docs.python.org/3/library/shutil.html#shutil.rmtree

        shutil.rmtree(path, ignore_errors=False, onerror=None)

    Delete an entire directory tree; path must point to a directory (but not a symbolic link to a directory).

    If ignore_errors is true, errors resulting from failed removals will be ignored;

    if false or omitted, such errors are handled by calling a handler specified by onerror or, if that is omitted, they raise an exception.
    """
    try:

        if isinstance(directory, str) and check_file_type(directory, 'dir', debug=debug):

            rmtree(directory)

            if v_true(debug, bool):
                logger.success(f'deleted directory: {directory}')

            return True

        elif v_true(directory, list, debug=debug):

            for _dir in directory:

                if v_true(_dir, str, debug=debug) and check_file_type(_dir, 'dir', debug=debug):
                    try:
                        rmtree(_dir)
                        if v_true(debug, bool):
                            logger.success(f'deleted directory: {_dir}')
                    except Exception as e:
                        if v_true(debug, bool):
                            logger.error(f'error directory: {_dir} {e}')
                else:
                    if v_true(debug, bool):
                        logger.error(f'error directory: {_dir}')

            return True

        else:
            if v_true(debug, bool):
                logger.error(f'error directory: {directory}')
            return False

    except Exception as e:
        if v_true(debug, bool):
            logger.exception(e)
        return False


# --------------------------------------------------------------------------------------------------


def process_pool(
    process_func: Callable,
    process_data: Any = None,
    process_num: int = 2,
    thread: bool = False,
    debug: bool = False,
    **kwargs
) -> list | bool:
    """
    多线程(MultiThread) | 多进程(MultiProcess)
    """
    # ThreadPool 线程池
    # ThreadPool 共享内存, Pool 不共享内存
    # ThreadPool 可以解决 Pool 在某些情况下产生的 Can't pickle local object 的错误
    # https://stackoverflow.com/a/58897266
    try:

        # 处理数据
        if v_true(debug, bool):
            logger.info("data split ......")
        if len(process_data) <= process_num:
            process_num = len(process_data)
            _data = process_data
        else:
            _data = list_split(process_data, process_num, equally=True, debug=debug)

        if _data is None:
            return False

        if v_true(debug, bool):
            logger.info(f"data: {_data}")

        # 执行函数
        if v_true(thread, bool):
            # 多线程
            if v_true(debug, bool):
                logger.info("execute multi thread ......")
            with ThreadPool(process_num, **kwargs) as p:
                return p.map(process_func, _data)
        else:
            # 多进程
            if v_true(debug, bool):
                logger.info("execute multi process ......")
            with Pool(process_num, **kwargs) as p:
                return p.map(process_func, _data)

    except Exception as e:
        if v_true(debug, bool):
            logger.exception(e)
        return False


def new_process(
    process_func: Callable,
    process_data: Any = None,
    thread: bool = False,
    daemon: bool = True,
    debug: bool = False,
    **kwargs
) -> Thread | Process | bool:
    """New Process"""
    try:
        if v_true(thread, bool):
            process = Thread(target=process_func, args=process_data, **kwargs)
        else:
            process = Process(target=process_func, args=process_data, **kwargs)
        process.daemon = daemon
        process.start()
        return process
    except Exception as e:
        if v_true(debug, bool):
            logger.exception(e)
        return False


# --------------------------------------------------------------------------------------------------


def create_empty_file(
    file: str | None = None,
    debug: bool = False
) -> str | None:
    """create empty file"""
    try:
        if file is None:
            # 当前时间戳(纳秒)
            timestamp = time.time_ns()
            if v_true(debug, bool):
                logger.info(f"timestamp: {timestamp}")
            # 空文件路径
            file = f'/tmp/empty_file_{timestamp}.txt'
        # 创建一个空文件
        if v_true(debug, bool):
            logger.info(f"file: {file}")
        # pylint: disable=R1732,disable=W1514
        open(file, 'w').close()
        # 返回文件路径
        return file
    except Exception as e:
        if v_true(debug, bool):
            logger.exception(e)
        return None


# --------------------------------------------------------------------------------------------------


def uuid4_hex() -> str:
    """UUID"""
    return uuid4().hex


def increment_version(
    version: str,
    debug: bool = False
) -> str | None:
    """版本号递增"""
    try:
        version_numbers = version.split('.')
        version_numbers[-1] = str(int(version_numbers[-1]) + 1)
        return '.'.join(version_numbers)
    except Exception as e:
        if v_true(debug, bool):
            logger.exception(e)
        return None


# --------------------------------------------------------------------------------------------------


def make_directory(
    directory: str,
    debug: bool = False
) -> bool:
    """创建目录"""
    try:
        os.makedirs(directory)
        return True
    except Exception as e:
        if v_true(debug, bool):
            logger.exception(e)
        return False

def change_directory(
    directory: str,
    debug: bool = False
) -> bool:
    """改变目录"""
    try:

        if not v_true(directory, str, debug=debug):
            return False

        if v_true(debug, bool):
            logger.info(f"directory: {directory}")

        if check_file_type(directory, 'dir', debug=debug):
            if v_true(debug, bool):
                logger.info(f"change directory to {directory}")
            os.chdir(directory)
            return True

        if v_true(debug, bool):
            logger.error(f"no such directory: {directory}")

        return False

    except Exception as e:
        if v_true(debug, bool):
            logger.exception(e)
        return False


# --------------------------------------------------------------------------------------------------


def load_toml_file(
    file: str,
    debug: bool = False
) -> dict | None:
    """Load TOML file"""
    info = '解析配置文件'
    try:
        if v_true(debug, bool):
            logger.info(f'{info}[执行]')
        with open(file, "rb") as _file:
            config = tomllib.load(_file)
        if v_true(debug, bool):
            logger.success(f'{info}[成功]')
        return config
    except Exception as e:
        if v_true(debug, bool):
            logger.error(f'{info}[失败]')
            logger.exception(e)
        return None


def git_clone(
    git_repository: str,
    local_repository: str,
    timeout: int = 30,
    delete: bool = False,
    log_prefix: str = '',
    debug: bool = False,
) -> bool:
    """GIT Clone"""
    try:

        # 日志前缀
        log_prefix = f'{log_prefix}[GitClone]'

        # 获取应用程序Git仓库
        if v_true(debug, bool):
            logger.info(f'{log_prefix}process the request')
            logger.info(f'{log_prefix}git repository: {git_repository}')
            logger.info(f'{log_prefix}local repository: {local_repository}')

        # 删除本地仓库
        if v_true(delete, bool):
            delete_directory(local_repository, debug=debug)
            time.sleep(1)

        # from shutil import which
        # logger.info(which('timeout')) if v_true(debug, bool) else next
        # if which('timeout') != None:
        #     command = f'timeout -s 9 {timeout} git clone {git_repository} {local_repository}'

        # 克隆仓库
        result = shell(
            command=f'timeout -s 9 {timeout} git clone {git_repository} {local_repository}',
            debug=debug,
            universal_newlines=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT
        )

        if result is None:
            return False

        result_code: int = result.returncode
        result_info = result.stdout.splitlines()

        if v_true(debug, bool):
            logger.error(f'{log_prefix}unsuccessful')
            for i in result_info:
                logger.error(f'{log_prefix}{i}')

        if result_code == 0:
            return True

        return False

    except Exception as e:
        if v_true(debug, bool):
            logger.error(f'{log_prefix}unsuccessful')
            logger.exception(e)
        return False


def url_parse(
    url: str,
    scheme: str = 'http',
    debug: bool = False
) -> ParseResult:
    """URL Parse"""
    none_result = ParseResult(scheme='', netloc='', path='', params='', query='', fragment='')
    try:
        if v_true(debug, bool):
            logger.info(f'url: {url}')
        # 如果没有 scheme 的话, 字符串是不解析的. 所以, 如果没有 scheme, 就添加一个 scheme, 默认添加 http
        if v_true(url, str) and (url.find('://') == -1) and v_true(scheme, str):
            url = f'{scheme}://{url}'
        if v_true(url, str):
            return urlparse(url)
        return none_result
    except Exception as e:
        if v_true(debug, bool):
            logger.exception(e)
        return none_result

# def debug_log(
#     log: None | str = None,
#     exception: None | Exception = None,
#     debug: bool = False,
#     error: bool = False
# ):
#     """debug log"""
#     if v_true(log, str) and v_true(debug, bool):
#         if v_true(error, bool):
#             logger.error(log)
#         else:
#             logger.info(log)
#         return

#     if v_true(exception, Exception):
#         if v_true(debug, bool):
#             logger.exception(exception)
#         else:
#             logger.error(exception)
