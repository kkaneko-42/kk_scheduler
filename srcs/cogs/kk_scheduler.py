from discord.ext import commands

class KKScheduler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
        print("initialized")

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Logged in as {self.bot.user}")

    @commands.command()
    async def hello(self, ctx):
        await ctx.send("hello!")

async def setup(bot):
    await bot.add_cog(KKScheduler(bot))
    print("cog.kk_scheduler loaded")
