import os
import shutil
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from database.models import Base
from config import DATABASE_URL

# Auto-migrate local DB to persistent volume if needed
if os.path.exists("/data") and not os.path.exists("/data/app.db"):
    if os.path.exists("app.db"):
        try:
            shutil.copy2("app.db", "/data/app.db")
            print("Successfully migrated app.db to /data/app.db")
        except Exception as e:
            print(f"Migration failed: {e}")

engine = create_async_engine(DATABASE_URL, echo=False)
async_session = sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)

from sqlalchemy import text

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
        # Auto-migration: Check if transaction_id exists in withdrawal_requests
        try:
            # Check existing columns
            def check_columns(connection):
                cursor = connection.execute(text("PRAGMA table_info(withdrawal_requests)"))
                return [row[1] for row in cursor]
            
            columns = await conn.run_sync(check_columns)
            if 'transaction_id' not in columns:
                await conn.execute(text("ALTER TABLE withdrawal_requests ADD COLUMN transaction_id VARCHAR(12)"))
                print("Successfully added transaction_id column to withdrawal_requests")
        except Exception as e:
            print(f"Migration check failed or not needed: {e}")
