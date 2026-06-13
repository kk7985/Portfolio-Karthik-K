from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)
CORS(app, origins=["https://kk7985.github.io"])

DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME")
}

def get_connection():
    return mysql.connector.connect(**DB_CONFIG)

@app.route("/", methods=["GET"])
def health():
    return jsonify({"status": "Flask server running"}), 200

@app.route("/contact", methods=["POST"])
def save_contact():
    data = request.get_json()
    name    = (data.get("name") or "").strip()
    email   = (data.get("email") or "").strip()
    message = (data.get("message") or "").strip()
    if not name or not email or not message:
        return jsonify({"success": False, "error": "All fields required."}), 400
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO contact_messages (name, email, message) VALUES (%s,%s,%s)",
            (name, email, message)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"success": True}), 200
    except Error as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)
