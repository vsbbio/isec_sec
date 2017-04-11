def append_di():
        limit = 0
        while limit <= 2:
            try:
                #Verificando se há um arquivo na pasta para ser utilizado
                if os.path.isfile("DI.csv") == False:
                    print("\nArquivo DI.txt não encontrado na pasta executada!")
                    break
            
                else:
                    #Extraindo e convertendo em Pandas.DataFrame os nomes dos arquivos disponíveis no FTP (Função gettxt())
                    txt_lst = gettxt()
                    txt_df = pd.DataFrame(txt_lst, columns=["Arquivo"])
                
                    #Abrindo arquivo DI.csv e convertendo em Pandas.DataFrame
                    di_csv = pd.read_csv("DI.csv", header=0, sep=";")
                    di_df = pd.DataFrame(di_csv)
                    
                    #Criando listagem em de branco
                    new_lst = []
            
                #Criando a listagem dos arquivos novos
                for file in txt_df:
                    if file in di_df["Arquivo"]:
                        new_temp = [file]
                        new_lst.append = [new_temp]
                        
                        #Criando uma barra de progresso
                        if txt_lst.index(file) == 0:
                            sys.stdout.write('\n')
                            sys.stdout.write('\r')
                            sys.stdout.write("Adding Values [%-20s] %d%%" % ('='*int((txt_lst.index(file)+1)*40/len(txt_lst)), 2.5*int((txt_lst.index(file)+1)*40/len(txt_lst))))
                        else:
                            sys.stdout.write('\r')
                            sys.stdout.write("Adding Values [%-20s] %d%%" % ('='*int((txt_lst.index(file)+1)*40/len(txt_lst)), 2.5*int((txt_lst.index(file)+1)*40/len(txt_lst))))
                    else:
                        continue
                
                #Testando se há arquivos novos, se sim ELSE, se não IF (rsrs)    
                if len(new_lst) == 0:
                    print("\nNão há novas taxas!")
                    break
            
                #Adicionando os arquivos novos à planilha já existente
                else:
                    di_lst = getvalue(new_lst)
                    di_df.append(di_lst, ignore_index=True)
                    print("\n %r taxas adicionas" %(len(new_lst)))
                    break
        
            except HTTPError:
                print("\n HTTPError, tentaremos de novo! %r \n %s" %(limit, regFunc(append_di)))
                sleep(10)
                limit += 1
                continue
    
            except URLError:
                print("\nURLError, tentaremos de novo! %r \n %s" %(limit, regFunc(append_di)))
                sleep(10)
                limit += 1
                continue