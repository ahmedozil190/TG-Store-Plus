import sqlite3
import os

db_path = r"d:\9- My Projects\6- Numbers Store Bot\app.db"

if not os.path.exists(db_path):
    print(f"Error: {db_path} not found.")
    exit(1)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

try:
    print("Starting migration...")
    
    # 1. Rename existing table
    cursor.execute("ALTER TABLE country_prices RENAME TO country_prices_old")
    
    # 2. Create new table with iso_code and without the UNIQUE constraint on country_code
    cursor.execute("""
    CREATE TABLE country_prices (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        country_code TEXT NOT NULL,
        iso_code TEXT DEFAULT 'XX',
        country_name TEXT NOT NULL,
        price FLOAT NOT NULL DEFAULT 1.0,
        buy_price FLOAT NOT NULL DEFAULT 0.5,
        approve_delay INTEGER NOT NULL DEFAULT 0,
        updated_at DATETIME
    )
    """)
    
    # 3. Copy data
    cursor.execute("""
    INSERT INTO country_prices (id, country_code, iso_code, country_name, price, buy_price, approve_delay, updated_at)
    SELECT id, country_code, 'XX', country_name, price, buy_price, approve_delay, updated_at FROM country_prices_old
    """)
    
    # 4. Drop old table
    cursor.execute("DROP TABLE country_prices_old")
    
    # 5. Create composite index for performance and logical uniqueness
    cursor.execute("CREATE UNIQUE INDEX idx_country_iso ON country_prices(country_code, iso_code)")
    
    conn.commit()
    print("Migration successful: Table recreated with iso_code and composite index.")

except Exception as e:
    conn.rollback()
    print(f"Migration failed: {e}")
finally:
    conn.close()
