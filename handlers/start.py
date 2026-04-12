from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from sqlalchemy.future import select
from database.models import User
from database.engine import async_session
from keyboards.client import main_keyboard

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    user_id = message.from_user.id
    
    async with async_session() as session:
        stmt = select(User).where(User.id == user_id)
        result = await session.execute(stmt)
        user = result.scalar_one_or_none()
        
        full_name = f"{message.from_user.first_name or ''} {message.from_user.last_name or ''}".strip() or None
        tg_username = message.from_user.username or None
        
        if not user:
            user = User(id=user_id, balance=0.0, full_name=full_name, username=tg_username)
            session.add(user)
        else:
            # Update name/username if it changed
            if full_name: user.full_name = full_name
            if tg_username: user.username = tg_username
            
        await session.commit()
            
    await message.answer(
        "- The main list.\n\n"
        f"- Your balance:{int(user.balance) if user.balance == 0 else user.balance}$ .\n"
        f"- Hands of your account:<code>{user.id}</code> .\n"
        "Official Bot Channel:@MOOO8O .\n"
        "Gover the bot through the buttons below.",
        reply_markup=main_keyboard(),
        parse_mode="HTML"
    )
