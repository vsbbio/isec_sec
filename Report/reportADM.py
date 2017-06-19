from trello import TrelloClient
from contextlib import redirect_stdout
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import datetime
import io
import smtplib

def send_email(user, pwd, recipient, subject, body):
    
    fromaddr = user
    toaddr = recipient
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = subject
 
    msg.attach(MIMEText(body, 'plain'))
    
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(fromaddr, pwd)
        text = msg.as_string()
        server.sendmail(fromaddr, toaddr, text)
        server.quit()
        print('successfully sent the mail')
     
    except:
        print("failed to send mail")  

#Creating Trello Object
    
#1- Generate your API_KEY
#link: https://trello.com/app-key
ap = '116ca1d51a01ca46cfe3cf14ce45efff'

#2 = Authorize your API_KEY and Generate a API_SECRET
#link: https://trello.com/1/authorize?expiration=never&name=SinglePurposeToken&key=REPLACE_API_KEY
aps = 'f4b01c8b246b9c94930d288e4a532540'

#3 = Authorize your API_KEY and Generate a Token:
#link: https://trello.com/1/authorize?expiration=never&scope=read,write,account&response_type=token&name=Server%20Token&key=REPLACE_API_KEY
tk = '2dd90ef3e7614b6451e5afe13b05e5d72867d5795cd1ec7443fdb6bdd1ff3ec2'

#4 = Get your Token_Secret:
#link: https://trello.com/app-key (OAuth - Secret)
tks = '17cfc6009d7f0c0d09e41754af93a94c50286ed4e5d0dd06d6cd844a9ca0d41f'
    
client = TrelloClient(api_key= ap, api_secret=aps, token=tk, token_secret=tks)
b_id = "589a04cf3e26d2d8a9f27533"

board = client.get_board(b_id)
now = datetime.datetime.now()
    
lst_name = []
card_name = []
        
lists = board.list_lists()
    
for lst in lists:
    cards = lst.list_cards()
    temp1 = []
        
    if len(cards) > 0:
            
        temp = lst.name
        lst_name.append(temp)
            
        for card in cards:
            date = card.card_created_date
            datestr = str(date.day)+"/"+str(date.month)+"/"+str(date.year)
            temp = datestr +" - "+ card.name + "\nCriado há: " + str((now-date).days) + " dias" + "\n" + "Link: " + card.url
            temp1.append(temp)
            
        card_name.append(temp1)
            
    else:
        pass
            
del temp, temp1, ap, aps, tk, tks

body = io.StringIO()

with redirect_stdout(body):
    print("####### REPORT PIPELINE @TRELLO: %s #######\n" %(datestr))
    j = 0
    for item in lst_name:
        print("\n\n#############  " + item + "\n")
        for item1 in card_name[j]:
            print("    " + item1 +"\n")
        j += 1
    
message = body.getvalue()
send_email("isecbrasil@isecbrasil.com.br","hn36$$879","pamella.lima@isecbrasil.com.br","PIPELINE", message)