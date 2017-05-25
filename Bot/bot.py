"""
This bot listens to port 5002 for incoming connections from Facebook. It takes
in any messages that the bot receives and echos it back.
"""
from flask import Flask, request
import requests
import json
import string
import random
import quandl
import locale
from datetime import *

app = Flask(__name__)

conf = json.loads(open("config.json").read())

# ACCESS_TOKEN = "EAADL1pcTtMEBABqPCHEtOZB9f5fP05zZCJN6tJbT5ZCKypPFWgyydXtZBH5w4i3qSBerohZCNDZCa6RKIZBG4Rg0379LLG9kqe3qpsZBZB9gbQZBVFlfvWaiM3v7mpKbzHjk9ZCT2q3jjGe4c8S2PMIxCixDxBDcvepXyQzRwDJZCcOpSQZDZD"
# VERIFY_TOKEN = "test_token"
# bot = Bot(ACCESS_TOKEN)

locale.setlocale(locale.LC_ALL, ('en_US', 'UTF-8')) # Set locale to en_US
quandl.ApiConfig.api_key = "V5uEXA4L1zfc9Q6Dp9Lz" # Set API key

from stock_price import *

def sendMessage(msg, img=None):
    data = {
        "bot_id":conf["GM_BOT"],
        "text":msg
    }
    return requests.post("https://api.groupme.com/v3/bots/post", data=data)


def getSessID():  # Generates a random ID
    chars = string.ascii_lowercase + string.digits
    return ''.join(random.choice(chars) for _ in range(36))


def getNLP(query):
    print(getSessID())
    headers = {"Authorization": "Bearer "+conf['APIAI_TOKEN']}
    url = "https://api.api.ai/v1/query"
    data = {"query":query, "lang":"en", "sessionId":getSessID()}
    print("sending req")
    return requests.get(url, headers=headers, params=data).json()


@app.route("/msg", methods=["GET", "POST"])
def groupme_message():
    print("hiya")
    j = request.json
    msg = j['text']

    if(j['sender_type'] == 'bot'):
        return "nope"

    if(msg.lower().find("onu") != -1):
        print("omu here")
        sendtxt = msg.replace(",", "").replace("onu", "") #todo: regex
        ai = getNLP(sendtxt)
        print(ai)

        #todo: error handling

        event = ai['result']['metadata']['intentName']

        if(event == "Price of stock"):
            ticker = ai['result']['parameters']['StockTickers'] #todo: no full full names
            print("ticker", ticker)
            price = get_stock_price_friendly(ticker)
            print(price)
            sendMessage(price)

        if(event == "Buy Stock"):
            ticker = ai['result']['parameters']['StockTickers']

            group_size = 5
            price = get_stock_price(ticker)
            div_price = price / group_size

            msg = "The current price of %s is %s, split among each of %s members, each of you will have to pay %s " \
                  % (ticker.upper(), locale.currency(price), group_size,locale.currency(div_price))
            sendMessage(msg)
            sendMessage("Favorite THIS message to confirm!") #todo: me send?



    else:
        pass




    return "okay"





"""@app.route("/", methods=['GET', 'POST'])
def hello():
    if request.method == 'GET':
        if request.args.get("hub.verify_token") == VERIFY_TOKEN:
            return request.args.get("hub.challenge")
        else:
            return 'Invalid verification token'

    if request.method == 'POST':
        output = request.get_json()
        for event in output['entry']:
            messaging = event['messaging']
            for x in messaging:
                if x.get('message'): #todo: make sure msg says onu

                    print(x)
                    j = getNLP(x)




                    recipient_id = x['sender']['id']
                    if x['message'].get('text'):
                        message = x['message']['text']
                        bot.send_text_message(recipient_id, message)
                    if x['message'].get('attachments'):
                        for att in x['message'].get('attachments'):
                            bot.send_attachment_url(recipient_id, att['type'], att['payload']['url'])
                else:
                    pass
        return "Success"
"""

if __name__ == "__main__":
    print("msg", sendMessage("Hiya, it's Onu!").text)
    app.run(port=5002, debug=True)
