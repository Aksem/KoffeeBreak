import asyncio

async def timer(loop, time_remain, configDict, state):
    while True:
        print(time_remain)
        time_remain -= 1
        await asyncio.sleep(1)
        if time_remain == 1495:
            state = 'break-1-4'
            if qtVersion == True:
            
