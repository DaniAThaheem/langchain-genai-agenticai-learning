import asyncio, time

async def make_tea(name):
    print(f"{name}: start")
    await asyncio.sleep(2)
    print(f"{name}: done")
    return name

async def main():
    start = time.perf_counter()

    t1 = asyncio.create_task(make_tea("A"))
    t2 = asyncio.create_task(make_tea("B"))
    t3 = asyncio.create_task(make_tea("C"))

    await t1
    await t2
    await t3

    print(f"Total: {time.perf_counter() - start:.1f}s")

asyncio.run(main())