from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from config import SELLER_URL, STORE_URL

def main_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🛒 Open Store | فتح المتجر", web_app=WebAppInfo(url=STORE_URL))
        ]
    ])

def profile_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="➕ شحن الرصيد", callback_data="deposit")],
        [InlineKeyboardButton(text="الرجوع 🔙", callback_data="back_main")]
    ])

def sell_menu_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="- Selling an account.", url="https://t.me/MOOO8O")],
        [InlineKeyboardButton(text="Account prices.", callback_data="sell_prices")],
        [InlineKeyboardButton(text="- Pull my balance.", callback_data="pull_balance")],
        [InlineKeyboardButton(text="Prices channel", url="https://t.me/MOOO8O")],
        [InlineKeyboardButton(text="- Return.", callback_data="back_main")]
    ])
