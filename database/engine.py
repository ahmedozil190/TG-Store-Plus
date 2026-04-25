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
        
        # Auto-migration: Check columns for various tables
        try:
            # 1. withdrawal_requests.transaction_id
            def check_withdraw_cols(connection):
                cursor = connection.execute(text("PRAGMA table_info(withdrawal_requests)"))
                return [row[1] for row in cursor]
            
            w_cols = await conn.run_sync(check_withdraw_cols)
            if 'transaction_id' not in w_cols:
                await conn.execute(text("ALTER TABLE withdrawal_requests ADD COLUMN transaction_id VARCHAR(12)"))
                print("Successfully added transaction_id column to withdrawal_requests")
            
            # 2. deposits.method
            def check_deposit_cols(connection):
                cursor = connection.execute(text("PRAGMA table_info(deposits)"))
                return [row[1] for row in cursor]
            
            d_cols = await conn.run_sync(check_deposit_cols)
            if 'method' not in d_cols:
                await conn.execute(text("ALTER TABLE deposits ADD COLUMN method VARCHAR(50)"))
                print("Successfully added method column to deposits")
                
        except Exception as e:
            print(f"Migration check failed: {e}")
