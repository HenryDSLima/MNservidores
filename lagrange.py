def separar_pontos(pontos):
    if len(pontos) == 0:
        raise ValueError("A lista de pontos está vazia.")

    xs = []
    ys = []
    for ponto in pontos:
        xs.append(float(ponto[0]))
        ys.append(float(ponto[1]))

    for i in range(len(xs)):
        for j in range(i + 1, len(xs)):
            if xs[i] == xs[j]:
                raise ValueError(f"Nó repetido em x = {xs[i]}.")

    return xs, ys


def polinomio_base(xs, k, x):
    resultado = 1.0
    for j in range(len(xs)):
        if j != k:
            resultado *= (x - xs[j]) / (xs[k] - xs[j])
    return resultado


def lagrange(pontos, x):
    xs, ys = separar_pontos(pontos)

    soma = 0.0
    for k in range(len(xs)):
        soma += ys[k] * polinomio_base(xs, k, x)
    return soma


def lagrange_varios(pontos, lista_x):
    return [lagrange(pontos, x) for x in lista_x]


def lagrange_local(pontos, x, grau=3):
    quantidade = grau + 1
    if quantidade > len(pontos):
        quantidade = len(pontos)

    ordenados = sorted(pontos, key=lambda p: abs(p[0] - x))
    escolhidos = ordenados[:quantidade]
    escolhidos.sort(key=lambda p: p[0])
    return lagrange(escolhidos, x)


def pontos_do_servidor(dados_servidores: dict, servidor: str) -> list[tuple[float, float]]:
    serie = dados_servidores[servidor]
    return list(zip(serie["t"], serie["temp"]))


if __name__ == "__main__":
    teste = [(0, 0), (1, 1), (2, 4)]
    print("P(1.5) =", lagrange(teste, 1.5), "(esperado 2.25)")

    for t, T in teste:
        print(f"P({t}) = {lagrange(teste, t)} (esperado {T})")