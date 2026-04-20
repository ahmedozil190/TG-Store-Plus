
import sqlite3
import os

def migrate():
    db = 'app.db'
    if not os.path.exists(db):
        print(f"Error: {db} not found!")
        return
    
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    
    # 1. Create country_prices if not exists
    print("Creating country_prices table...")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS country_prices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            country_code TEXT UNIQUE NOT NULL,
            country_name TEXT NOT NULL,
            price REAL NOT NULL DEFAULT 1.0,
            buy_price REAL NOT NULL DEFAULT 0.5,
            approve_delay INTEGER NOT NULL DEFAULT 0,
            is_active_store BOOLEAN NOT NULL DEFAULT 1,
            is_active_sourcing BOOLEAN NOT NULL DEFAULT 1,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # 2. Add isolation/ban flags to users if missing
    cursor.execute("PRAGMA table_info(users)")
    user_cols = [c[1] for c in cursor.fetchall()]
    print(f"User columns before: {user_cols}")

    for flag in ['is_banned_store', 'is_banned_sourcing']:
        if flag not in user_cols:
            print(f"Adding {flag} to users...")
            cursor.execute(f"ALTER TABLE users ADD COLUMN {flag} BOOLEAN DEFAULT 0")

    # 3. Seed some default countries if table is empty
    cursor.execute("SELECT COUNT(*) FROM country_prices")
    count = cursor.fetchone()[0]
    if count == 0:
        print("Seeding default countries...")
        defaults = [
            ("20", "Egypt", 1.5, 0.7, 0, 1, 1),
            ("1", "USA", 2.0, 1.0, 0, 1, 1),
            ("44", "UK", 1.8, 0.9, 0, 1, 1),
            ("966", "Saudi Arabia", 2.2, 1.1, 0, 1, 1),
            ("971", "UAE", 2.5, 1.25, 0, 1, 1)
        ]
        cursor.executemany("""
            INSERT INTO country_prices (country_code, country_name, price, buy_price, approve_delay, is_active_store, is_active_sourcing)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, defaults)

    # 4. Cleanup users table (Optional, but good for health)
    # We remove is_active_store/sourcing from users if they exist
    if 'is_active_store' in user_cols or 'is_active_sourcing' in user_cols:
        print("Cleaning up users table columns...")
        # SQLite doesn't support DROP COLUMN well in all versions, we'll keep them but they'll be ignored by the model
        pass

    conn.commit()
    conn.close()
    print("Migration V2 complete!")

if __name__ == "__main__":
    migrate()
