from telethon import TelegramClient, events
import asyncio

# --- تنظیمات اختصاصی شما ---
api_id = 32130791
api_hash = '70cf21e812d3ab24cbfec1745005c7b7'
# -------------------------

client = TelegramClient('final_session', api_id, api_hash)

# حافظه موقت برای ذخیره متن پیام‌ها
msg_cache = {}

print("🛡 ربات ضد-حذف و ضد-ویرایش در حال استارت است...")

@client.on(events.NewMessage)
async def cache_message(event):
    if event.text:
        msg_cache[event.id] = {
            'text': event.text,
            'sender': await event.get_sender()
        }

@client.on(events.MessageDeleted)
async def delete_handler(event):
    for msg_id in event.ids:
        if msg_id in msg_cache:
            data = msg_cache[msg_id]
            sender_name = getattr(data['sender'], 'first_name', 'نامشخص')
            report = (f"🗑 **پیام پاک شد!**\n"
                      f"👤 فرستنده: {sender_name}\n"
                      f"📝 متن پیام: {data['text']}")
            await client.send_message('me', report)
            del msg_cache[msg_id]

@client.on(events.MessageEdited)
async def edit_handler(event):
    if event.id in msg_cache:
        old_data = msg_cache[event.id]
        new_text = event.text
        if old_data['text'] != new_text:
            sender_name = getattr(old_data['sender'], 'first_name', 'نامشخص')
            report = (f"✏️ **پیام ویرایش شد!**\n"
                      f"👤 فرستنده: {sender_name}\n"
                      f"❌ متن قدیمی: {old_data['text']}\n"
                      f"✅ متن جدید: {new_text}")
            await client.send_message('me', report)
            msg_cache[event.id]['text'] = new_text

async def main():
    await client.start()
    print("🚀 ربات آنلاین شد! مچ‌گیری شروع شد...")
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
