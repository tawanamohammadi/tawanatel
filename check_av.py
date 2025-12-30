import asyncio
from api.ttc_api import TTCApi
from config import settings

async def check_telegram_availability(country_ids: list):
    # حتماً API_KEY را در config.py یا .env ست کرده باشید
    api = TTCApi(settings.TTC_API_KEY)
    
    print(f"{'Country ID':<12} | {'Service':<10} | {'Price':<10} | {'Available':<10}")
    print("-" * 50)
    
    for cid in country_ids:
        try:
            # action=getPrices&service=tg&country=cid
            prices = await api.get_prices("tg", cid)
            
            if not prices:
                print(f"{cid:<12} | {'tg':<10} | {'N/A':<10} | {'Out of Stock'}")
                continue
            
            # استخراج اطلاعات قیمت و تعداد
            # ساختار بازگشتی: [{"tg": {"cost": 0.08, "count": 25370}}]
            for country_data in prices:
                for service_code, info in country_data.items():
                    if service_code == "tg" or "tg" in service_code:
                        cost = info.get("cost", "??")
                        count = info.get("count", 0)
                        print(f"{cid:<12} | {service_code:<10} | {cost:<10} | {count:<10}")
        except Exception as e:
            print(f"Error checking country {cid}: {e}")

if __name__ == "__main__":
    # لیستی از آیدی کشورهایی که میخواهید چک کنید را اینجا بگذارید
    # مثال: 0 (روسیه)، 1 (اوکراین)، 2 (قزاقستان)، 6 (اندونزی)، 12 (آمریکا)
    target_countries = [0, 1, 2, 6, 12, 15, 22] 
    
    asyncio.run(check_telegram_availability(target_countries))
