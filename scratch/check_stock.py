import asyncio
from sqlalchemy import select, func
from database.engine import async_session
from database.models import Account, AccountStatus

async def test():
    async with async_session() as session:
        count = (await session.execute(select(func.count(Account.id)).where(Account.status == AccountStatus.AVAILABLE))).scalar()
        print(f"\nTotal AVAILABLE accounts: {count}")
        
        local_count = (await session.execute(select(func.count(Account.id)).where(Account.status == AccountStatus.AVAILABLE, Account.server_id == None))).scalar()
        print(f"Local AVAILABLE accounts: {local_count}")

if __name__ == "__main__":
    asyncio.run(test())
