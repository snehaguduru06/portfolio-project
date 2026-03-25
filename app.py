from flask import Flask, render_template, request
import psycopg2 # Use psycopg2 for Render Postgres
import os

app = Flask(__name__)

def get_db_connection():
    # This pulls the 'Internal Connection String' from your Render Postgres settings
    db_url = os.environ.get('DATABASE_URL')
    return psycopg2.connect(db_url)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/contact", methods=["POST"])
def contact():
    name = request.form.get("name")
    email = request.form.get("email")
    message = request.form.get("message")

    conn = get_db_connection()
    cur = conn.cursor()
    # Postgres uses %s for placeholders
    cur.execute("INSERT INTO messages (name, email, message) VALUES (%s, %s, %s)",
                (name, email, message))
    conn.commit()
    cur.close()
    conn.close()
    return "Message saved successfully"

if __name__ == "__main__":
    # Safety check for the Port to prevent the 'NoneType' error
    port = int(os.environ.get("PORT", 10000)) 
    app.run(host='0.0.0.0', port=port)
