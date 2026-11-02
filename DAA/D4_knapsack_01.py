def knapsack(w_arr, P, W):
    n = len(w_arr)
    # V is the DP matrix shown on the board
    V = [[0] * (W + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        for w in range(W + 1):
            if w_arr[i - 1] <= w:
                # V[i, w] = max{ V[i-1, w], V[i-1, w-w[i]] + P[i] }
                V[i][w] = max(
                    V[i - 1][w], 
                    V[i - 1][w - w_arr[i - 1]] + P[i - 1]
                )
            else:
                V[i][w] = V[i - 1][w]

    return V[n][W]

n = int(input("Enter number of items: "))
w_arr = [int(input("Enter weight: ")) for _ in range(n)]
P = [int(input("Enter value (profit): ")) for _ in range(n)]
W = int(input("Enter knapsack capacity: "))

print("Maximum value:", knapsack(w_arr, P, W))

# Aim
# To find the maximum profit that can be placed in a knapsack of capacity W, when each item must be taken whole or not at all (0/1), using dynamic programming.

# Theory
# In 0/1 Knapsack, each item is either taken (1) or left (0). Items cannot be split.
# Greedy by ratio fails here, so we use Dynamic Programming (DP).
# DP breaks the problem into smaller subproblems and stores their answers in a table, so nothing is calculated twice.
# V[i][w] = maximum profit using only the first i items with a bag of capacity w.
# Recurrence relation:
# If item i fits (weight ≤ w): V[i][w] = max( V[i-1][w], V[i-1][w - weight_i] + profit_i )
# Otherwise: V[i][w] = V[i-1][w]
# The first option means “don’t take item i”. The second means “take item i”: add its profit and use the best result for the remaining capacity.
# The final answer is V[n][W].
    
# Algorithm
# Create a table V of size (n+1) × (W+1), filled with 0.
# For each item i from 1 to n, and for each capacity w from 0 to W:
# If weight of item i ≤ w: V[i][w] = max(not take, take).
# Else: V[i][w] = V[i-1][w].
# Return V[n][W].

Dry run

Weights = [2, 3, 4], Profits = [3, 4, 5], W = 5

i \ w	        0	1	2	3	4	5
0 (no items)	0	0	0	0	0	0
1 (w=2, p=3)	0	0	3	3	3	3
2 (w=3, p=4)	0	0	3	4	4	7
3 (w=4, p=5)	0	0	3	4	5	7

Example cell: V[2][5] = max( V[1][5] = 3, V[1][2] + 4 = 3 + 4 = 7 ) = 7.

Maximum value = 7

Which items were taken (trace back from V[3][5]): V[3][5] = V[2][5], so item 3 is not taken. V[2][5] ≠ V[1][5], so item 2 is taken, leaving capacity 2. V[1][2] ≠ V[0][2], so item 1 is taken. Items taken: 1 and 2 (weight 5, profit 7). The program itself only prints the value, not the items.

Time and space complexity

n = number of items, W = capacity.

	Complexity	Reason
Time	O(n × W)	The table has (n+1)(W+1) cells, each filled in constant time
Space	O(n × W)	The full table is stored

Optimization: if only the final value is needed, use a single 1D array of size W+1 (looping w from W down to 0), which reduces space to O(W).

Note: O(nW) is called pseudo-polynomial, because it depends on the value of W, not just the number of inputs.

Comparison with other approaches
Point	Brute force	Greedy (by ratio)	DP (this code)
Idea	Try all 2ⁿ subsets	Pick the best ratio first	Build table of subproblems
Time	O(2ⁿ)	O(n log n)	O(n × W)
Space	O(n)	O(n)	O(n × W) or O(W)
Optimal for 0/1?	Yes	No	Yes
Practical?	Only tiny n	Fast but can be wrong	Yes

Why DP is better here: brute force is correct but exponential. Greedy is fast but wrong for 0/1. DP is both correct and reasonably fast.

Proof that greedy fails: W = 50, items (w=10, p=60), (w=20, p=100), (w=30, p=120).

Greedy by ratio picks items 1 and 2 → profit 160.
DP finds items 2 and 3 → profit 220.
Fractional vs 0/1 (very likely viva question)
	Fractional	0/1
Items divisible?	Yes	No
Method	Greedy	Dynamic programming
Time	O(n log n)	O(nW)
Answer for the example above	240	220
Easy example

You are packing a suitcase with a 5 kg limit. A laptop (2 kg, ₹3000), a camera (3 kg, ₹4000) and a heavy book (4 kg, ₹5000) can’t be cut into pieces. You either pack them whole or leave them. The table tries every combination smartly and finds that the laptop and camera together give the most value (₹7000).
