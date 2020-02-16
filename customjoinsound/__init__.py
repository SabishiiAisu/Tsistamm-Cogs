from .customjoinsound import CustomJoinSound

async def setup(bot):
    cog = CustomJoinSound(bot)
    bot.add_cog(cog)