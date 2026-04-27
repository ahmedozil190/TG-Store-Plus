import asyncio
from database.engine import async_session
from database.models import Transaction, Account, AccountStatus
from sqlalchemy import select

async def check():
    async with async_session() as s:
        txs = (await s.execute(select(Transaction).order_by(Transaction.id.desc()).limit(5))).scalars().all()
        print('Recent Transactions:')
        for t in txs:
            print(f" - ID: {t.id}, User: {t.user_id}, Type: {t.type}, Amount: {t.amount}")
            
        accs = (await s.execute(select(Account).order_by(Account.id.desc()).limit(5))).scalars().all()
        print('\nRecent Accounts:')
        for a in accs:
            print(f" - ID: {a.id}, Phone: {a.phone_number}, Status: {a.status}, Buyer: {a.buyer_id}")

if __name__ == "__main__":
    asyncio.run(check())
