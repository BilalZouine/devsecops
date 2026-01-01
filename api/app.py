from flask import Flask, request
import sqlite3
import subprocess
import hashlib
import os

app = Flask(__name__)

SECRET_KEY = "dev-secret-key-12345"  # Hardcoded secret

# SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-12345")



@app.route("/login", methods=["POST"])
def login():
    username = request.json.get("username")
    password = request.json.get("password")

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    
    
    cursor.execute(query)
    
    # cursor.execute(
    #     "SELECT * FROM users WHERE username=? AND password=?",
    #     (username, password)
    # )

    result = cursor.fetchone()
    if result:
        return {"status": "success", "user": username}
    return {"status": "error", "message": "Invalid credentials"}


@app.route("/ping", methods=["POST"])
def ping():
    
    host = request.json.get("host", "")
        
    cmd = f"ping -c 1 {host}"
    
    output = subprocess.check_output(cmd, shell=True)
    
    # output = subprocess.check_output(
    #     ["ping", "-c", "1", host], stderr=subprocess.STDOUT, timeout=5
    # )

    return {"output": output.decode()}


@app.route("/compute", methods=["POST"])
def compute():
    expression = request.json.get("expression", "1+1")
    result = eval(expression)  # CRITIQUE
    return {"result": result}


@app.route("/hash", methods=["POST"])
def hash_password():
    pwd = request.json.get("password", "admin")
    
    hashed = hashlib.md5(pwd.encode()).hexdigest()
    
    # hashed = hashlib.sha256(pwd.encode()).hexdigest()
    
    return {"sha256": hashed}


@app.route("/readfile", methods=["POST"])
def readfile():
    filename = request.json.get("filename", "test.txt")
    with open(filename, "r") as f:
        content = f.read()

    return {"content": content}


@app.route("/debug", methods=["GET"])
def debug():
    # Renvoie des détails sensibles -&gt; mauvaise pratique
    return {"debug": True, "secret_key": SECRET_KEY, "environment": dict(os.environ)}


@app.route("/hello", methods=["GET"])
def hello():
    return {"message": "Welcome to the DevSecOps vulnerable API"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
