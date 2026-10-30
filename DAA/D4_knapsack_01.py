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

