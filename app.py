from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

db = mysql.connector.connect(
    host="gateway01.ap-southeast-1.prod.aws.tidbcloud.com",
    port=4000,
    user="VhVBHqfkiAdJRDU.root",
    password="trcsQfVz4Vkmb7hV",
    database="registration_db"
)

cursor = db.cursor()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/register", methods=["POST"])
def register():
    name = request.form["name"]
    email = request.form["email"]
    phone = request.form["phone"]

    cursor.execute(
        "INSERT INTO users(name,email,phone) VALUES (%s,%s,%s)",
        (name, email, phone)
    )

    db.commit()

    return "Registration Successful ✔"

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)