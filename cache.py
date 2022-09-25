import functools
from tqdm import tqdm

def fib(n):
    if n==0:
        return 0
    elif n==1:
        return 1
    return fib(n-1) + fib(n-2)

@functools.lru_cache(maxsize=3)
def fib_with_cache(n):
    if n==0:
        return 0
    elif n==1:
        return 1
    return fib_with_cache(n-1) + fib_with_cache(n-2)


if __name__=="__main__":
    for i in tqdm(list(range(20)), desc="Calculating the fibonnaci sequence without caching"):
        print(fib(i))
    for i in tqdm(list(range(200000)), desc="Calculating with caching"):
        fib_with_cache(i)
