def input_data():
    S = map(int, input('Enter a vector of coefficients of supply').split())
    print('Enter a matrix of coefficients of cost')
    C = list()
    for i in range(len(S)):
        C.append(map(int, input().split()))
    D = map(int, input('Enter a vector of demand').split())
    return S, C, D

def north_west_corner(S: list[int], C: list[list[int]], D: list[int]):
    return


def vogel(S, C, D):
    return


def russell(S, C, D):
    return


