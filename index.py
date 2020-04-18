import discord
import yaml

from src.on_ready.on_ready import on_ready_handler
from src.utils.api_manager import APIManager

sanctions_manager = APIManager()

# An example
# a = sanctions_manager.get_data('news-groups')[1][1]
# sanctions_manager.edit_data('news-groups', a['id'], name="testresdsfs")
# print(a)

with open('run/config/tokens.yml', 'r') as file:
    tokens = yaml.safe_load(file)

client = discord.Client()


@client.event
async def on_ready():
    await on_ready_handler(client)


client.run(tokens['discord_token'])