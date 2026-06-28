from flask import Flask, render_template, request
import mysql.connector
import os

app = Flask(__name__)

# Database connection function
def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT")),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

# Home page
@app.route("/")
def home():
    return render_template("index.html")

# Register route
@app.route("/register", methods=["POST"])
def register():

    # Form data
    name = request.form["name"]
    email = request.form["email"]
    phone = request.form["phone"]

    # New DB connection
    db = get_db_connection()
    cursor = db.cursor()

    # Insert query
    cursor.execute(
        "INSERT INTO users(name, email, phone) VALUES(%s, %s, %s)",
        (name, email, phone)
    )

    # Save changes
    db.commit()

    # Close connection
    cursor.close()
    db.close()

    return "Registration Successful"

# Run app
if __name__ == "__main__":
    app.run(debug=True)