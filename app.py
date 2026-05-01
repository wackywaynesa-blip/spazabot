import os
import sys
from flask import Flask, request

app = Flask(__name__)

VERIFY_TOKEN = "spaza_secret_123"

@app.route('/webhook', methods=['GET', 'POST'])
def verify():
    if request.method == 'GET':
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")
        if token == VERIFY_TOKEN:
            return challenge, 200
        return "Verification failed", 403

    data = request.get_json()
    
    if data:
        try:
            # Drilling down into the Meta data structure
            entry = data['entry'][0]
            changes = entry['changes'][0]
            value = changes['value']
            
            if 'messages' in value:
                message_data = value['messages'][0]
                sender_name = value['contacts'][0]['profile']['name']
                sender_num = message_data['from']
                message_text = message_data['text']['body']

                # PRINTING CLEAN DATA FOR THE LOGS
                print(f"\n--- NEW MESSAGE ---", file=sys.stderr, flush=True)
                print(f"FROM: {sender_name} ({sender_num})", file=sys.stderr, flush=True)
                print(f"TEXT: {message_text}", file=sys.stderr, flush=True)
                print(f"-------------------\n", file=sys.stderr, flush=True)

        except (KeyError, IndexError):
            # This handles status updates (sent/delivered/read) which we don't need to print
            pass
            
    return "Message received", 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)))
