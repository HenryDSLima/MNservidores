def tabela_diferencas_divididas(x: list[float], y: list[float]) -> list[float]:
    if len(x) != len(y):
        raise ValueError("As listas 'x' e 'y' devem ter o mesmo tamanho.")
    if len(x) == 0:
        raise ValueError("As listas de pontos não podem estar vazias.")

    n = len(x) - 1
    d = [float(val) for val in y]

    for j in range(1, n + 1):
        for i in range(n, j - 1, -1):
            denominador = x[i] - x[i - j]
            if denominador == 0:
                raise ValueError("Os valores de 'x' devem ser todos distintos.")
            d[i] = (d[i] - d[i - 1]) / denominador

    return d


def interpolar_newton(x: list[float], y: list[float], t: float) -> float:
    d = tabela_diferencas_divididas(x, y)
    n = len(x) - 1

    p = 0.0
    for k in range(n + 1):
        produto = 1.0
        for j in range(k):
            produto *= (t - x[j])
        p += d[k] * produto

    return p


def imprimir_tabela_completa(x: list[float], y: list[float]) -> list[list[float]]:
    n = len(x)
    tabela = [[0.0] * n for _ in range(n)]

    for i in range(n):
        tabela[i][0] = float(y[i])

    for j in range(1, n):
        for i in range(n - j):
            tabela[i][j] = (tabela[i + 1][j - 1] - tabela[i][j - 1]) / (x[i + j] - x[i])

    return tabela
