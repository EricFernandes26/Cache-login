from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from cadastro import cadastrar_usuario, buscar_usuario
import bcrypt
import os

# Configura o Flask para servir arquivos da pasta "front"
app = Flask(__name__, static_folder="../front")
CORS(app)  # Habilita CORS, caso necessário para APIs externas

# Rota para servir o arquivo HTML principal (index.html)
@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

# Rota para servir outros arquivos estáticos, como CSS e JS
@app.route('/<path:path>')
def serve_static_files(path):
    return send_from_directory(app.static_folder, path)

# Rota para cadastro de usuários
@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    confirm_password = data.get('confirm_password')

    if password != confirm_password:
        return jsonify({"error": "Passwords do not match"}), 400

    try:
        user_id = cadastrar_usuario(email, email, password)
        return jsonify({"message": "User registered successfully", "user_id": user_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Rota para login de usuários
@app.route('/signin', methods=['POST'])
def signin():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    usuario = buscar_usuario(email)
    if usuario:
        senha_hash = usuario['senha_hash'].encode()
        if bcrypt.checkpw(password.encode(), senha_hash):
            return jsonify({"message": "Login successful"}), 200
        else:
            return jsonify({"error": "Invalid credentials"}), 401
    else:
        return jsonify({"error": "User not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
