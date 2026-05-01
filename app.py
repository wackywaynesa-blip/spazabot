import os
from flask import Flask, request

app = Flask(__name__)

# The secret word you put in the Meta dashboard
VERIFY_TOKEN = "spaza_secret_123"

@app.route('/webhook', methods=['GET', 'POST'])
def verify():
    if request.method == 'GET':
        # Meta sends a GET request to verify your bot
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")
        
        if token == VERIFY_TOKEN:
            return challenge, 200
        return "Verification failed", 403

    # This handles the POST (the actual WhatsApp messages)
    data = request.get_json()
    
    # This line prints the raw message data to your Render logs
    print(f"Incoming WhatsApp Data: {data}")
    
    return "Message received", 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)))
