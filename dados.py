import csv
from datetime import datetime


def _parse_data_hora(texto_data: str) -> datetime:
    """Converte strings de data/hora suportando os formatos ISO e brasileiro."""
    formatos = ("%Y-%m-%d %H:%M:%S", "%d-%m-%Y %H:%M:%S")
    for fmt in formatos:
        try:
            return datetime.strptime(texto_data.strip(), fmt)
        except ValueError:
            continue
    raise ValueError(f"Formato de data/hora não reconhecido: {texto_data}")


def carregar_temperaturas(
    caminho_csv: str,
) -> tuple[dict[str, dict[str, list[float]]], datetime]:
    """
    Lê o arquivo temperaturas.csv e organiza as séries por servidor.
    Converte os horários em horas decorridas (t) a partir da medição inicial.

    Retorna:
        - dados_servidores: {'SRV-01': {'t': [...], 'temp': [...]}, ...}
        - referencia_inicial: objeto datetime correspondente a t = 0.0
    """
    registros_brutos = []

    with open(caminho_csv, mode="r", encoding="utf-8") as arquivo:
        leitor = csv.DictReader(arquivo)
        for linha in leitor:
            dt = _parse_data_hora(linha["data_hora"])
            servidor = linha["servidor_id"].strip()
            temperatura = float(linha["temperatura_c"])
            registros_brutos.append((dt, servidor, temperatura))

    if not registros_brutos:
        raise ValueError("O arquivo CSV de temperaturas está vazio.")

    referencia_inicial = min(reg[0] for reg in registros_brutos)
    dados_servidores: dict[str, dict[str, list[float]]] = {}

    for dt, servidor, temperatura in registros_brutos:
        if servidor not in dados_servidores:
            dados_servidores[servidor] = {"t": [], "temp": []}

        horas_decorridas = (dt - referencia_inicial).total_seconds() / 3600.0
        dados_servidores[servidor]["t"].append(horas_decorridas)
        dados_servidores[servidor]["temp"].append(temperatura)

    return dados_servidores, referencia_inicial


def carregar_incidentes(caminho_log: str, referencia_inicial: datetime) -> list[dict]:
    """
    Lê o arquivo incidentes.log, corrige a inconsistência de formato na data
    e calcula o tempo relativo (t) em horas em relação à referencia_inicial.
    """
    incidentes = []

    with open(caminho_log, mode="r", encoding="utf-8") as arquivo:
        for linha in arquivo:
            linha_limpa = linha.strip()
            if not linha_limpa:
                continue

            # Os 19 primeiros caracteres contêm 'YYYY-MM-DD HH:MM:SS' ou 'DD-MM-YYYY HH:MM:SS'
            parte_data = linha_limpa[:19]
            mensagem = linha_limpa[20:].strip()

            dt = _parse_data_hora(parte_data)
            horas_decorridas = (dt - referencia_inicial).total_seconds() / 3600.0

            incidentes.append(
                {
                    "horario_original": parte_data,
                    "horario_iso": dt.strftime("%Y-%m-%d %H:%M:%S"),
                    "t": horas_decorridas,
                    "mensagem": mensagem,
                }
            )

    return incidentes
