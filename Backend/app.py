from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)

# ===============================
# TiDB Cloud Database Connection
# ===============================

db = mysql.connector.connect(
    host="gateway01.ap-southeast-1.prod.aws.tidbcloud.com",
    user="VhVBHqfkiAdJRDU.root",
    password="trcsQfVz4Vkmb7hV",
    database="registration_db",
    port=4000
)

cursor = db.cursor()


# ===============================
# Register API
# ===============================

@app.route("/register", methods=["POST"])
def register():

    data = request.get_json()

    name = data.get("name")
    email = data.get("email")
    phone = data.get("phone")

    # Check duplicate email
    cursor.execute(
        "SELECT * FROM users WHERE email=%s",
        (email,)
    )

    if cursor.fetchone():
        return jsonify({
            "success": False,
            "message": "Email already exists."
        })

    # Check duplicate phone
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
    sql = """
    INSERT INTO users(name,email,phone)
    VALUES(%s,%s,%s)
    """

    values = (name, email, phone)

    cursor.execute(sql, values)

    db.commit()

    return jsonify({
        "success": True,
        "message": "Registration Successful"
    })


# ===============================
# Run Server
# ===============================

if __name__ == "__main__":
    app.run(debug=True)