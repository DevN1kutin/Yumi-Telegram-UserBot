import logging
import os
from datetime import datetime, timezone
from telethon import TelegramClient, events

log = logging.getLogger("Yumi.Ping")

def _format_uptime(start_time: datetime) -> str:
    now = datetime.now()
    delta = now - start_time
    total_seconds = int(delta.total_seconds())

    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    parts = []
    if hours:
        parts.append(f"{hours}ч")
    if minutes:
        parts.append(f"{minutes}м")
    parts.append(f"{seconds:02d}с")

    return " ".join(parts)

def _build_ping_message(rtt_ms: float, uptime_str: str) -> str:
    bar_length = 8
    filled = min(bar_length, round((rtt_ms / 500) * bar_length))
    bar = "●" * filled + "○" * (bar_length - filled)

    if rtt_ms < 100:
        status, icon = "Stable", "💠"
    elif rtt_ms < 250:
        status, icon = "Normal", "🔹"
    else:
        status, icon = "Lagging", "🔸"

    return (
        f"**╭───  Yumi UserBot  ───**\n"
        f"**│**\n"
        f"**│**  {icon} **Status:** `{status}`\n"
        f"**│**  ⚡ **Ping:** `{rtt_ms:.1f}ms`\n"
        f"**│**  ⏱ **Up:** `{uptime_str}`\n"
        f"**│**\n"
        f"**╰───**  `{bar}`  **───╯**"
    )

async def ping_handler(event, start_time: datetime) -> None:
    log.info("Команда .ping получена")

    # Считаем RTT
    sent_at = datetime.now(timezone.utc)
    # Используем временное редактирование для замера
    await event.edit("`⏳ Calculating...`")
    rtt_ms = (datetime.now(timezone.utc) - sent_at).total_seconds() * 1000
    
    uptime_str = _format_uptime(start_time)
    text = _build_ping_message(rtt_ms, uptime_str)
    
    photo_path = "photo.png"

    if os.path.exists(photo_path):
        # Удаляем текстовое сообщение и шлем фото с подписью
        await event.delete()
        await event.client.send_file(event.chat_id, photo_path, caption=text)
    else:
        # Если картинки нет, просто выводим текст, чтобы не было ошибки
        await event.edit(text + "\n\n⚠️ `photo.png не найден`")
    
    log.info(f"Ping: {rtt_ms:.1f}ms")

def register(client: TelegramClient, start_time: datetime) -> None:
    @client.on(events.NewMessage(pattern=r"^\.ping$", outgoing=True))
    async def _ping(event):
        await ping_handler(event, start_time)