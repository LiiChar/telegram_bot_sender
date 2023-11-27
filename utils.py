import logging


def parse_message_text(text):
    try:
        manga = {}
        split_text = text.split("\n")
        manga["name"] = split_text[0]
        info_chapter = split_text[1].split(" ")
        manga["chapter"] = info_chapter[2]
        manga["part"] = info_chapter[0]
        manga["link"] = text[text.rfind("https") :]
        return manga
    except:  # noqa: E722
        logging.error("Parse message text failed")
