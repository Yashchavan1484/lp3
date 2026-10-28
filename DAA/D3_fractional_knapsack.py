
def fractional_knapsack(weights, values, capacity):
    items = sorted(
        zip(weights, values),
        key=lambda x: x[1] / x[0],
        reverse=True
    )

    total = 0

    for w, v in items:
        if capacity >= w:
            total += v
            capacity -= w
        else:
            total += v * (capacity / w)
            break

    return total


n = int(input("Enter number of items: "))

weights = [float(input("Enter weight: ")) for _ in range(n)]
values = [float(input("Enter value: ")) for _ in range(n)]
capacity = float(input("Enter knapsack capacity: "))

print("Maximum value:", fractional_knapsack(weights, values, capacity))
