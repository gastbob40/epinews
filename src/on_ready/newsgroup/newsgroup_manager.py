import nntplib
from typing import *
from datetime import datetime, timedelta
import yaml
import pytz
import discord
import asyncio

from src.utils.datetime_utils import get_date
from src.utils.log_manager import LogManager
from src.utils.embed_manager import EmbedsManager
from src.utils.api_manager import APIManager


class NewsGroupManager:

    NNTP: nntplib.NNTP = None
    address: str = None
    groups: Dict = None
    encoding: str = None
    config: Dict = None
    delta_time: str = None
    client: discord.Client
    api_manager: APIManager

    def __init__(self, client: discord.Client):
        self.client = client
        self.get_config()
        self.api_manager = APIManager()

    def open_connection(self):
        try:
            self.NNTP = nntplib.NNTP(self.address)
        except Exception as e:
            print("Error when opening nntp connection")
            raise e

    def close_connection(self):
        try:
            self.NNTP.quit()
        except Exception as e:
            print("Error when closing nntp connection")
            raise e

    def get_config(self):
        with open('run/config/config_newsgroups.yml', 'r') as file:
            self.config = yaml.safe_load(file)
        self.address = self.config["address"]
        self.encoding = self.config["encoding"]
        self.delta_time = self.config["delta_time"]

    def get_info_from_news(self, news_id: str) -> Dict:
        info = dict()
        _, head = self.NNTP.head(news_id)
        last = "NULL"
        for l in head.lines:
            s = l.decode(self.encoding).split(": ", 1)
            if len(s) != 2:
                info[last] = info[last] + nntplib.decode_header(s[0])
                continue
            last = s[0]
            info[s[0]] = nntplib.decode_header(s[1])
        return info

    async def print_news(self, group: Dict, news_id: str):
        info = self.get_info_from_news(news_id)
        author = info["From"]
        subject = info["Subject"]
        date = get_date(info["Date"])

        _, body = self.NNTP.body(news_id)
        content = ""
        for l in body.lines:
            content += l.decode(self.encoding) + "\n"

        # handle response
        is_response = False
        if subject[:4] == "Re: ":
            subject = subject[4:]
            is_response = True

        # get the tags
        tags = []
        s = subject.split("]", 1)
        while len(s) != 1:
            tags.append((s[0])[1:])
            s = s[1].split("]", 1)
        subject = s[0]

        # slice the msg in chunk of 5120 char
        msg = [content[i:i + 5117] for i in range(0, len(content), 5117)]

        # print msg in every channel newsgroup_filler_embed
        embed = EmbedsManager.newsgroup_embed(subject, tags, msg[0], author, date, group["name"],
                                              is_response)
        for guild in group['channels']:
            await self.client.get_channel(int(guild['channel_id'])).send(embed=embed)

        for i in range(1, len(msg)):
            embed = EmbedsManager.newsgroup_filler_embed("..." + msg[i], author, date, group["name"], is_response)
            for guild in group['channels']:
                await self.client.get_channel(int(guild['channel_id'])).send(embed=embed)

        return date

    async def print_news_from_group(self, group: Dict):
        last_update: datetime = datetime.strptime(group["last_update"], "%d/%m/%Y %H:%M:%S") \
            .astimezone(pytz.timezone("Europe/Paris"))

        _, news = self.NNTP.newnews(group['slug'], last_update)

        for i, news_id in enumerate(news):
            try:
                d: datetime = await self.print_news(group.copy(), news_id)
                if d > last_update:
                    last_update = d
            except Exception as exe:
                await LogManager.error_log(self.client, "Newsgroup error for news : {}\n{}".format(i, exe))

        group["last_update"] = (last_update + timedelta(seconds=1))\
            .astimezone(pytz.timezone("Europe/Paris")) \
            .strftime("%d/%m/%Y %H:%M:%S")

    async def get_news(self):
        try:

            # Load data from API
            state, res = self.api_manager.get_data('news-groups')

            # Check if we get a response from the API
            if not state:
                return

            # Start the connection
            self.open_connection()

            await LogManager.error_log(self.client, "Res: {}\n".format(res))

            # For each news group, do magic
            for group in res:
                await self.print_news_from_group(group)

            self.close_connection()

            # TODO: push updated res with API

            await asyncio.sleep(int(self.delta_time))
        except Exception as exe:
            await LogManager.error_log(self.client, "Newsgroup error while updating\n{}".format(exe))
