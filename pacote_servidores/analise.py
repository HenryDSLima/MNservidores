from .lagrange import lagrange, lagrange_local, pontos_do_servidor


def executar_analise_servidores(dados_servidores, incidentes):
    relatorio = []
    relatorio_geral = {
        "SRV-01": [],
        "SRV-02": [],
        "SRV-03": []
    }

    # pontos_serv1 = pontos_do_servidor(dados_servidores, "SRV-01")
    # pontos_serv2 = pontos_do_servidor(dados_servidores, "SRV-02")
    # pontos_serv3 = pontos_do_servidor(dados_servidores, "SRV-03")

    limite_critico = 80.0

    servidores = list(dados_servidores.keys())

    for inc in incidentes:
        t_inc = inc["t"]
        horario_str = inc["horario_original"]

        for srv in servidores:
            pontos = pontos_do_servidor(dados_servidores, srv)

            t_global = lagrange(pontos, t_inc)

            t_local_g3 = lagrange_local(pontos, t_inc, grau=3)

            pontos.append((t_inc, t_local_g3))
            pontos.sort(key=lambda p:p[0])

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

            for ponto in pontos:
                if ponto not in relatorio_geral[srv]:
                    relatorio_geral[srv].append(ponto)
                    relatorio_geral[srv].sort(key=lambda p:p[0])
                    

    return relatorio, relatorio_geral
