
import asyncio
from database.engine import engine, DATABASE_URL
from sqlalchemy import text

async def check():
    print(f"DATABASE_URL: {DATABASE_URL}")
    async with engine.connect() as conn:
        res = await conn.execute(text("PRAGMA table_info(users)"))
        columns = res.fetchall()
        print("Columns in 'users' table:")
        for col in columns:
            print(f" - {col[1]}")

if __name__ == "__main__":
    asyncio.run(check())
