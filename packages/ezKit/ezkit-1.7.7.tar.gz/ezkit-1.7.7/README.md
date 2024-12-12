# Python Easy Kit

保留关键字:

- <https://docs.python.org/3.10/reference/lexical_analysis.html#keywords>

```py
import keyword
keyword.kwlist

"""
[
    'False', 'None', 'True', 'and', 'as', 'assert', 'async', 'await', 'break', 'class', 'continue',
    'def', 'del', 'elif', 'else', 'except', 'finally', 'for', 'from', 'global', 'if', 'import', 'in', 'is',
    'lambda', 'nonlocal', 'not', 'or', 'pass', 'raise', 'return', 'try', 'while', 'with', 'yield'
]
```

内置函数:

- <https://docs.python.org/3.10/library/functions.html>

Built-in Functions

```py
# A
abs()
aiter()
all()
any()
anext()
ascii()

# B
bin()
bool()
breakpoint()
bytearray()
bytes()

# C
callable()
chr()
classmethod()
compile()
complex()

# D
delattr()
dict()
dir()
divmod()

# E
enumerate()
eval()
exec()

# F
filter()
float()
format()
frozenset()

# G
getattr()
globals()

# H
hasattr()
hash()
help()
hex()

# I
id()
input()
int()
isinstance()
issubclass()
iter()

# L
len()
list()
locals()

# M
map()
max()
memoryview()
min()

# N
next()

# O
object()
oct()
open()
ord()

# P
pow()
print()
property()

# R
range()
repr()
reversed()
round()

# S
set()
setattr()
slice()
sorted()
staticmethod()
str()
sum()
super()

# T
tuple()
type()

# V
vars()

# Z
zip()

# _
__import__()
```

代码规范:

- [PEP 8 – Style Guide for Python Code](https://peps.python.org/pep-0008/)
- [PEP8 翻译](https://www.jianshu.com/p/78d76f85bd82)
- [PEP 8 -- Python 代码风格指南](https://github.com/kernellmd/Knowledge/blob/master/Translation/PEP%208%20%E4%B8%AD%E6%96%87%E7%BF%BB%E8%AF%91.md)

注释长度: 100

手动安装:

```sh
pip install ezKit-1.1.3.tar.gz
```

版本号说明: [PEP 440 – Version Identification and Dependency Specification](https://peps.python.org/pep-0440/)

## 函数

- 明确 参数 和 返回值 的类型
- 必须有返回值
- 添加一个 debug 参数, 用于调试
    - 如果 debug 为 True, 则输出相关信息, 否则一律不输出任何信息
- 必须有说明
- 必须用 try ... except ... 包裹

try ... except ... 一律输出 Exception:

```py
def func():
    try:
        ...
    except Exception as e:
        logger.exception(e)
        return None
```

Boolen (False)

| Types | False |
| ---   | ---   |
| bool  | False |
| int   | 0     |
| float | 0.0   |
| str   | ''    |
| list  | []    |
| tuple | ()    |
| dict  | {}    |
| set   | {\*()} {\*[]} {\*{}} |

list/tuple/dict/set 初始化和类型转换:

- 变量初始化推荐使用 `[]/()/{}/{*()}/{*[]}/{*{}}` (性能更好)
- 类型转换则使用具体函数 `list()/tuple()/dict()/set()`

list/tuple/set 的区别:

- list 元素可以改变且可以不唯一
- tuple 元素不能改变且可以不唯一
- set 元素可以改变但唯一

变量类型

- 查看变量类型 type(x)
- 判断变量类型 isinstance(x, str)

函数: 不要判断类型, 否则会捕获不到异常, 无法定位到出问题的地方

函数: 必须有返回

- 有内容返回内容
- 无内容返回None
- 仅执行则返回True或False

函数变量

- 建议定义为 None
- 没有定义变量初始值, 添加 *args, **kwargs
- 定义了变量初始值, 添加 **kwargs
- 其它情况 *args, x=None, **kwargs
- 检查变量类型

配置文件用 JSON, 优点: 简单高效, 保持数据类型, 缺点: 不支持注释

```py
logger.info('配置文件解析...')

config_file = os.path.realpath(argument_config)
config_dict = utils.json_file_parser(config_file)

exit(1) if config_dict == None else next

print(config_dict)
```

## Exit

如果要编译脚本, 代码中有使用 exit 退出脚本时, 将 `exit()` 改为 `sys.exit()`, 否则编译的文件调用 `exit()` 会失败
