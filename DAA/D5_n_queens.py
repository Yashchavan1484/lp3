def is_safe(board, row, col, n):
    for i in range(n):
        if board[i] != -1:
            if board[i] == col or abs(board[i] - col) == abs(i - row):
                return False
    return True


def solve(board, row, n, first_row):
    if row == n:
        return True

    if row == first_row:
        return solve(board, row + 1, n, first_row)

    for col in range(n):
        if is_safe(board, row, col, n):
            board[row] = col

            if solve(board, row + 1, n, first_row):
                return True

            board[row] = -1

    return False


def print_board(board, n):
    for r in range(n):
        print(" ".join("Q" if board[r] == c else "." for c in range(n)))


n = 8
board = [-1] * n

r = int(input("Enter first queen row (0-7): "))
c = int(input("Enter first queen column (0-7): "))

board[r] = c

if solve(board, 0, n, r):
    print("Solution:")
    print_board(board, n)
else:
    print("No solution exists.")



# Aim
# To place 8 queens on an 8×8 chessboard so that no two queens attack each other, given that the first queen is already fixed at a position chosen by the user, using backtracking.

# Theory
# Two queens attack each other if they are in the same row, same column, or same diagonal.
# We place exactly one queen per row, so row conflicts never happen. Only columns and diagonals need checking.
# Backtracking builds the solution step by step. If a placement leads to a dead end, we undo it (backtrack) and try the next option.
# The board is stored as a 1D array: board[row] = column of the queen in that row, and -1 means no queen yet.
# Diagonal check: two queens at (r1, c1) and (r2, c2) are on the same diagonal if |c1 − c2| = |r1 − r2|.
# The user’s queen is fixed in advance, so the program skips that row and fills the others around it.

# Algorithm
# Create board of size 8 filled with -1. Place the user’s queen: board[r] = c.
# Call solve(row = 0):
# If row == 8, all queens are placed, so return True.
# If row is the user’s fixed row, skip it and go to the next row.
# For each column 0 to 7:
# If the position is safe, place the queen, then recursively solve the next row.
# If the recursive call succeeds, return True.
# Otherwise remove the queen (backtrack) and try the next column.
# If no column works, return False.
# If a solution is found, print the board; otherwise print “No solution exists”.

# Dry run (4×4 board for simplicity, first queen at row 0, column 1)
# Row	Columns tried	                                                   Result
# 0	fixed	                                                           Queen at column 1
# 1	col 0 (diagonal), col 1 (same column), col 2 (diagonal), col 3	   col 3 safe
# 2	col 0	                                                           safe
# 3	col 0 (column), col 1 (column), col 2	                           col 2 safe
# . Q . .
# . . . Q
# Q . . .
# . . Q .

# board = [1, 3, 0, 2], so a solution is found without any backtracking here.

# A backtracking case: on 4×4, if the first queen is at (0, 0), every path ends in a dead end, so the program prints “No solution exists.” On the real 8×8 board, every starting square can be completed to a full solution, but the program may backtrack many times before finding it.

# Time and space complexity

# n = 8 (board size).

#         Complexity	            Reason
# Time	O(n!)in the worst case	Row 1 has up to n choices, row 2 fewer, and so on. Each is_safe check also costs O(n), so the strict bound is O(n · n!)
# Space	O(n)	                The board array plus the recursion stack (depth n)

# In practice, pruning (unsafe columns are rejected immediately) makes it far faster than n!. For n = 8, only a few thousand placements are tried instead of 40,320 full arrangements.

# Comparison with other approaches

# | Point               | Brute Force                            | Backtracking (this code)              | Optimized Backtracking (sets or bitmask) |
# |---------------------|----------------------------------------|---------------------------------------|------------------------------------------|
# | Idea                | Try all C(64,8) placements, then check | Place row by row, reject unsafe early | Same, but safety check in O(1)           |
# | Placements examined | About 4.4 billion                      | Few thousand                          | Few thousand                             |
# | Safety check        | After full placement                   | O(n) per queen                        | O(1)                                     |
# | Time                | Exponential, huge                      | O(n!), heavily pruned                 | Faster by a factor of n                  |
# | Space               | O(n)                                   | O(n)                                  | O(n)                                     |

# Why backtracking is better than brute force: it abandons a partial solution the moment it breaks a rule, instead of building complete boards and checking them at the end. This prunes a huge part of the search space.

# Limitation: it is still exponential in the worst case, which is why it is only practical for small n.

# Easy example

# Think of seating guests at a wedding table where certain people refuse to sit near each other. You seat guests one by one. If you reach a seat where nobody can sit without a fight, you go back, move the previous guest elsewhere, and try again. That undo-and-retry process is backtracking.

# Another example is solving a maze: at every junction pick a path, and if you hit a dead end, return to the last junction and take a different path.
