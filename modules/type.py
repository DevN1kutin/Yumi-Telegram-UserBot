import asyncio
from telethon import events

async def type_handler(event):
    args = event.text.split(maxsplit=1)
    
    if len(args) < 2:
        await event.edit(
            "╭───  Yumi Type  ───\n"
            "│\n"
            "│  .type <текст>\n"
            "│\n"
            "╰──────────────────╯"
        )
        return

    full_text = args[1]
    typing_text = ""
    
    # Эффект печати
    for char in full_text:
        typing_text += char
        # Добавляем символ курсора для вида
        await event.edit(f"{typing_text}▒")
        await asyncio.sleep(0.1)
    
    # Финальный текст без курсора
    await event.edit(typing_text)

def register(client, start_time):
    @client.on(events.NewMessage(pattern=r"^\.type(\s.*)?$", outgoing=True))
    async def _type(event):
        await type_handler(event)