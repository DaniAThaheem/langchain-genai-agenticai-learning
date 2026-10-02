import asyncio
import time

async def make_tea(name):
    print(f"{name}: start")
    print(f"{name}: waiting for 2 seconds")
    await asyncio.sleep(2)     # pauses only this coroutine, loop runs others
    print(f"{name}: done")
    return name

async def main():
    start = time.perf_counter()

    await asyncio.gather(
        make_tea("A"),
        make_tea("B"),
        make_tea("C"),
    )

    print(f"Total: {time.perf_counter() - start:.1f}s")

asyncio.run(main())