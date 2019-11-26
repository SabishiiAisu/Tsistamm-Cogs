from redbot.core import commands

class TestCog(commands.Cog):
    """My custom cog"""

    @commands.command()
    async def test(self, ctx):
        """This does stuff!"""
        # Your code will go here
        await ctx.send("I can do stuff!")
    
    @commands.Cog.listener()
    async def on_reaction_add(self, ctx, reaction, user):
        channel = reaction.message.channel
        await ctx.send_message(channel, '{} has added {} to the message: {}'.format(user.name, reaction.emoji, reaction.message.content))

    @commands.Cog.listener()
    async def on_reaction_remove(self, ctx, reaction, user):
        channel = reaction.message.channel
        await ctx.send_message(channel, '{} has removed {} from the message: {}'.format(user.name, reaction.emoji, reaction.message.content))