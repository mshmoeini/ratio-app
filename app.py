from flask import Flask, render_template, request
from db import get_connection, init_db

init_db()

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    num1 = num2 = 0
    if request.method == "POST":
        num1 = float(request.form["num1"])
        num2 = float(request.form["num2"])
        result = round((num2 / num1) * 100, 2)
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO ratios (num1, num2, result) VALUES (%s, %s, %s)", (num1, num2, result))
        conn.commit()
        conn.close()

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM ratios ORDER BY timestamp DESC LIMIT 10")
    history = cur.fetchall()
    conn.close()
    return render_template("index.html", result=result, num1=num1, num2=num2, history=history)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
