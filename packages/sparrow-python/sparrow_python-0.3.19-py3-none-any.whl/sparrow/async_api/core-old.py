import asyncio
import itertools

import time
from typing import Any, Iterable, Optional, Callable
from aiohttp import ClientSession, TCPConnector, ClientTimeout
from contextlib import asynccontextmanager
from ..decorators.core import async_retry
from .interface import RequestResult
from .progress import ProgressTracker, ProgressBarConfig



class RateLimiter:
    """速率限制器"""

    def __init__(self, max_fps: Optional[float] = None):
        self.max_fps = max_fps
        self.min_interval = 1 / max_fps if max_fps else 0
        self.last_request_time = 0

    async def acquire(self):
        if not self.max_fps:
            return

        current_time = time.time()
        elapsed = current_time - self.last_request_time
        if elapsed < self.min_interval:
            # await asyncio.sleep(self.min_interval - elapsed)
            time.sleep(self.min_interval - elapsed)
        self.last_request_time = time.time()


class ConcurrentRequester:
    """
    并发请求管理器

    Example
    -------

    requester = ConcurrentRequester(
        concurrency_limit=5,
        max_fps=10,
        timeout=0.7,
    )

    request_params = [
        {
            'json': {
                'messages': [{"role": "user", "content": "讲个笑话" }],
                'model': "qwen2.5:latest",
            },
            'headers': {'Content-Type': 'application/json'}
        } for i in range(10)
    ]

    # 执行并发请求
    results, tracker = await requester.process_requests(
        request_params=request_params,
        url='http://localhost:11434/v1/chat/completions',
        method='POST',
        show_progress=True
    )
    """

    def __init__(
            self,
            concurrency_limit: int,
            max_fps: Optional[float] = None,
            timeout: float | None = None,
    ):
        self._concurrency_limit = concurrency_limit
        if timeout:
            self._timeout = ClientTimeout(total=timeout, connect=min(10., timeout))
        else:
            self._timeout = None
        self._rate_limiter = RateLimiter(max_fps)
        self._semaphore = asyncio.Semaphore(concurrency_limit)

    @asynccontextmanager
    async def _get_session(self):
        connector = TCPConnector(limit=self._concurrency_limit+10, limit_per_host=0, force_close=False)
        async with ClientSession(timeout=self._timeout, connector=connector) as session:
            yield session

    @async_retry(retry_times=3, retry_delay=0.55)
    async def _send_single_request(
            self,
            session: ClientSession,
            request_id: int,
            url: str,
            method: str = 'POST',
            meta: dict = None,
            **kwargs
    ) -> RequestResult:
        """发送单个请求"""
        async with self._semaphore:
            try:
                # todo: 速率限制也许需要优化
                await self._rate_limiter.acquire()

                start_time = time.time()

                async with session.request(
                        method, url,
                        **kwargs
                ) as response:
                    data = await response.json()
                    latency = time.time() - start_time

                    if response.status != 200:
                        error_info = {
                            'status_code': response.status,
                            'response_data': data,
                            'error': f"HTTP {response.status}"
                        }
                        return RequestResult(
                            request_id=request_id,
                            data=error_info,
                            status='error',
                            meta=meta,
                            latency=latency
                        )

                    return RequestResult(
                        request_id=request_id,
                        data=data,
                        status="success",
                        meta=meta,
                        latency=latency
                    )

            except asyncio.TimeoutError as e:
                return RequestResult(
                    request_id=request_id,
                    data={'error': 'Timeout error', 'detail': str(e)},
                    status='error',
                    meta=meta,
                    latency=time.time() - start_time
                )
            except Exception as e:
                return RequestResult(
                    request_id=request_id,
                    data={'error': e.__class__.__name__, 'detail': str(e)},
                    status='error',
                    meta=meta,
                    latency=time.time() - start_time
                )

    async def process_requests(
            self,
            request_params: Iterable[dict[str, Any]],
            url: str,
            method: str = 'POST',
            total_requests: Optional[int] = None,
            show_progress: bool = True
    ) -> tuple[list[RequestResult], Optional[ProgressTracker]]:
        """
        处理批量请求

        Returns:
            Tuple[list[RequestResult], Optional[ProgressTracker]]:
            请求结果列表和进度跟踪器（如果启用了进度显示）
        """
        # --------------------------------
        # 如果没有提供total_requests，且需要显示进度，则计算总数
        progress = None
        if total_requests is None and show_progress:
            # 创建迭代器的副本
            request_params, params_for_counting = itertools.tee(request_params)
            total_requests = sum(1 for _ in params_for_counting)

        if show_progress and total_requests is not None:
            progress = ProgressTracker(
                total_requests,
                concurrency=self._concurrency_limit,
                config=ProgressBarConfig()
            )

        async with self._get_session() as session:
            results = await self.process_with_concurrency_window(
                items=request_params,
                process_func=lambda params, request_id: self._send_single_request(
                    session=session,
                    request_id=request_id,
                    url=url,
                    method=method,
                    meta=params.pop('meta', None),
                    **params
                ),
                concurrency_limit=self._concurrency_limit,
                progress=progress
            )

            if progress:
                progress.print_summary()

            return results, progress


    async def process_with_concurrency_window(
        self,
        items: Iterable,
        process_func: Callable,
        concurrency_limit: int,
        progress: Optional[ProgressTracker] = None,
    ) -> list:
        """
        使用滑动窗口方式处理并发任务

        Args:
            items: 待处理的项目迭代器
            process_func: 处理单个项目的异步函数，接收item和项目item_id作为参数
            concurrency_limit: 并发限制数量,也是窗口大小
            progress: 可选的进度跟踪器

        Returns:
            list[R]: 按照输入顺序返回的处理结果列表
        """
        results = []
        item_id = 0
        active_tasks = set()

        for item in items:
            # 如果活跃任务数达到并发限制，等待某个任务完成
            if len(active_tasks) >= concurrency_limit:
                done, active_tasks = await asyncio.wait(
                    active_tasks,
                    return_when=asyncio.FIRST_COMPLETED
                )
                # 处理完成的任务结果
                for task in done:
                    result = await task
                    if progress:
                        progress.update(result)
                    results.append(result)

            # 创建新任务
            task = asyncio.create_task(process_func(item, item_id))
            active_tasks.add(task)
            item_id += 1

        # 等待剩余任务完成
        if active_tasks:
            done, _ = await asyncio.wait(active_tasks)
            for task in done:
                result = await task
                if progress:
                    progress.update(result)
                results.append(result)

        return sorted(results, key=lambda x: getattr(x, 'request_id', 0))
