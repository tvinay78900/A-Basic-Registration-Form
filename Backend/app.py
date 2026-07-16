from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
import os

app = Flask(__name__)
CORS(app)

def get_db():
    return mysql.connector.connect(
        host="gateway01.ap-southeast-1.prod.aws.tidbcloud.com",
        user="VhVBHqfkiAdJRDU.root",
        password="trcsQfVz4Vkmb7hV",
        database="registration_db",
        port=4000,
        ssl_verify_cert=False,
        connection_timeout=30
    )

@app.route("/")
def home():
    return "Backend Running Successfully 🚀"

@app.route("/register", methods=["POST"])
def register():
    db = None
    cursor = None

    try:
        data = request.get_json()

        db = get_db()
        cursor = db.cursor()

        name = data["name"]
        email = data["email"]
        phone = data["phone"]

        cursor.execute(
            "SELECT id FROM users WHERE email=%s",
            (email,)
        )

        if cursor.fetchone():
            return jsonify({
                "success": False,
                "message": "Email already exists"
            })

        cursor.execute(
            "SELECT id FROM users WHERE phone=%s",
            (phone,)
        )

        if cursor.fetchone():
            return jsonify({
                "success": False,
                "message": "Phone already exists"
            })

        cursor.execute(
            "INSERT INTO users(name,email,phone) VALUES(%s,%s,%s)",
            (name,email,phone)
        )

        db.commit()

        return jsonify({
            "success": True,
            "message": "Registration Successful"
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }),500

    finally:
        if cursor:
            cursor.close()
        if db and db.is_connected():
            db.close()

if __name__ == "__main__":
    port=int(os.environ.get("PORT",5000))
    app.run(host="0.0.0.0",port=port)