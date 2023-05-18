import discord
import config
from discord.ext import commands
from discord import app_commands
from typing import Tuple
from datetime import datetime

class Schedule():
    def __init__(self, date, members_id):
        self.date: datetime         = date
        self.members_id: List[int]  = members_id
        self.contents: str          = ""
        self.remind_date: datetime  = None

    def __str__(self):
        # begin json
        result = "{"

        # date
        result += f"\"date\": {self.date}"
        # members_id
        result += ", \"members\": ["
        for id in self.members_id:
            result += str(id)
            if id != self.members_id[-1]:
                result += ", "
        result += "]"
        # contents
        result += f", \"contents\": \"{self.contents}\""
        # remind_date
        result += f", \"remind_date\": {self.remind_date}"

        # end json
        result += "}"
        return result

class KKScheduler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
        print("initialized")

    @commands.Cog.listener()
    async def on_ready(self):
        # Guild command
        await self.bot.tree.sync(guild=discord.Object(config.GUILD_ID))
        print(f"Logged in as {self.bot.user}")

    @commands.command()
    async def hello(self, ctx):
        await ctx.send("hello!")

    @app_commands.command(
        name        = "schedule",
        description = "Create new schedule"
    )
    @app_commands.guilds(config.GUILD_ID)
    @app_commands.guild_only() # Forbbiden using in DM
    @app_commands.describe(
        date        = "date description",
        members     = "members description",
        contents    = "contents description",
        remind_date = "remind description"
    )
    async def schedule(
        self,
        interaction: discord.Interaction,
        date:        str,
        members:     discord.Member,
        contents:    str = "",
        remind_date: str = None
    ):
        date_parsed = datetime.strptime(date, "%m/%d %H:%M")
        sche = Schedule(date_parsed, [members.id])
        print(sche)
        await interaction.response.send_message("accepted")

async def setup(bot):
    await bot.add_cog(KKScheduler(bot))
    print("cog.kk_scheduler loaded")
