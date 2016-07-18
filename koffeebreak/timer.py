import asyncio

async def timer(loop, time_remain):
    while True:
        print(time_remain)
        time_remain -= 1
        await asyncio.sleep(1)
