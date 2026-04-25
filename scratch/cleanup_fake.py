
import asyncio
import aiosqlite
import os

async def cleanup_fake_data():
    db_path = "app.db"
    if not os.path.exists(db_path):
        return

    async with aiosqlite.connect(db_path) as db:
        print("Cleaning up fake data from accounts table...")
        # Delete accounts with our dummy session strings
        await db.execute("DELETE FROM accounts WHERE session_string LIKE 'SEED_%' OR session_string = 'DUMMY_SESSION_STRING' OR session_string = 'SEED_DUMMY_SESSION'")
        await db.commit()
        print("Cleanup complete.")

if __name__ == "__main__":
    asyncio.run(cleanup_fake_data())
