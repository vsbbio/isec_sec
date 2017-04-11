#Função APOIO para extrair a listagem com o nome dos arquivos disponíveis no FTP
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

            #Invertando a ordem da lista    
            txt_lst.reverse()
            
            #Removendo a primeira linha da lista
            txt_lst.remove(txt_lst[0])
            
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