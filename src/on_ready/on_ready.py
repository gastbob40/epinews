import discord
import yaml
import datetime

from src.on_ready.newsgroup.get_news import get_news


async def on_ready_handler(client: discord.Client):
    print('We have logged in as {0.user}'.format(client))
    await get_news(client)
