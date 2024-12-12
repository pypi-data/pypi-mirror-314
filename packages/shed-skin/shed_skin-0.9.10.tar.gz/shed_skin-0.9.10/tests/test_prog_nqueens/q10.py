def n_queens():
    n = 4
    width = 4

    if n == 0:
        return [[]]
    else:
        return add_queen(n_queens())


def add_queen(previous_solutions):
    solutions = []
    for sol in previous_solutions:
        for new_col in range(5):
            solutions.append(sol + [new_col])
    return solutions


n_queens()
