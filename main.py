 import asyncio
import logging
from aiogram import Bot, Dispatcher
from config import settings
from database.models import init_db
from handlers import start, purchase, orders, admin, profile

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

bot = Bot(token=settings.BOT_TOKEN)
dp = Dispatcher()

async def main():
    # Initialize DB
    await init_db()
    
    # Register routers
    dp.include_router(start.router)
    dp.include_router(purchase.router)
    dp.include_router(orders.router)
    dp.include_router(admin.router)
    dp.include_router(profile.router)

    logging.info("Starting bot...")
    
    # Start polling
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
