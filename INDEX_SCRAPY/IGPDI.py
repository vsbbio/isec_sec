import pandas as pd
import pymysql


from os import getcwd
from urllib.request import urlopen
from bs4 import BeautifulSoup

limit = 0
table_name = "IGPDI"

#Loop para evitar erros de request
while limit <= 10:
    try:
        #Capturando os valores contidos entre as tags "td"
        html = urlopen("http://www.ipeadata.gov.br/ExibeSerie.aspx?serid=37796&module=M")
        Bso = BeautifulSoup(html,"lxml")
        indice = Bso.find_all("td", {"class":"dxgv"})
        break

    except HTTPError:
            print("\nHTTPError, tentaremos de novo! %r \n %s" %(limit))
            sleep(10)
            limit += 1
            continue

    except URLError:
            print("\nURLError, tentaremos de novo! %r \n %s" %(limit))
            sleep(10)
            limit += 1
            continue

#Criando listagens em de branco
date = []
var = []

#Extraindo/Retirando as tags e mantendo o texto do Web Scraping
for item in indice:
    if indice.index(item)%2 == 0:
        date_temp = item.get_text()
        date.append(date_temp)
    else:
        var_temp = str(item.get_text())
        var.append(var_temp)

#Removendo valores em branco
try:
    date.remove("")
    var.remove("")
except:
    pass

#Editando a data para um valor INTEGER e criando uma lista de listas chamada **data**
j = 0
data = []
while j < len(date):
    date[j] = int(date[j][:4]+date[j][5:7]+"01")
    data_temp = [date[j], float(str(var[j]).replace(",","."))]
    data.append(data_temp)
    j += 1

def export_csv(table_name="IGPDI", select="*"):
    c1 = pymysql.connect(host="localhost", user="root", passwd="isec@3320", db="indices")
    c2 = c1.cursor()
    dates = []

    sql_select = "SELECT * FROM %s" %(table_name)

    c2.execute(sql_select)

    data = c2.fetchall()
    data = pd.DataFrame(data, columns=["Date","VAR"])

    data.to_csv(getcwd()+"\IGPDI.csv", sep=";",index=False, doublequote=False, decimal=",")
    c2.close()
    c1.close()

#end of declaration

c1 = pymysql.connect(host="localhost", user="root", passwd="isec@3320", db="indices")
c2 = c1.cursor()



c2.execute("CREATE TABLE IF NOT EXISTS %s(date INTEGER primary key, VAR float)" %(table_name))

for item in data:
    c2.execute("INSERT IGNORE INTO %s (date, VAR) VALUES(%d, %7.4f)" %(table_name, item[0], item[1]))

c1.commit()
c2.close()
c1.close()

answer = input("Você deseja exportar o arquivo para CSV?")

if answer.upper() == "SIM":
    export_csv(table_name="IGPDI")
