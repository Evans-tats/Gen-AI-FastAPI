import asyncio
import time

async def task():
    print("Start of async task")
    await asyncio.sleep(5)
    print("Task resumed after 5 seconds")

# async def spawn_tasks():
#     await asyncio.gather(task(), task(), task())

async def spawn_tasks():
    await task()
    print("hello")
    await task()
    print("hello2")
    await task()
    print("helloe")
# start = time.time()
# asyncio.run(spawn_tasks())
# print("hell")
# duration = time.time() - start
# print(f"Duration: {duration}")
async def main():
    start = time.time()
    await task()
    await task()
    duration = time.time() - start
    print(f"Duration: {duration}")

asyncio.run(main())