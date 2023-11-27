from telebot import types
import logging

crossIcon = "\u274C"
apllyIcon = "\u2714\uFE0F"


def list_manga(manga, user_id, message_id=False):
    try:
        markup = types.InlineKeyboardMarkup()

        for m in manga:
            markup.add(
                types.InlineKeyboardButton(
                    text=m[1],
                    callback_data=f"get_by_id:{m[0]}",
                ),
                types.InlineKeyboardButton(
                    text=crossIcon,
                    callback_data=f"delete:{m[0]}-{user_id}-{message_id}",
                ),
                row_width=5,
            )

        return markup
    except:  # noqa: E722
        logging.error("Create markup anime list failed")


def search_list_manga(manga):
    try:
        markup = types.InlineKeyboardMarkup()

        for m in manga:
            markup.add(
                types.InlineKeyboardButton(
                    text=m[1],
                    callback_data=f"get_by_id:{m[0]}",
                )
            )

        return markup
    except:  # noqa: E722
        logging.error("Create markup search manga list failed")


def manga_choose_chapter(prev_id, next_id, is_prev=True, is_next=True):
    try:
        markup = types.InlineKeyboardMarkup()
        if is_prev is not None and is_next is None:
            markup.add(
                types.InlineKeyboardButton(
                    text=prev_id,
                    callback_data=f"get_by_chapter:{prev_id}-{is_prev}-prev",
                )
            )
        elif is_prev is None and is_next is not None:
            markup.add(
                types.InlineKeyboardButton(
                    text=next_id,
                    callback_data=f"get_by_chapter:{next_id}-{is_next}-next",
                )
            )
        elif is_prev is not None and is_next is not None:
            markup.add(
                types.InlineKeyboardButton(
                    text=prev_id,
                    callback_data=f"get_by_chapter:{prev_id}-{is_prev}-prev",
                ),
                types.InlineKeyboardButton(
                    text=next_id,
                    callback_data=f"get_by_chapter:{next_id}-{is_next}-next",
                ),
            )

        return markup
    except:  # noqa: E722
        logging.error("Create markup manga_choose_chapter failed")
