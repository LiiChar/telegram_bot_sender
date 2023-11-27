from telethon import TelegramClient, events
import config as Config
import telebot
from db import db
import kb
from utils import parse_message_text

client = ""

client = TelegramClient(
    "auth", Config.API_ID, Config.API_HASH, system_version="4.16.30-vxCUSTOM"
)

# assert client.connect()
# if not client.is_user_authorized():
#     client.send_code_request(79126234458)
#     client.sign_in(79126234458, input("Enter code: "))

# client = TelegramClient("auth", Config.API_ID, Config.API_HASH).start(
#     bot_token=Config.BOT_TOKEN, max_attempts=10
# )

bot = telebot.TeleBot(Config.BOT_TOKEN)

parse_mod = False
chat_id = -1001551102382
chat_id2 = 1551102382


@client.on(events.NewMessage())
async def normal_handler(event):
    ev = event.message.to_dict()
    if "channel_id" in ev["peer_id"] and (
        int(ev["peer_id"]["channel_id"]) == chat_id
        or int(ev["peer_id"]["channel_id"]) == chat_id2
    ):
        message = ev["message"]
        manga = parse_message_text(message)
        prev_manga = db.get_near_prev_or_next_manga_by_chapter(
            manga["name"], manga["part"], manga["chapter"], "MAX"
        )
        next_manga = db.get_near_prev_or_next_manga_by_chapter(
            manga["name"], manga["part"], manga["chapter"], "MIN"
        )
        manga["date"] = ev["date"]
        print(manga)
        db.create_manga_or_return_id(manga)
        text = f"""
        <b>{manga["name"]}</b>

        Том {manga["part"]} глава {manga["chapter"]}
        Прочитать <a href='{manga["link"]}'>{manga["name"]}</a> 
        """
        users_id = db.get_manga_user_by_name(manga["name"])
        print(users_id)
        for user_id in users_id:
            bot.send_message(
                chat_id=user_id[0],
                reply_markup=kb.manga_choose_chapter(
                    str(prev_manga[3]) + "-" + str(prev_manga[2]),
                    str(next_manga[3]) + "-" + str(next_manga[2]),
                    prev_manga[0],
                    next_manga[0],
                ),
                text=text,
                parse_mode="HTML",
                disable_web_page_preview=False,
            )


client.start()
client.run_until_disconnected()
