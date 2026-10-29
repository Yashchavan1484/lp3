nterms = int(input("How many terms? "))

if nterms <= 0:
    print("Please enter a positive integer")
else:
    print("\n--- Iterative Method ---")
    print("Fibonacci sequence:")

    n1, n2 = 0, 1
    iter_steps = 0

    while iter_steps < nterms:
        print(n1, end=" ")
        n1, n2 = n2, n1 + n2
        iter_steps += 1

    print(f"\nTotal Iterative Steps: {iter_steps}")


    rec_steps = 0


    def recur_fibo(n):
        global rec_steps
        rec_steps += 1

        if n <= 1:
            return n
        else:
            return recur_fibo(n - 1) + recur_fibo(n - 2)


    print("\n--- Recursive Method ---")
    print("Fibonacci sequence:")

    for i in range(nterms):
        print(recur_fibo(i), end=" ")

    print(f"\nTotal Recursive Steps: {rec_steps}")