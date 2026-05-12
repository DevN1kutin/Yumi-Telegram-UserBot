import logging
import os
from datetime import datetime
from telethon import TelegramClient, events

log = logging.getLogger("Yumi.Modules")

def _build_modules_message(modules_list: list) -> str:
    count = len(modules_list)
    items = "\n".join([f"**│**  `❯ {m}`" for m in modules_list])

    return (
        f"**╭───  Yumi Modules  ───**\n"
        f"**│**\n"
        f"{items}\n"
        f"**│**\n"
        f"**╰───**  `Total: {count}`  **───╯**"
    )

async def modules_handler(event) -> None:
    modules_dir = "modules"
    module_files = []
    
    if os.path.exists(modules_dir):
        for file in os.listdir(modules_dir):
            if file.endswith(".py") and not file.startswith("__"):
                module_files.append(file.replace(".py", ""))
    
    module_files.sort()
    await event.edit(_build_modules_message(module_files))

def register(client: TelegramClient, start_time: datetime) -> None:
    @client.on(events.NewMessage(pattern=r"^\.modules$", outgoing=True))
    async def _modules(event):
        await modules_handler(event)