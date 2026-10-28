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
