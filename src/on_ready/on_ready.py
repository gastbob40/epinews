import discord
import yaml
import datetime

from src.on_ready.newsgroup.newsgroup_manager import NewsGroupManager


async def on_ready_handler(client: discord.Client):
    print('We have logged in as {0.user} on {1}'.format(client,
                                                        datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S%z")))
    manager = NewsGroupManager(client)
    while True:
        # print("new get news at {}".format(datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S%z")))
        await manager.get_news()
