import asyncio
import nntplib
import re
from datetime import datetime, timedelta
from typing import *

import discord
import pytz
import yaml

from src.utils.api_manager import APIManager
from src.utils.datetime_utils import get_date
from src.utils.embed_manager import EmbedsManager
from src.utils.log_manager import LogManager


class NewsGroupManager:
    NNTP: nntplib.NNTP = None
    address: str = None
    groups: Dict = None
    encoding: str = None
    config: Dict = None
    delta_time: str = None
    client: discord.Client
    api_manager: APIManager
    stop_on_error: bool = None
    date_format: str = None
    assistants: List = None

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
        self.date_format = self.config["date_format"]
        self.stop_on_error = self.config["stop_on_error"]
        self.delta_time = self.config["delta_time"]
        self.assistants = self.config["assistants"]

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
        ref = None if "References" not in info else info["References"]
        match = re.search('.*<(.*)>', author)
        mail = match.group(1) if match else ""
        subject = info["Subject"]
        date = get_date(info["Date"])

        _, body = self.NNTP.body(news_id)
        content = ""
        for l in body.lines:
            content += l.decode(self.encoding) + "\n"

        is_assistant = mail in self.assistants
        # get the tags
        tags = []
        if subject[:4] != "Re: ":
            subject = subject[4:]
        s = subject.split("]", 1)
        while len(s) != 1:
            tags.append((s[0])[1:])
            s = s[1].split("]", 1)
        subject = s[0]

        # slice the msg in chunk of 5120 char
        msg = [content[i:i + 5117] for i in range(0, len(content), 5117)]

        # print msg in every channel newsgroup_filler_embed
        if is_assistant:
            embed = EmbedsManager.newsgroup_embed_assistant(subject, tags, msg[0], author,
                                                            date, group["name"], ref is not None)
        else:
            embed = EmbedsManager.newsgroup_embed(subject, tags, author, date, group["name"], ref is not None)

        for guild in group['channels']:
            await self.client.get_channel(int(guild['channel_id'])).send(embed=embed)

        if not is_assistant:
            return

        for i in range(1, len(msg)):
            embed = EmbedsManager.newsgroup_filler_embed("..." + msg[i], author, date, group["name"], ref is not None)
            for guild in group['channels']:
                await self.client.get_channel(int(guild['channel_id'])).send(embed=embed)

    async def print_news_from_group(self, group: Dict):
        last_update: datetime = datetime.strptime(group["last_update"], self.date_format) \
            .astimezone(pytz.timezone("Europe/Paris"))

        _, news = self.NNTP.newnews(group['slug'], last_update)

        for news_id in list(dict.fromkeys(news)):
            try:
                await self.print_news(group.copy(), news_id)
            except Exception as exe:
                print("err for news {}".format(news_id))
                if self.stop_on_error:
                    raise exe
                await LogManager.error_log(self.client, "Newsgroup error for news : {}\n{}".format(news_id, exe))

        if len(news) == 0:
            return
        group["last_update"] = (datetime.now() + timedelta(seconds=1)) \
            .astimezone(pytz.timezone("Europe/Paris")) \
            .strftime(self.date_format)

        b, reason = self.api_manager.edit_data("news-groups",
                                               id=group["id"],
                                               last_update=group["last_update"])

        if not b:
            raise Exception("cannot send information to server, reason: {}".format(reason))

    async def get_news(self):
        try:

            # Load data from API
            state, res = self.api_manager.get_data('news-groups')

            # Check if we get a response from the API
            if not state:
                return

            # Start the connection
            self.open_connection()

            # For each news group, do magic
            for group in res:
                await self.print_news_from_group(group)

            self.close_connection()
        except Exception as exe:
            if self.stop_on_error:
                raise exe
            await LogManager.error_log(self.client, "Newsgroup error while updating\n{}".format(exe))

        await asyncio.sleep(int(self.delta_time))
