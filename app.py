import os
import psycopg2
from flask import Flask, render_template, request

app = Flask(__name__)

def get_db_connection():
    database_url = os.environ.get('DATABASE_URL')
    return psycopg2.connect(database_url,sslmode='require')

# THIS PART IS NEW - It builds the table for you!
def create_table():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255),
            email VARCHAR(255),
            message TEXT
        );
    ''')
    conn.commit()
    cur.close()
    conn.close()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/contact", methods=["POST"])
def contact():
    name = request.form.get("name")
    email = request.form.get("email")
    message = request.form.get("message")

    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # 1. Force create the table right before saving
        cur.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255),
                email VARCHAR(255),
                message TEXT
            );
        ''')
        
        # 2. Now save the message
        cur.execute("INSERT INTO messages (name, email, message) VALUES (%s, %s, %s)",
                    (name, email, message))
        
        conn.commit()
        cur.close()
        conn.close()
        return "Message saved successfully!"
    except Exception as e:
        return f"Database Error: {e}"
if __name__ == "__main__":
    # This block creates the table automatically
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255),
                email VARCHAR(255),
                message TEXT
            );
        ''')
        conn.commit()
        cur.close()
        conn.close()
        print("Table created successfully!")
    except Exception as e:
        print(f"Database error: {e}")

    # This starts your website
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
