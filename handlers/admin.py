from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from config import settings
from database.db_manager import DBManager

router = Router()

def is_admin(user_id: int):
    return user_id in settings.ADMIN_IDS

@router.message(Command("admin"), F.from_user.id.in_(settings.ADMIN_IDS))
async def admin_panel(message: Message):
    await message.answer(
        "🛠 **Admin Panel**\n\n"
        "Usage:\n"
        "`/topup <user_id> <amount>` - Add balance to user\n"
        "`/setbalance <user_id> <amount>` - Set exact balance\n"
        "`/stats` - View bot statistics"
    )

@router.message(Command("topup"), F.from_user.id.in_(settings.ADMIN_IDS))
async def topup_user(message: Message):
    args = message.text.split()
    if len(args) != 3:
        await message.answer("Usage: `/topup <user_id> <amount>`")
        return
    
    try:
        user_id = int(args[1])
        amount = float(args[2])
    except ValueError:
        await message.answer("Invalid ID or Amount.")
        return

    user = await DBManager.get_user(user_id)
    if not user:
        await message.answer("User not found.")
        return

    await DBManager.update_balance(user_id, amount, "TOPUP", f"Manual topup by admin {message.from_user.id}")
    await message.answer(f"✅ Successfully added `{amount}` to user `{user_id}`.")
    
    # Notify User
    try:
        from main import bot
        await bot.send_message(user_id, f"💰 Your balance has been topped up with `{amount}` by an administrator.")
    except Exception as e:
        await message.answer(f"⚠️ User was not notified: {e}")
