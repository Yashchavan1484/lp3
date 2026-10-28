
def fib_iterative(n):
    a, b = 0, 1
    steps = 0

    for i in range(n):
        print(a, end=" ")
        a, b = b, a + b
        steps += 1

    print("\nStep count (Iterative):", steps)


def fib_recursive(n, steps):
    steps[0] += 1

    if n <= 1:
        return n

    return fib_recursive(n - 1, steps) + fib_recursive(n - 2, steps)


if __name__ == "__main__":
    n = int(input("Enter n: "))

    print("Fibonacci series (Iterative):")
    fib_iterative(n)

    steps = [0]
    result = fib_recursive(n, steps)

    print("Fibonacci number (Recursive):", result)
    print("Step count (Recursive):", steps[0])
