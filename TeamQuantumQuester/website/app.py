'''from flask import Flask, render_template
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
    app.run(debug=True)'''
from flask import Flask, render_template, request, redirect, url_for
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

# Route for Home Page (Driver Score Dashboard)
@app.route('/')
def index():
    score = get_score()
    return render_template('index.html', score=score)

# Route for Driver Profile (Demo: Manual Entry)
@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if request.method == 'POST':
        # Process the submitted driver profile info
        name = request.form.get('name')
        age = request.form.get('age')
        license_no = request.form.get('license_no')
        # In a real application, you'd store these details in a database.
        # For demo, we simply pass them back to the template.
        return render_template('profile.html', name=name, age=age, license_no=license_no, submitted=True)
    return render_template('profile.html', submitted=False)

# Route for Subscription Plans Demo Page
@app.route('/subscription')
def subscription():
    return render_template('subscription.html')

if __name__ == '__main__':
    app.run(debug=True)
