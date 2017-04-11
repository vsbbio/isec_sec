#Função para consolidar todos os DI's disponíveis no FTP
    def getall_di():
        limit = 0
        while limit <= 2:
            try:
                #Extração dos nomes dos arquivos disponíveis no FTP
                txt_lst = gettxt()
            
                #Extração do texto/conteúdo dos arquivos contidos no diretório
                di_lst = getvalue(txt_lst)
        
                #Convertendo a listagem em DataFrame
                di_df = pd.DataFrame(di_lst, columns=["Arquivo", "Data", "Taxa x 100"])
    
                #Salvando o arquivo em CSV
                di_df.to_csv(pathFILE+"\\DI"+snowflake+".csv", sep=";",index=False, doublequote=False, decimal=",", mode="a")
                print("\nArquivo salvo em %s, por favor verificar a correta alocação!" %(pathFILE))
                break
    
        
            except HTTPError:
                print("\nHTTPError, tentaremos de novo! %r \n %s" %(limit, regFunc(getall_di)))
                sleep(10)
                limit += 1
                continue
        
            except URLError:
                print("\nURLError, tentaremos de novo! %r \n %s" %(limit, regFunc(getall_di)))
                sleep(10)
                limit += 1
                continue