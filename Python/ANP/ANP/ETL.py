#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import xlsxwriter as xlsx
import glob, os, sys
import pymysql
from sqlalchemy import create_engine


# In[ ]:


#Variaveis de acesso | ANP
engine_anp = create_engine('mysql+pymysql://luiz_carvalho:ads123@localhost:3306/ANP')


# In[ ]:


#functions
def zerar_nan(frame, colunas):
    for coluna in colunas:
        frame[coluna] = frame[coluna].fillna(0)


# In[ ]:


#Define caminho
df = pd.DataFrame([])
path = "C:\\Users\\latc-\\Python\\ANP\\downloaded_files\\full"
os.chdir(path)


# In[ ]:


#Lê todos arquivos e agrupa em um único
arquivos = glob.glob(os.path.join(path , "*"))
agrupador = []

for arquivo in arquivos:
    df = pd.read_csv(arquivo, sep=";", header=0, encoding="utf-8")
    agrupador.append(df)
    
frame = pd.concat(agrupador, axis=0, ignore_index=True)


# In[ ]:


#Transforma colunas NaN em 0
colunas_nan = ["Complemento", "Valor de Compra"]
zerar_nan(frame, colunas_nan)


# In[ ]:


#Altera nome das colunas
frame.rename(
    columns={
        "Regiao - Sigla": "regiao_sigla",
        "Estado - Sigla": "estado_sigla",
        "Municipio": "municipio",
        "Revenda": "revenda",
        "CNPJ da Revenda": "cnpj_revenda",
        "Nome da Rua": "nome_rua",
        "Numero Rua": "numero_rua",
        "Complemento": "complemento",
        "Bairro": "bairro",
        "Cep": "cep",
        "Produto": "produto",
        "Data da Coleta": "data_coleta",
        "Valor de Venda": "valor_venda",
        "Valor de Compra": "valor_compra",
        "Unidade de Medida": "unidade_medida",
        "Bandeira": "bandeira"
}, inplace=True)


# In[ ]:


#Carrega no MYSQL
frame.to_sql(name='f_preco_combustivel', con=engine_anp, if_exists='replace')


# In[ ]:




