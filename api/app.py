from flask import Flask, request
import sqlite3
import subprocess
import hashlib
import os

app = Flask(__name__)

# # BON: Utilisation d'une variable d'environnement pour la clé secrète
# SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-12345")


# # ==================== BON CODE (IMPLÉMENTATIONS SÉCURISÉES) ====================

# @app.route("/hello", methods=["GET"])
# def hello():
#     return {"message": "Welcome to the DevSecOps vulnerable API"}


# @app.route("/hash", methods=["POST"])
# def hash_password():
#     pwd = request.json.get("password", "admin")
#     # BON: Utilisation de SHA256 au lieu de MD5 faible
#     hashed = hashlib.sha256(pwd.encode()).hexdigest()
#     return {"sha256": hashed}


# @app.route("/ping", methods=["POST"])
# def ping():
#     host = request.json.get("host", "")
#     # BON: Utilisation de subprocess avec une liste au lieu de shell=True, avec timeout
#     output = subprocess.check_output(
#         ["ping", "-c", "1", host], stderr=subprocess.STDOUT, timeout=5
#     )
#     return {"output": output.decode()}


# @app.route("/login", methods=["POST"])
# def login():
#     username = request.json.get("username")
#     password = request.json.get("password")

#     conn = sqlite3.connect("users.db")
#     cursor = conn.cursor()

#     # BON: Utilisation de requêtes paramétrées pour prévenir l'injection SQL
#     cursor.execute(
#         "SELECT * FROM users WHERE username=? AND password=?",
#         (username, password)
#     )

#     result = cursor.fetchone()
#     if result:
#         return {"status": "success", "user": username}
#     return {"status": "error", "message": "Invalid credentials"}





MAUVAIS: Clé secrète codée en dur
SECRET_KEY = "dev-secret-key-12345"

MAUVAIS: Vulnérabilité d'injection SQL
@app.route("/login", methods=["POST"])
def login_bad():
    username = request.json.get("username")
    password = request.json.get("password")

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    #  SQL Injection évidente
    query = "SELECT * FROM users WHERE username='" + username + "' AND password='" + password + "'"
    cursor.execute(query)

    result = cursor.fetchone()
    if result:
        return {"status": "success", "user": username}
    return {"status": "error", "message": "Invalid credentials"}

MAUVAIS: Vulnérabilité d'injection de commande (utilisation de shell=True)
@app.route("/ping", methods=["POST"])
def ping_bad():
    host = request.json.get("host", "")
    cmd = f"ping -c 1 {host}"
    output = subprocess.check_output(cmd, shell=True)
    return {"output": output.decode()}

MAUVAIS: Injection de code utilisant eval()
@app.route("/compute", methods=["POST"])
def compute():
    expression = request.json.get("expression", "1+1")
    result = eval(expression)  # CRITIQUE - permet l'exécution de code arbitraire
    return {"result": result}

MAUVAIS: Utilisation de l'algorithme de hachage MD5 faible
@app.route("/hash", methods=["POST"])
def hash_password_bad():
    pwd = request.json.get("password", "admin")
    hashed = hashlib.md5(pwd.encode()).hexdigest()
    return {"md5": hashed}

MAUVAIS: Vulnérabilité de traversée de chemin - aucune validation sur le nom de fichier
@app.route("/readfile", methods=["POST"])
def readfile():
    filename = request.json.get("filename", "test.txt")
    with open(filename, "r") as f:
        content = f.read()
    return {"content": content}

MAUVAIS: Exposition d'informations sensibles dans l'endpoint de débogage
@app.route("/debug", methods=["GET"])
def debug():
    # Renvoie des détails sensibles - mauvaise pratique
    return {"debug": True, "secret_key": SECRET_KEY, "environment": dict(os.environ)}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
