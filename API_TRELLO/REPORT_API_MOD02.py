from trello import TrelloClient
from pytz import timezone
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
ap = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

#2 = Authorize your API_KEY and Generate a API_SECRET
#link: https://trello.com/1/authorize?expiration=never&name=SinglePurposeToken&key=REPLACE_API_KEY
aps = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

#3 = Authorize your API_KEY and Generate a Token:
#link: https://trello.com/1/authorize?expiration=never&scope=read,write,account&response_type=token&name=Server%20Token&key=REPLACE_API_KEY
tk = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

#4 = Get your Token_Secret:
#link: https://trello.com/app-key (OAuth - Secret)
tks = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

client = TrelloClient(api_key= ap, api_secret=aps, token=tk, token_secret=tks)
boards = client.list_boards()
now = datetime.datetime.now()

board_name = []
board_id = []
list_id = []
card_name = []
            
for board in boards:
    lists = board.list_lists()
    for lst in lists:
        if lst.name == "XXXXXXXX":
            
            temp = lst.board.name
            board_name.append(temp)
            
            temp = lst.board.id
            board_id.append(temp)
            
            temp = lst.id
            list_id.append(temp)
            
            cards = lst.list_cards()
            temp1 = []
            for card in cards:
                date = card.card_created_date
                datestr = str(date.day)+"/"+str(date.month)+"/"+str(date.year)
                temp = datestr +" - "+ card.name + "\n" + "Criado há: " + str((now-date).days) + " dias" + "\n" + "Link: " + card.url
                temp1.append(temp)
            
            card_name.append(temp1)
            
        else:
            pass            
        
del temp, temp1, ap, aps, tk, tks

body = io.StringIO()

with redirect_stdout(body):
    print("####### NAME OF YOUR REPORT @TRELLO: %s #######\n" %(datestr))
    j = 0
    for item in board_name:
        print("\n####### " + item + "\n")
        for item1 in card_name[j]:
            print("    " + item1 +"\n")
        j += 1
    
message = body.getvalue()

send_email("XXXXXX","XXXXXXXX","XXXXXXXX","XXXXXXXX", message)