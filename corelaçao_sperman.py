import pandas as pd
from scipy.stats import spearmanr

# 1. Carrega a tabela única gerada após o merge
tabela_final = pd.read_csv("tabela_unica_powerbi.csv") 

# 2. Cria uma lista para guardar os resultados
resultados_corr = []

# 3. Calcula a correlação de Spearman para cada fundo em relação ao CDI
for fundo in tabela_final['nome_fundo'].unique():
    dados_fundo = tabela_final[tabela_final['nome_fundo'] == fundo]
    
    # Calcula Spearman
    correlacao, _ = spearmanr(dados_fundo['rentabilidade_mensal'], dados_fundo['taxa_cdi'])
    
    # Salva no dicionário
    resultados_corr.append({
        'Nome do Fundo': fundo,
        'CDI': correlacao
    })

# 4. Transforma em DataFrame e salva como CSV
tabela_spearman = pd.DataFrame(resultados_corr)
tabela_spearman.to_csv("matriz_spearman.csv", index=False)

print("✅ Arquivo 'matriz_spearman.csv' gerado com sucesso!")
print(tabela_spearman)