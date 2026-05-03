import asyncio
from database.engine import async_session
from database.models import Account, AccountStatus
from sqlalchemy import select, func

async def main():
    async with async_session() as s:
        # Check sold accounts
        count = await s.scalar(select(func.count(Account.id)).where(Account.status == AccountStatus.SOLD))
        print(f"Total SOLD accounts in DB: {count}")
        
        # Check all statuses
        results = await s.execute(select(Account.status, func.count(Account.id)).group_by(Account.status))
        for row in results:
            print(f"Status {row[0]}: {row[1]}")

asyncio.run(main())
