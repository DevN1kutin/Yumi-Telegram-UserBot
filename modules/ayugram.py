import asyncio
import random
import string
from telethon import events

class AyuState:
    is_enabled = False
    ghost_mode = False
    bot_username = None

def generate_username():
    chars = string.ascii_lowercase + string.digits
    return f"yumi_{''.join(random.choice(chars) for _ in range(8))}_bot"

def register(client, start_time):
    
    @client.on(events.NewMessage(pattern=r"^\.ayugram$", outgoing=True))
    async def setup_ayugram(event):
        if AyuState.bot_username:
            status_logs = "✅" if AyuState.is_enabled else "❌"
            status_ghost = "👻" if AyuState.ghost_mode else "👁️"
            
            await event.edit(
                f"**⚙️ AYUGRAM PANEL**\n"
                f"**Бот:** @{AyuState.bot_username}\n"
                f"**Логи:** `{status_logs}` | **Призрак:** `{status_ghost}`\n"
                f"━━━━━━━━━━━━━━\n"
                f"`.ayu` — логи | `.ghost` — призрак | `.save` — в бота"
            )
            return

        await event.edit("🛠 **Поиск активного лог-бота...**")
        
        if not AyuState.bot_username:
            await event.edit("🛠 **Создаю нового бота...**")
            async with client.conversation("@BotFather") as conv:
                await conv.send_message("/newbot")
                await asyncio.sleep(1)
                await conv.send_message("AyuGram Logs")
                await asyncio.sleep(1)
                
                username = generate_username()
                await conv.send_message(username)
                
                resp = await conv.get_response()
                if "Done!" in resp.text:
                    AyuState.bot_username = username
                    AyuState.is_enabled = True
                    await client.send_message(username, "Логирование активировано.")
                    await event.edit(f"✅ **Бот готов:** @{username}")
                else:
                    await event.edit("❌ **Ошибка BotFather. Проверь лимиты.**")

    @client.on(events.MessageEdited(incoming=True))
    async def edit_logger(event):
        if AyuState.is_enabled and AyuState.bot_username:
            user = await event.get_sender()
            name = user.first_name if user else "User"
            await client.send_message(AyuState.bot_username, f"📝 **{name} изменил соо:**")
            await client.forward_messages(AyuState.bot_username, event.message)

    @client.on(events.NewMessage(incoming=True))
    async def media_logger(event):
        if AyuState.is_enabled and AyuState.bot_username and event.media:
            if getattr(event.media, 'ttl_seconds', None):
                await client.send_message(AyuState.bot_username, "🚀 **Перехват исчезайки:**")
                await client.forward_messages(AyuState.bot_username, event.message)

    @client.on(events.NewMessage(pattern=r"^\.save$", outgoing=True))
    async def save_handler(event):
        reply = await event.get_reply_message()
        if reply and AyuState.bot_username:
            await client.forward_messages(AyuState.bot_username, reply)
            await event.delete()

    @client.on(events.NewMessage(incoming=True))
    async def ghost_handler(event):
        if AyuState.ghost_mode and event.is_private:
            await client.send_read_acknowledge(event.chat_id, max_id=0, clear_mentions=True)

    @client.on(events.NewMessage(pattern=r"^\.ayu$", outgoing=True))
    async def toggle_l(event):
        AyuState.is_enabled = not AyuState.is_enabled
        await event.edit(f"Логи: {'ВКЛ' if AyuState.is_enabled else 'ВЫКЛ'}")
        await asyncio.sleep(1)
        await event.delete()

    @client.on(events.NewMessage(pattern=r"^\.ghost$", outgoing=True))
    async def toggle_g(event):
        AyuState.ghost_mode = not AyuState.ghost_mode
        await event.edit(f"Призрак: {'ВКЛ' if AyuState.ghost_mode else 'ВЫКЛ'}")
        await asyncio.sleep(1)
        await event.delete()