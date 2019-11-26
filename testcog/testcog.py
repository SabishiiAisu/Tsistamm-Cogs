from redbot.core import commands

class TestCog(commands.Cog):
    """My custom cog"""

    @commands.command()
    async def test(self, ctx):
        """This does stuff!"""
        # Your code will go here
        await ctx.send("I can do stuff!")
    
    @client.event
    async def on_reaction_add(reaction, user):
        channel = reaction.message.channel
        await client.send_message(channel, '{} has added {} to the message: {}'.format(user.name, reaction.emoji, reaction.message.content))

    @client.event
    async def on_reaction_remove(reaction, user):
         channel = reaction.message.channel
        await client.send_message(channel, '{} has removed {} from the message: {}'.format(user.name, reaction.emoji, reaction.message.content))
