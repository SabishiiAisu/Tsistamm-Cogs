from redbot.core import commands

class TestCog(commands.Cog):
    """My custom cog"""

    def __init__(self, bot):
        self.bot = bot
        # self.list = []
    
    @commands.command()
    async def test(self, ctx):
        """This does stuff!"""
        # Your code will go here
        await ctx.send("I can do stuff!")

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        user = self.bot.get_user(payload.user_id)
        if (user.bot):
            return
        channel = self.bot.get_channel(payload.channel_id)
        # self.list.append(self.bot.get_emoji(payload.emoji_id).name)
        await channel.send('I see you!')

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        user = self.bot.get_user(payload.user_id)
        if (user.bot):
            return
        channel = self.bot.get_channel(payload.channel_id)
        # self.list.remove(self.bot.get_emoji(payload.emoji_id).name)
        await channel.send('Stop hiding!')