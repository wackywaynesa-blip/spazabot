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

    # Force the log to show up immediately
    data = request.get_json()
    print(f"DEBUG: Received a POST request", file=sys.stderr, flush=True)
    
    if data:
        print(f"Incoming WhatsApp Data: {data}", file=sys.stderr, flush=True)
    else:
        # If get_json() failed, show the raw text
        raw_data = request.data.decode('utf-8')
        print(f"Raw Data Received: {raw_data}", file=sys.stderr, flush=True)
    
    return "Message received", 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)))
