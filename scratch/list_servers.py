import asyncio
import logging
from sqlalchemy import select
from database.engine import async_session
from database.models import ApiServer

async def test():
    async with async_session() as session:
        servers = (await session.execute(select(ApiServer))).scalars().all()
        print("\n--- API SERVERS IN DB ---")
        print(f"Total: {len(servers)}")
        for s in servers:
            print(f"- {s.name} (Active: {s.is_active}) ID: {s.id}")

if __name__ == "__main__":
    asyncio.run(test())
