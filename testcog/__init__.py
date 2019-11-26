from .testcog import TestCog

async def setup(bot):
    cog = TestCog(bot)
    bot.add_cog(cog)