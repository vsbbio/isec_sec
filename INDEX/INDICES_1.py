import pandas as pd
import pymysql
from urllib.request import urlopen
from bs4 import BeautifulSoup

table_name = ["IGPDI", "IGPM", "IPCA"]
limit = 0
j = 0

IGPDI_URL = "http://www.ipeadata.gov.br/ExibeSerie.aspx?serid=33593&module=M"
IGPM_URL = "http://www.ipeadata.gov.br/ExibeSerie.aspx?serid=37796&module=M"
IPCA_URL = "http://www.ipeadata.gov.br/ExibeSerie.aspx?serid=36482&module=M"

#Criando listagens em de branco
date_igpdi = []
var_igpdi = []

date_igpm = []
var_igpm = []

date_ipca = []
var_ipca = []

Igpdi = []
Igpm = []
Ipca = []

#Capturando os valores contidos entre as tags "td"
html = urlopen(IGPDI_URL)
Bso = BeautifulSoup(html,"lxml")
igpdi = Bso.find_all("td", {"class":"dxgv"})

html = urlopen(IGPM_URL)
Bso = BeautifulSoup(html,"lxml")
igpm = Bso.find_all("td", {"class":"dxgv"})

html = urlopen(IPCA_URL)
Bso = BeautifulSoup(html,"lxml")
ipca = Bso.find_all("td", {"class":"dxgv"})

#IGPDI
#Extraindo/Retirando as tags e mantendo o texto do Web Scraping
for item in igpdi:
    if igpdi.index(item)%2 == 0:
        date_temp = item.get_text()
        date_igpdi.append(date_temp)
    else:
        var_temp = item.get_text()
        var_igpdi.append(var_temp)
#Removendo valores em branco
try:
    date_igpdi.remove("")
    var_igpdi.remove("")
except:
    pass

#Editando a data para um valor INTEGER e criando uma lista de listas chamada **data**
j = 0
while j < len(date_igpdi):
    date_igpdi[j] = int(date_igpdi[j][:4]+date_igpdi[j][5:7]+"01")
    data_temp = [date_igpdi[j], float(str(var_igpdi[j]).replace(".","").replace(",","."))]
    Igpdi.append(data_temp)
    j += 1

#IGPM
#Extraindo/Retirando as tags e mantendo o texto do Web Scraping
for item in igpm:
    if igpm.index(item)%2 == 0:
        date_temp = item.get_text()
        date_igpm.append(date_temp)
    else:
        var_temp = item.get_text()
        var_igpm.append(var_temp)
#Removendo valores em branco
try:
    date_igpm.remove("")
    var_igpm.remove("")
except:
    pass

#Editando a data para um valor INTEGER e criando uma lista de listas chamada **data**
j = 0
while j < len(date_igpm):
    date_igpm[j] = int(date_igpm[j][:4]+date_igpm[j][5:7]+"01")
    data_temp = [date_igpm[j], float(str(var_igpm[j]).replace(".","").replace(",","."))]
    Igpm.append(data_temp)
    j += 1

#IPCA
#Extraindo/Retirando as tags e mantendo o texto do Web Scraping
for item in ipca:
    if ipca.index(item)%2 == 0:
        date_temp = item.get_text()
        date_ipca.append(date_temp)
    else:
        var_temp = item.get_text()
        var_ipca.append(var_temp)
#Removendo valores em branco
try:
    date_ipca.remove("")
    var_ipca.remove("")
except:
    pass

#Editando a data para um valor INTEGER e criando uma lista de listas chamada **data**
j = 0
while j < len(date_ipca):
    date_ipca[j] = int(date_ipca[j][:4]+date_ipca[j][5:7]+"01")
    data_temp = [date_ipca[j], float(str(var_ipca[j]).replace(".","").replace(",","."))]
    Ipca.append(data_temp)
    j += 1

#CRIANDO TABELA SQL E INSERINDO DADOS
c1 = pymysql.connect(host="localhost", user="root", passwd="isec@3320", db="indices")
c2 = c1.cursor()

for indice in table_name:
    sql_create = "CREATE TABLE IF NOT EXISTS %s(date INTEGER primary key, VAR float)" %(indice)
    c2.execute(sql_create)

for item in Igpdi:
    sql_insert = "INSERT IGNORE INTO IGPDI (date, VAR) VALUES(%d, %7.3f)" %(item[0], item[1])
    c2.execute(sql_insert)
    c1.commit()

for item in Igpm:
    sql_insert = "INSERT IGNORE INTO IGPM (date, VAR) VALUES(%d, %7.3f)" %(item[0], item[1])
    c2.execute(sql_insert)
    c1.commit()

for item in Ipca:
    sql_insert = "INSERT IGNORE INTO IPCA (date, VAR) VALUES(%d, %7.3f)" %(item[0], item[1])
    c2.execute(sql_insert)
    c1.commit()

c2.close()
c1.close()
print("Finish!")
