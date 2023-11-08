#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import xlsxwriter as xlsx
import glob, os, sys
import pymysql
import seaborn as sns
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")

from sqlalchemy import create_engine
from pandas.plotting import parallel_coordinates


# In[ ]:


#Variaveis de acesso | ANP
engine_anp = create_engine('mysql+pymysql://luiz_carvalho:ads123@localhost:3306/ANP')


# In[ ]:


#Define caminho
consulta = "SELECT * FROM f_preco_combustivel"
df = pd.DataFrame([])
df = pd.read_sql(consulta, engine_anp)


# In[ ]:


#Conjunto de dados bruto
df


# In[ ]:


#Monta as series de dados a serem plotadas
produtos = df.produto.unique().tolist()
regioes = df.regiao_sigla.unique().tolist()
periodos = df.mes_coleta.unique().tolist()

var_produto = []
for produto in produtos: 
    var_produto.append(df[["produto", "regiao_sigla", "valor_venda"]].loc[df["produto"]==produto].groupby(
        ["regiao_sigla", "produto"]).mean())

var_regiao = []    
for produto in produtos:
    var_regiao.append(df[["produto", "regiao_sigla", "valor_venda"]].loc[df["produto"]==produto])


# In[ ]:


#Grafico de barras
df[["produto", "valor_venda"]].groupby("produto").mean().plot(kind="barh", title="Valor médio por tipo de produto")


# In[ ]:


#Grafico de linhas paralelas
gasolina = var_produto[0].reset_index()
etanol = var_produto[1].reset_index()
gasolina_adt = var_produto[2].reset_index()

ax=gasolina["regiao_sigla"].tolist()
ay1=gasolina["valor_venda"].tolist()
ay2=etanol["valor_venda"].tolist()
ay3=gasolina_adt["valor_venda"].tolist()

plt.plot(ax, ay1, label="Gasolina")
plt.plot(ax, ay3, label="Gasolina ADT")
plt.plot(ax, ay2, label="Etanol")

plt.xlabel("Regiões")
plt.ylabel("Preço médio")

plt.title("Preço médio por produto e região")
plt.legend()
plt.show()


# In[ ]:


#Gráfico boxplot (min, q1, q2 (mediana), q3, max)
prd1 = df["valor_venda"].loc[df["produto"]=="GASOLINA"]
prd2 = df["valor_venda"].loc[df["produto"]=="GASOLINA ADITIVADA"]
prd3 = df["valor_venda"].loc[df["produto"]=="ETANOL"]

boxplot_data = [prd1, prd2, prd3]
plt.title("Estatística por produto")
plt.boxplot(boxplot_data, patch_artist=True, labels=["Gasolina", "Etanol", "Gasolina Adv"])
plt.show()


# In[ ]:


for produto in produtos:
    dfx = df[["produto", "regiao_sigla", "valor_venda"]].loc[df["produto"]==produto]
    rg1 = dfx["valor_venda"].loc[df["regiao_sigla"]=="N"]
    rg2 = dfx["valor_venda"].loc[df["regiao_sigla"]=="S"]
    rg3 = dfx["valor_venda"].loc[df["regiao_sigla"]=="NE"]
    rg4 = dfx["valor_venda"].loc[df["regiao_sigla"]=="SE"]
    rg5 = dfx["valor_venda"].loc[df["regiao_sigla"]=="CO"]

    boxplot_data = [rg1, rg2, rg3, rg4, rg5]
    plt.title(produto + " por região")
    plt.boxplot(boxplot_data, patch_artist=True, labels=["N", "S", "NE", "SE", "CO"])
    plt.show()


# In[ ]:


#Grafico de linhas paralelas
dfx = df[["valor_venda", "mes_coleta", "produto"]].groupby(
    ['mes_coleta', "produto"]).mean().sort_values(by="mes_coleta" , ascending=True).reset_index()

ax = periodos
ax.sort()
ay1 = dfx["valor_venda"].loc[dfx["produto"]=="GASOLINA"].tolist()
ay2 = dfx["valor_venda"].loc[dfx["produto"]=="GASOLINA ADITIVADA"].tolist()
ay3 = dfx["valor_venda"].loc[dfx["produto"]=="ETANOL"].tolist()

plt.plot(ax, ay1, label="Gasolina")
plt.plot(ax, ay3, label="Gasolina ADT")
plt.plot(ax, ay2, label="Etanol")

plt.xlabel("Regiões")
plt.ylabel("Preço médio")

plt.title("Preço médio por produto e região")
plt.legend()

plt.show()


# Análises
# 
# *Os produtos gasolina, etanol e adt precisam ser analisados separadamente
# *O valor médio da gasolina e adt são simétricos enquanto que o etanol é assimétrico
# *Todos produtos possuem outliers em todas regiões, especialmente SE onde mais está mais evidente
# *A gasolina e o etanol possuem uma variação minima e máxima muito alta em algumas regiões
# *Em alguns meses o valor médio da gasolina sobe enquanto que o etanol desce
# 
# Conclusão
# O conjunto de dados não requer tanta profundidade técnica, pois tratam-se de registros simples não transacionais em pequena escala. A recomendação é um dashboard com análise adhoc onde o cliente tenha liberdade de usar filtros para aprofundar sua própria análise personalizada.

# In[ ]:


# #Matriz de região/estado
# df[["valor_venda", "regiao_sigla", "estado_sigla"]].groupby(
#     ['regiao_sigla', "estado_sigla"]).mean().sort_values(by=["regiao_sigla", "valor_venda"], ascending=False)

# #Gráfico de colunas
# df[["regiao_sigla", "valor_venda"]].groupby(
#     "regiao_sigla").mean().sort_values(by="valor_venda", ascending=False).plot(kind="bar", title="Valor médio por região")

# #Histograma
# df[["valor_venda", "data_coleta"]].groupby(
#     'data_coleta').mean().sort_values(by="data_coleta", ascending=False).plot(kind="hist", title="Frequência de preço médio")

