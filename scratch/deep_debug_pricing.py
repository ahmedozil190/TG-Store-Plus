import asyncio
import phonenumbers
from sqlalchemy.future import select
from database.engine import async_session
from database.models import CountryPrice, UserCountryPrice

async def debug_detection(phone, user_id=0):
    print(f"\n--- Debugging Phone: {phone} (User: {user_id}) ---")
    try:
        phone_p = phone if phone.startswith('+') else f"+{phone}"
        parsed = phonenumbers.parse(phone_p)
        cc = str(parsed.country_code)
        target_iso = phonenumbers.region_code_for_number(parsed) or 'XX'
        print(f"Parsed CC: {cc}, ISO: {target_iso}")
        
        async with async_session() as session:
            # Check Global
            stmt = select(CountryPrice).where(CountryPrice.country_code.like(f"%{cc}%"))
            rows = (await session.execute(stmt)).scalars().all()
            print(f"Global matches for code {cc}:")
            for r in rows:
                print(f"  - DB Code: '{r.country_code}', DB ISO: '{r.iso_code}', BuyPrice: {r.buy_price}")
            
            # Check User
            if user_id > 0:
                stmt2 = select(UserCountryPrice).where(UserCountryPrice.user_id == user_id, UserCountryPrice.country_code.like(f"%{cc}%"))
                rows2 = (await session.execute(stmt2)).scalars().all()
                print(f"User matches for code {cc}:")
                for r in rows2:
                    print(f"  - DB Code: '{r.country_code}', DB ISO: '{r.iso_code}', BuyPrice: {r.buy_price}")

    except Exception as e:
        print(f"Error: {e}")

async def run():
    # Test cases for the user's problematic countries
    await debug_detection("+393241234567") # Italy
    await debug_detection("+212612345678") # Morocco
    await debug_detection("+14155552671")  # US for comparison

if __name__ == "__main__":
    asyncio.run(run())
