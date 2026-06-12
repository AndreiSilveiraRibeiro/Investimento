import pandas as pd
import numpy as np

# 1. Carrega as tabelas que já passaram pela primeira limpeza de strings/datas
tabela_cdi = pd.read_csv("tabela_cdi_limpo.csv")
tabela_fundos = pd.read_csv("tabela_fundos_limpo.csv")

# 2. Calcula os Quartis e o IQR agrupado por cada fundo
Q1 = tabela_fundos.groupby('id_fundo')['rentabilidade_mensal'].transform(lambda x: x.quantile(0.25))
Q3 = tabela_fundos.groupby('id_fundo')['rentabilidade_mensal'].transform(lambda x: x.quantile(0.75))
IQR = Q3 - Q1

# 3. Define os limites matemáticos corretos usando o IQR
limite_alto = Q3 + (1.5 * IQR)
limite_baixo = Q1 - (1.5 * IQR)

# 4. Puxa a mediana de cada fundo para usar como substituta
mediana_por_fundo = tabela_fundos.groupby('id_fundo')['rentabilidade_mensal'].transform('median')

tabela_outliers = tabela_fundos[(tabela_fundos['rentabilidade_mensal'] > limite_alto) | (tabela_fundos['rentabilidade_mensal'] < limite_baixo)]

print(f"Outliers: {tabela_outliers}")

# 5. O Filtro mágico: substitui os outliers pela mediana do respectivo fundo
tabela_fundos['rentabilidade_mensal'] = np.where((tabela_fundos['rentabilidade_mensal'] > limite_alto) | (tabela_fundos['rentabilidade_mensal'] < limite_baixo), mediana_por_fundo, tabela_fundos['rentabilidade_mensal'])

print("✅ Outliers por fundo substituídos pela mediana com sucesso!")
print(tabela_fundos.describe())

# 6. Sobrescreve os arquivos limpos agora SEM nenhuma distorção para o Power BI
tabela_fundos.to_csv("tabela_fundos_limpo.csv", index=False)
tabela_cdi.to_csv("tabela_cdi_limpo.csv", index=False)
print("🚀 Arquivos atualizados e prontos para o Dashboard!")