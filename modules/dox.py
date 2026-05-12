import asyncio
from telethon import events

# Карта замены символов
TRANSLATE_MAP = {
    ord("з"): "3", ord("е"): "3", ord("Е"): "3", ord("З"): "3", ord("z"): "3",
    ord("о"): "0", ord("o"): "0",
    ord("и"): "u", ord("И"): "U", ord("i"): "1",
    ord("А"): "4", ord("а"): "4", ord("a"): "4", ord("A"): "4",
}

class State:
    enabled = False

def register(client, start_time):
    @client.on(events.NewMessage(pattern=r"^\.dox$", outgoing=True))
    async def toggle(event):
        State.enabled = not State.enabled
        status = "ON" if State.enabled else "OFF"
        await event.edit(
            "**╭───  Yumi Doxxer  ───**\n"
            f"**│**  Статус: `{status}`\n"
            "**╰──────────────────╯**"
        )

    @client.on(events.NewMessage(pattern=r"^\.dox_msg$", outgoing=True))
    async def transform(event):
        reply = await event.get_reply_message()
        if reply and reply.text:
            new_text = reply.text.translate(TRANSLATE_MAP)
            await event.edit(new_text)
        else:
            await event.edit("**│**  `Ошибка: нужен реплей!`")

    @client.on(events.NewMessage(outgoing=True))
    async def watcher(event):
        if State.enabled and event.text and not event.text.startswith("."):
            new_text = event.text.translate(TRANSLATE_MAP)
            if event.text != new_text:
                await event.edit(new_text)