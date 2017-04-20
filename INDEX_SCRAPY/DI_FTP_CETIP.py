import pandas as pd
import os
import sys
from urllib.request import urlopen
from urllib.error import HTTPError, URLError
from bs4 import BeautifulSoup
from time import localtime, strftime, sleep

#Definindo parâmetros do sistema
pathFILE = os.getcwd()
snowflake = strftime("%d %b %Y", localtime())

#Função Genérica
def regFunc(func):
    return func

#Função geTxt.py - extração da listagem com os nomes dos arquivos disponíveis no FTP
def gettxt():
    limit = 0
    while limit <= 10:
        try:
            
            #Capturando o conteúdo da página
            html = urlopen("ftp://ftp.cetip.com.br/MediaCDI")
            txt_bs = BeautifulSoup(html,"lxml")
            
            #Extraindo a listagem com o nome e extensão dos arquivos
            for txt in txt_bs:
                txt_str = txt.get_text()
            
            #Convertendo a string em lista 
            txt_lst = txt_str.split("\n")
            
            #Removendo valores em branco
            txt_lst.remove("")
            
            #Criando listagem em de branco
            txt_out = []
            
            #Editando os registros para excluir espaços e outros caracteres 
            for file in txt_lst:
                txt_out.append(file[-13:-1])
                
                #Criando uma barra de progresso
                if txt_lst.index(file) == 0:
                    sys.stdout.write('\n')
                    sys.stdout.write('\r')
                    sys.stdout.write("Getting Names [%-20s] %d%%" % ('='*int((txt_lst.index(file)+1)*20/len(txt_lst)), 5*int((txt_lst.index(file)+1)*20/len(txt_lst))))
                else:
                    sys.stdout.write('\r')
                    sys.stdout.write("Getting Names [%-20s] %d%%" % ('='*int((txt_lst.index(file)+1)*20/len(txt_lst)), 5*int((txt_lst.index(file)+1)*20/len(txt_lst))))
            
            #Retornando o resultado do tratamento
            return txt_out
        
        except HTTPError:
            print("\nHTTPError, tentaremos de novo! %r \n %s" %(limit, regFunc(gettxt)))
            sleep(10)
            limit += 1
            continue
        
        except URLError:
            print("\nURLError, tentaremos de novo! %r \n %s" %(limit, regFunc(gettxt)))
            sleep(10)
            limit += 1
            continue

#Função getValues.py - extração do conteúdo dos arquivos contidos no diretório
def getvalue(txt_lst):
    limit = 0
    
    #Criando uma variável vázia para preenchimento posterior
    di_lst = []
    
    #Loop para leitura e captura do conteúdo dos arquivos contidos no diretório
    for file in txt_lst:
        
        #Loop para evitar erros de conexão com a fonte
        while limit <= 10:
            try:
                
                #Capturando o conteúdo de cada arquivo contido no diretório
                html = urlopen("ftp://ftp.cetip.com.br/MediaCDI/"+file)
                di_bs = BeautifulSoup(html,"lxml")
                di = di_bs.get_text()
                
                #Editando o conteúdo, excluindo espaços e outros caracteres
                di = float(di[:9])
                
                #Armazenando temporariamente o resultado em uma lista composta de arquivo|data|taxa_di
                di_lst_temp = [file, str(file[:4])+"."+str(file[4:6])+"."+str(file[6:8]), float(di/100)]
                
                #Incluindo o arquivo temporária na listagem final
                di_lst.append(di_lst_temp)
                
                #Criando uma barra de progresso
                if txt_lst.index(file) == 0:
                    sys.stdout.write('\n')
                    sys.stdout.write('\r')
                    sys.stdout.write("Getting Values [%-20s] %d%%" % ('='*int((txt_lst.index(file)+1)*20/len(txt_lst)), 5*int((txt_lst.index(file)+1)*20/len(txt_lst))))
                else:
                    sys.stdout.write('\r')
                    sys.stdout.write("Getting Values [%-20s] %d%%" % ('='*int((txt_lst.index(file)+1)*20/len(txt_lst)), 5*int((txt_lst.index(file)+1)*20/len(txt_lst))))
                break
            
            except HTTPError:
                print("\nHTTPError, tentaremos de novo! %r \n %s" %(limit, regFunc(getvalue)))
                sleep(10)
                limit += 1
                continue
            except URLError:
                print("\nURLError, tentaremos de novo! %r \n %s" %(limit, regFunc(getvalue)))
                sleep(10)
                limit += 1
                continue
            
    #Retornando o resultado do tratamento
    return di_lst

#Verificando se há um arquivo na pasta para ser utilizado
if os.path.isfile("DI.csv") == False:
    
    """Executando GetTxt e GetValues. Extração dos nomes 
    dos arquivos disponíveis no FTP. Extração do texto/conteúdo 
    dos arquivos contidos no diretório"""
            
    di_lst = getvalue(gettxt())
                                
    #Convertendo a listagem em DataFrame
    di_df = pd.DataFrame(di_lst, columns=["Arquivo", "Data", "Taxa x 100"])
                
    #Salvando o arquivo em CSV
    di_df.to_csv(pathFILE+"\\DI"+snowflake+".csv", sep=";",index=False, doublequote=False, decimal=",")
    print("\nArquivo salvo em %s, por favor verificar a correta alocação!" %(pathFILE))
    

else:
    #Extraindo e os nomes dos arquivos disponíveis no FTP (Função gettxt())
    txt_lst = gettxt()
            
    #Abrindo e convertendo o arquivo DI.csv em Data Frame
    di_csv = pd.read_csv("DI.csv", sep=";", decimal=",")
    di_df = pd.DataFrame(di_csv, columns=["Arquivo","Data","Taxa x 100"])
                    
    #Isolando a coluna "Arquivo" para comparação
    di_lst = list(di_csv["Arquivo"])
                    
                    
    #Criando listagem em de branco
    new_lst = []
                    
    #Criando a listagem dos arquivos novos
    for file in txt_lst:
        if file not in di_lst:
        
            new_temp = file
            new_lst.append(new_temp)
            
        else:
            pass
        
            #Criando uma barra de progresso
            if txt_lst.index(file) == 0:
                sys.stdout.write('\n')
                sys.stdout.write('\r')
                sys.stdout.write("Comparing Files [%-20s] %d%%" % ('='*int((txt_lst.index(file)+1)*40/len(txt_lst)), 2.5*int((txt_lst.index(file)+1)*40/len(txt_lst))))
            else:
                sys.stdout.write('\r')
                sys.stdout.write("Comparing Files [%-20s] %d%%" % ('='*int((txt_lst.index(file)+1)*40/len(txt_lst)), 2.5*int((txt_lst.index(file)+1)*40/len(txt_lst))))
        
    #Testando se há arquivos novos, se sim ELSE, se não IF (rsrs)       
    if len(new_lst) == 0:
        print("\nNão há novas taxas!")
        
            
    #Adicionando os arquivos novos à planilha já existente
    else:
        #Executando função GetValue e convertendo em Data Frame
        val_df = pd.DataFrame(getvalue(new_lst), columns=["Arquivo","Data","Taxa x 100"])
                
        #Convertendo a Coluna "Taxa x 100" em numerico
        val_df["Taxa x 100"] = pd.to_numeric(val_df["Taxa x 100"])
                
        #Adicionando os novos valores e salvando o arquivo na pasta executada
        di_df.append(val_df, ignore_index=True).to_csv(pathFILE+"\\DI.csv", sep=";",index=False, doublequote=False, decimal=",")
                
        print("\n %r taxas adicionas" %(len(new_lst)))