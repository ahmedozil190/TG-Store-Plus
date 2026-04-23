import asyncio
from sqlalchemy.future import select
from database.engine import async_session
from database.models import UserCountryPrice, CountryPrice

async def check():
    target_user = 6841123943
    async with async_session() as session:
        print(f"--- Checking UserCountryPrice for {target_user} ---")
        res = await session.execute(select(UserCountryPrice).where(UserCountryPrice.user_id == target_user))
        rows = res.scalars().all()
        for r in rows:
            print(f"User: {r.user_id}, Code: {r.country_code}, ISO: {r.iso_code}, Price: {r.buy_price}")
        
        print(f"\n--- Checking CountryPrice Table ---")
        res2 = await session.execute(select(CountryPrice))
        rows2 = res2.scalars().all()
        for r in rows2:
            print(f"Code: {r.country_code}, ISO: {r.iso_code}, BuyPrice: {r.buy_price}")

if __name__ == "__main__":
    asyncio.run(check())
