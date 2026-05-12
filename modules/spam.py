import asyncio
from telethon import events

async def spam_handler(event):
    args = event.text.split(maxsplit=3)
    
    if len(args) < 4:
        await event.edit(
            "**╭───  Yumi Spammer  ───**\n"
            "**│**\n"
            "**│**  `ОШИБКА:` Недостаточно данных\n"
            "**│**\n"
            "**│**  **Использование:**\n"
            "**│**  `.spam <кол-во> <кд> <текст>`\n"
            "**│**\n"
            "**│**  **Пример:**\n"
            "**│**  `.spam 10 0.5 привет`\n"
            "**│**\n"
            "**╰───**  `WAITING_INPUT`  **───╯**"
        )
        return

    try:
        count = int(args[1])
        delay = float(args[2])
        text = args[3]
    except ValueError:
        await event.edit("**│**  `Ошибка: проверь числа!`")
        return

    await event.delete()

    for _ in range(count):
        await event.respond(text)
        if delay > 0:
            await asyncio.sleep(delay)

def register(client, start_time):
    @client.on(events.NewMessage(pattern=r"^\.spam(\s.*)?$", outgoing=True))
    async def _spam(event):
        await spam_handler(event)