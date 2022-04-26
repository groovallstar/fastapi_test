import time
import os
import threading
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor

nums = [50, 63, 32]

def cpu_bound_func(num):
    print(f"{os.getpid()} process | {threading.get_ident()} thread, {num}")
    numbers = range(1, num)
    total = 1
    for i in numbers:
        for j in numbers:
            for k in numbers:
                total *= i * j * k
    return total

# cpu bound
# def main():
#     results = [cpu_bound_func(num) for num in nums]
#     print(results)

def main():
    # multithread
    # executor = ThreadPoolExecutor(max_workers=10)
    executor = ProcessPoolExecutor(max_workers=10)
    results = list(executor.map(cpu_bound_func, nums))
    print(results)

if __name__ == "__main__":
    start = time.time()
    main()
    end = time.time()
    print(end - start)
