from flask import Flask, render_template, request
from db import get_connection, init_db
from google.cloud import storage, secretmanager
import os
from datetime import datetime

app = Flask(__name__)


def get_credentials_from_secret():
    client = secretmanager.SecretManagerServiceClient()
    name = "projects/msh-cloud-project/secrets/gcp-sa-ratioapp/versions/latest"
    response = client.access_secret_version(request={"name": name})
    return response.payload.data.decode("UTF-8")


with open("credentials.json", "w") as f:
    f.write(get_credentials_from_secret())


os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "credentials.json"


init_db()

def upload_to_bucket(data):
    bucket_name = "ratio-app-storage-bucket"
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    
    filename = f"log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    blob = bucket.blob(filename)
    
    blob.upload_from_string(data)
    print(f"Uploaded {filename} to bucket {bucket_name}")

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

        log_data = f"Inputs: {num1}, {num2} | Ratio: {result}\n"
        upload_to_bucket(log_data)

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM ratios ORDER BY timestamp DESC LIMIT 10")
    history = cur.fetchall()
    conn.close()

    return render_template("index.html", result=result, num1=num1, num2=num2, history=history)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
