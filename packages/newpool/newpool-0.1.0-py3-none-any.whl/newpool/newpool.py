"""
异步协程和线程池
"""

import os
import time
import concurrent.futures
from functools import wraps
from rich.panel import Panel
from rich import print
import asyncio

__all__ = [
    "asyncio",
    "async_gather",
    "async_sleep",
    "async_taskgroup",
    "to_async",
    "Pool",
]

async_sleep = asyncio.sleep


def to_async(n=None):
    """
    ## 同步函数转异步（装饰器）

    该方式通过线程池的方式运行，非协程。

    n: 线程池数量, 默认为(CPU核心数+4)

    ## 使用示例:
    ```py
    import jsz

    @jsz.to_async()
    def hello1():
        jsz.sleep(3)
        jsz.print("hello")

    @jsz.to_async(5)
    def hello2():
        jsz.sleep(3)
        jsz.print("hello")

    jsz.async_gather([hello1() for i in range(20)])
    jsz.async_taskgroup([hello2() for i in range(20)])
    ```
    """

    if n:
        pool = concurrent.futures.ThreadPoolExecutor(max_workers=n)
    else:
        pool = None

    def _to_async(func):
        @wraps(func)
        async def wraped(*args, **kwargs):
            loop = asyncio.get_event_loop()
            return await loop.run_in_executor(pool, func, *args, **kwargs)

        return wraped

    return _to_async


def async_taskgroup(
    coros_or_futures: list,
    sem: None | int = None,
) -> list:
    """
    ## 并发运行协程函数（基于 asyncio.TaskGroup()）

    返回值列表为Future 对象, 包含协程函数的各种状态

    一个异常会导致其他待执行任务取消，更安全

    coros_or_futures: 协程对象列表
    sem: 协程池数量, 通过信号量实现，默认不加锁无限制
    """
    if sem:
        semaphore = asyncio.Semaphore(sem)

    if not isinstance(coros_or_futures, list):
        coros_or_futures = [coros_or_futures]

    async def with_sem(coro):
        if sem:
            async with semaphore:
                return await coro
        else:
            return await coro

    async def main():
        results = []
        async with asyncio.TaskGroup() as tg:
            for coro in coros_or_futures:
                task = tg.create_task(with_sem(coro))
                results.append(task)
        return results

    return asyncio.run(main())


def async_gather(
    coros_or_futures: list,
    sem: None | int = None,
) -> list:
    """
    ## 并发运行协程函数（基于 asyncio.gather）

    返回值列表中只有函数返回值。

    出现异常不会自动取消，而是把错误原因汇总到返回列表。

    coros_or_futures: 协程对象列表
    sem: 协程池数量, 通过信号量实现，默认不加锁无限制
    """
    if sem:
        semaphore = asyncio.Semaphore(sem)

    if not isinstance(coros_or_futures, list):
        coros_or_futures = [coros_or_futures]

    async def with_sem(coro):
        if sem:
            async with semaphore:
                return await coro
        else:
            return await coro

    async def main():
        return await asyncio.gather(
            *[with_sem(i) for i in coros_or_futures],
            return_exceptions=True,
        )

    return asyncio.run(main())


class Pool:
    """
    线程池
    """

    def __init__(self, n: int | None = None):
        """
        线程池

        n: 线程数。默认为CPU核心数+4, 可以自定义线程数。

        ```
        import time
        import newpool

        pool = newpool.Pool()

        @pool.task
        def hello():
            time.sleep(5)
            print('hello')

        for i in range(10):
            hello()

        pool.state() # 查看运行状态
        pool.cancel_all() # 全部取消
        pool.clear() # 取消并清空任务队列
        pool.wait() # 阻塞等待全部完成
        ```
        """
        if n:
            self.n = n
        else:
            self.n = min(32, (os.cpu_count() or 1) + 4)
        self.pool = concurrent.futures.ThreadPoolExecutor(max_workers=self.n)
        self.results = []
        self.callbacks = []

    def run(self, f, *args, **kwargs):
        self.pool._max_workers = self.n
        self.pool._adjust_thread_count()
        f = self.pool.submit(f, *args, **kwargs)
        self.results.append(f)
        return f

    def task(self, f):
        """
        添加任务
        """

        @wraps(f)
        def do_task(*args, **kwargs):
            result = self.run(f, *args, **kwargs)
            for cb in self.callbacks:
                result.add_done_callback(cb)
            return result

        return do_task

    def callback(self, f):
        """
        通过装饰器增加回调函数，函数需要使用参数 future。

        @pool.callable
        def hello_callback(future):
            print(future.result())
        """
        self.callbacks.append(f)

        @wraps(f)
        def register_callback():
            f()

        return register_callback

    def wait(self, timeout: float = None, return_when: str = "ALL_COMPLETED"):
        """
        阻塞等待 Future 实例完成。

        timeout: 超时秒数
        return_when: 结束信号, 共三种, 分别为 ALL_COMPLETED、FIRST_COMPLETED、FIRST_EXCEPTION
        """
        while self.state_dict()["正在运行"] > 0 or self.state_dict()["剩余任务"] > 0:
            time.sleep(0.1)
            concurrent.futures.wait(
                fs=self.results,
                timeout=timeout,
                return_when=return_when,
            )

    def cancel_all(self):
        """
        全部取消
        """
        for i in self.results:
            i.cancel()
        self.state({"备注": "[green]未运行的程序已取消[/green]"})

    def clear(self):
        """
        取消任务，并清空任务队列
        """
        self.cancel_all()
        self.results.clear()
        self.state({"备注": "[green]任务队列已清空[/green]"})

    def state_dict(self):
        """
        返回线程池当前运行状态

        extend: 拓展字段。
        """
        count_all = len(self.results)
        count_done = 0
        count_running = 0
        count_exception = 0
        count_cancelled = 0
        count_other = 0
        for i in self.results:
            if i.done():
                count_done += 1
                if i.cancelled():
                    count_cancelled += 1
                elif i.exception():
                    count_exception += 1
            elif i.running():
                count_running += 1
            else:
                count_other += 1
        count_success = count_done - count_cancelled - count_exception
        state_result = {
            "时间": time.strftime("%F %T"),
            "总任务": count_all,
            "已完成": count_done,
            "成功": count_success,
            "取消": count_cancelled,
            "报错": count_exception,
            "正在运行": count_running,
            "剩余任务": count_other,
        }
        return state_result

    def state_str(self, extend: dict = None):
        """
        线程池运行状态，字符串

        extend: 拓展字段。
        """
        state_dict = self.state_dict()
        state_result = (
            f"时间:{state_dict['时间']}\n"
            f"总任务:{state_dict['总任务']}\n"
            f"已完成:{state_dict['已完成']} (成功:{state_dict['成功']} 取消:{state_dict['取消']} 报错:{state_dict['报错']})\n"
            f"正在运行:{state_dict['正在运行']}\n"
            f"剩余任务:{state_dict['剩余任务']}"
        )

        if extend and isinstance(extend, dict):
            state_result += "\n" + "\n".join([f"{i[0]}:{i[1]}" for i in extend.items()])
        return state_result

    def state(self, extend: dict = None):
        """
        打印线程池运行状态

        extend: 拓展字段。
        """
        print(Panel(self.state_str(extend), expand=False))
