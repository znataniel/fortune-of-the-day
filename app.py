import sqlite3
import random
from flask import Flask, render_template, request, jsonify

def create_app():
    app = Flask(__name__)

    with app.app_context():
        # Initialize DB here
        init_db()

    return app

app = create_app()

DATABASE = 'fortunes.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute('CREATE TABLE IF NOT EXISTS fortunes (id INTEGER PRIMARY KEY AUTOINCREMENT, text TEXT NOT NULL)')
    
    # Seed with some initial fortunes if empty
    cursor = conn.cursor()
    cursor.execute('SELECT count(*) FROM fortunes')
    if cursor.fetchone()[0] == 0:
        initial_fortunes = [
            "Your talents will be recognized and suitably rewarded.",
            "A small house will soon be filled with happiness.",
            "Believe in yourself and others will too.",
            "Good news will be brought to you by mail.",
            "Patience is a virtue, but persistence is a power."
        ]
        conn.executemany('INSERT INTO fortunes (text) VALUES (?)', [(f,) for f in initial_fortunes])
    
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/fortune', methods=['GET'])
def get_fortune():
    conn = get_db_connection()
    fortunes = conn.execute('SELECT text FROM fortunes').fetchall()
    conn.close()
    if not fortunes:
        return jsonify({"fortune": "No fortunes found!"})
    return jsonify({"fortune": random.choice(fortunes)['text']})

@app.route('/api/fortune', methods=['POST'])
def add_fortune():
    data = request.get_json()
    new_fortune = data.get('fortune')
    if not new_fortune:
        return jsonify({"error": "Fortune text is required"}), 400
    
    conn = get_db_connection()
    conn.execute('INSERT INTO fortunes (text) VALUES (?)', (new_fortune,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Fortune added successfully!"}), 201

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
