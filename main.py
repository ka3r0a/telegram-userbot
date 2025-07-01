from pyrogram import Client, filters
import os, re, json

api_id = int(os.environ["API_ID"])
api_hash = os.environ["API_HASH"]

source_channels = ["@HopeNet", "@vmessorg"]
destination_channel = "@SFcMAh"

app = Client("static/my_account", api_id=api_id, api_hash=api_hash)

def modify_config(text: str) -> str:
    if "vmess://" in text:
        try:
            base64_part = text.split("vmess://")[1].strip()
            import base64
            decoded = base64.b64decode(base64_part + "===").decode()
            j = json.loads(decoded)
            j['ps'] = "@eliiteshop"
            new_config = base64.b64encode(json.dumps(j).encode()).decode()
            return "vmess://" + new_config
        except Exception as e:
            print("⚠️ خطا در ویرایش vmess:", e)
            return text

    if "vless://" in text:
        return re.sub(r'name=[^&\n\r]*', 'name=@eliiteshop', text)

    return text

@app.on_message(filters.chat(source_channels) & filters.text)
async def process_config(client, message):
    text = message.text.lower()
    if "vmess://" in text or "vless://" in text:
        edited_text = modify_config(message.text)
        try:
            await client.send_message(destination_channel, edited_text)
            print("✅ پیام ارسال شد.")
        except Exception as e:
            print("❌ خطا در ارسال:", e)

app.run()
