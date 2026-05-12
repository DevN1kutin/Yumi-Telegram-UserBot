import asyncio
from telethon import events

def register(client, start_time):
    @client.on(events.NewMessage(pattern=r"^\.love$", outgoing=True))
    async def love_animation(event):
        # Список кадров анимации
        frames = [
            "❤️", 
            "❤️ 🧡", 
            "❤️ 🧡 💛", 
            "❤️ 🧡 💛 💚", 
            "❤️ 🧡 💛 💚 💙", 
            "❤️ 🧡 💛 💚 💙 💜",
            "**I**",
            "**I LOVE**",
            "**I LOVE YOU**",
            "**I LOVE YOU** ❤️",
            "✨ **I LOVE YOU** ✨",
            "❤️ **I LOVE YOU** ❤️"
        ]
        
        for frame in frames:
            try:
                await event.edit(frame)
                await asyncio.sleep(0.4) # Скорость анимации
            except:
                break # Если сообщение удалят или возникнет лимит, выходим из цикла