import asyncio
import time

async def async_function(param, delay):
    print("starting")
    await asyncio.sleep(delay)
    print(f'{param}')
    

async def main():
    print('guacamole')
    result = asyncio.create_task(async_function("pooping", 5))
    result2 = asyncio.create_task(async_function("poopy pants", 10))
    
    await result
    await result2






if __name__ == '__main__':
    asyncio.run(main())