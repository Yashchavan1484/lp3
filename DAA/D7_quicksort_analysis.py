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

# Aim

# To sort an array using Quick Sort with a fixed pivot and with a random pivot, and compare their running time.

# Theory
# Quick Sort picks a pivot, puts smaller elements on its left and larger ones on its right (this step is called partitioning), then sorts the left and right parts recursively.
# It works in place, so it needs no extra array.
# It is not stable: equal elements may change their relative order.
# Deterministic version: the pivot is always the last element. On an already sorted array this gives very uneven splits, so the worst case is O(n²).
# Randomized version: a random element is swapped to the last position before partitioning. No fixed input is always bad, so the expected time is O(n log n).
# Algorithm
# If low < high, continue. Otherwise stop (base case).
# (Randomized only) pick a random index r in [low, high] and swap arr[r] with arr[high].
# Partition: pivot = arr[high]. Move every element ≤ pivot to the left side. Finally place the pivot in its correct position p.
# Recursively sort the left part (low to p−1) and the right part (p+1 to high).


# | Point         | Quick Sort     | Merge Sort | Heap Sort  | Bubble Sort |
# |---------------|----------------|------------|------------|-------------|
# | Best time     | O(n log n)     | O(n log n) | O(n log n) | O(n)        |
# | Average time  | O(n log n)     | O(n log n) | O(n log n) | O(n²)       |
# | Worst time    | O(n²)          | O(n log n) | O(n log n) | O(n²)       |
# | Space         | O(log n)       | O(n)       | O(1)       | O(1)        |
# | In place      | Yes            | No         | Yes        | Yes         |
# | Stable        | No             | Yes        | No         | Yes         |
# | Practical speed | Fastest usually | Good     | Slower     | Very slow   |

# | Point                   | Deterministic Quick Sort        | Randomized Quick Sort                  |
# |-------------------------|---------------------------------|----------------------------------------|
# | Pivot choice            | Always last element             | Random element                         |
# | Worst case              | O(n²) on sorted / reverse input | O(n²) possible but extremely unlikely  |
# | Expected time           | O(n log n) on random input      | O(n log n) on any input                |
# | Same output every time? | Same steps every run            | Steps vary, sorted result is the same  |
# | Extra cost              | None                            | One random call per partition          |
# | Best used when          | Input is random                 | Input may be sorted or adversarial     |

# | Case                             | Time Complexity | Reason                                              |
# |----------------------------------|-----------------|-----------------------------------------------------|
# | Best                             | O(n log n)      | Pivot splits the array into two equal halves        |
# | Average                          | O(n log n)      | Splits are reasonably balanced                      |
# | Worst (deterministic)            | O(n²)           | Sorted or reverse-sorted input, 0 and n-1 split     |
# | Expected (randomized)            | O(n log n)      | Random pivot makes a bad split very unlikely        |

# | Space Complexity | Value                          | Reason                                       |
# |------------------|--------------------------------|----------------------------------------------|
# | Average          | O(log n)                       | Recursion stack depth                        |
# | Worst            | O(n)                           | Stack depth when splits are completely uneven |
