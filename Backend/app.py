from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
import os

app = Flask(__name__)

# Enable CORS
CORS(
    app,
    resources={r"/*": {"origins": "*"}},
    supports_credentials=True
)


# ===============================
# Database Connection Function
# ===============================

def get_db_connection():
    return mysql.connector.connect(
        host="gateway01.ap-southeast-1.prod.aws.tidbcloud.com",
        user="VhVBHqfkiAdJRDU.root",
        password="trcsQfVz4Vkmb7hV",   # Apna password yaha dal
        database="registration_db",
        port=4000,
        ssl_disabled=False,
        autocommit=True
    )


# ===============================
# Register API
# ===============================

@app.route("/register", methods=["POST", "OPTIONS"])
def register():

    if request.method == "OPTIONS":
        return "", 200

    db = None
    cursor = None

    try:

        data = request.get_json()

        name = data.get("name")
        email = data.get("email")
        phone = data.get("phone")

        db = get_db_connection()
        cursor = db.cursor()

        # Duplicate Email Check
        cursor.execute(
            "SELECT * FROM users WHERE email=%s",
            (email,)
        )

        if cursor.fetchone():
            return jsonify({
                "success": False,
                "message": "Email already exists."
            })

        # Duplicate Phone Check
        cursor.execute(
            "SELECT * FROM users WHERE phone=%s",
            (phone,)
        )

        if cursor.fetchone():
            return jsonify({
                "success": False,
                "message": "Phone number already exists."
            })

        # Insert Data
        cursor.execute(
            "INSERT INTO users(name,email,phone) VALUES(%s,%s,%s)",
            (name, email, phone)
        )

        return jsonify({
            "success": True,
            "message": "Registration Successful"
        })

    except Exception as e:

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500

    finally:

        if cursor:
            cursor.close()

        if db:
            db.close()


# ===============================
# Home Route
# ===============================

@app.route("/")
def home():
    return "Backend Running Successfully 🚀"


# ===============================
# Run Server
# ===============================

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)