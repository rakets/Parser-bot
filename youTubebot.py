from youtube_search import YoutubeSearch
from config import TOKEN
from aiogram import Bot, types, utils
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import InputTextMessageContent, InlineQueryResultArticle
import hashlib

def searcher(text):
    res = YoutubeSearch(text, max_results = 10).to_dict()
    return res

#inicializd bot
bot = Bot(token=TOKEN)

#create dispatcher
dp = Dispatcher(bot)

@dp.inline_handler()
async def inline_handler(query : types.InlineQuery):
    text = query.query or 'echo'
    links = searcher(text)

    articles = [types.InlineQueryResultArticle(
        id = hashlib.md5(f'{link["id"]}'.encode()).hexdigest(),
        title = f'{link["title"]}',
        url = f'https://www.youtube.com/watch?v={link["id"]}',
        thumb_url = f'{link["thumbnails"][0]}',
        input_message_content=types.InputTextMessageContent(
            message_text = f'https://www.youtube.com/watch?v={link["id"]}')
    ) for link in links]

    await query.answer(articles, cache_time=60, is_personal=True) #Отправка результатов встроенного запроса пользователю.

#create executor(start of polling)
executor.start_polling(dp, skip_updates=True)







