import telebot
import config
import kb
from utils import parse_message_text
from text import text_manga, welcome, help
from db import db

config.IS_SEARCH = False
bot = telebot.TeleBot(config.BOT_TOKEN)
keys = ["help", "start", "favorite"]


# Handle '/start'
@bot.message_handler(commands=["start"])
def handle_welcome(message):
    bot.send_message(message.chat.id, welcome)


@bot.message_handler(commands=["help"])
def handle_help(message):
    bot.send_message(message.chat.id, help)


@bot.message_handler(commands=["favorite"])
def handle_favorite_manga(message):
    user_id = db.create_user_or_return_id(message.chat.id)
    manga = db.get_manga_by_user(user_id)
    if len(manga) > 0:
        res = bot.send_message(chat_id=message.chat.id, text="List of manga")
        bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=res.message_id,
            text="List of manga",
            reply_markup=kb.list_manga(manga, user_id, res.message_id),
        )
        return
    else:
        bot.send_message(
            chat_id=message.chat.id,
            text="У вас отсутствует манга в закладках. Пополните закладки.",
        )
        return


@bot.message_handler(commands=["search"])
def handle_search_manga(message):
    config.IS_SEARCH = True
    bot.send_message(
        chat_id=message.chat.id, text="Введите название манги:", parse_mode="HTML"
    )
    return


@bot.message_handler(
    func=lambda message: config.IS_SEARCH is True
    and message.text.find("get_by_id:") < 0
    and message.text.find("get_by_chapter:") < 0
    and message.text.find("delete:") < 0
)
def search(message):
    manga = db.search_manga_by_name(message.text)
    if manga is not None and len(manga) > 0 and manga:
        user_id = db.create_user_or_return_id(message.chat.id)
        bot.send_message(
            chat_id=message.chat.id,
            text="Список найденных манг",
            reply_markup=kb.search_list_manga(manga, user_id),
            parse_mode="HTML",
        )
        config.IS_SEARCH = False
    else:
        bot.send_message(
            chat_id=message.chat.id, text="Манга не найдена", parse_mode="HTML"
        )
        config.IS_SEARCH = False


@bot.callback_query_handler(
    func=lambda call: call.data.find(":") > 0 and config.IS_SEARCH is False
)
def button_handler(call):
    user_manga_id = call.data.split(":")[1]
    method = call.data.split(":")[0]

    if method == "get_by_id":
        manga_name = db.get_manga_by_id(user_manga_id)
        user_id = db.create_user_or_return_id(call.from_user.id)
        manga = db.get_unread_less_manga(user_id, manga_name[1])
        if manga is None:
            bot.send_message(
                chat_id=call.from_user.id, text="Произошла ошибка на стороне сервера"
            )
        prev_manga = db.get_near_prev_or_next_manga_by_chapter(
            manga[1], manga[2], manga[3], "MAX"
        )
        next_manga = db.get_near_prev_or_next_manga_by_chapter(
            manga[1], manga[2], manga[3], "MIN"
        )
        text = text_manga(manga)
        bot.send_message(
            chat_id=call.from_user.id,
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
    if method == "get_by_chapter":
        part = user_manga_id.split("-")[1]
        chapter = user_manga_id.split("-")[0]
        manga_id = user_manga_id.split("-")[2]
        dir = user_manga_id.split("-")[3]
        name = db.get_manga_name_by_id(manga_id)
        user_id = db.create_user_or_return_id(call.from_user.id)
        print(user_id, manga_id)
        manga = db.create_manga_read_user(user_id, manga_id)
        print(manga)
        aggregator = "MIN"
        if dir == "next":
            aggregator = "MIN"
        else:
            aggregator = "MAX"
        near_manga = db.get_near_manga_by_chapter(name, part, chapter, aggregator)
        if not near_manga:
            bot.send_message(chat_id=call.from_user.id, text="Manga not found")
            return

        prev_manga = db.get_near_prev_or_next_manga_by_chapter(
            name, part, chapter, "MAX"
        )
        next_manga = db.get_near_prev_or_next_manga_by_chapter(
            name, part, chapter, "MIN"
        )

        text = text_manga(near_manga)
        bot.edit_message_text(
            chat_id=call.from_user.id,
            message_id=call.message.message_id,
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
        return

    if method == "add":
        manga_id = user_manga_id.split("-")[0]
        user_id = user_manga_id.split("-")[1]
        db.add_manga_user(user_id, manga_id)

    if method == "delete":
        manga_id = user_manga_id.split("-")[0]
        user_id = user_manga_id.split("-")[1]
        message_id = user_manga_id.split("-")[2]
        manga_name = db.get_manga_by_id(manga_id)[1]
        db.delete_manga_user_by_name_user_id(manga_name, user_id)
        manga = db.get_manga_by_user(user_id)
        if len(manga) <= 0 or manga is None:
            bot.edit_message_text(
                chat_id=call.from_user.id,
                message_id=message_id,
                text="У вас отсутствует манга в закладках. Пополните закладки.",
            )
            return
        bot.edit_message_text(
            chat_id=call.from_user.id,
            message_id=message_id,
            text="List of manga",
            reply_markup=kb.list_manga(manga, user_id, message_id),
            disable_web_page_preview=False,
        )


@bot.message_handler(
    func=lambda message: config.IS_SEARCH is False
    and not (
        message.text.find(":") > 0
        and (message.text.find("get") > 0 or message.text.find("delete") > 0)
    )
)
def reply_manga(message):
    if message.forward_from_chat is None:
        return
    if message.forward_from_chat.title != "Слив платных глав | LN Manga":
        bot.send_message(
            message.chat.id, text="Вы переслали сообщение не из нужной группы"
        )
        return

    manga = parse_message_text(message.text)
    is_exists_manga = db.get_manga_user_by_name(manga["name"])
    if len(is_exists_manga):
        bot.send_message(message.chat.id, text="Данная манга уже у вас в закладках")
        return
    manga["date"] = message.date
    manga_id = db.create_manga_or_return_id(manga)
    user_id = db.create_user_or_return_id(message.chat.id)
    if not user_id:
        bot.send_message(message.chat.id, text="Вы не вошли, сами в этом виноваты")
        return
    db.add_manga_user(user_id, manga_id)
    bot.send_message(
        message.chat.id, text=f"<<{manga['name']}>> добавлено в ваши закладки"
    )


bot.infinity_polling()
