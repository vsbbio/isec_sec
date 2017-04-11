#Função APOIO para extrair o texto dos arquivos contidos no diretório
def getvalue(txt_lst):
    limit = 0
    #Criando uma variável vázia para preenchimento posterior
    di_lst = []
    
    #Loop para leitura e captura do conteúdo dos arquivos contidos no diretório
    for file in txt_lst:
        
        #Loop para evitar erros de conexão com a fonte
        while limit <= 10:
            try:
                html = urlopen("ftp://ftp.cetip.com.br/MediaCDI/"+file)
                di_bs = BeautifulSoup(html,"lxml")
                di = di_bs.get_text()
                
                #Editando o conteúdo, excluindo espaços e outros caracteres
                di = di[:9]
                
                #Armazenando temporariamente o resultado em uma lista composta de arquivo|data|taxa_di
                di_lst_temp = [file, file[:-4],int(di)/100]
                
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
                
    return di_lst
