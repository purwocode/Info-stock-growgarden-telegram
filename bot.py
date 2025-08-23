import os
import asyncio
import aiohttp
import html
from telegram import Bot

API_URL = "https://gagapi.onrender.com/alldata"
HEADERS = {
    "accept": "application/json",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}
DEFAULT_INTERVAL = 20

# =======================
# KATEGORI SEEDS
# =======================
SEED_RARITY = {
    "Uncommon": ["Carrot", "Strawberry", "Blueberry", "Orange Tulip"],
    "Rare": ["Tomato", "Corn", "Daffodil", "Wat"],
    "Legendary": ["Watermelon", "Pumpkin", "Apple", "Bamboo"],
    "Mythical": ["Coconut", "Cactus", "Dragon Fruit", "Mango"],
    "Divine": ["Grape", "Mushroom", "Pepper", "Cacao"],
    "Prismatic": [
        "Beanstalk", "Ember Lily", "Sugar Apple", "Burning Bud",
        "Giant Pinecone", "Elder Strawberry", "Romanesco"
    ]
}

# =======================
# KATEGORI GEAR
# =======================
GEAR_RARITY = {
    "Uncommon": ["Watering Can", "Trading Ticket", "Trowel", "Recall Wrench"],
    "Rare": ["Basic Sprinkler"],
    "Legendary": ["Advanced Sprinkler", "Medium Toy", "Medium Treat"],
    "Mythical": ["Godly Sprinkler", "Magnifying Glass"],
    "Divine": ["Master Sprinkler", "Cleaning Spray", "Favorite Tool", "Harvest Tool", "Friendship Pot"],
    "Prismatic": ["Grandmaster Sprinkler", "Levelup Lollipop"]
}

# =======================
# KATEGORI EGGS
# =======================
EGG_RARITY = {
    "Common": ["Common Egg", "Common Summer Egg"],
    "Rare": ["Rare Summer Egg"],
    "Mythical": ["Mythical Egg", "Paradise Egg"],
    "Divine": ["Bug Egg"]
}

# =======================
# EMOJI RARITY
# =======================
RARITY_EMOJI = {
    "Common": "⚪",
    "Uncommon": "🟢",
    "Rare": "🔵",
    "Legendary": "🟣",
    "Mythical": "🟠",
    "Divine": "🔴",
    "Prismatic": "🌈",
    "Unknown": "❓"
}

def get_category(item_name: str, category_dict: dict) -> str:
    for category, items in category_dict.items():
        if item_name in items:
            return category
    return "Unknown"

# =======================
# FETCH & FORMAT DATA
# =======================
async def fetch_and_format(session: aiohttp.ClientSession) -> str:
    async with session.get(API_URL, headers=HEADERS) as resp:
        status = resp.status
        try:
            data = await resp.json()
        except Exception:
            text = await resp.text()
            return f"Status {status}\n{html.escape(text[:500])}"

        lines = []

        # WEATHER
        weather = data.get("weather")
        if weather:
            lines.append("== WEATHER ==")
            lines.append(f"Type: {weather.get('type', '-')}")
            lines.append(f"Active: {'✅' if weather.get('active') else '❌'}")

            effects = weather.get("effects")
            if effects and isinstance(effects, list):
                lines.append("Effects:")
                for eff in effects:
                    lines.append(f"- {eff}")

            if weather.get("lastUpdated"):
                lines.append(f"Last Updated: {weather['lastUpdated']}")
            lines.append("")

        # WEATHER HISTORY
        whist = data.get("weatherHistory")
        if whist and isinstance(whist, list):
            lines.append("== WEATHER HISTORY ==")
            for item in whist:
                lines.append(
                    f"Type: {item.get('type','-')}, Active: {'✅' if item.get('active') else '❌'}"
                )
            lines.append("")

        # TRAVELING MERCHANT
        tm = data.get("travelingMerchant")
        if tm:
            lines.append("== TRAVELING MERCHANT ==")
            lines.append(tm.get("merchantName", "-"))

            items = tm.get("items")
            if items and isinstance(items, list):
                for item in items:
                    name = item.get("name", "-")
                    qty = item.get("quantity", "-")
                    avail = "✅" if item.get("available") else "❌"
                    lines.append(f"{name} : {qty} ({avail})")

        # KATEGORI LIST (gear, seeds, eggs, honey, cosmetics, dsb.)
        for key, value in data.items():
            if isinstance(value, list) and all(isinstance(v, dict) for v in value):
                lines.append(f"== {key.upper()} ==")
                for item in value:
                    name = item.get("name", "-")
                    qty = item.get("quantity", "-")

                    category = "Unknown"
                    if key.lower() == "seeds":
                        category = get_category(name, SEED_RARITY)
                    elif key.lower() == "gear":
                        category = get_category(name, GEAR_RARITY)
                    elif key.lower() == "eggs":
                        category = get_category(name, EGG_RARITY)

                    emoji = RARITY_EMOJI.get(category, "❓")
                    lines.append(f"{name} : {qty} ({category}) {emoji}")

                lines.append("")

        return "\n".join(lines).strip()

# =======================
# AUTO WATCH & SEND TELEGRAM
# =======================
async def auto_watch(bot: Bot, chat_id: int, interval: int):
    last_text = None
    async with aiohttp.ClientSession() as session:
        while True:
            try:
                new_text = await fetch_and_format(session)
                if new_text != last_text:
                    await bot.send_message(
                        chat_id,
                        f"<pre>{html.escape(new_text)}</pre>",
                        parse_mode="HTML"
                    )
                    print("✅ Kirim pesan baru")
                    last_text = new_text
                else:
                    print("ℹ️ Tidak ada perubahan data, skip kirim")
            except Exception as e:
                print("❌ Error:", e)
                await bot.send_message(chat_id, f"Error: {html.escape(str(e))}", parse_mode="HTML")

            await asyncio.sleep(interval)

# =======================
# MAIN
# =======================
async def main():
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TARGET_CHAT_ID")
    interval = int(os.getenv("WATCH_INTERVAL", DEFAULT_INTERVAL))

    if not token:
        raise RuntimeError("Env TELEGRAM_BOT_TOKEN belum di-set.")
    if not chat_id:
        raise RuntimeError("Env TARGET_CHAT_ID belum di-set.")

    bot = Bot(token=token)
    await auto_watch(bot, int(chat_id), interval)

if __name__ == "__main__":
    asyncio.run(main())
