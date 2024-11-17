import asyncio
import json

import aiohttp

from src.app.delivery.repository.cache_tools import RedisTools
from src.app.config import settings


async def fetch_content(url, session):
    async with session.get(url, allow_redirects=True) as response:
        content = await response.read()
        data = json.loads(content)
        value = data['Valute']['USD']['Value']
        return value


async def get_currency_exchange_rate():
    url = settings.get_url_currency_exchange_rate
    async with aiohttp.ClientSession() as session:
        task = await asyncio.create_task(fetch_content(url, session))
        await RedisTools.set_pair('rate_usd', task)
