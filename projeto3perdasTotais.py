import csv

# --- Configurações ---
OLT_GAIN_DB = 4
POTENCIA_OLT_DBM = 4.5
ATENUADOR = -10
PERDAS_CONECTORES_CEO = -0.4
PERDA_POR_METRO = -0.00035

def ler_distancias(path):
    distancias = {}
    with open(path, 'r') as f:
        leitor = csv.reader(f)
        for linha in leitor:
            if not linha or len(linha) < 2:
                continue
            try:
                cto = linha[0].strip()
                dist = float(linha[1])
                distancias[cto] = dist
            except ValueError:
                continue
    return distancias

def calcular_perdas_por_cto(caminho):
    ctos = [p for p in caminho if p.startswith("CTO")]
    n_ctos = len(ctos)

    if n_ctos == 2:
        perda_passagem = -0.7
        perda_ramo = -11
        perda_final = -13.7
        perda_conector = -0.2
    elif n_ctos == 3:
        perda_passagem = -0.4
        perda_ramo = -18.7
        perda_final = -13.7
        perda_conector = -0.2
    else:
        perda_passagem = -0.5
        perda_ramo = -14.6
        perda_final = -13.7
        perda_conector = -0.2

    resultados = []
    for i, cto in enumerate(ctos):
        n_splitters_1_2 = i
        perda_conector_cto = n_splitters_1_2 * perda_conector

        if i == n_ctos - 1:
            perda_splitters = n_splitters_1_2 * perda_passagem + perda_passagem + perda_final + ATENUADOR + perda_conector
        else:
            perda_splitters = n_splitters_1_2 * perda_passagem + perda_ramo + perda_final + perda_conector_cto

        ceo_associado = f"CEO{cto[-2:]}" if len(cto) >= 2 else "CEO desconhecido"

        resultados.append({
            "CTO": cto,
            "CEO associado": ceo_associado,
            "Perda splitters (dB)": round(perda_splitters, 2),
            "Perda conector (dB)": round(perda_conector_cto, 2)
        })
    return resultados

def calcular_perda_total_por_cto(caminho, distancias):
    perdas_ctos = calcular_perdas_por_cto(caminho)
    resultado = []

    for item in perdas_ctos:
        cto = item["CTO"]
        distancia_m = distancias.get(cto, 0)  # assume 0 se não encontrado
        perda_distancia = distancia_m * PERDA_POR_METRO

        perda_total = item["Perda splitters (dB)"] + OLT_GAIN_DB + PERDAS_CONECTORES_CEO + perda_distancia
        potencia_recebida = POTENCIA_OLT_DBM + perda_total

        resultado.append({
            "Usuário CTO que atende": cto,
            "CEO associado": item["CEO associado"],
            "Distância (m)": round(distancia_m, 2),
            "Perda Splitters (dB)": item["Perda splitters (dB)"],
            "Perda conector (dB)": item["Perda conector (dB)"],
            "Perda distância (dB)": round(perda_distancia, 4),
            "Perda CEO (dB)": round(PERDAS_CONECTORES_CEO, 2),
            "Ganho OLT (dB)": OLT_GAIN_DB,
            "Perda Total (dB)": round(perda_total, 4),
            "Potência OLT (dBm)": POTENCIA_OLT_DBM,
            "Potência Recebida (dBm)": round(potencia_recebida, 4)
        })
    return resultado

def main():
    txt_path = "caminho_completo.txt"
    dist_csv_path = "distancias_cto.csv"
    saida_csv_path = "resultado_perdas.csv"

    print("Processando caminhos e calculando perdas...")
    resultados_finais = []

    try:
        distancias = ler_distancias(dist_csv_path)

        with open(txt_path, 'r', encoding='utf-8') as f:
            linhas = f.readlines()

        for linha in linhas:
            caminho = [p.strip() for p in linha.strip().split(',') if p.strip()]
            if caminho:
                res = calcular_perda_total_por_cto(caminho, distancias)
                resultados_finais.extend(res)

        headers = [
            "Usuário CTO que atende", "CEO associado", "Distância (m)",
            "Perda Splitters (dB)", "Perda conector (dB)",
            "Perda distância (dB)", "Perda CEO (dB)", "Ganho OLT (dB)",
            "Perda Total (dB)", "Potência OLT (dBm)", "Potência Recebida (dBm)"
        ]

        print(f"\n{'CTO':<6} | {'CEO':<5} | {'Distância (m)':<13} | {'Splitters':<10} | {'Conect.':<9} | {'Dist.dB':<10} | {'CEO(dB)':<7} | {'OLT Gain':<9} | {'Perda T.':<10} | {'OLT (dBm)':<10} | {'Rx (dBm)':<10}")
        print("-" * 130)

        for r in resultados_finais:
            print(f"{r['Usuário CTO que atende']:<6} | "
                  f"{r['CEO associado']:<5} | "
                  f"{r['Distância (m)']:<13} | "
                  f"{r['Perda Splitters (dB)']:<10} | "
                  f"{r['Perda conector (dB)']:<9} | "
                  f"{r['Perda distância (dB)']:<10} | "
                  f"{r['Perda CEO (dB)']:<7} | "
                  f"{r['Ganho OLT (dB)']:<9} | "
                  f"{r['Perda Total (dB)']:<10} | "
                  f"{r['Potência OLT (dBm)']:<10} | "
                  f"{r['Potência Recebida (dBm)']:<10}")

        with open(saida_csv_path, 'w', newline='', encoding='utf-8') as fcsv:
            writer = csv.DictWriter(fcsv, fieldnames=headers)
            writer.writeheader()
            for linha in resultados_finais:
                writer.writerow(linha)

        print(f"\nResultados salvos em: {saida_csv_path}")

    except Exception as e:
        print(f"Erro ao processar os caminhos: {e}")

if __name__ == "__main__":
    main()
