import csv

# --- Configurações ---
OLT_GAIN_DB = 4
POTENCIA_OLT_DBM = 4.5
ATENUADOR = -10
PERDAS_CONECTORES_CEO = -0.4

def calcular_perdas_por_cto(caminho):
    ctos = [p for p in caminho if p.startswith("CTO")]
    n_ctos = len(ctos)

    if n_ctos == 2:
        #10/90
        perda_passagem = -0.7
        perda_ramo = -11
        perda_final = -13.7
        perda_conector = -0.2
    elif n_ctos == 3:
        #2/98
        perda_passagem = -0.4
        perda_ramo = -18.7
        perda_final = -13.7
        perda_conector = -0.2
    else:
        #5/95
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

def calcular_perda_total_por_cto(caminho):
    perdas_ctos = calcular_perdas_por_cto(caminho)
    resultado = []

    for item in perdas_ctos:
        perda_total = item["Perda splitters (dB)"] + OLT_GAIN_DB + PERDAS_CONECTORES_CEO
        potencia_recebida = POTENCIA_OLT_DBM + perda_total
        resultado.append({
            "Usuário CTO que atende": item["CTO"],
            "CEO associado": item["CEO associado"],
            "Perda Splitters (dB)": item["Perda splitters (dB)"],
            "Perda conector (dB)": item["Perda conector (dB)"],
            "Perda CEO (dB)": round(PERDAS_CONECTORES_CEO, 2),
            "Ganho OLT (dB)": OLT_GAIN_DB,
            "Perda Total (dB)": round(perda_total, 2),
            "Potência OLT (dBm)": POTENCIA_OLT_DBM,
            "Potência Recebida (dBm)": round(potencia_recebida, 2)
        })
    return resultado

def main():
    txt_path = "caminho_completo.txt"
    csv_path = "resultado_perdas.csv"

    print("Processando caminhos e calculando perdas...")
    resultados_finais = []

    try:
        with open(txt_path, 'r', encoding='utf-8') as f:
            linhas = f.readlines()

        for linha in linhas:
            caminho = [p.strip() for p in linha.strip().split(',') if p.strip()]
            if caminho:
                res = calcular_perda_total_por_cto(caminho)
                resultados_finais.extend(res)

        # Cabeçalho enxuto
        headers = [
            "Usuário CTO que atende", "CEO associado",
            "Perda Splitters (dB)", "Perda conector (dB)",
            "Perda CEO (dB)", "Ganho OLT (dB)",
            "Perda Total (dB)", "Potência OLT (dBm)", "Potência Recebida (dBm)"
        ]

        # Exibição enxuta
        print(f"\n{'CTO':<6} | {'CEO':<5} | {'Splitters':<10} | {'Conect.':<9} | {'CEO(dB)':<7} | {'OLT Gain':<9} | {'Perda T.':<9} | {'OLT (dBm)':<10} | {'Rx (dBm)':<9}")
        print("-" * 100)

        for r in resultados_finais:
            print(f"{r['Usuário CTO que atende']:<6} | "
                  f"{r['CEO associado']:<5} | "
                  f"{r['Perda Splitters (dB)']:<10} | "
                  f"{r['Perda conector (dB)']:<9} | "
                  f"{r['Perda CEO (dB)']:<7} | "
                  f"{r['Ganho OLT (dB)']:<9} | "
                  f"{r['Perda Total (dB)']:<9} | "
                  f"{r['Potência OLT (dBm)']:<10} | "
                  f"{r['Potência Recebida (dBm)']:<9}")

        # Exporta CSV enxuto
        with open(csv_path, 'w', newline='', encoding='utf-8') as fcsv:
            writer = csv.DictWriter(fcsv, fieldnames=headers)
            writer.writeheader()
            for linha in resultados_finais:
                writer.writerow(linha)

        print(f"\nResultados salvos em: {csv_path}")

    except Exception as e:
        print(f"Erro ao processar os caminhos: {e}")

if __name__ == "__main__":
    main()
