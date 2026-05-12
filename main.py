import asyncio
import logging
import sys
from datetime import datetime
from telethon import TelegramClient
from config import API_ID, API_HASH, SESSION_NAME
from modules import load_modules

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s │ %(levelname)-8s │ %(name)s │ %(message)s",
    datefmt="%H:%M:%S",
    handlers=[logging.StreamHandler(sys.stdout)],
)

log = logging.getLogger("Yumi")

# Глобальное время запуска
START_TIME = datetime.now()

async def main():
    log.info("Инициализация Yumi UserBot...")

    client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

    # Авторизация
    await client.start()

    # Загрузка модулей
    load_modules(client, START_TIME)

    me = await client.get_me()
    name = me.first_name or me.username or "Unknown"

    print("\n" + "─" * 44)
    print(f"  🌸 Yumi UserBot")
    print(f"  🕐 Старт: {START_TIME.strftime('%Y-%m-%d %H:%M:%S')}")
    print("─" * 44 + "\n")

    log.info(f"Авторизован как: {name} (ID: {me.id})")
    log.info("Бот активен. Нажмите Ctrl+C для остановки.")

    await client.run_until_disconnected()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        log.info("🌸 Yumi UserBot остановлен.")