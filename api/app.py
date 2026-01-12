from flask import Flask, request
import sqlite3
import subprocess
import hashlib
import os

app = Flask(__name__)

# ❌ Hardcoded secret
SECRET_KEY = "dev-secret-key-12345"


@app.route("/hello", methods=["GET"])
def hello():
    return {"message": "Hello insecure world"}


# ❌ Weak hashing (MD5)
@app.route("/hash", methods=["POST"])
def hash_password():
    pwd = request.json.get("password", "admin")
    hashed = hashlib.md5(pwd.encode()).hexdigest()
    return {"md5": hashed}


# ❌ Command Injection (shell=True)
@app.route("/ping", methods=["POST"])
def ping():
    host = request.json.get("host", "")
    cmd = f"ping -c 1 {host}"
    output = subprocess.check_output(cmd, shell=True)
    return {"output": output.decode()}


# ❌ SQL Injection
@app.route("/login", methods=["POST"])
def login():
    username = request.json.get("username")
    password = request.json.get("password")

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    query = (
        "SELECT * FROM users WHERE username='"
        + username +
        "' AND password='"
        + password +
        "'"
    )

    cursor.execute(query)
    result = cursor.fetchone()

    if result:
        return {"status": "success", "user": username}
    return {"status": "error"}


# ❌ Arbitrary code execution
@app.route("/compute", methods=["POST"])
def compute():
    expression = request.json.get("expression", "1+1")
    return {"result": eval(expression)}


# ❌ Path Traversal
@app.route("/readfile", methods=["POST"])
def readfile():
    filename = request.json.get("filename")
    with open(filename, "r") as f:
        return {"content": f.read()}


# ❌ Sensitive info disclosure
@app.route("/debug", methods=["GET"])
def debug():
    return {
        "secret": SECRET_KEY,
        "env": dict(os.environ)
    }


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
