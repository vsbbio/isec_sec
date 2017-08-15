#importando biblioteca necessária
import pandas as pd
import pymysql
import time
from urllib.request import urlopen
from bs4 import BeautifulSoup

#%% CDI CDI CDI CDI CDI CDI CDI CDI CDI CDI
html = urlopen("ftp://ftp.cetip.com.br/MediaCDI")
bs = BeautifulSoup(html,"lxml")

#obtendo os nomes dos arquivos disponíveis no FTP
for txt in bs:
    txt_temp = txt.get_text().split("\n")

names = []

for item in txt_temp:
    if item == "":
        pass
    else:
        names.append(item[-13:-5])

#Leitura e captura do conteúdo dos arquivos contidos no diretório FTP
diset = []
for file in names:
    #Capturando o conteúdo de cada arquivo contido no diretório
    html2 = urlopen("ftp://ftp.cetip.com.br/MediaCDI/"+str(file)+".txt")
    bs2 = BeautifulSoup(html2,"lxml")
    value = bs2.get_text()
    #Editando o conteúdo, excluindo espaços e outros caracteres
    value = float(value[:9])
    data_temp = [int(file), float(value/10000)]
    diset.append(data_temp)

del(html, bs, html2, bs2, data_temp, file, item, names, txt_temp, value)
print("CDI [ OK ]")

#%% TR TR TR TR TR TR TR TR TR TR TR

#definindo parâmetros da API do BACEN
index = 226
dt_init = "01/02/1991"
dt_end = time.strftime("%d/%m/%Y")

#criando URL para extração dos dados via API
html = "http://api.bcb.gov.br/dados/serie/bcdata.sgs." + \
        str(index) +"/dados?formato=csv&dataInicial=" + dt_init + "&dataFinal=" + dt_end+".csv"

#Lendo os dados obtidos pelo API
df = pd.read_csv(html ,decimal=",",delimiter=";")

#Editando os dados para inserção no db
j = 0
trset = []
while j < len(df.data):

    data_temp = [int(str(df.data[j][-4:])+str(df.data[j][-7:-5])+str(df.data[j][:2])),
                 float(df.valor[j])]
    trset.append(data_temp)
    j += 1

del(data_temp, df, dt_end, dt_init, html, index, j)
print("TR [ OK ]")

#%%INCC-DI INCC-DI INCC-DI
url = "http://indiceseconomicos.secovi.com.br/indicadormensal.php?idindicador=59"

html = urlopen(url)
bs = BeautifulSoup(html, "lxml")
month1 = bs.find_all("td", {"class":"borderLeft "})
month2 = bs.find_all("td", {"class":"borderLeft borderBottom "})
bowl = bs.find_all("td")

lst_b = []
for item in bowl:
    lstt = item.get_text()
    lst_b.append(lstt)

lst_m1 = []
for item in month1:
    lstt = item.get_text()
    lst_m1.append(lstt)

lst_m2 = []
for item in month2:
    lstt = item.get_text()
    lst_m2.append(lstt)

inccdiset = []
y = 1995
j = 0
month = {"JAN":"01","FEV":"02","MAR":"03","ABR":"04","MAI":"05",
         "JUN":"06","JUL":"07","AGO":"08","SET":"09","OUT":"10","NOV":"11","DEZ":"12",}

for item in lst_b:
    if item in lst_m1:
        indext = [int(str(y) + str(month[item])+"01"),
                  float(str(lst_b[j+1]).replace(" ","").replace("\n",
                        "").replace(".","").replace(",","."))]

        inccdiset.append(indext)

    elif item in lst_m2:
        indext = [int(str(y) + str(month[item])+"01"),
                  float(str(lst_b[j+1]).replace(" ","").replace("\n",
                        "").replace(".","").replace(",","."))]

        inccdiset.append(indext)
        y += 1

    j += 1

del(indext, item, j, lst_b, lst_m1, lst_m2, lstt, month, url, y)
print("INCC-DI [ OK ]")

#%%#%%INPC INPC INPC INPC INPC
url = "http://indiceseconomicos.secovi.com.br/indicadormensal.php?idindicador=60"

html = urlopen(url)
bs = BeautifulSoup(html, "lxml")
month1 = bs.find_all("td", {"class":"borderLeft "})
month2 = bs.find_all("td", {"class":"borderLeft borderBottom "})
bowl = bs.find_all("td")

lst_b = []
for item in bowl:
    lstt = item.get_text()
    lst_b.append(lstt)

lst_m1 = []
for item in month1:
    lstt = item.get_text()
    lst_m1.append(lstt)

lst_m2 = []
for item in month2:
    lstt = item.get_text()
    lst_m2.append(lstt)

inpcset = []
y = 1995
j = 0
month = {"JAN":"01","FEV":"02","MAR":"03","ABR":"04","MAI":"05",
         "JUN":"06","JUL":"07","AGO":"08","SET":"09","OUT":"10","NOV":"11","DEZ":"12",}

for item in lst_b:
    if item in lst_m1:
        indext = [int(str(y) + str(month[item])+"01"),
                  float(str(lst_b[j+1]).replace(" ","").replace("\n",
                        "").replace(".","").replace(",","."))]

        inpcset.append(indext)

    elif item in lst_m2:
        indext = [int(str(y) + str(month[item])+"01"),
                  float(str(lst_b[j+1]).replace(" ","").replace("\n",
                        "").replace(".","").replace(",","."))]

        inpcset.append(indext)
        y += 1

    j += 1

del(indext, item, j, lst_b, lst_m1, lst_m2, lstt, month, url, y)
print("INPC [ OK ]")

#%%IGPDI IGPDI IGPDI IGPDI IGPDI IGPDI

url = "http://www.ipeadata.gov.br/ExibeSerie.aspx?serid=33593&module=M"

html = urlopen(url)
bs = BeautifulSoup(html,"lxml")
indice = bs.find_all("td", {"class":"dxgv"})

igpdiset =[]
date = []
var = []

#Extraindo/Retirando as tags e mantendo o texto do Web Scraping
for item in indice:
    if indice.index(item)%2 == 0:
        date_temp = item.get_text()
        date.append(date_temp)
    else:
        var_temp = item.get_text()
        var.append(var_temp)
#Removendo valores em branco
empty = date.count("")
empty2 = var.count("")
count = 1
count2 = 1

while count <= empty:
    try:
        date.remove("")
        count +=1
    except:
        continue
        count +=1

while count2 <= empty2:
    try:
        var.remove("")
        count2 +=1
    except:
        continue
        count2 +=1


#Editando a data para um valor INTEGER e criando uma lista de listas chamada **data**
j = 0
while j < len(date):
    date[j] = int(date[j][:4]+date[j][5:7]+"01")
    data_temp = [date[j], float(str(var[j]).replace(".","").replace(",","."))]
    igpdiset.append(data_temp)
    j += 1

del(data_temp, date, date_temp, j, url, var, var_temp, count, empty, count2, empty2)
print("IGP-DI [ OK ]")

#%%IGPM IGPM IGPM IGPM
url = "http://www.ipeadata.gov.br/ExibeSerie.aspx?serid=37796&module=M"

html = urlopen(url)
bs = BeautifulSoup(html,"lxml")
indice = bs.find_all("td", {"class":"dxgv"})

igpmset =[]
date = []
var = []

#Extraindo/Retirando as tags e mantendo o texto do Web Scraping
for item in indice:
    if indice.index(item)%2 == 0:
        date_temp = item.get_text()
        date.append(date_temp)
    else:
        var_temp = item.get_text()
        var.append(var_temp)
#Removendo valores em branco
empty = date.count("")
empty2 = var.count("")
count = 1
count2 = 1

while count <= empty:
    try:
        date.remove("")
        count +=1
    except:
        continue
        count +=1

while count2 <= empty2:
    try:
        var.remove("")
        count2 +=1
    except:
        continue
        count2 +=1

#Editando a data para um valor INTEGER e criando uma lista de listas chamada **data**
j = 0
while j < len(date):
    date[j] = int(date[j][:4]+date[j][5:7]+"01")
    data_temp = [date[j], float(str(var[j]).replace(".","").replace(",","."))]
    igpmset.append(data_temp)
    j += 1

del(data_temp, date, date_temp, j, url, var, var_temp, count, empty, count2, empty2)
print("IGP-M [ OK ]")

#%%IPCA IPCA IPCA IPCA
url = "http://www.ipeadata.gov.br/ExibeSerie.aspx?serid=36482&module=M"

html = urlopen(url)
bs = BeautifulSoup(html,"lxml")
indice = bs.find_all("td", {"class":"dxgv"})

ipcaset =[]
date = []
var = []

#Extraindo/Retirando as tags e mantendo o texto do Web Scraping
for item in indice:
    if indice.index(item)%2 == 0:
        date_temp = item.get_text()
        date.append(date_temp)
    else:
        var_temp = item.get_text()
        var.append(var_temp)
#Removendo valores em branco
empty = date.count("")
empty2 = var.count("")
count = 1
count2 = 1

while count <= empty:
    try:
        date.remove("")
        count +=1
    except:
        continue
        count +=1

while count2 <= empty2:
    try:
        var.remove("")
        count2 +=1
    except:
        continue
        count2 +=1

#Editando a data para um valor INTEGER e criando uma lista de listas chamada **data**
j = 0
while j < len(date):
    date[j] = int(date[j][:4]+date[j][5:7]+"01")
    data_temp = [date[j], float(str(var[j]).replace(".","").replace(",","."))]
    ipcaset.append(data_temp)
    j += 1

del(data_temp, date, date_temp, j, url, var, var_temp, empty, count, count2, empty2)
print("IPCA [ OK ]")

#%% INSERINDO DADOS NO DB

#conectando no db ISEC e inserindo os novos dados
c1 = pymysql.connect(host="localhost", user="root", passwd="isec@3320", db="indices")
c2 = c1.cursor()

#CDI
for item in diset:
    sql_insert = "INSERT IGNORE INTO CDI (date, VAR) VALUES({:d}, {:.4f})".format(item[0],item[1])
    c2.execute(sql_insert)
    c1.commit()
print("CDI_insert [ ok ]")

#TR
for item in trset:
    sql_insert = "INSERT IGNORE INTO TR (date, VAR) VALUES({:d}, {:6.2f})".format(item[0], item[1])
    c2.execute(sql_insert)
    c1.commit()
print("TR_insert [ ok ]")

#INCCDI
for item in inccdiset:
    sql_insert = "INSERT IGNORE INTO INCCDI (date, VAR) VALUES({:d}, {:7.3f})".format(item[0], item[1])
    c2.execute(sql_insert)
    c1.commit()
print("INCCDI_insert [ ok ]")

#INPC
for item in inpcset:
    sql_insert = "INSERT IGNORE INTO INPC (date, VAR) VALUES({:d}, {:7.3f})".format(item[0], item[1])
    c2.execute(sql_insert)
    c1.commit()
print("INPC_insert [ ok ]")

#IGPDI
for item in igpdiset:
    sql_insert = "INSERT IGNORE INTO IGPDI (date, VAR) VALUES({:d}, {:7.3f})".format(item[0], item[1])
    c2.execute(sql_insert)
    c1.commit()
print("IGPDI_insert [ ok ]")

#IGPM
for item in igpmset:
    sql_insert = "INSERT IGNORE INTO IGPM (date, VAR) VALUES({:d}, {:7.3f})".format(item[0], item[1])
    c2.execute(sql_insert)
    c1.commit()
print("IGPM_insert [ ok ]")

#IPCA
for item in ipcaset:
    sql_insert = "INSERT IGNORE INTO IPCA (date, VAR) VALUES({:d}, {:7.3f})".format(item[0], item[1])
    c2.execute(sql_insert)
    c1.commit()
print("IPCA_insert [ ok ]")

c2.close()
c1.close()
