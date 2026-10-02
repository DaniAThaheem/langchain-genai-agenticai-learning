import time

def make_tea(name):
    print(f"{name}: start")
    time.sleep(2)              # thread is frozen here, nothing else can run
    print(f"{name}: done")
    return name

def main():
    start = time.perf_counter()

    make_tea("A")
    make_tea("B")
    make_tea("C")

    print(f"Total: {time.perf_counter() - start:.1f}s")

main()