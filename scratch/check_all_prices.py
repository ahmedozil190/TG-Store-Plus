import asyncio
from sqlalchemy.future import select
from database.engine import async_session
from database.models import CountryPrice

async def check():
    async with async_session() as session:
        print("--- All Country Prices in DB ---")
        res = await session.execute(select(CountryPrice))
        rows = res.scalars().all()
        for r in rows:
            print(f"Code: '{r.country_code}', ISO: '{r.iso_code}', Name: '{r.country_name}', BuyPrice: {r.buy_price}")

if __name__ == "__main__":
    asyncio.run(check())
