from redbot.core import commands

class CustomJoinSound(commands.Cog):
    """My custom cog"""

    def __init__(self, bot):
        self.bot = bot
        self.owner = bot.get_user(136242970000097280)
        self.mylist = []
    
    @commands.group()
    async def cjs(ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send('Invalid subcommand passed...')

    @cjs.command()
    async def setsound(ctx):
        await ctx.send('Setting sound!')