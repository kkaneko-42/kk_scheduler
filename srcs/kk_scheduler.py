import config
import re
import discord
from discord.ext import commands
from discord import app_commands
from typing import List
from datetime import datetime, timedelta

class Schedule():
    def __init__(self, date, members_id):
        self.date: datetime             = date
        self.members_id: List[int]      = members_id
        self.contents: str              = ""
        self.remind_delta: timedelta    = timedelta()

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
        result += f", \"remind_delta\": {self.remind_delta}"

        # end json
        result += "}"
        return result

class KKScheduler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
        self._schedules = []
        print("initialized")

    @commands.Cog.listener()
    async def on_ready(self):
        # Guild command
        await self.bot.tree.sync(guild=discord.Object(config.GUILD_ID))
        print(f"Logged in as {self.bot.user}")

    def __parse_remind_delta(self, str):
        days = re.findall("(\d+)d", str)
        hours = re.findall("(\d+)h", str)
        minutes = re.findall("(\d+)m", str)

        res = timedelta(
            days = int(days[0]) if len(days) != 0 else 0,
            hours = int(hours[0]) if len(hours) != 0 else 0,
            minutes = int(minutes[0]) if len(minutes) != 0 else 0
        )
        return res

    @app_commands.command(
        name        = "schedule",
        description = "Create new schedule"
    )
    @app_commands.guilds(config.GUILD_ID)
    @app_commands.guild_only() # Forbbiden using in DM
    @app_commands.describe(
        date            = "date description",
        members         = "members description",
        contents        = "contents description",
        remind_delta    = "remind description"
    )
    async def schedule(
        self,
        interaction:    discord.Interaction,
        date:           str,
        members:        str,
        contents:       str = "",
        remind_delta:   str = ""
    ):
        # Parse date
        date_parsed = datetime.strptime(date, "%m/%d %H:%M")
        # TODO: 12 -> 1 case
        date_parsed = date_parsed.replace(year = datetime.now().year)

        # Parse members id
        # Format: <@{id}>
        # NOTE: Slice [3:-1] in order to get id only
        members_id_parsed = list(map(lambda s: int(s.strip()[3:-1]), members.split(",")))

        # Parse remind_date
        remind_delta_parsed = self.__parse_remind_delta(remind_delta)

        # Construct schedule
        sche = Schedule(date_parsed, members_id_parsed)
        sche.contents = contents
        sche.remind_delta = remind_delta_parsed

        # Append the schedule
        self._schedules.append(sche)

        await interaction.response.send_message("accepted")

async def setup(bot):
    await bot.add_cog(KKScheduler(bot))
    print("cog.kk_scheduler loaded")
