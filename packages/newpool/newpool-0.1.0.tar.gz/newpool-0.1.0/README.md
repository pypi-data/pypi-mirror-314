# newpool

>更简单的使用异步协程和线程池

## 安装

```
pip install newpool
```

## 使用

### 异步协程

`newpool.async_gather()` 并发执行多个协程, 返回结果列表, 遇到异常不会中断, 而是将错误原因返回到结果列表中
`newpool.async_taskgroup()` 并发执行多个协程, 返回列表, 包含更详细的状态, 遇到异常会中断

```py
import newpool

async def test():
    await newpool.async_sleep(1)
    print("test")

gather_results = newpool.async_gather([test() for i in range(20)], sem=5) # sem 为并发协程数
taskgroup_results = newpool.async_taskgroup([test() for i in range(20)]) # 此处没有使用 sem, 默认基于设备自动计算并发协程数
```

### 线程池

**基于 `concurrent.futures.ThreadPoolExecutor` 实现**

```py
import newpool
import time

pool = newpool.Pool(5)

@pool.task
def test():
    time.sleep(2)
    print("test")

for i in range(20):
    test()

pool.wait() # 等待所有任务执行完毕
pool.state() # 线程池状态
pool.results # 所有任务执行结果
pool.cancel_all() # 取消所有任务
```

内置可以直接使用的线程池 `newpool.pool`, 无需实例化。
线程数默认基于设备自动计算, 也可以通过 `newpool.pool.n = 5` 修改线程数 

```py
import newpool

@newpool.pool.task
def test():
    print("test")

for i in range(20):
    test()

newpool.pool.wait() # 等待所有任务执行完毕
newpool.pool.state() # 线程池状态
newpool.pool.results # 所有任务执行结果
newpool.pool.cancel_all() # 取消所有任务
```

**基于 `asyncio` 实现的线程池**

需要通过 asyncio 运行, 可以直接使用 `newpool.async_gather()` 或者 `newpool.async_taskgroup()`

默认线程数基于设备自动计算，也可以通过 `newpool.to_async(n=5)` 修改线程数。

```py
import newpool
import time

@newpool.to_async()
def test():
    time.sleep(2)
    print("test")

newpool.async_gather([test() for i in range(20)])

@newpool.to_async(n=5)
def test2():
    time.sleep(2)
    print("test")

newpool.async_gather([test2() for i in range(20)])
```