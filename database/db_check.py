
import sqlite3
import os

def check_db():
    db = 'app.db' # Correct path now
    if not os.path.exists(db):
        print(f"Error: {db} not found!")
        return
    
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [t[0] for t in cursor.fetchall()]
    print(f"Tables found: {tables}")
    
    for table in tables:
        cursor.execute(f"PRAGMA table_info({table})")
        columns = cursor.fetchall()
        print(f"Columns in {table}: {[c[1] for c in columns]}")
    
    conn.close()

if __name__ == "__main__":
    check_db()
