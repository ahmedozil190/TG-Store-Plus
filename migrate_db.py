import asyncio
from sqlalchemy import text
from database.engine import engine

async def migrate():
    async with engine.begin() as conn:
        try:
            await conn.execute(text("ALTER TABLE deposits ADD COLUMN method VARCHAR(50)"))
            print("Successfully added 'method' column to 'deposits' table.")
        except Exception as e:
            print(f"Migration failed or column already exists: {e}")

if __name__ == "__main__":
    asyncio.run(migrate())
