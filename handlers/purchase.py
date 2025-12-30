from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from api.ttc_api import TTCApi
from config import settings
from database.db_manager import DBManager

router = Router()
api = TTCApi(settings.TTC_API_KEY)

# Simplified list of popular countries for initial view
POPULAR_COUNTRIES = [
    {"id": 0, "name": "Russia"},
    {"id": 1, "name": "Ukraine"},
    {"id": 2, "name": "Kazakhstan"},
    {"id": 6, "name": "Indonesia"},
    {"id": 12, "name": "USA"},
    {"id": 15, "name": "Vietnam"},
    {"id": 22, "name": "India"},
]

@router.callback_query(F.data == "buy_number")
async def choose_country(callback: CallbackQuery):
    keyboard = []
    for country in POPULAR_COUNTRIES:
        keyboard.append([InlineKeyboardButton(text=country["name"], callback_data=f"country_{country['id']}")])
    
    keyboard.append([InlineKeyboardButton(text="🌍 All Countries", callback_data="all_countries")])
    keyboard.append([InlineKeyboardButton(text="🔙 Back", callback_data="main_menu")])
    
    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    await callback.message.edit_text("🌍 **Select a Country:**", reply_markup=markup, parse_mode="Markdown")

@router.callback_query(F.data.startswith("country_"))
async def choose_service(callback: CallbackQuery):
    country_id = int(callback.data.split("_")[1])
    
    # Popular services
    services = [
        {"code": "tg", "name": "Telegram"},
        {"code": "wa", "name": "WhatsApp"},
        {"code": "go", "name": "Google/Gmail"},
        {"code": "ig", "name": "Instagram"},
        {"code": "fb", "name": "Facebook"},
        {"code": "tk", "name": "TikTok"},
    ]
    
    keyboard = []
    for svc in services:
        keyboard.append([InlineKeyboardButton(text=svc["name"], callback_data=f"svc_{country_id}_{svc['code']}")])
    
    keyboard.append([InlineKeyboardButton(text="🔙 Back to Countries", callback_data="buy_number")])
    
    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    await callback.message.edit_text("📱 **Select a Service:**", reply_markup=markup, parse_mode="Markdown")

@router.callback_query(F.data.startswith("svc_"))
async def confirm_purchase(callback: CallbackQuery):
    _, country_id, service_code = callback.data.split("_")
    country_id = int(country_id)
    
    # Check Price
    prices = await api.get_prices(service_code, country_id)
    if not prices:
        await callback.answer("❌ No numbers available for this service/country.", show_alert=True)
        return
    
    price_info = next(iter(prices[0].values())) if prices else None
    if not price_info:
        await callback.answer("❌ Price information not found.", show_alert=True)
        return
    
    cost = price_info["cost"]
    count = price_info["count"]
    
    text = (
        f"💳 **Confirmation**\n\n"
        f"🌍 Country: `{country_id}`\n"
        f"📱 Service: `{service_code}`\n"
        f"💰 Price: `{cost:.2f}`\n"
        f"📦 Available: `{count}`\n\n"
        "Do you want to buy this number?"
    )
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Buy Now", callback_data=f"order_{country_id}_{service_code}_{cost}")],
        [InlineKeyboardButton(text="❌ Cancel", callback_data=f"country_{country_id}")]
    ])
    
    await callback.message.edit_text(text, reply_markup=keyboard, parse_mode="Markdown")
