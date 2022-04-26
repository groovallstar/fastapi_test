# https://docs.aiohttp.org/en/stable/
# pip install aiohttp~=3.7.3

import asyncio
import aiohttp
import time

# sync
# def fetcher(session, url):
#     with session.get(url) as response:
#         return response.text

# def main():
#     urls = ["https://naver.com", "https://google.com", "https://instagram.com"]
#     import requests    
#     with requests.Session() as session:
#         result = [fetcher(session, url) for url in urls]
#         print(result)

async def fetcher(session, url):
    async with session.get(url) as response:
        return await response.text()

async def main():
    urls = ["https://naver.com", "https://google.com", "https://instagram.com"]
    
    async with aiohttp.ClientSession() as session:
        result = await asyncio.gather(*[fetcher(session, url) for url in urls])
        print(result)


if __name__ == "__main__":
    start = time.time()
    asyncio.run(main())
    end = time.time()
    print(end - start)
    
