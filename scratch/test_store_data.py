import asyncio
import logging
from web_admin import get_store_data
from database.engine import init_db

async def test():
    logging.basicConfig(level=logging.INFO)
    await init_db()
    try:
        data = await get_store_data()
        print("\n--- STORE DATA RESULT ---")
        print(f"Countries count: {len(data['countries'])}")
        for c in data['countries'][:5]:
            print(f"- {c['name']}: {c['count']} @ {c['buy_price']}")
    except Exception as e:
        print(f"FAILED: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test())
