import xml.etree.ElementTree as ET
from geopy.distance import geodesic
import csv

def extrair_pontos_kml_manual(caminho_kml):
    tree = ET.parse(caminho_kml)
    root = tree.getroot()

    ns = {'kml': 'http://www.opengis.net/kml/2.2'}

    pontos = {}

    for placemark in root.findall('.//kml:Placemark', ns):
        nome = placemark.find('kml:name', ns)
        coords = placemark.find('.//kml:coordinates', ns)
        if nome is not None and coords is not None:
            nome_text = nome.text.strip()
            coords_text = coords.text.strip()
            lon_str, lat_str, *_ = coords_text.split(',')
            pontos[nome_text] = (float(lat_str), float(lon_str))

    return pontos

def ler_caminhos_txt(caminho_txt):
    caminhos = []
    with open(caminho_txt, 'r') as f:
        for linha in f:
            linha = linha.strip()
            if not linha:
                continue
            pontos = linha.split(',')
            caminhos.append([p.strip() for p in pontos if p.strip()])
    return caminhos

def calcular_distancia_caminho(caminho, coordenadas):
    distancia_total = 0
    for i in range(len(caminho) - 1):
        p1 = coordenadas.get(caminho[i])
        p2 = coordenadas.get(caminho[i + 1])
        if not p1 or not p2:
            print(f"[ERRO] Ponto não encontrado: {caminho[i]} ou {caminho[i+1]}")
            return None
        distancia_total += geodesic(p1, p2).meters
    return distancia_total

def main():
    # Ajuste os caminhos aqui:
    kml_path = 'stcProjeto3.kml'
    txt_path = 'caminho_completo.txt'
    csv_output_path = 'distancias_cto.csv'

    print("Extraindo pontos do KML...")
    coordenadas = extrair_pontos_kml_manual(kml_path)
    print(f"Pontos extraídos: {len(coordenadas)}")
    print(f"Exemplo: {list(coordenadas.items())[:5]}")

    print("\nLendo caminhos do arquivo TXT...")
    caminhos = ler_caminhos_txt(txt_path)
    print(f"Caminhos encontrados: {len(caminhos)}")

    resultados = []

    print("\nCalculando distâncias acumuladas do POP até cada CTO:")
    for caminho in caminhos:
        if len(caminho) == 0:
            continue
        if not caminho[0].startswith("POP"):
            print(f"[AVISO] Caminho ignorado por não iniciar com POP: {caminho[0]}")
            continue
        for i, ponto in enumerate(caminho):
            if ponto.startswith("CTO"):
                subcaminho = caminho[:i + 1]  # do POP até este CTO
                distancia = calcular_distancia_caminho(subcaminho, coordenadas)
                if distancia is not None:
                    print(f"{ponto}: {distancia:.2f} metros")
                    resultados.append([ponto, distancia])

    # Exportar para CSV
    with open(csv_output_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["CTO", "Distância do POP (m)"])
        writer.writerows(resultados)

    print(f"\nResultados salvos em: {csv_output_path}")

if __name__ == "__main__":
    main()
