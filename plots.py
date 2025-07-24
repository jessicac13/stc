import pandas as pd
import matplotlib.pyplot as plt

# --- Caminho para seu CSV ---
ARQUIVO_CSV = 'dados_cto.csv'  # Substitua pelo nome real do seu arquivo

# --- Leitura do CSV ---
df = pd.read_csv(ARQUIVO_CSV, sep=';', skipinitialspace=True)

# --- Conversão das colunas numéricas ---
colunas_float = [
    'Distância (m)', 'Perda Splitters (dB)', 'Perda conector (dB)',
    'Perda distância (dB)', 'Perda CEO (dB)', 'Ganho OLT (dB)',
    'Perda Total (dB)', 'Potência OLT (dBm)', 'Potência Recebida (dBm)'
]
df[colunas_float] = df[colunas_float].apply(pd.to_numeric, errors='coerce')

# --- Plot 1: Usuário (CTO) vs Perda Total ---
plt.figure(figsize=(12, 5))
plt.bar(df['Usuário CTO que atende'], df['Perda Total (dB)'], color='tomato')
plt.xlabel('Usuário (CTO)')
plt.ylabel('Perda Total (dB)')
plt.title('Perda Total por CTO')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.grid(True)
plt.show()

# --- Plot 2: Usuário (CTO) vs Potência Recebida (Rx) ---
plt.figure(figsize=(12, 5))
plt.bar(df['Usuário CTO que atende'], df['Potência Recebida (dBm)'], color='mediumseagreen')
plt.xlabel('Usuário (CTO)')
plt.ylabel('Potência Recebida (dBm)')
plt.title('Potência Recebida por CTO')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.grid(True)
plt.show()
