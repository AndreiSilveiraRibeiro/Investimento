import pandas as pd

# Carrega as bases brutas do jeito que vieram do sistema
tabela_cdi = pd.read_csv("tbl_cdi_sujo.csv")
tabela_fundos = pd.read_csv("tbl_fundos_sujo.csv")

# --- ANÁLISE INICIAL DO CDI ---
print(tabela_cdi)
print(tabela_cdi.shape)
print(tabela_cdi.info())

print(tabela_cdi['data'])

# Mixed resolve a bagunça de formatos (com e sem hora) e coerce não deixa travar se tiver texto bizarro
tabela_cdi['data'] = pd.to_datetime(tabela_cdi['data'], format='mixed', errors='coerce')

tabela_cdi = tabela_cdi[tabela_cdi['data'] <= '2024-12-31']

# Cria a coluna padrão BR com barras para não passar trabalho manual no Power BI
tabela_cdi['data_formatada'] = tabela_cdi['data'].dt.strftime("%d/%m/%Y")

# Validações de integridade da data e checagem de nulos/duplicados
print(tabela_cdi['data'])
print(f"Quantidade de valores nulos: {tabela_cdi['data'].isnull().sum()}")

print(tabela_cdi['taxa_cdi'])

tabela_cdi['taxa_cdi'] = tabela_cdi['taxa_cdi'].round(2)

print(f"Quantidade de valores nulos na tabela inteira: \n{tabela_cdi.isnull().sum()}")
print(f"Quantidade de valores duplicados na tabela inteira: {tabela_cdi.duplicated().sum()}")

# Print final do CDI para ver os tipos e os números do describe
print(tabela_cdi)
print(tabela_cdi.shape)
print(tabela_cdi.describe())


# ==========================================
# ----- TABELA FUNDOS -----
# ==========================================
print(f"{10 * '-='} Tabela Fundos {10 * '-='}")

print(tabela_fundos)
print(tabela_fundos.info())
print(tabela_fundos.shape)

print(tabela_fundos['id_fundo'])

# Força o ID a virar número inteiro puro
tabela_fundos['id_fundo'] = tabela_fundos['id_fundo'].astype(int)

print(f"Quantidade de valores nulos na tabela 'id_fundo': {tabela_fundos['id_fundo'].isnull().sum()}")
print(tabela_fundos['id_fundo'])

print(tabela_fundos['nome_fundo'])
print(tabela_fundos['nome_fundo'].unique())

# TRATAMENTO DE STRING (NOME DO FUNDO):
# Strip limpa as pontas, Title deixa a primeira letra Maiúscula
tabela_fundos['nome_fundo'] = tabela_fundos['nome_fundo'].str.strip().str.title()

# Regex cirúrgico para caçar e esmagar espaços duplos no meio do texto
tabela_fundos['nome_fundo'] = tabela_fundos['nome_fundo'].str.replace(r'(\w*)\s\s(\w*)', r'\1 \2', regex=True)

# Valida se os nomes duplicados juntaram de verdade
print(tabela_fundos['nome_fundo'].unique())
print(f"Quantidade de valores nulos na tabela 'nome_fundo': {tabela_fundos['nome_fundo'].isnull().sum()}")

print(tabela_fundos['data'])

# Mesmo tratamento do CDI: mixed e coerce para blindar a conversão da data
tabela_fundos['data'] = pd.to_datetime(tabela_fundos['data'], format='mixed', errors='coerce')

tabela_fundos = tabela_fundos[tabela_fundos['data'] <= '2024-12-31']

# Salva a data bonitinha com barras para os gráficos do Power BI
tabela_fundos['data_formatada'] = tabela_fundos['data'].dt.strftime("%d/%m/%Y")

print(f"Linhas com data errada: \n{tabela_fundos[tabela_fundos['data'].dt.day > 31]}")
print(f"Quantidade de valores nulos na coluna 'data': {tabela_fundos['data'].isnull().sum()}")
print(tabela_fundos['data'])

print(tabela_fundos['rentabilidade_mensal'])

tabela_fundos['rentabilidade_mensal'] = tabela_fundos['rentabilidade_mensal'].round(2)

print(tabela_fundos['risco'])

# TRATAMENTO DE STRING (RISCO):
# Arranca espaços ocultos no fim (ex: 'Médio ') e padroniza o texto
tabela_fundos['risco'] = tabela_fundos['risco'].str.strip().str.title()

print(tabela_fundos['risco'].unique())
print(f"Valores nulos na coluna 'risco': {tabela_fundos['risco'].isnull().sum()}")
print(tabela_fundos['risco'])

# CONFERÊNCIA FINAL DOS DADOS TRATADOS
print(tabela_fundos)
print(tabela_fundos.shape)
print(tabela_fundos.describe())
print(tabela_fundos.info())

# Exportação dos arquivos limpos sem levar o índice chato do Pandas junto
tabela_fundos.to_csv("tabela_fundos_limpo.csv", index=False)
tabela_cdi.to_csv("tabela_cdi_limpo.csv", index=False)