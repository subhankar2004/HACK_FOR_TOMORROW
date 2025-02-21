from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

DB_PATH = '../driver_score/database.db'

def get_score():
    """Fetch the latest driver score."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT score FROM driver_score WHERE id=1')
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else 0

@app.route('/')
def index():
    score = get_score()
    return render_template('index.html', score=score)

if __name__ == '__main__':
    app.run(debug=True)
