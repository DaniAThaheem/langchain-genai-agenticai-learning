import asyncio, time

async def fetch(n):
    await asyncio.sleep(1)
    return n * 2

async def main():
    t = time.perf_counter()

    # Sequential: ~3s
    a = await fetch(1)
    b = await fetch(2)
    c = await fetch(3)
    results = [a, b, c]

    # Concurrent: ~1s
    # results = await asyncio.gather(fetch(1), fetch(2), fetch(3))
    print(results, time.perf_counter() - t)

asyncio.run(main())