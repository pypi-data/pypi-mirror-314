def n_queens():
    n = 4
    width = 4

    if n == 0:
        return [[]]
    else:
        return add_queen(n - 1, width, n_queens())


def add_queen(new_row, width, previous_solutions):
    solutions = []
    for sol in previous_solutions:
        for new_col in range(width):
            solutions.append(sol + [new_col])
    return solutions

n_queens()
