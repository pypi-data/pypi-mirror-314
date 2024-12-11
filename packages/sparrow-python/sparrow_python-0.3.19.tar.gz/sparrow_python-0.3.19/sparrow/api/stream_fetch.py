import asyncio
import aiohttp



# deprecated

async def async_request(method, urls, request_params_list, qps=10, concurrent=2):
    """
    Example:
        >>> urls = ["http://127.0.0.1:8000/benchmark/v1/chat/completions"] * 10
        >>> request_params_list = [
        ...     {'json': {
        ...         "model": "gpt-3.5-turbo",
        ...         "messages": [{"role": "user", "content": "hi"}],
        ...         "stream": False
        ...         },
        ...     },
        ...     ] * 10
        >>> results = asyncio.run(async_request("POST", urls, request_params_list, qps=10, concurrent=2))

    """

    async def predict(idx, client: aiohttp.ClientSession, method, url, **kwargs):
        resp = await client.request(method=method, url=url, **kwargs)
        return idx, await resp.json()

    async with aiohttp.ClientSession() as session:
        tasks = []
        time_interval = concurrent / qps

        total_num = len(urls)
        for i in range(0, total_num, concurrent):
            batch_tasks = []
            for j in range(concurrent):
                index = i + j
                if index < total_num:
                    task = asyncio.create_task(
                        predict(index, session, method, url=urls[index], **request_params_list[index])
                    )
                    batch_tasks.append(task)
            tasks.append(asyncio.gather(*batch_tasks))
            await asyncio.sleep(time_interval)

        results = []
        for task_group in tasks:
            batch_results = await task_group
            results.extend(batch_results)
        results.sort(key=lambda x: x[0])

        return [x[1] for x in results]


def sync_request(method, urls, request_params_list, qps=10, concurrent=2):
    """
    A function that performs a synchronous request using the provided
        method, URLs, request parameters list, QPS, and concurrent value.

    Example:
        >>> urls = ["http://127.0.0.1:8000/benchmark/v1/chat/completions"] * 10
        >>> request_params_list = [
        ...     {'json': {
        ...         "model": "gpt-3.5-turbo",
        ...         "messages": [{"role": "user", "content": "hi"}],
        ...         "stream": False
        ...         },
        ...     },
        ...     ] * 10
        >>> results = sync_request("POST", urls, request_params_list, qps=10, concurrent=2)
    """
    return asyncio.run(async_request(
        method, urls, request_params_list, qps=qps, concurrent=concurrent
    ))


if __name__ == "__main__":
    param_list = [
                     {'json': {
                         "model": "gpt-3.5-turbo",
                         "messages": [{"role": "user", "content": "Say hi"}],
                         "stream": False
                     },

                     }] * 10
    urls = ["http://127.0.0.1:8000/benchmark/v1/chat/completions"] * 10
    print(sync_request("POST", urls, param_list, qps=10, concurrent=2))
