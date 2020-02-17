from redbot.core import commands

class CustomJoinSound(commands.Cog):
    """My custom cog"""

    @commands.group()
    async def cjs(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("Invalid subcommand!")

    @cjs.command
    async def setsound(self, ctx):
        await ctx.send("Something!")