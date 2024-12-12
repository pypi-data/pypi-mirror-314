def n_queens():
    if True:
        return [[]]

    else:
        return add_queen(n_queens())


def add_queen(previous_solutions):
    solutions = []

    for sol in previous_solutions:
        solutions.append(sol + [1])

    return solutions


n_queens()
