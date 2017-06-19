import pandas as pd
import pymysql
from urllib.request import urlopen
from urllib.error import HTTPError, URLError
from bs4 import BeautifulSoup
from time import sleep

table_name = "CDI"

def wsName():
    limit = 0
    while limit <= 10:
        try:
            #Capturando o conteúdo da página
            html = urlopen("ftp://ftp.cetip.com.br/MediaCDI")
            Bso = BeautifulSoup(html,"lxml")

            #Extraindo a listagem com o nome e extensão dos arquivos
            for txt in Bso:
                txt_temp = txt.get_text()

            #Convertendo a string em lista
            txt_temp = txt_temp.split("\r")

            #Removendo valores em branco e Criando listagem em de branco
            try:

                try:
                    txt_temp.remove("")
                    txt_temp.remove("\n")
                except:
                    txt_temp.remove("\n")

            except:
                    txt_temp.remove("")

            finally:
                txt = []

            #Editando os registros para excluir espaços e outros caracteres
            for item in txt_temp:
                txt.append(int(item[-12:-4]))

            #Retornando o resultado à uma variável
            return txt

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

def wsValue(names):

    #Criando uma variável vázia para preenchimento posterior
    data = []

    #Loop para leitura e captura do conteúdo dos arquivos contidos no diretório
    for file in names:
        try:
            #Capturando o conteúdo de cada arquivo contido no diretório
            html = urlopen("ftp://ftp.cetip.com.br/MediaCDI/"+str(file)+".txt")
            Bso = BeautifulSoup(html,"lxml")
            value = Bso.get_text()

            #Editando o conteúdo, excluindo espaços e outros caracteres
            value = float(value[:9])
            data_temp = [int(file), float(value/10000)]
            data.append(data_temp)
        except:
            print("Erro link: %s" %(html))
            continue

    #Retornando o resultado do tratamento
    return data

#Acessando DB para coletar as datas já inclusas
c1 = pymysql.connect(host="localhost", user="root", passwd="isec@3320", db="indices")
c2 = c1.cursor()
sql_create = "CREATE TABLE IF NOT EXISTS %s(date INTEGER primary key, VAR float)" %(table_name)
c2.execute(sql_create)
c2.execute("SELECT date FROM CDI")
dates = c2.fetchall()

#Alterando formado das datas no DB
dates2 = []
for item in dates:
    temp = item[0]
    dates2.append(temp)

#Coletando todos os nomes dos arquivos disponíveis no diretório FTP da CETIP
names = wsName()
#Criando listagem em de branco
new = []
#Comparando e criando a listagem dos arquivos novos
for item in names:
    if item not in dates2:
        new_temp = item
        new.append(new_temp)
    else:
        pass

if len(new) > 0:
    #CRIANDO TABELA SQL E INSERINDO DADOS
    data = wsValue(new)

    for item in data:
        sql_insert = "INSERT IGNORE INTO CDI (date, VAR) VALUES(%d, %4.2f)" %(item[0], item[1])
        c2.execute(sql_insert)
        c1.commit()

    c2.close()
    c1.close()
    print("Foram adicionadas %d Taxas!" %(len(new)))

else:
    print("\nNão há novas taxas!")
