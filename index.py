import discord
import yaml

from src.on_ready.on_ready import on_ready_handler

with open('run/config/tokens.yml', 'r') as file:
    tokens = yaml.safe_load(file)

client = discord.Client()


@client.event
async def on_ready():
    await on_ready_handler(client)


client.run(tokens['discord_token'])
