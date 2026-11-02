
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

# Aim

# To find the maximum total value that can be placed in a knapsack of limited capacity, when items can be broken into fractions, using the greedy method.

# Theory
# In the Fractional Knapsack problem, we have n items, each with a weight and a value, and a bag with a fixed capacity.
# Items can be divided, so we can take a part of an item (for example, half of an item gives half its value).
# Greedy strategy: always pick the item with the highest value/weight ratio first, because it gives the most value per unit of capacity.
# Take whole items while they fit. When an item doesn’t fit, take only the fraction that fills the remaining space, then stop.
# This greedy approach always gives the optimal solution for the fractional version. It does not work for 0/1 Knapsack, where items cannot be split.
                                                                                                   
# Algorithm
# Calculate the ratio value/weight for every item.
# Sort the items in descending order of ratio.
# Set total = 0.
# For each item in sorted order:
# If the whole item fits (capacity ≥ weight), take it: add its value to total and reduce the capacity by its weight.
# Otherwise, take the fraction capacity/weight of it, add value × fraction to total, and stop.
# Return total.

# Dry run

# Items: weights = [10, 20, 30], values = [60, 100, 120], capacity = 50

# Item	Weight	Value	Ratio (V/W)
# 1	10	60	6
# 2	20	100	5
# 3	30	120	4

# Sorted order (already highest ratio first): Item 1, Item 2, Item 3.

# Step	Item	Fits?	Action	Total	Capacity left
# 1	1 (w=10)	Yes	Take full	60	40
# 2	2 (w=20)	Yes	Take full	160	20
# 3	3 (w=30)	No	Take 20/30 of it → 120 × 2/3 = 80	240	0

# Maximum value = 240

# Time and space complexity

# Let n = number of items.

# Step	Time
# Calculating ratios and sorting	O(n log n)
# Loop through items	            O(n)
# Total	                            O(n log n)

# Space: O(n) for the sorted list of items (O(1) extra if sorted in place).

# Reason: sorting is the most expensive step, and the loop is only one pass.

# Comparison with other approaches
# Point	Fractional              Knapsack (Greedy)	0/1 Knapsack (DP)	Brute force
# Items divisible?	                     Yes	             No	             Depends
# Method	                           Greedy                DP	         Try all combinations
# Time	                             O(n log n)	           O(n × W)	          O(2ⁿ)
# Space	                             O(n)	               O(n × W), O(W)   optimized	O(n)
# Optimal?	                            Yes	                Yes	               Yes
# Speed	                             Very fast	           Slower	        Impractical for large n
