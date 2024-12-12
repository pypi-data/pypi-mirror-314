# seatools uvicorn 启动器

## 使用指南
1. 安装, `poetry add seatools-server-uvicorn`
2. 假设`xxx.boot`模块存在`start`的启动`ioc`函数
```python
from seatools.ioc import run

def start():
    run('xxx', './config')

```
命令行启动`uvicorn xxx.boot:start xxx.fastapi.app:app`, 其他参数与官方`uvicorn`一致, 在`uvicorn`基础上增加了一个`ioc_app`的参数, 需要指明`ioc`应用启动的函数
3. 程序直接调用

```python
from xxx.boot import start
from seatools.ioc.server import uvicorn


def main():
    uvicorn.run(start, 'xxx.fastapi.app:app')


if __name__ == '__main__':
    main()

```