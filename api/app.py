from flask import Flask, request
import sqlite3
import subprocess
import hashlib
import os

app = Flask(__name__)

# ✅ Secret from environment
SECRET_KEY = os.environ.get("SECRET_KEY")


@app.route("/hello", methods=["GET"])
def hello():
    return {"message": "Welcome to secure API"}


# ✅ Strong hashing
@app.route("/hash", methods=["POST"])
def hash_password():
    pwd = request.json.get("password", "")
    hashed = hashlib.sha256(pwd.encode()).hexdigest()
    return {"sha256": hashed}


# ✅ Safe subprocess usage
@app.route("/ping", methods=["POST"])
def ping():
    host = request.json.get("host", "")
    output = subprocess.check_output(
        ["ping", "-c", "1", host],
        stderr=subprocess.STDOUT,
        timeout=5
    )
    return {"output": output.decode()}


# ✅ Parameterized SQL
@app.route("/login", methods=["POST"])
def login():
    username = request.json.get("username")
    password = request.json.get("password")

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (username, password)
    )

    result = cursor.fetchone()
    if result:
        return {"status": "success", "user": username}

    return {"status": "error"}


# ✅ No eval, safe math
@app.route("/compute", methods=["POST"])
def compute():
    a = int(request.json.get("a", 0))
    b = int(request.json.get("b", 0))
    return {"result": a + b}


# ✅ Path validation
@app.route("/readfile", methods=["POST"])
def readfile():
    filename = request.json.get("filename", "")
    base_dir = "/app/data"
    full_path = os.path.abspath(os.path.join(base_dir, filename))

    if not full_path.startswith(base_dir):
        return {"error": "Access denied"}, 403

    with open(full_path, "r") as f:
        return {"content": f.read()}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
