import asyncio
from sqlalchemy.future import select
from database.engine import async_session
from database.models import UserCountryPrice

async def check():
    async with async_session() as session:
        res = await session.execute(select(UserCountryPrice))
        rows = res.scalars().all()
        print(f"Total Rows: {len(rows)}")
        for r in rows:
            print(f"ID: {r.id}, User: {r.user_id}, Code: {r.country_code}, ISO: {r.iso_code}, Price: {r.buy_price}")

if __name__ == "__main__":
    asyncio.run(check())
