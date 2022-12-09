import logging
import hashlib
from aiogram import Bot, types
from aiogram.types import InputTextMessageContent, InlineQueryResultArticle
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from youtube_search import YoutubeSearch
from config import TOKEN

logging.basicConfig(level=logging.INFO)

bot = Bot(TOKEN)
dp = Dispatcher(bot)


def searcher(request: str):
    response = YoutubeSearch(request, max_results=10).to_dict()
    return response


@dp.inline_handler()
async def inline_handler(query: types.InlineQuery):
    message_text = query.query or 'echo'
    links = searcher(message_text)

    articles = [InlineQueryResultArticle(
        id=hashlib.md5(f"{link['id']}".encode()).hexdigest(),
        title=f"{link['title']}",
        url=f"https://www.youtube.com/watch?v={link['id']}",
        thumb_url=f"{link['thumbnails'][0]}",
        input_message_content=types.InputMessageContent(
            message_text=f"https://www.youtube.com/watch?v={link['id']}")
    ) for link in links]

    await query.answer(articles, cache_time=60, is_personal=True)


if __name__ == '__main__':
    executor.start_polling(dp)
