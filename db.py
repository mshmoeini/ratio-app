

import psycopg2


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