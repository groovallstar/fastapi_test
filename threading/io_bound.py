# https://docs.python.org/ko/3.7/library/concurrent.futures.html

import requests
import time
import os
import threading
from concurrent.futures import ThreadPoolExecutor

def fetcher(params):
    session = params[0]
    url = params[1]
    print(f"{os.getpid()} process | {threading.get_ident()} url : {url}")
    with session.get(url) as response:
        return response.text

def main():
    urls = ["https://naver.com", "https://google.com", "https://instagram.com"]
    
    executor = ThreadPoolExecutor(max_workers=3)
    
    with requests.Session() as session:
        params = [(session, url) for url in urls]
        result = list(executor.map(fetcher, params))
        # result = [fetcher(session, url) for url in urls]
        # print(result)


if __name__ == "__main__":
    start = time.time()
    main()
    end = time.time()
    print(end - start)
    
