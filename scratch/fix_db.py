
import sqlite3
import os

db_path = "app.db"

def fix():
    if not os.path.exists(db_path):
        print(f"Database {db_path} not found.")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Add referred_by to users
    try:
        cursor.execute("ALTER TABLE users ADD COLUMN referred_by INTEGER")
        print("Added referred_by column.")
    except sqlite3.OperationalError as e:
        print(f"referred_by: {e}")

    # Add referral_earnings to users
    try:
        cursor.execute("ALTER TABLE users ADD COLUMN referral_earnings FLOAT DEFAULT 0.0")
        print("Added referral_earnings column.")
    except sqlite3.OperationalError as e:
        print(f"referral_earnings: {e}")

    conn.commit()
    conn.close()
    print("Done.")

if __name__ == "__main__":
    fix()
