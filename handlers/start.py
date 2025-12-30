from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from database.db_manager import DBManager

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    user = await DBManager.get_user(message.from_user.id)
    if not user:
        await DBManager.create_user(message.from_user.id, message.from_user.username)
        user = await DBManager.get_user(message.from_user.id)

    welcome_text = (
        f"👋 Welcome {message.from_user.full_name} to **Tawana Telecom** (TTC)!\n\n"
        f"💰 Your Balance: `{user.balance:.2f}`\n"
        "Use the menu below to buy a virtual number for your favorite services."
    )
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📱 Buy Number", callback_data="buy_number")],
        [InlineKeyboardButton(text="👤 My Profile", callback_data="profile"), 
         InlineKeyboardButton(text="⏳ Active Orders", callback_data="active_orders")],
        [InlineKeyboardButton(text="💳 Add Funds", callback_data="add_funds"),
         InlineKeyboardButton(text="ℹ️ Support", callback_data="support")]
    ])
    
    await message.answer(welcome_text, reply_markup=keyboard, parse_mode="Markdown")

@router.callback_query(F.data == "main_menu")
async def back_to_main(callback):
    user = await DBManager.get_user(callback.from_user.id)
    welcome_text = (
        f"👋 Welcome back to **Tawana Telecom**!\n\n"
        f"💰 Your Balance: `{user.balance:.2f}`"
    )
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📱 Buy Number", callback_data="buy_number")],
        [InlineKeyboardButton(text="👤 My Profile", callback_data="profile"), 
         InlineKeyboardButton(text="⏳ Active Orders", callback_data="active_orders")],
        [InlineKeyboardButton(text="💳 Add Funds", callback_data="add_funds"),
         InlineKeyboardButton(text="ℹ️ Support", callback_data="support")]
    ])
    await callback.message.edit_text(welcome_text, reply_markup=keyboard, parse_mode="Markdown")
