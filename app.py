from flask import Flask, render_template, request
import psycopg2
import os
from urllib.parse import urlparse

app = Flask(__name__)

def get_db_connection():
    # Render provides 'DATABASE_URL' automatically
    db_url = os.environ.get('DATABASE_URL')
    
    # If we are on Render, use the URL; otherwise, use local settings
    if db_url:
        return psycopg2.connect(db_url)
    else:
        # This is for your local testing (replace with your local postgres details if needed)
        return psycopg2.connect(
            host="localhost",
            database="portfolio_db",
            user="postgres",
            password="your_password"
        )

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/contact", methods=["POST"])
def contact():
    name = request.form["name"]
    email = request.form["email"]
    message = request.form["message"]

    conn = get_db_connection()
    cur = conn.cursor()
    # Postgres uses %s just like MySQL
    cur.execute("INSERT INTO messages (name, email, message) VALUES (%s, %s, %s)",
                (name, email, message))
    conn.commit()
    cur.close()
    conn.close()
    return "Message saved successfully"

@app.route("/messages")
def messages():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM messages")
    data = cur.fetchall()
    cur.close()
    conn.close()
    return render_template("messages.html", messages=data)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
