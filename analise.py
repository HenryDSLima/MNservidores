from lagrange import lagrange, lagrange_local, pontos_do_servidor


def executar_analise_servidores(dados_servidores, incidentes):
    relatorio = []
    limite_critico = 80.0

    servidores = list(dados_servidores.keys())

    for inc in incidentes:
        t_inc = inc["t"]
        horario_str = inc["horario_original"]

        for srv in servidores:
            pontos = pontos_do_servidor(dados_servidores, srv)
            xs = [p[0] for p in pontos]
            ys = [p[1] for p in pontos]

            t_global = lagrange(pontos, t_inc)

            t_local_g3 = lagrange_local(pontos, t_inc, grau=3)

            status = "NORMAL"
            if t_global >= limite_critico or t_local_g3 >= limite_critico:
                status = "CRÍTICO (Ultrapassou 80°C)"
            elif t_global >= (limite_critico - 5.0):
                status = "ALERTA (Próximo de 80°C)"

            relatorio.append({
                "servidor": srv,
                "horario_incidente": horario_str,
                "t_incidente": t_inc,
                "global_grau9": round(t_global, 2),
                "local_grau3": round(t_local_g3, 2),
                "status": status
            })

    return relatorio