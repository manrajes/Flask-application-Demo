import os
from flask import Flask, jsonify
import psycopg2

app = Flask(__name__)

def get_db_connection():
    # Environment variables will be injected by Kubernetes
    conn = psycopg2.connect(
        host=os.getenv('DATABASE_HOST', 'my-postgres-postgresql'),
        database=os.getenv('DATABASE_NAME', 'postgres'),
        user=os.getenv('DATABASE_USER', 'postgres'),
        password=os.getenv('DATABASE_PASSWORD')
    )
    return conn

@app.route('/')
def index():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT version();')
        db_version = cur.fetchone()
        cur.close()
        conn.close()
        return jsonify({"status": "Connected!", "database_version": db_version[0]})
    except Exception as e:
        return jsonify({"status": "Database Connection Failed", "error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)