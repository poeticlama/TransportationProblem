def input_data():
    S = list(map(int, input('Enter a vector of coefficients of supply\n').split()))
    print('Enter a matrix of coefficients of cost')
    C = list()
    for i in range(len(S)):
        C.append(list(map(int, input().split())))
    D = list(map(int, input('Enter a vector of demand\n').split()))
    return S, C, D


def north_west_corner(S: list[int], C: list[list[int]], D: list[int]) -> (list[list[int]], int):
    D_copy = D.copy()
    S_copy = S.copy()
    solution = [[0 for _ in range(len(C[0]))] for _ in range(len(C))]
    z = 0

    for i in range(len(C)):
        for j in range(len(C[i])):
            if D_copy[j] <= S_copy[i]:
                solution[i][j] = D_copy[j]
                D_copy[j] -= solution[i][j]
                S_copy[i] -= solution[i][j]
                z += solution[i][j] * C[i][j]
            elif D_copy[j] > S_copy[i]:
                solution[i][j] = S_copy[i]
                S_copy[i] -= solution[i][j]
                D_copy[j] -= solution[i][j]
                z += solution[i][j] * C[i][j]
                break

    return solution, z


def vogel(S: list[int], C: list[list[int]], D: list[int]) -> (list[list[int]], int):
    D_copy = D.copy()
    S_copy = S.copy()
    C_copy = [C[i].copy() for i in range(len(C))]
    z = 0
    solution = [[0 for _ in range(len(C[0]))] for _ in range(len(C))]
    columns = list()
    for j in range(len(C[0])):
        columns.append([C[i][j] for i in range(len(C))])
    row_difference = [0 for _ in range(len(S))]
    column_difference = [0 for _ in range(len(D))]
    while sum(S_copy) > 0:
        c = 0
        for i in range(len(S_copy)):
            if S_copy[i] != 0:
                c += 1
                ind = i
        if c == 1:
            for i in range(len(D_copy)):
                if D_copy[i] != 0:
                    z += D_copy[i] * C[ind][i]
                    solution[ind][i] = D_copy[i]
            break

        for i in range(len(D)):
            column_sorted = sorted(columns[i])
            if column_sorted[1] != 10**5:
                column_difference[i] = column_sorted[1] - column_sorted[0]
            else:
                column_difference[i] = 0
        for i in range(len(S)):
            row_sorted = sorted(C_copy[i])
            if row_sorted[1] != 10**5:
                row_difference[i] = row_sorted[1] - row_sorted[0]
            else:
                row_difference[i] = 0
        max_row = max(row_difference)
        max_column = max(column_difference)
        if max_row >= max_column:
            ind_diff = row_difference.index(max_row)
            chosen_el = min(C_copy[ind_diff])
            elem_indexes = (ind_diff, C_copy[ind_diff].index(chosen_el))
            if S_copy[elem_indexes[0]] >= D_copy[elem_indexes[1]]:
                solution[elem_indexes[0]][elem_indexes[1]] = D_copy[elem_indexes[1]]
                z += solution[elem_indexes[0]][elem_indexes[1]] * C_copy[elem_indexes[0]][elem_indexes[1]]
                S_copy[elem_indexes[0]] -= D_copy[elem_indexes[1]]
                D_copy[elem_indexes[1]] -= D_copy[elem_indexes[1]]
                C_copy[elem_indexes[0]][elem_indexes[1]] = 10**5
                columns[elem_indexes[1]][elem_indexes[0]] = 10**5
            elif S_copy[elem_indexes[0]] < D_copy[elem_indexes[1]]:
                solution[elem_indexes[0]][elem_indexes[1]] = S_copy[elem_indexes[0]]
                z += solution[elem_indexes[0]][elem_indexes[1]] * C_copy[elem_indexes[0]][elem_indexes[1]]
                D_copy[elem_indexes[1]] -= S_copy[elem_indexes[0]]
                S_copy[elem_indexes[0]] -= S_copy[elem_indexes[0]]
                C_copy[elem_indexes[0]][elem_indexes[1]] = 10 ** 5
                columns[elem_indexes[1]][elem_indexes[0]] = 10 ** 5
        elif max_column > max_row:
            ind_diff = column_difference.index(max_column)
            chosen_el = min(columns[ind_diff])
            elem_indexes = (ind_diff, columns[ind_diff].index(chosen_el))
            if S_copy[elem_indexes[1]] >= D_copy[elem_indexes[0]]:
                solution[elem_indexes[1]][elem_indexes[0]] = D_copy[elem_indexes[0]]
                z += solution[elem_indexes[1]][elem_indexes[0]] * columns[elem_indexes[0]][elem_indexes[1]]
                S_copy[elem_indexes[1]] -= D_copy[elem_indexes[0]]
                D_copy[elem_indexes[0]] -= D_copy[elem_indexes[0]]
                C_copy[elem_indexes[1]][elem_indexes[0]] = 10 ** 5
                columns[elem_indexes[0]][elem_indexes[1]] = 10 ** 5
            elif S_copy[elem_indexes[1]] < D_copy[elem_indexes[0]]:
                solution[elem_indexes[1]][elem_indexes[0]] = S_copy[elem_indexes[1]]
                z += solution[elem_indexes[1]][elem_indexes[0]] * columns[elem_indexes[0]][elem_indexes[1]]
                D_copy[elem_indexes[0]] -= S_copy[elem_indexes[1]]
                S_copy[elem_indexes[1]] -= S_copy[elem_indexes[1]]
                C_copy[elem_indexes[1]][elem_indexes[0]] = 10 ** 5
                columns[elem_indexes[0]][elem_indexes[1]] = 10 ** 5
    return solution, z


def russell(S: list[int], C: list[list[int]], D: list[int]) -> (list[list[int]], int):
    S_copy = S.copy()
    D_copy = D.copy()
    z = 0
    solution = [[0 for _ in range(len(C[0]))] for _ in range(len(C))]
    columns = list()
    for j in range(len(C[0])):
        columns.append([C[i][j] for i in range(len(C))])
    U = [max(C[i]) for i in range(len(C))]
    V = [max(columns[i]) for i in range(len(columns))]
    rows_checked = list()
    columns_checked = list()

    while sum(S_copy) > 0:
        delta = [[0 for _ in range(len(C[0]))] for _ in range(len(C))]
        minimal = 10 ** 5
        for i in range(len(S)):
            if i in rows_checked:
                for j in range(len(D)):
                    delta[i][j] = 10 ** 5
                continue
            for j in range(len(D)):
                if j in columns_checked:
                    delta[i][j] = 10 ** 5
                    continue
                delta[i][j] = C[i][j] - (U[i] + V[j])
                if delta[i][j] < minimal:
                    i_min, j_min = (i, j)
                    minimal = delta[i][j]
        if S_copy[i_min] == D_copy[j_min]:
            z += S_copy[i_min] * C[i_min][j_min]
            rows_checked.append(i_min)
            columns_checked.append(j_min)
            solution[i_min][j_min] = D_copy[j_min]
            S_copy[i_min] = 0
            D_copy[j_min] = 0
        elif S_copy[i_min] > D_copy[j_min]:
            z += D_copy[j_min] * C[i_min][j_min]
            columns_checked.append(j_min)
            solution[i_min][j_min] = D_copy[j_min]
            S_copy[i_min] -= D_copy[j_min]
            D_copy[j_min] = 0
        elif D_copy[j_min] > S_copy[i_min]:
            z += S_copy[i_min] * C[i_min][j_min]
            rows_checked.append(i_min)
            solution[i_min][j_min] = S_copy[i_min]
            D_copy[j_min] -= S_copy[i_min]
            S_copy[i_min] = 0
    return solution, z


def main():
    S, C, D = input_data()
    if sum(S) != sum(D):
        print('The problem is not balanced!')
        return
    solution, z = north_west_corner(S, C, D)
    print('Initial basic feasible solution by using North-West corner method:')
    for vector in solution:
        print(vector)
    print('Answer:', z)
    print()

    solution, z = vogel(S, C, D)
    print("Initial basic feasible solution by using Vogel's approximation method:")
    for vector in solution:
        print(vector)
    print('Answer:', z)
    print()

    solution, z = russell(S, C, D)
    print("Initial basic feasible solution by using Russell's approximation method:")
    for vector in solution:
        print(vector)
    print('Answer:', z)
    print()


main()