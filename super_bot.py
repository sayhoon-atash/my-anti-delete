from telethon import TelegramClient, events
from telethon.tl.functions.account import UpdateProfileRequest
import asyncio
import os

# اطلاعات تو
api_id = 32130791
api_hash = '70cf21e812d3ab24cbfec1745005c7b7'

client = TelegramClient('secure_session', api_id, api_hash)
msg_cache = {}

async def name_worker():
    print("✨ سیستم آپدیت نام فعال شد.")
    while True:
        try:
            me = await client.get_me()
            base_name = me.first_name.split(' |')[0].strip()
            # به جای آیدی عددی پیچیده، اینجا ایموجی دلخواهت را بگذار
            new_name = f"{base_name} | 🌟" 
            if me.first_name != new_name:
                await client(UpdateProfileRequest(first_name=new_name))
        except: pass
        await asyncio.sleep(300)

@client.on(events.NewMessage(incoming=True))
async def handler(event):
    if event.is_private:
        sender = await event.get_sender()
        name = sender.first_name if sender else "ناشناس"
        msg_cache[event.id] = {'text': event.text, 'name': name, 'id': event.sender_id}
        
        # ذخیره عکس تایمری
        if event.media and hasattr(event.media, 'ttl_seconds') and event.media.ttl_seconds:
            path = await event.download_media()
            await client.send_file('me', path, caption=f"📸 عکس تایمری از: {name}")
            if os.path.exists(path): os.remove(path)

@client.on(events.MessageDeleted)
async def delete_handler(event):
    for m_id in event.deleted_ids:
        if m_id in msg_cache:
            m = msg_cache[m_id]
            await client.send_message('me', f"⚠️ **پیام حذف شد**\n👤 فرستنده: {m['name']}\n🆔 آیدی: `{m['id']}`\n💬 متن: {m['text']}")

async def main():
    await client.start()
    print("🚀 ربات با موفقیت روشن شد! برو توی تلگرام تست کن.")
    await asyncio.gather(name_worker(), client.run_until_disconnected())

if __name__ == '__main__':
    client.loop.run_until_complete(main())
