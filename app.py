from flask import Flask, request, render_template
import psycopg2

init_db()

app = Flask(__name__)

def get_connection():
    return psycopg2.connect(
        dbname="ratios",
        user="appuser",
        password="StrongPassword123",
        host="34.27.28.193", 
        port="5432"
    )

def init_db():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS ratios (
            id SERIAL PRIMARY KEY,
            num1 FLOAT,
            num2 FLOAT,
            result FLOAT,
            timestamp TIMESTAMP DEFAULT NOW()
        )
    """)
    conn.commit()
    conn.close()

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        num1 = float(request.form["num1"])
        num2 = float(request.form["num2"])
        result = (num2 / num1) * 100

        conn = get_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO ratios (num1, num2, result) VALUES (%s, %s, %s)", (num1, num2, result))
        conn.commit()
        cur.close()
        conn.close()

    # Table
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT num1, num2, result, timestamp FROM ratios ORDER BY timestamp DESC LIMIT 10")
    records = cur.fetchall()
    cur.close()
    conn.close()

    return render_template("index.html", result=result, records=records)

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)
