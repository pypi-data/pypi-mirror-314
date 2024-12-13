# Python Easy Kit

## 代码规范

- [PEP 8 – Style Guide for Python Code](https://peps.python.org/pep-0008/)
- [PEP8 翻译](https://www.jianshu.com/p/78d76f85bd82)
- [PEP 8 -- Python 代码风格指南](https://github.com/kernellmd/Knowledge/blob/master/Translation/PEP%208%20%E4%B8%AD%E6%96%87%E7%BF%BB%E8%AF%91.md)

注释长度: 100

版本号说明: [PEP 440 – Version Identification and Dependency Specification](https://peps.python.org/pep-0440/)

配置文件格式: TOML

----------------------------------------------------------------------------------------------------

## 函数

- 明确 参数 的类型
    - 尽量避免使用 *args 和 **kwargs
    - 必须判断参数: 先判断参数是否为 None, 然后再判断参数类型
- 必须有返回值, 且明确返回值的类型(默认返回 bool 类型)
    - 函数执行成功返回 True
    - 执行执行失败返回 False
- 添加一个 debug 参数, 用于调试
    - 如果 debug 为 True, 则输出相关信息, 否则一律不输出任何信息
- 必须有说明
- 必须用 `try ... except ...` 包裹
- 使用 loguru 输出信息 (不使用 print), 方便定位

```py
from loguru import logger
def func(debug: bool = False) -> bool:
    try:
        if debug is True:
            logger.info("info ...")
        # ...
        return True
    except Exception as e:
        logger.exception(e)
        return False
```

----------------------------------------------------------------------------------------------------

相关命令

```sh
# 打包
bash -x build.sh

# 上传
bash -x upload.sh

# 在线安装
pip install -U ezKit

# 离线安装
pip install -U ezKit-1.7.0.tar.gz
```
