import asyncio

import valve.source.a2s
from discord import Embed, Color
from discord.errors import NotFound
from discord.ext import commands
from valve.source import NoResponseError

from utils import settings


class Query(commands.Cog, name="Query"):
    def __init__(self, bot):
        self.bot = bot
        self.config = {}
        if settings.check_existence("query.json"):
            self.config = settings.get("query.json")
        self.bot.add_listener(self.messagedelete, "on_message_delete")
        self.bot.add_listener(self.guildjoin, "on_guild_join")
        self.bot.add_listener(self.onready, "on_ready")

    @commands.Cog.listener()
    async def messagedelete(self, message):
        try:
            self.config[str(message.guild.id)].remove(message.id)
            settings.save(self.config, "query.json")
        except ValueError:
            pass

    @commands.Cog.listener()
    async def guildjoin(self, guild):
        if str(guild.id) not in self.config:
            self.config[str(guild.id)] = []
            settings.save(self.config, "query.json")

    @commands.command(pass_context=True, description='Add server to check status for', usage="!addserver IP Query_Port")
    @commands.has_permissions(manage_channels=True)
    async def addserver(self, ctx, ip, query_port: int, appid=None):
        try:
            with valve.source.a2s.ServerQuerier((ip, query_port)) as server:
                info = server.info()
        except NoResponseError:
            await ctx.send("No response from the server. Make sure your IP and Query Port are correct!")
            return
        embed = Embed(title=info["server_name"], description=f"{ip}:{query_port}", color=Color.green())
        if appid is None:
            embed.set_thumbnail(url=f"https://steamcdn-a.akamaihd.net/steam/apps/{info['app_id']}/logo.png")
        else:
            embed.set_thumbnail(url=f"https://steamcdn-a.akamaihd.net/steam/apps/{appid}/logo.png")
        embed.add_field(name="Player Count", value=info['player_count'], inline=True)
        message = await ctx.send(embed=embed)
        self.config[str(ctx.guild.id)].append([message.channel.id, message.id])
        settings.save(self.config, "query.json")

    @addserver.error
    async def addserver_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(error)
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send("You do not have permission to perform that command!")
        else:
            print(error)

    @commands.Cog.listener()
    async def onready(self):
        for guild in self.bot.guilds:
            if str(guild.id) not in self.config:
                self.config[str(guild.id)] = []
                settings.save(self.config, "query.json")
        self.bot.loop.create_task(self.check_query())

    async def check_query(self):
        while True:
            messages = []
            for guild in self.config:
                for message in self.config[guild]:
                    try:
                        channel = self.bot.get_channel(message[0])
                        if channel is None:
                            raise TypeError("Channel can't be type None")
                        messages.append(await channel.fetch_message(message[1]))
                    except NotFound:
                        self.config[guild].remove(message)
                        settings.save(self.config, "query.json")
                    except TypeError:
                        self.config[guild].remove(message)
                        settings.save(self.config, "query.json")

            for message in messages:
                old_embed = message.embeds[0]
                ip_port = message.embeds[0].description.split(":")
                title = old_embed.title
                try:
                    with valve.source.a2s.ServerQuerier((ip_port[0], int(ip_port[1]))) as server:
                        info = server.info()
                    title = info["server_name"]
                    color = Color.green()
                    player_count = info['player_count']
                except NoResponseError:
                    color = Color.red()
                    player_count = 0
                if old_embed.color != color or old_embed.fields[0].value != str(player_count):
                    embed = Embed(title=title, description=old_embed.description, color=color)
                    embed.set_thumbnail(url=old_embed.thumbnail.url)
                    embed.add_field(name="Player Count", value=player_count, inline=True)
                    await message.edit(embed=embed)
            await asyncio.sleep(5)


def setup(bot):
    bot.add_cog(Query(bot))
