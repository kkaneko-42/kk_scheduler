import config
import re
import json
import discord
from discord.ext import commands
from discord import app_commands
from datetime import datetime, timedelta

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
    
    def __split_without_empty_str(self, str, delim):
        splited = str.split(delim)
        return [s for s in splited if s != ""]

    @app_commands.command(
        name        = "schedule",
        description = "Create new schedule"
    )
    @app_commands.guilds(config.GUILD_ID)
    @app_commands.guild_only() # Forbbiden using in DM
    @app_commands.describe(
        date            = "date description",
        title           = "title description",
        members         = "members description",
        contents        = "contents description",
        remind_delta    = "remind description"
    )
    async def schedule(
        self,
        interaction:    discord.Interaction,
        date:           str,
        title:          str,
        members:        str = "",
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
        members_id_parsed = list(map(
            lambda s: int(s.strip()[3:-1]),
            self.__split_without_empty_str(members, ",")
        ))

        # Parse remind_date
        remind_delta_parsed = self.__parse_remind_delta(remind_delta)

        # Construct schedule
        sche = {}
        sche["date"] = date_parsed.isoformat()
        sche["title"] = title
        sche["members_id"] = members_id_parsed
        sche["contents"] = contents
        sche["remind_date"] = (date_parsed - remind_delta_parsed).isoformat()
        print(json.dumps(sche))

        # Append the schedule
        self._schedules.append(sche)

        await interaction.response.send_message("accepted")

async def setup(bot):
    await bot.add_cog(KKScheduler(bot))
    print("cog.kk_scheduler loaded")
