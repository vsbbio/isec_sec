import pandas as pd
import pymysql
from time import sleep
from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.error import HTTPError, URLError

INCCDI_URL = "http://indiceseconomicos.secovi.com.br/indicadormensal.php?idindicador=59"
table_name = "INCCDI"
limit = 0
j = 0

while limit <= 10:
    try:

        html = urlopen(INCCDI_URL)
        bso = BeautifulSoup(html, "lxml")

        month1 = bso.find_all("td", {"class":"borderLeft "})
        month2 = bso.find_all("td", {"class":"borderLeft borderBottom "})
        bowl = bso.find_all("td")

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

            index_t = []
            y = 1995
            j = 0
            month = {"JAN":"01","FEV":"02","MAR":"03","ABR":"04","MAI":"05",\
                "JUN":"06","JUL":"07","AGO":"08","SET":"09","OUT":"10","NOV":"11","DEZ":"12",}

        for item in lst_b:
            if item in lst_m1:
                indext = [int(str(y) + str(month[item])+"01"), float(str(lst_b[j+1]).replace(" ","").replace("\n","").replace(".","").replace(",","."))]
                index_t.append(indext)
            elif item in lst_m2:
                indext = [int(str(y) + str(month[item])+"01"), float(str(lst_b[j+1]).replace(" ","").replace("\n", "").replace(".","").replace(",","."))]
                index_t.append(indext)
                y += 1
            else:
                pass
            j += 1
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

#CRIANDO TABELA SQL E INSERINDO DADOS
c1 = pymysql.connect(host="localhost", user="root", passwd="isec@3320", db="indices")
c2 = c1.cursor()

sql_create = "CREATE TABLE IF NOT EXISTS %s(date INTEGER primary key, VAR float)" %(table_name)
c2.execute(sql_create)

for item in index_t:
    sql_insert = "INSERT IGNORE INTO INCCDI (date, VAR) VALUES(%d, %7.3f)" %(item[0], item[1])
    c2.execute(sql_insert)
    c1.commit()

c2.close()
c1.close()
print("Finish!")
