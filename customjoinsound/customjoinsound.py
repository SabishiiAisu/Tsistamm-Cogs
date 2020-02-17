from redbot.core import commands

class CustomJoinSound(commands.Cog):
    """My custom cog"""

    @commands.command()
    async def cjs(self, ctx):
        await ctx.send("Something!")