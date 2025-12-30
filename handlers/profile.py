from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from database.db_manager import DBManager

router = Router()

@router.callback_query(F.data == "profile")
async def view_profile(callback: CallbackQuery):
    user = await DBManager.get_user(callback.from_user.id)
    text = (
        f"👤 **Your Profile**\n\n"
        f"🆔 ID: `{user.id}`\n"
        f"💰 Balance: `{user.balance:.2f}`\n"
        f"📅 Joined: {user.created_at.strftime('%Y-%m-%d')}"
    )
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⏳ Active Orders", callback_data="active_orders")],
        [InlineKeyboardButton(text="🔙 Back", callback_data="main_menu")]
    ])
    await callback.message.edit_text(text, reply_markup=keyboard, parse_mode="Markdown")

@router.callback_query(F.data == "active_orders")
async def view_active_orders(callback: CallbackQuery):
    activations = await DBManager.get_active_activations(callback.from_user.id)
    
    if not activations:
        await callback.answer("You have no active orders.")
        return

    text = "⏳ **Active Orders:**\n\n"
    keyboard = []
    
    for act in activations:
        text += f"📱 `{act.number}` ({act.service_code})\n"
        keyboard.append([InlineKeyboardButton(text=f"Manage {act.number}", callback_data=f"manage_{act.activation_id}")])
    
    keyboard.append([InlineKeyboardButton(text="🔙 Back", callback_data="profile")])
    await callback.message.edit_text(text, reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard), parse_mode="Markdown")

@router.callback_query(F.data.startswith("manage_"))
async def manage_order(callback: CallbackQuery):
    activation_id = callback.data.split("_")[1]
    act = await DBManager.get_activation_by_id(activation_id)
    
    if not act:
        await callback.answer("Order not found.")
        return

    text = (
        f"📦 **Order Management**\n\n"
        f"📱 Number: `{act.number}`\n"
        f"🆔 ID: `{activation_id}`\n"
        f"💰 Cost: `{act.cost:.2f}`\n"
        f"⏳ Status: {act.status}\n"
    )
    
    keyboard = []
    if act.status == "WAITING":
        keyboard.append([InlineKeyboardButton(text="🔄 Check SMS", callback_data=f"check_{activation_id}")])
        keyboard.append([InlineKeyboardButton(text="❌ Cancel & Refund", callback_data=f"cancel_{activation_id}")])
    
    keyboard.append([InlineKeyboardButton(text="🔙 Back", callback_data="active_orders")])
    await callback.message.edit_text(text, reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard), parse_mode="Markdown")
