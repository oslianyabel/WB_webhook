from flask import Flask, request, jsonify
import os
from datetime import datetime

app = Flask(__name__)

port = int(os.environ.get('PORT', 3000))
verify_token = os.environ.get('VERIFY_TOKEN')

# Ruta para GET
@app.route('/', methods=['GET'])
def verify_webhook():
    mode = request.args.get('hub.mode')
    challenge = request.args.get('hub.challenge')
    token = request.args.get('hub.verify_token')

    if mode == 'subscribe' and token == verify_token:
        print('WEBHOOK VERIFIED')
        return challenge, 200
    else:
        return '', 403

# Ruta para POST
@app.route('/', methods=['POST'])
def receive_webhook():
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"\n\nWebhook received {timestamp}\n")
    print(request.get_json())
    return '', 200

if __name__ == '__main__':
    print(f"\nListening on port {port}\n")
    app.run(host='0.0.0.0', port)