import time
from telethon import events

class AFKState:
    is_afk = False
    start_time = 0

def register(client, start_time):
    # Включить AFK
    @client.on(events.NewMessage(pattern=r"^\.afk$", outgoing=True))
    async def set_afk(event):
        AFKState.is_afk = True
        AFKState.start_time = time.time()
        await event.edit(
            "**╭───  Yumi AFK  ───**\n"
            "**│**  Статус: `Включен`\n"
            "**╰──────────────────╯**"
        )

    @client.on(events.NewMessage(pattern=r"^\.unafk$", outgoing=True))
    async def stop_afk(event):
        if AFKState.is_afk:
            AFKState.is_afk = False
            await event.edit(
                "**╭───  Yumi AFK  ───**\n"
                "**│**  Статус: `Выключен`\n"
                "**╰──────────────────╯**"
            )

    @client.on(events.NewMessage(outgoing=True))
    async def auto_off(event):
        if AFKState.is_afk and not event.text.startswith("."):
            AFKState.is_afk = False
            uptime = int(time.time() - AFKState.start_time)
            await event.respond(
                "**╭───  Yumi AFK  ───**\n"
                "**│**  Статус: `OFF`\n"
                f"**│**  Был в AFK: `{uptime} сек.`\n"
                "**╰──────────────────╯**"
            )

    @client.on(events.NewMessage(incoming=True))
    async def reply_afk(event):
        if AFKState.is_afk and (event.is_private or event.mentioned):
            await event.reply(
                "**╭───  Yumi AFK  ───**\n"
                "**│**  Я сейчас не на месте.\n"
                "**╰──────────────────╯**"
            )