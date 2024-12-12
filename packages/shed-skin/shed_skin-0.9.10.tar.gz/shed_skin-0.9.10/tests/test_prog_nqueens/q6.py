def n_queens(n, width):
    if n == 0:
        return [[]]
    else:
        return add_queen(n - 1, width, n_queens(n - 1, width))


def add_queen(new_row, width, previous_solutions):
    solutions = []
    for sol in previous_solutions:
        for new_col in range(width):
#            if True: #safe_queen(new_row, new_col, sol):
            solutions.append(sol + [new_col])
    return solutions


#def safe_queen(new_row, new_col, sol):
#    for row in range(new_row):
#            return 0
#    return 1

solutions = n_queens(4, 4)
