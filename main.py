# Function for scanning input
def input_data():
    S = list(map(int, input('Enter a vector of coefficients of supply\n').split()))
    print('Enter a matrix of coefficients of cost')
    C = list()
    for i in range(len(S)):
        C.append(list(map(int, input().split())))
    D = list(map(int, input('Enter a vector of demand\n').split()))
    return S, C, D


# North-West corner method function
def north_west_corner(S: list[int], C: list[list[int]], D: list[int]) -> (list[list[int]], int):
    # Copies of demand and supply lists to work with them without affecting other solutions
    D_copy = D.copy()
    S_copy = S.copy()
    solution = [[0 for _ in range(len(C[0]))] for _ in range(len(C))]
    z = 0

    # Loop for moving in the matrix
    for i in range(len(C)):
        for j in range(len(C[i])):
            # If demand is less than supply
            if D_copy[j] <= S_copy[i]:
                solution[i][j] = D_copy[j]
                # Fixing demand and supply lists
                D_copy[j] -= solution[i][j]
                S_copy[i] -= solution[i][j]
                z += solution[i][j] * C[i][j]
            # If demand is more than supply
            elif D_copy[j] > S_copy[i]:
                solution[i][j] = S_copy[i]
                # Fixing demand and supply lists
                S_copy[i] -= solution[i][j]
                D_copy[j] -= solution[i][j]
                z += solution[i][j] * C[i][j]
                break

    return solution, z


# Vogel's approximation method
def vogel(S: list[int], C: list[list[int]], D: list[int]) -> (list[list[int]], int):
    # Copying lists to have no effect for inputs used in another solutions
    D_copy = D.copy()
    S_copy = S.copy()
    C_copy = [C[i].copy() for i in range(len(C))]
    z = 0
    solution = [[0 for _ in range(len(C[0]))] for _ in range(len(C))]
    columns = list()
    # Making list of columns for easier finding of maximum
    for j in range(len(C[0])):
        columns.append([C[i][j] for i in range(len(C))])
    # Lists for collecting differences between 2 smallest numbers in each row/column
    row_difference = [0 for _ in range(len(S))]
    column_difference = [0 for _ in range(len(D))]

    # Main loop
    while sum(S_copy) > 0:
        c = 0
        # Checking if only one row is not finished
        for i in range(len(S_copy)):
            if S_copy[i] != 0:
                c += 1
                ind = i
        # Finishing of solution if only one row of supply left
        if c == 1:
            for i in range(len(D_copy)):
                if D_copy[i] != 0:
                    z += D_copy[i] * C[ind][i]
                    solution[ind][i] = D_copy[i]
            break

        # Collecting differences in each row and column
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
        # Finding maximum difference
        max_row = max(row_difference)
        max_column = max(column_difference)

        if max_row >= max_column:
            # Finding an element to be chosen
            ind_diff = row_difference.index(max_row)
            chosen_el = min(C_copy[ind_diff])
            elem_indexes = (ind_diff, C_copy[ind_diff].index(chosen_el))
            if S_copy[elem_indexes[0]] >= D_copy[elem_indexes[1]]:
                solution[elem_indexes[0]][elem_indexes[1]] = D_copy[elem_indexes[1]]
                z += solution[elem_indexes[0]][elem_indexes[1]] * C_copy[elem_indexes[0]][elem_indexes[1]]
                S_copy[elem_indexes[0]] -= D_copy[elem_indexes[1]]
                D_copy[elem_indexes[1]] -= D_copy[elem_indexes[1]]
                # Leaving 10**5 not to choose same row/column in the future
                C_copy[elem_indexes[0]][elem_indexes[1]] = 10**5
                columns[elem_indexes[1]][elem_indexes[0]] = 10**5
            elif S_copy[elem_indexes[0]] < D_copy[elem_indexes[1]]:
                solution[elem_indexes[0]][elem_indexes[1]] = S_copy[elem_indexes[0]]
                z += solution[elem_indexes[0]][elem_indexes[1]] * C_copy[elem_indexes[0]][elem_indexes[1]]
                D_copy[elem_indexes[1]] -= S_copy[elem_indexes[0]]
                S_copy[elem_indexes[0]] -= S_copy[elem_indexes[0]]
                # Leaving 10**5 not to choose same row/column in the future
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
                # Leaving 10**5 not to choose same row/column in the future
                C_copy[elem_indexes[1]][elem_indexes[0]] = 10 ** 5
                columns[elem_indexes[0]][elem_indexes[1]] = 10 ** 5
            elif S_copy[elem_indexes[1]] < D_copy[elem_indexes[0]]:
                solution[elem_indexes[1]][elem_indexes[0]] = S_copy[elem_indexes[1]]
                z += solution[elem_indexes[1]][elem_indexes[0]] * columns[elem_indexes[0]][elem_indexes[1]]
                D_copy[elem_indexes[0]] -= S_copy[elem_indexes[1]]
                S_copy[elem_indexes[1]] -= S_copy[elem_indexes[1]]
                # Leaving 10**5 not to choose same row/column in the future
                C_copy[elem_indexes[1]][elem_indexes[0]] = 10 ** 5
                columns[elem_indexes[0]][elem_indexes[1]] = 10 ** 5
    return solution, z


# Russell's approximation method
def russell(S: list[int], C: list[list[int]], D: list[int]) -> (list[list[int]], int):
    # Copying inputs to avoid changing them
    S_copy = S.copy()
    D_copy = D.copy()
    z = 0
    solution = [[0 for _ in range(len(C[0]))] for _ in range(len(C))]
    columns = list()
    # Finding list of columns
    for j in range(len(C[0])):
        columns.append([C[i][j] for i in range(len(C))])
    # Finding maximum element of each row/column
    U = [max(C[i]) for i in range(len(C))]
    V = [max(columns[i]) for i in range(len(columns))]
    # Lists of indexes of rows and columns that were checked
    rows_checked = list()
    columns_checked = list()

    # Main loop
    while sum(S_copy) > 0:
        delta = [[0 for _ in range(len(C[0]))] for _ in range(len(C))]
        minimal = 10 ** 5
        # Finding delta matrix
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


# Main function
def main():
    # Collecting inputs
    S, C, D = input_data()
    # Checking if problem is balanced
    if sum(S) != sum(D):
        print('The problem is not balanced!')
        return
    # Finding solution by North-West corner method
    solution, z = north_west_corner(S, C, D)
    print('Initial basic feasible solution by using North-West corner method:')
    for vector in solution:
        print(vector)
    print('Answer:', z)
    print()

    # Finding solution by Vogel's approximation method
    solution, z = vogel(S, C, D)
    print("Initial basic feasible solution by using Vogel's approximation method:")
    for vector in solution:
        print(vector)
    print('Answer:', z)
    print()

    # Finding solution by Russell's approximation method
    solution, z = russell(S, C, D)
    print("Initial basic feasible solution by using Russell's approximation method:")
    for vector in solution:
        print(vector)
    print('Answer:', z)
    print()


main()