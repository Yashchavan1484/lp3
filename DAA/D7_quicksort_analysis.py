import random
import time

def partition(arr, low, high):
    pivot = arr[high]
    i = low - 1

    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]

    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1


def quicksort(arr, low, high, randomized=False):
    if low < high:
        if randomized:
            r = random.randint(low, high)
            arr[r], arr[high] = arr[high], arr[r]

        p = partition(arr, low, high)
        quicksort(arr, low, p - 1, randomized)
        quicksort(arr, p + 1, high, randomized)


arr = [10, 80, 30, 90, 40, 50, 70]

a = arr.copy()
start = time.time()
quicksort(a, 0, len(a) - 1)
print("Deterministic:", a)
print("Time:", time.time() - start)

b = arr.copy()
start = time.time()
quicksort(b, 0, len(b) - 1, True)
print("Randomized:", b)
print("Time:", time.time() - start)