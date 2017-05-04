import pandas as pd
import pymysql
import requests
import time

index = 226
dt_init = "01/02/1991"
dt_end = time.strftime("%d/%m/%Y")
table_name = "TR"

#Criando a URL do API do Bacen
url = "http://api.bcb.gov.br/dados/serie/bcdata.sgs." + \
        str(index) +"/dados?formato=csv&dataInicial=" + dt_init + "&dataFinal=" + dt_end+".csv"

#Lendo os dados obtidos pelo API
df = pd.read_csv(url,decimal=",",delimiter=";")

#Editando os dados para inserção no db
j = 0
data = []
while j < len(df.data):
    data_temp = [int(str(df.data[j][-4:])+str(df.data[j][-7:-5])+str(df.data[j][:2])), float(df.valor[j])]
    data.append(data_temp)
    j += 1

#CRIANDO TABELA SQL E INSERINDO DADOS
c1 = pymysql.connect(host="localhost", user="root", passwd="isec@3320", db="indices")
c2 = c1.cursor()

sql_create = "CREATE TABLE IF NOT EXISTS %s(date INTEGER primary key, VAR float)" %(table_name)
c2.execute(sql_create)

for item in data:
    sql_insert = "INSERT IGNORE INTO TR (date, VAR) VALUES(%d, %6.2f)" %(item[0], item[1])
    c2.execute(sql_insert)
    c1.commit()

c2.close()
c1.close()
print("Finish!")
