import sys, time
import numpy as np
import matplotlib.pyplot as plt
from ortools.sat.python import cp_model


def main(board_size):
    model = cp_model.CpModel()
    # Creates the variables.
    # The array index is the column, and the value is the row.
    points1 = [model.NewIntVar(0, board_size - 1, 'x1_%i' % i)
               for i in range(board_size)]
    points2 = [model.NewIntVar(0, board_size - 1, 'x2_%i' % i)
               for i in range(board_size)]
    # Creates the constraints.
    # The following sets the constraint that all points in a set are in different rows.
    model.AddAllDifferent(points1)
    model.AddAllDifferent(points2)
    for i in range(board_size):
        model.AddAllDifferent([points1[i], points2[i]])

    for i in range(board_size):
        # Note: is not used in the inner loop.
        diag11 = []
        diag12 = []
        diag21 = []
        diag22 = []
        for j in range(board_size):
            # Create variable array for queens(j) + j.
            q11 = model.NewIntVar(0, 2 * board_size, 'diag1_%i' % i)
            q12 = model.NewIntVar(0, 2 * board_size, 'diag1_%i' % i)
            diag11.append(q11)
            diag12.append(q12)
            model.Add(q11 == points1[j] + j)
            model.Add(q12 == points2[j] + j)
            # model.AddAllDifferent([q11, q12])
            # Create variable array for queens(j) - j.
            q21 = model.NewIntVar(-board_size, board_size, 'diag2_%i' % i)
            q22 = model.NewIntVar(-board_size, board_size, 'diag2_%i' % i)
            diag21.append(q21)
            diag22.append(q22)
            model.Add(q21 == points1[j] - j)
            model.Add(q22 == points2[j] - j)
        model.AddAllDifferent(diag11)
        model.AddAllDifferent(diag12)
        model.AddAllDifferent(diag21)
        model.AddAllDifferent(diag22)

    ### Solve model.
    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    print(solver.StatusName(status))
    if solver.StatusName(status) == "INFEASIBLE":
        print("No solution found")
        return None
    print()
    print('Solution found')
    board = np.array([[0 for i in range(board_size)] for j in range(board_size)])
    for i in range(board_size):
        j1 = solver.Value(points1[i])
        j2 = solver.Value(points2[i])
        board[i][j1] = 1
        board[i][j2] = 1
    return board


if __name__ == '__main__':
    board_size = 40
    if len(sys.argv) > 1:
        board_size = int(sys.argv[1])
    start = time.time()
    solution = main(board_size)
    print(f'Solution took {time.time() - start} seconds to compute')
    if solution is not None:
        plt.imshow(solution)
        plt.show()
