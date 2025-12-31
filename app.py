import os
from flask import Flask, request, render_template, send_file, redirect, url_for
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
KEY_FILE = 'secret.key'

# 1. Key Management: Load or Generate a Key
def load_key():
    if not os.path.exists(KEY_FILE):
        key = get_random_bytes(32)  # 256-bit AES Key
        with open(KEY_FILE, 'wb') as f:
            f.write(key)
    with open(KEY_FILE, 'rb') as f:
        return f.read()

SECRET_KEY = load_key()

# 2. Encryption Function (AES-EAX Mode)
def encrypt_file(file_path):
    with open(file_path, 'rb') as f:
        data = f.read()
    
    cipher = AES.new(SECRET_KEY, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(data)
    
    # Save: Nonce + Tag + Ciphertext
    with open(file_path + ".enc", 'wb') as f:
        f.write(cipher.nonce + tag + ciphertext)
    
    # Remove original unencrypted file
    os.remove(file_path)

# 3. Decryption Function
def decrypt_file(enc_file_path, original_filename):
    with open(enc_file_path, 'rb') as f:
        nonce = f.read(16)
        tag = f.read(16)
        ciphertext = f.read()
    
    cipher = AES.new(SECRET_KEY, AES.MODE_EAX, nonce)
    data = cipher.decrypt_and_verify(ciphertext, tag)
    
    # Write to a temporary file to send to user
    dec_path = os.path.join(UPLOAD_FOLDER, "temp_" + original_filename)
    with open(dec_path, 'wb') as f:
        f.write(data)
    return dec_path

@app.route('/')
def index():
    files = [f for f in os.listdir(UPLOAD_FOLDER) if f.endswith('.enc')]
    return render_template('index.html', files=files)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)
    
    # Encrypt immediately
    encrypt_file(file_path)
    return redirect(url_for('index'))

@app.route('/download/<filename>')
def download_file(filename):
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    # Remove .enc extension for the user download
    original_name = filename.replace('.enc', '')
    
    try:
        decrypted_path = decrypt_file(file_path, original_name)
        return send_file(decrypted_path, as_attachment=True, download_name=original_name)
    except Exception as e:
        return f"Error decrypting file: {str(e)}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
