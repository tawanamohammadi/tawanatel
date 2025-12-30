from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from api.ttc_api import TTCApi
from config import settings
from database.db_manager import DBManager
import asyncio

router = Router()
api = TTCApi(settings.TTC_API_KEY)

@router.callback_query(F.data.startswith("order_"))
async def process_order(callback: CallbackQuery):
    _, country_id, service_code, cost = callback.data.split("_")
    country_id = int(country_id)
    cost = float(cost)
    
    user = await DBManager.get_user(callback.from_user.id)
    if user.balance < cost:
        await callback.answer("❌ Insufficient balance. Please top up your wallet.", show_alert=True)
        return

    # Request Number
    number_data = await api.get_number(service_code, country_id)
    if not number_data:
        await callback.answer("❌ Error getting number. It might be out of stock.", show_alert=True)
        return

    activation_id = number_data["id"]
    phone_number = number_data["number"]

    # Deduct Balance
    await DBManager.update_balance(user.id, -cost, "PURCHASE", f"Number for {service_code} ({phone_number})")
    
    # Save Activation
    await DBManager.add_activation(user.id, activation_id, service_code, country_id, phone_number, cost)

    # Set Status to 1 (Ready)
    await api.set_status(activation_id, 1)

    text = (
        f"✅ **Number Reserved!**\n\n"
        f"📱 Number: `{phone_number}`\n"
        f"🆔 ID: `{activation_id}`\n\n"
        "Waiting for SMS... Click 'Check SMS' once you've sent the code to this number."
    )
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔄 Check SMS", callback_data=f"check_{activation_id}")],
        [InlineKeyboardButton(text="❌ Cancel & Refund", callback_data=f"cancel_{activation_id}")]
    ])
    
    await callback.message.edit_text(text, reply_markup=keyboard, parse_mode="Markdown")

@router.callback_query(F.data.startswith("check_"))
async def check_sms(callback: CallbackQuery):
    activation_id = callback.data.split("_")[1]
    
    status = await api.get_status(activation_id)
    
    if status.startswith("STATUS_OK:"):
        code = status.split(":")[1]
        await DBManager.update_activation_status(activation_id, "FINISHED", code)
        
        # Complete activation on remote
        await api.set_status(activation_id, 6)
        
        await callback.message.edit_text(
            f"📩 **SMS Received!**\n\n"
            f"🔑 Code: `{code}`\n\n"
            "Thank you for using Tawana Telecom!",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="🔙 Main Menu", callback_data="main_menu")]])
        )
    elif status == "STATUS_WAIT_CODE":
        await callback.answer("⏳ Still waiting for SMS...", show_alert=False)
    else:
        await callback.answer(f"Status: {status}", show_alert=True)

@router.callback_query(F.data.startswith("cancel_"))
async def cancel_order(callback: CallbackQuery):
    activation_id = callback.data.split("_")[1]
    
    activation = await DBManager.get_activation_by_id(activation_id)
    if not activation or activation.status != "WAITING":
        await callback.answer("❌ This order cannot be cancelled.")
        return

    # Cancel on remote
    remote_status = await api.set_status(activation_id, 8)
    
    if "ACCESS_CANCEL" in remote_status:
        # Refund User
        await DBManager.update_balance(activation.user_id, activation.cost, "REFUND", f"Refund for {activation.number}")
        await DBManager.update_activation_status(activation_id, "CANCELLED")
        
        await callback.message.edit_text(
            "❌ **Order Cancelled**\n\nYour balance has been refunded.",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="🔙 Main Menu", callback_data="main_menu")]])
        )
    else:
        await callback.answer(f"❌ Could not cancel: {remote_status}", show_alert=True)
