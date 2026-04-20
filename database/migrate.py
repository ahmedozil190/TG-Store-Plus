
import sqlite3
import os

db_path = r'd:\9- My Projects\6- Numbers Store Bot\database\store.db'

def setup():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Check country_prices columns
    cursor.execute("PRAGMA table_info(country_prices)")
    cols = [c[1] for c in cursor.fetchall()]
    print(f"country_prices columns: {cols}")
    
    if 'is_active_store' not in cols:
        print("Adding is_active_store to country_prices")
        cursor.execute("ALTER TABLE country_prices ADD COLUMN is_active_store BOOLEAN DEFAULT 1")
    if 'is_active_sourcing' not in cols:
        print("Adding is_active_sourcing to country_prices")
        cursor.execute("ALTER TABLE country_prices ADD COLUMN is_active_sourcing BOOLEAN DEFAULT 1")

    # Check users columns
    cursor.execute("PRAGMA table_info(users)")
    cols = [c[1] for c in cursor.fetchall()]
    print(f"users columns: {cols}")
    
    if 'is_banned_store' not in cols:
        print("Adding is_banned_store to users")
        cursor.execute("ALTER TABLE users ADD COLUMN is_banned_store BOOLEAN DEFAULT 0")
    if 'is_banned_sourcing' not in cols:
        print("Adding is_banned_sourcing to users")
        cursor.execute("ALTER TABLE users ADD COLUMN is_banned_sourcing BOOLEAN DEFAULT 0")
    
    # Update existing logic to ensure they have default values if null
    cursor.execute("UPDATE country_prices SET is_active_store = 1 WHERE is_active_store IS NULL")
    cursor.execute("UPDATE country_prices SET is_active_sourcing = 1 WHERE is_active_sourcing IS NULL")
    cursor.execute("UPDATE users SET is_banned_store = 0 WHERE is_banned_store IS NULL")
    cursor.execute("UPDATE users SET is_banned_sourcing = 0 WHERE is_banned_sourcing IS NULL")

    conn.commit()
    conn.close()
    print("Migration complete!")

if __name__ == "__main__":
    setup()
