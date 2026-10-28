def knapsack(weights, values, W):
    n = len(weights)
    dp = [[0] * (W + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        for w in range(W + 1):
            dp[i][w] = dp[i - 1][w]

            if weights[i - 1] <= w:
                dp[i][w] = max(
                    dp[i][w],
                    values[i - 1] + dp[i - 1][w - weights[i - 1]]
                )

    return dp[n][W]


n = int(input("Enter number of items: "))
weights = [int(input("Enter weight: ")) for _ in range(n)]
values = [int(input("Enter value: ")) for _ in range(n)]
W = int(input("Enter knapsack capacity: "))

print("Maximum value:", knapsack(weights, values, W))
