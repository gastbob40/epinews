from datetime import datetime, timedelta
import discord
import pytz


class EmbedsManager:

    @staticmethod
    def debug_embed(content):
        embed = discord.Embed(color=0xEFCC00) \
            .set_author(icon_url="https://cdn0.iconfinder.com/data/icons/simply-orange-1/128/questionssvg-512.png",
                        name="Additional information.")
        embed.timestamp = datetime.now() - timedelta(hours=2)
        embed.description = content
        return embed

    @staticmethod
    def error_embed(content):
        embed = discord.Embed(color=0xD72727) \
            .set_author(icon_url="https://cdn0.iconfinder.com/data/icons/shift-free/32/Error-512.png",
                        name="An error has occurred.")
        embed.timestamp = datetime.now().astimezone(pytz.timezone("Europe/Paris"))
        embed.description = content
        return embed

    colors = ["css\n", "http\n", "cs\n# ", "yaml\n", "md\n# ", "\n"]

    @staticmethod
    def newsgroup_embed(title, tags, msg, author, date: datetime, group, is_response):
        if is_response:
            embed = discord.Embed(color=0xc40c0c, title="Re:" + title)
        else:
            embed = discord.Embed(color=0x0080ff, title=title)
        for tag in tags:
            color = sum([ord(c) for c in tag]) % 5
            embed.add_field(name="​", value="```{}{}```".format(EmbedsManager.colors[color], tag), inline=True)
        parts = [msg[i:i+1021] for i in range(0, len(msg), 1021)]
        embed.add_field(name="{}\n{}".format(author, date.strftime("%a, %d %b %Y %H:%M:%S")), value=parts[0], inline=False)
        for i in range(1, len(parts)):
            embed.add_field(name="​", value="..." + parts[i], inline=False)
        embed.set_footer(text=group)
        return embed

    @staticmethod
    def newsgroup_filler_embed(msg, author, date: datetime, group, is_response):
        if is_response:
            embed = discord.Embed(color=0xc40c0c)
        else:
            embed = discord.Embed(color=0x0080ff)
        parts = [msg[i:i+1021] for i in range(0, len(msg), 1021)]
        embed.add_field(name="{}\n{}".format(author, date.strftime("%a, %d %b %Y %H:%M:%S")), value=parts[0], inline=False)
        for i in range(1, len(parts)):
            embed.add_field(name="​", value="..." + parts[i], inline=False)
        embed.set_footer(text=group)
        return embed



