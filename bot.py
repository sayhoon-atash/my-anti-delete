from telethon import TelegramClient

# این دو مورد را با کلیدهایی که از سایت تلگرام گرفتی پر کن
api_id = YOUR_API_ID  # فقط عدد را بنویس، مثلا 123456
api_hash = 'YOUR_API_HASH' # داخل کوتیشن بماند

client = TelegramClient('session_zero', api_id, api_hash)

async def main():
    print("--- اتصال برقرار شد ---")
    # اینجا آیدی عددی خودت یا اکانت تست را بگذار
    target = 777000 
    user = await client.get_entity(target)
    print(f"نام: {user.first_name}\nآیدی: {user.id}")

