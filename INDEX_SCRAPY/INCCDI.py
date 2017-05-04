import pandas as pd
import sqlite3 as sq3

from urllib.request import urlopen
from urllib.error import HTTPError, URLError
from time import sleep
from bs4 import BeautifulSoup
from os import getcwd

def wsValue():
    limit = 0
    while limit <= 10:
        try:
            html = urlopen("http://indiceseconomicos.secovi.com.br/indicadormensal.php?idindicador=59")
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
                    indext = [int(str(y) + str(month[item])+"01"), str(lst_b[j+1]).replace(" ","").replace("\n","")]
                    index_t.append(indext)
                elif item in lst_m2:
                    indext = [int(str(y) + str(month[item])+"01"), str(lst_b[j+1]).replace(" ","").replace("\n", "")]
                    index_t.append(indext)
                    y += 1
                else:
                    pass
                j += 1

            return index_t
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
            
#Funções para lidar com os dados contidos no db sqlite3
def criar(table_name="INCCDI"):
    c1 = sq3.connect("INDEX.db")
    c2 = c1.cursor()

    sql_create = "CREATE TABLE IF NOT EXISTS %s(date datetime primary key, VAR INTEGER)" %(table_name)
    c2.execute(sql_create)

    c2.close()
    c1.close()

def inserir(table_name="INCCDI", data_insert="DATA"):
    c1 = sq3.connect("INDEX.db")
    c2 = c1.cursor()

    sql_insert = "INSERT OR IGNORE INTO %s VALUES(?, ?)" %(table_name)

    for item in data_insert:
        c2.execute(sql_insert, item)

    c1.commit()
    c2.close()
    c1.close()

def export_csv(table_name="TABELA", select="*"):
    c1 = sq3.connect("INDEX.db")
    c2 = c1.cursor()
    dates = []

    sql_select = "SELECT %s FROM %s" %(select, table_name)

    c2.execute(sql_select)

    data = c2.fetchall()
    data = pd.DataFrame(data, columns=["Date","VAR"])

    data.to_csv(getcwd()+"\INCCDI.csv", sep=";",index=False, doublequote=False, decimal=".")

criar(table_name="INCCDI")
inserir(table_name="INCCDI", data_insert=wsValue())

answer = input("Você deseja exportar o arquivo para CSV?")

if answer.upper() == "SIM":
    export_csv(table_name="INCCDI")