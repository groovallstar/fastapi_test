import time
import asyncio

async def delivery(name, mealtime):
    print(f"{name} delivery...")
    await asyncio.sleep(mealtime)
    print(f"{name} finished meal, {mealtime} sec...")
    print(f"{name} complete....")
    return mealtime

async def main():
    # 일종의 예약
    task1 = asyncio.create_task(delivery("A", 2))
    task2 = asyncio.create_task(delivery("B", 1))

    await task2
    await task1


async def main_gather():
    """동시에 task 실행하기"""
    # 동시성.
    result = await asyncio.gather(
        delivery("A", 1),
        delivery("B", 1),
        delivery("C", 1)
    )
    print(result)

if __name__ == "__main__":
    start = time.time()
    #asyncio.run(main())
    asyncio.run(main_gather())
    end = time.time()
    print(end - start)
