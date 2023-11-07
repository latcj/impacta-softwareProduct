#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import xlsxwriter as xlsx
import glob, os, sys
import pymysql
import seaborn as sns
import matplotlib.pyplot as plt
from sqlalchemy import create_engine


# In[2]:


#Variaveis de acesso | ANP
engine_anp = create_engine('mysql+pymysql://luiz_carvalho:ads123@localhost:3306/ANP')


# In[21]:


#Define caminho
consulta = "SELECT * FROM f_preco_combustivel"
df = pd.DataFrame([])
df = pd.read_sql(consulta, engine_anp)


# In[42]:


#Conjunto de dados bruto
df


# In[47]:


#Grafico de barras
df[["produto", "valor_venda"]].groupby("produto").mean().plot(kind="barh", title="Valor médio por tipo de produto")


# In[23]:


#Matriz de região/estado
df[["valor_venda", "regiao_sigla", "estado_sigla"]].groupby(
    ['regiao_sigla', "estado_sigla"]).mean().sort_values(by=["regiao_sigla", "valor_venda"], ascending=False)


# In[49]:


#Gráfico de colunas
df[["regiao_sigla", "valor_venda"]].groupby(
    "regiao_sigla").mean().sort_values(by="valor_venda", ascending=False).plot(kind="bar", title="Valor médio por região")


# In[25]:


#Gráfico boxplot (min, q1, q2 (mediana), q3, max)
rg1 = df["valor_venda"].loc[df["regiao_sigla"]=="N"]
rg2 = df["valor_venda"].loc[df["regiao_sigla"]=="S"]
rg3 = df["valor_venda"].loc[df["regiao_sigla"]=="NE"]
rg4 = df["valor_venda"].loc[df["regiao_sigla"]=="SE"]
rg5 = df["valor_venda"].loc[df["regiao_sigla"]=="CO"]

boxplot_data = [rg1, rg2, rg3, rg4, rg5]
plt.title("Estatística por região")
plt.boxplot(boxplot_data, patch_artist=True, labels=["N", "S", "NE", "SE", "CO"])
plt.show()


# In[51]:


#Histograma
df[["valor_venda", "data_coleta"]].groupby(
    'data_coleta').mean().sort_values(by="data_coleta", ascending=False).plot(kind="hist", title="Frequência de preço médio")


# In[52]:


df[["valor_venda", "mes_coleta"]].groupby(
    'mes_coleta').mean().sort_values(by="mes_coleta", ascending=True).plot(title="Preço médio por período")


# In[ ]:


# #Carrega no MYSQL
# frame.to_sql(name='f_preco_combustivel', con=engine_anp, if_exists='replace')

