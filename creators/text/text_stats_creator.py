import aiohttp
from config import SERVER_URL
from datetime import date
import datetime
from utils.currency_codes import CURRENCY_NAMES


async def date_range(start, end):
    delta = end - start  # as timedelta
    days = [start + datetime.timedelta(days=i) for i in range(delta.days + 1)]
    return days


async def get_text_stats(chart_query: dict, chat_id):
    pass


