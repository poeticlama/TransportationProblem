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


def vogel(S: list[int], C: list[list[int]], D: list[int]):
    return


def russell(S: list[int], C: list[list[int]], D: list[int]):
    return


def main():
    S, C, D = input_data()
    north_west_solution, z = north_west_corner(S, C, D)
    print('Initial basic feasible solution by using North-West corner method:')
    for vector in north_west_solution:
        print(vector)
    print('Answer:', z)


main()