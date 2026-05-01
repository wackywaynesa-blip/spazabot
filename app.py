import os
import sys
from flask import Flask, request, render_template_string

app = Flask(__name__)

# The secret word for Meta
VERIFY_TOKEN = "spaza_secret_123"

# This list stores messages while the server is running
messages_list = []

# Dark Theme HTML Dashboard
DASHBOARD_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>SpazaBot Dashboard</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { background-color: #121212; color: #e0e0e0; font-family: sans-serif; padding: 20px; }
        h2 { color: #00e676; border-bottom: 2px solid #333; padding-bottom: 10px; }
        .card { background: #1e1e1e; padding: 15px; border-radius: 8px; margin-bottom: 10px; border-left: 5px solid #00e676; }
        .name { font-weight: bold; color: #bb86fc; }
        .time { font-size: 0.8em; color: #757575; float: right; }
        .msg { margin-top: 5px; color: #ffffff; }
    </style>
    <meta http-equiv="refresh" content="10"> <!-- Auto-refreshes every 10 seconds -->
</head>
<body>
    <h2>Workshop Inbox</h2>
    {% if not messages %}
        <p>No messages yet. Waiting for customers...</p>
    {% endif %}
    {% for msg in messages %}
        <div class="card">
            <span class="name">{{ msg.name }} ({{ msg.num }})</span>
            <div class="msg">{{ msg.text }}</div>
        </div>
    {% endfor %}
</body>
</html>
"""

@app.route('/')
def dashboard():
    # Shows the dark-themed page with all collected messages
    return render_template_string(DASHBOARD_HTML, messages=messages_list)

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
            entry = data['entry'][0]
            changes = entry['changes'][0]
            value = changes['value']
            
            if 'messages' in value:
                message_data = value['messages'][0]
                sender_name = value['contacts'][0]['profile']['name']
                sender_num = message_data['from']
                message_text = message_data['text']['body']

                # Save to our list (newest on top)
                messages_list.insert(0, {
                    "name": sender_name,
                    "num": sender_num,
                    "text": message_text
                })

                print(f"Captured message from {sender_name}", file=sys.stderr, flush=True)

        except (KeyError, IndexError):
            pass
            
    return "Message received", 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)))
