from flask import Flask, render_template, request
import mysql.connector
import os # New: needed to read cloud settings

app = Flask(__name__)

# This function connects to the database using Railway's environment variables
def get_db_connection():
    return mysql.connector.connect(
        host=os.environ.get('MYSQLHOST'),
        user=os.environ.get('MYSQLUSER'),
        password=os.environ.get('MYSQLPASSWORD'),
        database=os.environ.get('MYSQLDATABASE'),
        port=int(os.environ.get('MYSQLPORT', 3306))
    )

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/contact", methods=["POST"])
def contact():
    name = request.form["name"]
    email = request.form["email"]
    message = request.form["message"]

    # Open connection, save data, then close
    db = get_db_connection()
    cursor = db.cursor()
    sql = "INSERT INTO messages (name, email, message) VALUES (%s, %s, %s)"
    cursor.execute(sql, (name, email, message))
    db.commit()
    cursor.close()
    db.close()

    return "Message saved successfully"

@app.route("/messages")
def messages():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM messages")
    data = cursor.fetchall()
    cursor.close()
    db.close()
    return render_template("messages.html", messages=data)

if __name__ == "__main__":
    # In cloud, port is usually provided by the platform
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
