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

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
