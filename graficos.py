import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import spearmanr

# 1. Carrega as bases que você acabou de limpar
tabela_fundos = pd.read_csv("tabela_fundos_limpo.csv")
tabela_cdi = pd.read_csv("tabela_cdi_limpo.csv")

tabela_fundos['data'] = pd.to_datetime(tabela_fundos['data'])
tabela_cdi['data'] = pd.to_datetime(tabela_cdi['data'])

tabela_fundos = tabela_fundos.sort_values('data')
tabela_cdi = tabela_cdi.sort_values('data')

tabela_final = pd.merge(tabela_fundos, tabela_cdi, on='data', how='inner')

correlacao_por_fundo = tabela_final.groupby('nome_fundo').apply(lambda x: spearmanr(x['rentabilidade_mensal'], x['taxa_cdi'])[0])

print("📊 --- CORRELAÇÃO DE SPEARMAN POR FUNDO ---")
for fundo in tabela_final['nome_fundo'].unique():
    dados_fundo = tabela_final[tabela_final['nome_fundo'] == fundo]
    # Calcula a correlação entre rentabilidade e cdi
    correlacao, p_valor = spearmanr(dados_fundo['rentabilidade_mensal'], dados_fundo['taxa_cdi'])
    print(f"Fundo {fundo}: Correlação de Spearman = {correlacao:.4f}")

# 2. Configura o estilo visual do gráfico (Seaborn deixa mais moderno)
sns.set_theme(style="whitegrid")
plt.figure(figsize=(12, 6)) # Define o tamanho da tela (Largura, Altura)

# 3. Plota a rentabilidade de cada fundo (Separados por cor usando o 'hue')
sns.lineplot(
    data=tabela_fundos, 
    x='data', 
    y='rentabilidade_mensal', 
    hue='nome_fundo', 
    marker='o', # Adiciona bolinhas nos pontos de cada mês
    linewidth=2
)

# 4. Plota a linha do CDI como referência (em preto e tracejada para destacar)
sns.lineplot(
    data=tabela_cdi, 
    x='data', 
    y='taxa_cdi', 
    color='black', 
    label='CDI (Benchmark)', 
    linewidth=2.5, 
    linestyle='--'
)

# 5. Perfumaria e Ajustes de Legendas (Pra ficar nível apresentação)
plt.title('Evolução da Rentabilidade Mensal: Fundos vs CDI', fontsize=14, fontweight='bold', pad=15)
plt.xlabel('Período', fontsize=12)
plt.ylabel('Rentabilidade Mensal (%)', fontsize=12)

plt.legend(title='Ativos', bbox_to_anchor=(1.05, 1), loc='upper left') # Joga a legenda para fora do gráfico
plt.tight_layout() # Ajusta as margens para não cortar nada

# 6. Exibe o gráfico na tela
plt.show()

tabela_final.to_csv("tabela_unica_powerbi.csv", index=False)
print("\n🚀 Tabela única gerada com sucesso para o Power BI!")