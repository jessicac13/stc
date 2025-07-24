import pandas as pd
import matplotlib.pyplot as plt

ARQUIVO_CSV = 'resultado_perdas.csv'  # Altere se necessário

# Leitura do CSV (separador padrão vírgula)
df = pd.read_csv(ARQUIVO_CSV, encoding='utf-8')

# Remove espaços extras nos nomes das colunas
df.columns = df.columns.str.strip()

# Diagnóstico (opcional)
print("Colunas lidas:", df.columns.tolist())

# Lista das colunas numéricas que vamos converter
colunas_float = [
    'Distância (m)', 'Perda Splitters (dB)', 'Perda conector (dB)',
    'Perda distância (dB)', 'Perda CEO (dB)', 'Ganho OLT (dB)',
    'Perda Total (dB)', 'Potência OLT (dBm)', 'Potência Recebida (dBm)'
]

# Converte as colunas para tipo numérico (forçando NaN nos erros)
df[colunas_float] = df[colunas_float].apply(pd.to_numeric, errors='coerce')

# Criar eixo X numérico sequencial de 1 até o número de linhas do dataframe
eixo_x = range(1, len(df) + 1)

# Plot 1 – Perda Total por CTO (com eixo numérico)
plt.figure(figsize=(12, 5))
plt.bar(eixo_x, df['Perda Total (dB)'], color='tomato')
plt.xlabel('Número do Ponto')
plt.ylabel('Perda Total (dB)')
plt.title('Perda Total por CTO')
plt.xticks(ticks=range(1, len(df) + 1, 5), rotation=45)  # tick a cada 5 pontos
plt.tight_layout()
plt.grid(True)
plt.show()

# Plot 2 – Potência Recebida por CTO (com eixo numérico)
plt.figure(figsize=(12, 5))
plt.bar(eixo_x, df['Potência Recebida (dBm)'], color='mediumseagreen')
plt.xlabel('Número do Ponto')
plt.ylabel('Potência Recebida (dBm)')
plt.title('Potência Recebida por CTO')
plt.xticks(ticks=range(1, len(df) + 1, 5), rotation=45)
plt.tight_layout()
plt.grid(True)
plt.show()
