from redbot.core import commands

class TestCog(commands.Cog):
    """My custom cog"""

    def __init__(self, bot):
        self.bot = bot
        self.owner = bot.get_user(136242970000097280)
        self.mylist = [1,2,3,4]
    
    @commands.command()
    async def test(self, ctx):
        """This does stuff!"""
        # Your code will go here
        author = ctx.author
        await author.send(self.mylist)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        author = self.bot.get_user(payload.user_id)
        if author.bot or author != self.owner):
            return
        # channel = self.bot.get_channel(payload.channel_id)
        # self.list.append(self.bot.get_emoji(payload.emoji_id).name)
        await author.send('I see you!')

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        author = self.bot.get_user(payload.user_id)
        if (author.bot or author != self.owner):
            return
        # channel = self.bot.get_channel(payload.channel_id)
        # self.list.remove(self.bot.get_emoji(payload.emoji_id).name)
        await author.send('Stop hiding!')