import asyncio
import time

import aiohttp


async def download_url_one_session(worker_name: str, urls: list[str], session: aiohttp.ClientSession) -> int:
    for url in urls:
        async with session.get(url) as response:
            content = await response.text()
            print(f"Worker: {worker_name} => read {len(content)} from {url}")
    return len(urls)


async def main_one_session(urls: list[str], workers_count: int):
    tasks = []
    session = aiohttp.ClientSession()
    for i in range(workers_count):
        tasks.append(download_url_one_session(worker_name=str(i), urls=urls[i::workers_count], session=session))
    results = await asyncio.gather(*tasks)
    await session.close()
    print(f"downloads per worker {results=}")


async def download_url_self_session(worker_name: str, urls: list[str]) -> int:
    async with aiohttp.ClientSession() as session:
        for url in urls:
            async with session.get(url) as response:
                content = await response.text()
                print(f"Worker: {worker_name} => read {len(content)} from {url}")
    return len(urls)


async def main_session_per_worker(urls: list[str], workers_count: int):
    tasks = []
    for i in range(workers_count):
        tasks.append(download_url_self_session(worker_name=str(i), urls=urls[i::workers_count]))
    results = await asyncio.gather(*tasks)
    print(f"Session per workers: downloads per worker {results=}")


if __name__ == '__main__':
    sites = [
        "https://www.jython.org",
        "http://olympus.realpython.org/dice",
    ] * 80

    workers_count = int(input("Workers count:"))

    # session per worker
    start_time = time.time()
    asyncio.run(main_session_per_worker(urls=sites, workers_count=workers_count))
    duration_per_sessions = time.time() - start_time

    # one session
    start_time = time.time()
    asyncio.run(main_one_session(urls=sites, workers_count=workers_count))
    duration_one_session = time.time() - start_time

    # report
    print(f"One Session: Downloaded {len(sites)} in {duration_one_session:.2f} seconds")
    print(f"Many Sessions: Downloaded {len(sites)} in {duration_per_sessions:.2f} seconds")
