import os
import sys
import requests
from flask import Flask, request

app = Flask(__name__)

# CONFIGURATION
VERIFY_TOKEN = "spaza_secret_123"
WHATSAPP_TOKEN = "PASTE_YOUR_TEMPORARY_ACCESS_TOKEN_HERE"
PHONE_NUMBER_ID = "1159935663863682"

# THE BRAIN: Your Shop Data
PRICES = {
    "bread": "R18.50",
    "milk": "R16.00",
    "eggs": "R30.00 (Dozen)",
    "coke": "R15.00"
}
SPECIALS = "Today's Special: 2x Bread for R35!"

def send_whatsapp_message(to, text):
    url = f"https://graph.facebook.com/v18.0/{PHONE_NUMBER_ID}/messages"
    headers = {"Authorization": f"Bearer {WHATSAPP_TOKEN}", "Content-Type": "application/json"}
    data = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {"body": text}
    }
    response = requests.post(url, headers=headers, json=data)
    return response.status_code

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        if request.args.get("hub.verify_token") == VERIFY_TOKEN:
            return request.args.get("hub.challenge"), 200
        return "Failed", 403

    data = request.get_json()
    if data:
        try:
            entry = data['entry'][0]['changes'][0]['value']
            if 'messages' in entry:
                msg = entry['messages'][0]
                customer_num = msg['from']
                user_text = msg['text']['body'].lower().strip()

                # LOGIC: What does the bot say?
                reply = "Hi! Type 'Prices' for a list or 'Special' for today's deal."

                if "price" in user_text:
                    reply = "Our Prices:\n" + "\n".join([f"{k.capitalize()}: {v}" for k, v in PRICES.items()])
                elif "special" in user_text:
                    reply = SPECIALS
                elif any(product in user_text for product in PRICES):
                    for product in PRICES:
                        if product in user_text:
                            reply = f"The price for {product} is {PRICES[product]}."
                
                # SEND THE REPLY BACK
                send_whatsapp_message(customer_num, reply)
                print(f"Replied to {customer_num}", file=sys.stderr, flush=True)

        except: pass
            
    return "OK", 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)))
