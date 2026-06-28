from flask import Flask, render_template, request
import mysql.connector
import os

app = Flask(__name__)

db = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    port=int(os.getenv("DB_PORT")),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
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