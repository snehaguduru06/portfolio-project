from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="sneha",
    database="portfolio_db"
)

cursor = db.cursor(dictionary=True)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/contact", methods=["POST"])
def contact():
    name = request.form["name"]
    email = request.form["email"]
    message = request.form["message"]

    sql = "INSERT INTO messages (name, email, message) VALUES (%s, %s, %s)"
    cursor.execute(sql, (name, email, message))
    db.commit()

    return "Message saved successfully"

@app.route("/messages")
def messages():
    cursor.execute("SELECT * FROM messages")
    data = cursor.fetchall()
    return render_template("messages.html", messages=data)

if __name__ == "__main__":
    app.run(debug=True)
