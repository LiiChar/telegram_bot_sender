def text_manga(manga) -> str:
    return f"""
<b>{manga[1]}</b>

Том {manga[3]} глава {manga[2]}
Прочитать <a href='{manga[4]}'>{manga[1]}</a> 
"""

manag_not_found="Манга по такому названию не найдена. Попробуйте снов или напишите /отмена"
welcome="""\
    Hi there, I am MangaBot.
Select yout favorite manga or reply from https://web.telegram.org/a/#-1001551102382\
    """
    
help="""
Возможности бота:
1. Искать мангу по названию
2. Добавлять мангу в закладки
3. При Добавлении манги в закладки вы подписывайтесь на рассылку новых глав
4. Запоминиме последней прочитанной главы

Способы добавления манги в закладки
1. Переслать мангу из группы 'Слив платных глав | LN Manga'
2. При поиске, появляется кнопка добавления на против названия
"""