import sqlite3

DB_PATH = 'database.db'
  # Ensure path is correct

def init_db():
    """Creates the database and sets the initial driver score."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS driver_score (
            id INTEGER PRIMARY KEY,
            score INTEGER
        )
    ''')
    cursor.execute('SELECT COUNT(*) FROM driver_score')
    if cursor.fetchone()[0] == 0:
        cursor.execute('INSERT INTO driver_score (score) VALUES (?)', (100,))
    conn.commit()
    conn.close()

def get_score():
    """Returns the current driver score."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT score FROM driver_score WHERE id=1')
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else 0

def update_score(deduction):
    """Deducts points from the driver score."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    current_score = get_score()
    new_score = max(current_score - deduction, 0)  # Prevent negative scores
    cursor.execute('UPDATE driver_score SET score = ? WHERE id=1', (new_score,))
    conn.commit()
    conn.close()
    print(f"Updated Score: {new_score}")

if __name__ == "__main__":
    init_db()
    print("Database initialized. Current score:", get_score())
