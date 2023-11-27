from telethon import TelegramClient
import config as Config
import db
import time
from utils import parse_message_text

client = TelegramClient("auth", Config.API_ID, Config.API_HASH)


async def main():
    print("start parse")
    dialogs = await client.get_dialogs()
    for dialog in dialogs:
        if dialog.name == "Слив платных глав | LN Manga":
            messages = client.iter_messages(dialog)
            async for message in messages:
                manga = parse_message_text(message.text)
                manga["date"] = message.date
                db.db.create_manga_or_return_id(manga)
                print(
                    message.id,
                )
                time.sleep(1)


with client:
    client.loop.run_until_complete(main())
