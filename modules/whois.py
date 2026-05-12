from telethon import events
from telethon.tl.functions.users import GetFullUserRequest

def get_reg_date(user_id):
    if user_id < 5000000: return "2013"
    elif user_id < 50000000: return "2014"
    elif user_id < 150000000: return "2015"
    elif user_id < 250000000: return "2016"
    elif user_id < 450000000: return "2017"
    elif user_id < 700000000: return "2018"
    elif user_id < 950000000: return "2019"
    elif user_id < 1200000000: return "2020"
    elif user_id < 1450000000: return "2021"
    elif user_id < 5000000000: return "2022-2024"
    else: return "2025-2026"

async def whois_handler(event):
    args = event.text.split(maxsplit=1)
    reply = await event.get_reply_message()
    
    await event.edit("🔍 **Анализирую цель...**")
    
    try:
        if len(args) > 1:
            user = await event.client.get_entity(args[1])
        elif reply:
            user = await event.client.get_entity(reply.sender_id)
        else:
            user = await event.client.get_me()
        
        full = await event.client(GetFullUserRequest(user.id))
        
        scam_status = "✅ Чист"
        if user.scam: scam_status = "⚠️ SCAM (Мошенник)"
        if user.fake: scam_status = "🚫 FAKE (Подделка)"

        text = (
            "**╭───  Yumi OSINT  ───**\n"
            f"**│**  Имя: `{user.first_name}`\n"
        )
        
        if user.last_name:
            text += f"**│**  Фамилия: `{user.last_name}`\n"
            
        text += f"**│**  ID: `{user.id}`\n"
        
        if user.username: 
            text += f"**│**  Юзер: @{user.username}\n"
            
        phone = f"+{user.phone}" if user.phone else "Скрыт"
        text += f"**│**  Номер: `{phone}`\n"
        
        text += f"**│**  Статус: `{scam_status}`\n"
        text += f"**│**  Регистрация: `~{get_reg_date(user.id)} год`\n"
        
        text += f"**│**  Общих чатов: `{full.full_user.common_chats_count}`\n"
        
        if full.full_user.about:
            bio = full.full_user.about.replace('\n', ' ')
            text += f"**│**  Био: `{bio[:50]}...`\n" if len(bio) > 50 else f"**│**  Био: `{bio}`\n"

        text += f"**│**  Бот: `{'Да' if user.bot else 'Нет'}`\n"
        text += "**╰──────────────────╯**"
        
        await event.edit(text)

    except Exception as e:
        await event.edit(f"**❌ Ошибка проверки:**\n`{str(e)}`")

def register(client, start_time):
    @client.on(events.NewMessage(pattern=r"^\.whois(\s.*)?$", outgoing=True))
    async def _whois(event):
        await whois_handler(event)