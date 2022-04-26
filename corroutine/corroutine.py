# 코루틴 hello world!
# https://docs.python.org/ko/3/library/asyncio-task.html

import asyncio

async def hello_world():
    print("hello world")
    
    # 객체가 await 표현식에서 사용될 수 있을 때 어웨이터블 객체라고 말함
    # corroutine, task, Future
    # await print("hello world")
    
    return 123

if __name__ == "__main__":
    asyncio.run(hello_world())
