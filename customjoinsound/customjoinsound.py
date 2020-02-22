import asyncio
import discord
import os

from redbot.core import commands
from redbot.core import data_manager
from redbot.core import Config

class CustomJoinSound(commands.Cog):
    # TODO: error handling
    #       help text

    def __init__(self):
        self.config = Config.get_conf(self, identifier=628874672)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        users = self.config.users()
        async with users as user_list:
            if str(member.id) in user_list:
                volume = user_list[str(member.id)]['volume']
                file_name = user_list[str(member.id)]['sfx']
                file_path = str(data_manager.cog_data_path(self)) + '/' + file_name
                if after.channel is not None and after.channel != member.guild.afk_channel and not await self.isrestricted(after.channel.id):
                    if before.channel is not None:
                        if before.channel.id != after.channel.id:
                            if os.path.isfile(file_path):
                                await self.playsound(file_path, volume, after.channel)
                    else:
                        if os.path.isfile(file_path):
                            await self.playsound(file_path, volume, after.channel)

    @commands.command()
    async def setjoinvol(self, ctx, username, volume: int):
        if isinstance(volume, int) and volume in range(1, 201):
            all_users = self.config.users()
            has_sound = False
            user_id = None
            async with all_users as user_list:
                for user in user_list:
                    if username == user_list[user]['display_name']:
                        has_sound = True
                        user_id = user
                if has_sound:
                    await self.config.set_raw('users', user_id, 'volume', value=volume)
                    await ctx.send("{}'s custom join sound volume set to {}.".format(username, volume))
                else:
                    await ctx.send('{} does not have a custom join sound!'.format(username))
        else:
            await ctx.send('Volume must be within the range 1-200.')

    @commands.command()
    async def getjoinvol(self, ctx, username):
        all_users = self.config.users()
        has_sound = False
        user_id = None
        async with all_users as user_list:
            for user in user_list:
                if username == user_list[user]['display_name']:
                    has_sound = True
                    user_id = user
            if has_sound:
                await ctx.send(user_list[user_id]['volume'])
            else:
                await ctx.send('{} does not have a custom join sound!'.format(username))

    @commands.command()
    async def setrestrictedchannel(self, ctx, channel_name):
        channel_id = None
        restricted_channels = await self.config.get_raw('restricted_channels')
        voice_channels = ctx.guild.voice_channels
        for channel in voice_channels:
            if channel.name == channel_name:
                channel_id = channel.id
        if channel_id not in restricted_channels:
            restricted_channels.append(channel_id)
            await self.config.restricted_channels.set(restricted_channels)
            await ctx.send('{} is now a restricted channel.'.format(channel_name))
        else:
            await ctx.send('{} is already a restricted channel'.format(channel_name))

    @commands.command()
    async def setjoin(self, ctx, username):
        if len(ctx.message.attachments)  == 1:
            join_file = ctx.message.attachments[0]
            ext = join_file.filename[-4:]
            user_id = None
            is_member = False
            for member in ctx.guild.members:
                if username == member.display_name:
                    is_member = True
                    user_id = member.id
            if is_member:            
                if ext == '.mp3':
                    user_list = await self.config.get_raw('users')
                    new_file_path = '{}/{}'.format(data_manager.cog_data_path(self), join_file.filename)
                    if user_id in user_list:
                        old_file_path = '{}/{}'.format(data_manager.cog_data_path(self), user_list[user_id]['sfx'])
                        if os.path.isfile(old_file_path):
                            os.remove(old_file_path)
                        user_list[user_id]['sfx'] = join_file.filename
                        user_list[user_id]['volume'] = 75
                        await join_file.save(new_file_path)
                        await self.config.users.set(user_list)
                    else:
                        user_list[user_id] = {"display_name" : username, "sfx" : join_file.filename, "volume" : 75}
                        await join_file.save(new_file_path)
                        await self.config.users.set(user_list)
                    await ctx.send("{}'s join sound has been set to {}.".format(username, join_file.filename[:-4]))
                else:
                    await ctx.send('Error: incorrect file extension! Please only upload mp3 files with this command!')
            else:
                await ctx.send("{} is not a member of this server!".format(username))
        else:
            await ctx.send("Missing attachment or added too many attachments! Please only upload a single mp3 file!")
    
    @commands.command()
    async def removejoin(self, ctx, username):
        user_list = await self.config.get_raw('users')
        has_sound = False
        user_id = None
        for user in user_list:
            if username == user_list[user]['display_name']:
                has_sound = True
                user_id = user
        if has_sound:
            old_file_path = '{}/{}'.format(data_manager.cog_data_path(self), user_list[user_id]['sfx'])
            if os.path.isfile(old_file_path):
                os.remove(old_file_path)
            user_list.pop(user_id)
            await self.config.users.set(user_list)
            await ctx.send("{}'s join sound has been removed.".format(username))
        else:
            await ctx.send("{} does not have a join sound!".format(username))
    
    async def isrestricted(self, channel):
        restricted_channels = await self.config.get_raw('restricted_channels')
        if channel in restricted_channels:
            return True
        else:
            return False

    async def playsound(self, file_path, volume, channel):
        voice_client = await channel.connect()
        raw_stream = discord.FFmpegPCMAudio(file_path)
        leveled_stream = discord.PCMVolumeTransformer(raw_stream, volume=volume/100)
        voice_client.play(leveled_stream)
        while voice_client.is_playing():
            await asyncio.sleep(1)
        voice_client.stop()
        await voice_client.disconnect()