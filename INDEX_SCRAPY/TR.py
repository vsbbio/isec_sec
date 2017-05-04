import pandas as pd
import sqlite3 as sq3
import requests

from os import getcwd

index = 226
dt_init = "01/02/1991"
dt_end = "28/04/2017"

#Criando a URL do API do Bacen
url = "http://api.bcb.gov.br/dados/serie/bcdata.sgs." + \
        str(index) +"/dados?formato=csv&dataInicial=" + dt_init + "&dataFinal=" + dt_end+".csv"

#Lendo os dados obtidos pelo API
df = pd.read_csv(url,decimal=",",delimiter=";")

#Editando os dados para inserção no db
j = 0
data = []
while j < len(df.data):
    data_temp = [int(str(df.data[j][-4:])+str(df.data[j][-7:-5])+str(df.data[j][:2])), df.valor[j]]
    data.append(data_temp)
    j += 1

def criar(table_name="TR"):
    c1 = sq3.connect("INDEX.db")
    c2 = c1.cursor()
    
    sql_create = "CREATE TABLE IF NOT EXISTS %s(date datetime primary key, VAR INTEGER)" %(table_name)
    c2.execute(sql_create)
    
    c2.close()
    c1.close()

def inserir(table_name="TR", data_insert="DATA"):
    c1 = sq3.connect("INDEX.db")
    c2 = c1.cursor()
    
    sql_insert = "INSERT OR IGNORE INTO %s VALUES(?, ?)" %(table_name)
    
    for item in data_insert:
        c2.execute(sql_insert, item)
    
    c1.commit()
    c2.close()
    c1.close()
    
def export_csv(table_name="TR", select="*"):
    c1 = sq3.connect("INDEX.db")
    c2 = c1.cursor()
    dates = []
        
    sql_select = "SELECT %s FROM %s" %(select, table_name)
    
    c2.execute(sql_select)
    
    data = c2.fetchall()
    data = pd.DataFrame(data, columns=["Date","VAR"])
    
    data.to_csv(getcwd()+"\\TR.csv", sep=";",index=False, doublequote=False, decimal=",")
    
criar(table_name="TR")
inserir(table_name="TR", data_insert=data)

answer = input("Você deseja exportar o arquivo para CSV?")

if answer.upper() == "SIM":
    export_csv(table_name="TR")