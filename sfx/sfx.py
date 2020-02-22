import asyncio
import discord
import os

from redbot.core import commands
from redbot.core import data_manager
from redbot.core import Config

class Sfx(commands.Cog):
    # TODO: remove sfx
    #       rename sfx
    #       replace sfx
    #       queuing
    #           If a request occurs during playback queue it so playback is seamless
    #       back up
    #       retrieve sfx file
    #       help text

    def __init__(self):
        self.config = Config.get_conf(self, identifier=628874671)

    @commands.command()
    async def sfx(self, ctx, sfx_name):
        user = ctx.author
        voice_channel = user.voice.channel
        sfx_list = await self.config.get_raw('sfx')
        if sfx_name in sfx_list:
            vol = sfx_list[sfx_name]['volume']
            file_path = '{}/{}.mp3'.format(data_manager.cog_data_path(self), sfx_name)
            if os.path.isfile(file_path):
                if voice_channel != None:
                    await self.playsound(file_path, vol, voice_channel)
                else:
                    await ctx.send('User is not in a channel.')
            else:
                await ctx.send("Can't seem to find the file. Please contact an admin!")
        else:
            await ctx.send('{} does not exist!'.format(sfx_name))
    
    @commands.command()
    async def addsfx(self, ctx, sfx_name, volume=75):
        sfx_list = await self.config.get_raw('sfx')
        if sfx_name in sfx_list:
            await ctx.send('{} already exists!'.format(sfx_name))
        else:
            if len(ctx.message.attachments) == 1:
                sfx_file = ctx.message.attachments[0]
                ext = sfx_file.filename[-4:]
                if ext == '.mp3':
                    new_file = '{}/{}'.format(data_manager.cog_data_path(self), sfx_file.filename)
                    await sfx_file.save(new_file)
                    sfx_list[sfx_name] = {"volume" : volume}
                    await self.config.sfx.set(sfx_list)
                    await ctx.send('{} has been added at volume {}!'.format(sfx_name, volume))
                else:
                    await ctx.send('Error: incorrect file extension! Please only upload mp3 files with this command!')
            else:
                await ctx.send("Missing attachment or added too many attachments! Please only upload a single mp3 file!")
    
    @commands.command()
    async def setvol(self, ctx, sfx_name, volume: int):
        if isinstance(volume, int) and volume in range(1, 201):
            sfx_list = await self.config.get_raw('sfx')
            if sfx_name in sfx_list:
                await self.config.set_raw('sfx', sfx_name, 'volume', value=volume)
                await ctx.send('{} set to volume {}.'.format(sfx_name, volume))
            else:
                await ctx.send('{} does not exist!'.format(sfx_name))
        else:
            await ctx.send('Volume must be within the range 1-200.')

    @commands.command()
    async def getvol(self, ctx, sfx_name):
        sfx_list = await self.config.get_raw('sfx')
        if sfx_name in sfx_list:
            await ctx.send(sfx_list[sfx_name]['volume'])
        else:
            await ctx.send('{} does not exist!'.format(sfx_name))

    @commands.command()
    async def allsfx(self, ctx):
        # TODO: DM list of all sfx
        sfx_list = await self.config.get_raw('sfx')
        embed = discord.Embed()
        message = ''
        for val in sfx_list:
            message += val + '\n'
        embed.title = 'List of available SFX:'
        embed.description = message
        await ctx.author.send(embed=embed)
    
    async def playsound(self, file_path, volume, channel):
        voice_client = await channel.connect()
        raw_stream = discord.FFmpegPCMAudio(file_path)
        leveled_stream = discord.PCMVolumeTransformer(raw_stream, volume=volume/100)
        voice_client.play(leveled_stream)
        while voice_client.is_playing():
            await asyncio.sleep(1)
        voice_client.stop()
        await voice_client.disconnect()
        