import discord
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
from discord.ext import commands
import asyncio
# 🔐🤖👾

load_dotenv()

terminal = int(os.getenv('terminal'))
guild_id = int(os.getenv('server_id'))
bot_token = os.getenv('bot_token')
best_dog = int(os.getenv('best_dog'))
meowking = int(os.getenv('meowking'))
mathman = int(os.getenv('mathman'))
erebus = int(os.getenv('erebus'))
haagen = int(os.getenv('haagen'))
general = int(os.getenv('general'))
client = discord.Client()


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')


@client.event
async def on_message(message):
    global terminal
    server = client.get_guild(guild_id)
    terminal = client.get_channel(terminal)
    if message.content == '!purgeall':
        await message.channel.purge(limit=125)
    elif message.content == '!hello':
        await message.channel.send("Hi!")  # if the user says !hello, we will send back hi
    elif message.content == '!woof':
        await message.channel.send(f'<@{best_dog}>, you are best meow. _meows erratically_')
    elif message.content == '!users':
        await message.channel.purge(limit=1)
        await message.channel.send(f'# of Members: {server.member_count}')
    elif message.content == '!meowking':
        await message.channel.purge(limit=1)
        await message.channel.send(f'<@{meowking}> Raid/Help/Emergency')
    elif "guys" in message.content:
        await message.channel.send('Hi! "Guys" is an inherently gendered pronoun, even if you didn\'t mean it that '
                                   'way. And since we have lots of stellar folks of all genders in this discord, we '
                                   'want to be inclusive of all. "Everyone", "folks", "team", and "y\'all" are all '
                                   'great replacements. :heart: Spudnik')
    elif message.content == '!meow':
        await message.channel.send('https://www.youtube.com/watch?v=X1kOBNWQO0E')
    elif message.content == '!help':
        embed = discord.Embed(title='Help with Spudnik', description='Spudnik\'s commands')
        embed.add_field(name='!purgeall', value='Deletes last 125 messages.')
        embed.add_field(name='!hello', value='Spudnik will say hi back.')
        embed.add_field(name='!woof', value='Tags dog and tells him he\'s a good boy then barks erratically.')
        embed.add_field(name='!users', value='Displays number of members in server.')
        embed.add_field(name='!meowking', value='Tags Meowking. Use in emergency only.')
        embed.add_field(name='!meow', value='Provides a link to Rosini\'s meow choir piece.')
        embed.add_field(name='!help', value='Displays Spudnik\'s commands.')
        await message.channel.send(content=None, embed=embed)


@client.event
async def on_member_join(member):
    print(member.guild.channels)
    for channel in member.guild.channels:
        if str(channel) == '🚪-front-door':
            await channel.send(f'Welcome {member.mention}, tell us about yourself and how you found our '
                                       f'server.')

    # elif message.content == '!d bump' and message.channel == terminal:
    #     print(f'Message of: {message.content} at {message.created_at}')
    #     successful_bump_times = []
    #     async for msg in terminal.history(limit=25):
    #         if msg.embeds == []:
    #             continue
    #         elif isinstance(msg.embeds[0].description, str):
    #             if "Bump done" in msg.embeds[0].description:
    #                 successful_bump_times.append(msg.created_at)
    #                 successful_bump = max(successful_bump_times)
    #                 if successful_bump:
    #                   await asyncio.sleep(60 * 60 * 2)
    #                   await terminal.send(f'Reminder to bump server. Command for this is !d bump.'
    #                                         f' cc <@{meowking}>, <@{mathman}>, @<{erebus}>, @<{haagen}>')

# @client.event
# async def on_member_update(before, after):
#     global general
#     general = client.get_channel(general)
#     if before.id == best_dog:
#         if not after.status == 'offline':
#             dog = 'http://24.media.tumblr.com/adc13162b265b7721f7efd5c7d12035f/tumblr_n0ooo4msyo1toamj8o1_250.gif'
#             await general.send(dog)

client.run(bot_token)
