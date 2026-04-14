#!/usr/bin/env python3
"""
Task 3: N-Queens Problem
Solves N-Queens using backtracking and displays all solutions.
"""


def is_safe(board, row, col, n):
    """Check if placing a queen at (row, col) is safe."""
    # Check column
    for i in range(row):
        if board[i][col] == 1:
            return False
    # Check upper-left diagonal
    i, j = row - 1, col - 1
    while i >= 0 and j >= 0:
        if board[i][j] == 1:
            return False
        i -= 1
        j -= 1
    # Check upper-right diagonal
    i, j = row - 1, col + 1
    while i >= 0 and j < n:
        if board[i][j] == 1:
            return False
        i -= 1
        j += 1
    return True


def solve_nqueens(board, row, n, solutions):
    """Backtracking solver — tries to place a queen in each row."""
    if row == n:
        # Deep-copy the current board as a solution
        solutions.append([r[:] for r in board])
        return

    for col in range(n):
        if is_safe(board, row, col, n):
            board[row][col] = 1
            solve_nqueens(board, row + 1, n, solutions)
            board[row][col] = 0  # Backtrack


def print_board(board, solution_num=None):
    """Pretty-print a chessboard solution."""
    n = len(board)
    header = f"Solution #{solution_num}" if solution_num else "Board"
    print(f"\n{header}")
    print("  " + " ".join(str(c) for c in range(n)))
    for r, row in enumerate(board):
        cells = " ".join("Q" if cell else "." for cell in row)
        print(f"{r} {cells}")


def get_queen_positions(board):
    """Return (row, col) tuples for each queen."""
    return [(r, row.index(1)) for r, row in enumerate(board)]


def main():
    print("╔══════════════════════════╗")
    print("║  N-Queens Solver         ║")
    print("╚══════════════════════════╝\n")

    try:
        n = int(input("Enter N (board size, e.g. 8): ").strip())
        if n < 1:
            raise ValueError
    except ValueError:
        print("Please enter a positive integer.")
        return

    board = [[0] * n for _ in range(n)]
    solutions = []

    print(f"\nSolving {n}-Queens problem...")
    solve_nqueens(board, 0, n, solutions)

    if not solutions:
        print(f"No solutions exist for N={n}.")
        return

    print(f"✅ Found {len(solutions)} solution(s) for N={n}.\n")

    # Ask how many to display
    try:
        show = int(input(f"How many solutions to display? (1-{len(solutions)}): ").strip())
        show = max(1, min(show, len(solutions)))
    except ValueError:
        show = 1

    for i, sol in enumerate(solutions[:show], start=1):
        print_board(sol, solution_num=i)
        positions = get_queen_positions(sol)
        print(f"  Queens at: {positions}")

    if len(solutions) > show:
        print(f"\n... and {len(solutions) - show} more solution(s) not displayed.")

    print(f"\nTotal solutions for N={n}: {len(solutions)}")

    # Show known counts for reference
    known = {1: 1, 2: 0, 3: 0, 4: 2, 5: 10, 6: 4, 7: 40, 8: 92, 9: 352, 10: 724}
    if n in known:
        expected = known[n]
        match = "✅" if len(solutions) == expected else "❌"
        print(f"{match} Expected solutions for N={n}: {expected}")


if __name__ == "__main__":
    main()