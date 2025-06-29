from pyrogram import Client, filters
import re

api_id = 24753191  # جایگزین کن
api_hash = "a07a75baddd964940ec0dc076131541b"

source_channels = ["@HopeNet", "@vmessorg"]
destination_channel = "@SFcMAh"

app = Client("my_account", api_id=api_id, api_hash=api_hash)

# تابع برای ویرایش اسم کانفیگ و جایگزینی با @eliiteshop
def modify_config(text: str) -> str:
    # تلاش برای پیدا کردن بخش name در کانفیگ vmess
    if "vmess://" in text:
        try:
            # decode base64 برای vmess
            base64_part = text.split("vmess://")[1].strip()
            import base64, json
            decoded = base64.b64decode(base64_part + "===").decode()
            j = json.loads(decoded)
            j['ps'] = "@eliiteshop"
            new_config = base64.b64encode(json.dumps(j).encode()).decode()
            return "vmess://" + new_config
        except Exception as e:
            print("خطا در ویرایش vmess:", e)
            return text

    # تلاش برای تغییر name=... در vless
    if "vless://" in text:
        new_text = re.sub(r'name=[^&\n\r]*', 'name=@eliiteshop', text)
        return new_text

    return text

@app.on_message(filters.chat(source_channels) & filters.text)
async def process_config(client, message):
    text = message.text.lower()
    if "vmess://" in text or "vless://" in text:
        edited_text = modify_config(message.text)
        await client.send_message(destination_channel, edited_text)

app.run()
