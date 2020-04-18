import discord
import yaml
import datetime

from src.on_ready.newsgroup.newsgroup_manager import NewsGroupManager


async def on_ready_handler(client: discord.Client):
    print('We have logged in as {0.user}'.format(client))
    manager = NewsGroupManager(client)
    while True:
        await manager.get_news()
