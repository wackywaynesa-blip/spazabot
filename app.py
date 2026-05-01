import os
from flask import Flask, request

app = Flask(__name__)

# This is the secret word you will put in the Meta dashboard later
VERIFY_TOKEN = "spaza_secret_123"

@app.route('/webhook', methods=['GET'])
def verify():
    # Meta sends a GET request to verify your bot
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    
    if token == VERIFY_TOKEN:
        return challenge, 200
    return "Verification failed", 403

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)))
