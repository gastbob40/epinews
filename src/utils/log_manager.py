import discord
import yaml

from src.utils.api_manager import APIManager
from src.utils.embed_manager import EmbedsManager

api_manager = APIManager()


class LogManager:

    @staticmethod
    async def debug_log(client: discord.Client, error_content: str):
        main_channel_log = client.get_channel(699646458827374614)
        embed = EmbedsManager.debug_embed(error_content)
        if main_channel_log:
            await main_channel_log.send(embed=embed)

    @staticmethod
    async def error_log(client: discord.Client, error_content: str):
        main_channel_log = client.get_channel(699646458827374614)
        embed = EmbedsManager.error_embed(error_content)
        if main_channel_log:
            await main_channel_log.send(embed=embed)
