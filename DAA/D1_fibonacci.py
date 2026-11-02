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

#theory:- 
# Theory
# 1) The Fibonacci sequence is a series where each term is the sum of the previous two: 0, 1, 1, 2, 3, 5, 8, 13...
# 2) Formula: F(n) = F(n-1) + F(n-2), with F(0) = 0 and F(1) = 1.
# 3) Iterative method: uses a loop and keeps only the last two values.
# 4) Recursive method: the function calls itself for smaller values until it reaches the base case (n ≤ 1).
# 5) A step counter is used to show how many operations or function calls each method needs.
    
# Algorithm
# 1) Iterative
# i)Read n (number of terms). If n ≤ 0, print an error.
# ii)Set n1 = 0, n2 = 1, steps = 0.
# iii)Repeat n times: print n1, then update n1 = n2 and n2 = n1 + n2 (done together), and increase steps by 1.
# iv) Print total steps.

# 2) Recursive

# i) Define recur_fibo(n) and increase the counter on every call.
# ii) If n ≤ 1, return n (base case).
# iii) Else return recur_fibo(n-1) + recur_fibo(n-2).
# iv) Call it for i = 0 to n-1, print each result, and print the total calls.

# Dry run (nterms = 5)
# Output for both: 0 1 1 2 3
# Iterative steps = 5
# Recursive calls for i = 0, 1, 2, 3, 4 are 1, 1, 3, 5, 9, so the total is 19

# Comparison (why iterative is better)
# Point	Iterative	    Recursive	           Recursive + Memoization
# Time	O(n)	         O(2ⁿ)	                O(n)
# Space	O(1)	         O(n)	                O(n)
# Speed   for n = 40	Instant	Very slow 
#                  (hundreds of millions of calls)	Instant
# Code	Slightly longer	Short, matches the formula	Short
# Risk	None	  Stack overflow for large n	        Stack depth for large n

