from flask import Flask, request, jsonify
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
import base64
import threading
import time

app = Flask(__name__)

public_key_pem = """
-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCff+RRh8ENnKSz/XqhkC8EPiUBVuiW46JbYdbbqfkYM8JoTjwStPIXUOwvHaOb1jdyUCm5zSWxSBT3qe7WtZ1O28M3o6c0OslA/bRZ32sb5n+W66tF4lP4f4dQP2fAMYoR6LPYRhc2DLKU4Ifz1c1iTpTlXkaxLFe9GRp2Wd+OPQIDAQAB
-----END PUBLIC KEY-----
"""

def encrypt_message(public_key_pem, message):
    public_key = serialization.load_pem_public_key(
        public_key_pem.encode('utf-8'),
        backend=default_backend()
    )
    encrypted = public_key.encrypt(
        message,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return base64.b64encode(encrypted).decode('utf-8')

def refresh_console():
    while True:
        print("Console refreshed at", time.strftime("%Y-%m-%d %H:%M:%S"))
        time.sleep(1)

@app.route('/', methods=['POST'])
def encrypt_and_return():
    try:
        request_data = request.get_json()
        message = request_data.get('message', '')
        
        if message:
            encrypted_message = encrypt_message(public_key_pem, message.encode('utf-8'))
            return encrypted_message, 200
        else:
            return 'Missing or empty "message" field in the JSON payload', 400
    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    threading.Thread(target=refresh_console, daemon=True).start()
    app.run(host='0.0.0.0', port=2069,threaded=True)
