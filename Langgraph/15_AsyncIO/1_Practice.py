import asyncio

async def main():
    print("hello")
    await asyncio.sleep(5)   # yields control to the loop
    print("world")

asyncio.run(main())          # entry point: creates and closes the loop