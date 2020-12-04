import discord
import os
import asyncio
from dotenv import load_dotenv
from datetime import datetime
from discord.ext import commands
from discord.errors import Forbidden
from discord import HTTPException

load_dotenv()
intents = discord.Intents.default()
intents.members = True
intents.presences = True
intents.guilds = True
bot = commands.Bot(command_prefix='.', intents=intents)
bot_token = os.getenv('bot_token')
guild_id = int(os.getenv('server_id'))
meow_id = int(os.getenv("entry_role"))
member_id = int(os.getenv("member_role"))
mods = int(os.getenv("mods"))


@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')


@bot.command()
async def ping(ctx):
    await ctx.send(f'{bot.ws.latency * 1000.0:.2f} ms')


@bot.command()
async def purge(ctx, lim: int):
    await ctx.message.channel.purge(limit=lim)


@bot.command()
async def meow(ctx):
    await ctx.send("Meow!")


@bot.command()
async def users(ctx):
    server = bot.get_guild(guild_id)
    await ctx.message.channel.purge(limit=1)
    await ctx.message.channel.send(f'# of Members: {server.member_count}')


@bot.command()
async def kitty(ctx):
    await ctx.message.channel.send('https://www.youtube.com/watch?v=SaA_cs4WZHM')


@bot.command()
async def woof(ctx):
    best_dog = int(os.getenv('best_dog'))
    await ctx.message.channel.send(f'<@{best_dog}>, you are best meow. _meows erratically_')
    await ctx.message.channel.send("https://tenor.com/view/excited-dog-happy-gif-15784013")


@bot.command()
async def meowking(ctx):
    meow_king = int(os.getenv('meowking'))
    await ctx.message.channel.purge(limit=1)
    await ctx.message.channel.send(f'<@{meow_king}> Raid/Help/Emergency')


@bot.command()
async def command(ctx):
    embed = discord.Embed(title='Help with Bearcat', description='Bearcat\'s commands', color=discord.Colour.blue())
    embed.add_field(name='.commands', value='Displays Bearcat\'s commands.')
    embed.add_field(name='.kitty', value='Provides a link to the kitty cat dance.')
    embed.add_field(name='.math', value='Sends lytics from man\'s not hot.')
    embed.add_field(name='.meow', value='Bearcat will meow back.')
    embed.add_field(name='.meowking', value='Tags Meowking. Use in emergency only.')
    embed.add_field(name='.purgeall', value='Deletes last 125 messages.')
    embed.add_field(name='.ping', value='Displays how long it takes for communication between bot and Discord API.')
    embed.add_field(name='.woof', value='Tags dog and tells him he\'s a good boy then barks erratically.')
    embed.add_field(name='.users', value='Displays number of members in server.')
    await ctx.message.channel.send(content=None, embed=embed)


@bot.command()
@commands.has_any_role('Head Meow in Charge (Admin)', 'Meow King (Owner)', 'Meow Control (Mod)')
async def kick(ctx, member: discord.Member, *, reason=None):
    if reason is None:
        await ctx.send(f'{ctx.author.mention}, please provide a reason for kicking')
    else:
        try:
            await member.kick(reason=reason)
            dm = f'You have been kicked from {ctx.guild.name} for {reason}'
            await member.send(dm)
            await ctx.message.send(f'{member} has been successfully kicked')
        except Forbidden:
            await ctx.send("Bitch pls. You thought")


@bot.command()
@commands.has_any_role('Meow King (Owner)', 'Head Meow in Charge (Admin)', 'Meow Control (Mod)')
async def ban(ctx, member: discord.Member, *, reason=None):
    if reason is None:
        await ctx.send(f'{ctx.author.mention}, please provide a reason for banning')
    else:
        try:
            await member.ban(reason=reason)
            dm = f'You have been banned from {ctx.guild.name} for {reason}'
            await member.send(dm)
            await ctx.message.send(f'{member} has been successfully banned')
        except Forbidden:
            await ctx.send("Bitch pls. You thought")


@bot.command()
@commands.has_any_role('Head Meow in Charge (Admin)', 'Meow King (Owner)', 'Meow Control (Mod)')
async def unban(ctx, member: discord.Member, *, reason=None):
    if reason is None:
        await ctx.send(f'{ctx.author.mention}, please provide a reason for unbanning')
    else:
        await member.unban(reason=reason)
        await ctx.message.send(f'{member} has been successfully unbanned')


@bot.command()
@commands.has_any_role('Head Meow in Charge (Admin)', 'Meow King (Owner)', 'Meow Control (Mod)')
async def mute(ctx, member: discord.Member):
    server = bot.get_guild(guild_id)
    timeout = int(os.getenv("timeout_role"))
    timeout_role = server.get_role(timeout)
    for role in member.roles:
        await member.remove_roles(role)
    await member.add_roles(timeout_role)
    await ctx.send(f'{member} has been successfully muted')


@bot.command()
async def avatar(ctx, member: discord.Member):
    if member is None:
        await ctx.send(f'Please tag a user.')
    else:
        embed = discord.Embed(title='Bearcat Avatar Showcase', description=f'**{member}**',
                              color=discord.Colour.blue())
        embed.set_image(url=member.avatar_url)
        embed.set_footer(text=f'Today at {datetime.now().strftime("%I:%M %p")}')
        await ctx.message.channel.send(content=None, embed=embed)


@bot.command()
async def enlarge(ctx, emoji: discord.Emoji):
    await ctx.send(emoji.url)


@bot.command()
async def approve(ctx, member: discord.Member):
    server = bot.get_guild(guild_id)
    entry_role = server.get_role(meow_id)
    member_role = server.get_role(member_id)
    if member is None:
        pass
    else:
        try:
            await member.remove_roles(entry_role)
            await member.add_roles(member_role)
            await ctx.send(f'{member.display_name} has been approved')
        except HTTPException:
            await ctx.send('Something has failed. I desire a sacrifice')


@bot.command()
async def math(ctx):
    await ctx.send("Two plus two is four minus one, that's three, quick maths")


@bot.event
async def on_member_join(member):
    global mods
    server = bot.get_guild(guild_id)
    mods = server.get_role(mods)
    entry_role = server.get_role(meow_id)
    try:
        await member.add_roles(entry_role)
        for channel in member.guild.channels:
            if str(channel) == '🚪-front-door':
                await asyncio.sleep(3)
                await channel.send(f'Welcome {member.mention}, plase tell us about yourself and how you found our '
                                   f'server. A {mods.mention} will be with you to let you in momentatily. \n \n **Note:'
                                   f' We are not veterinarians and cannot provide sound medical advice for your cat. '
                                   f'If this is an emergency, please contact your veterinarian ASAP.**')

    except AttributeError:
        await asyncio.sleep(3)
        await channel.send(f'Welcome, plase tell us about yourself and how you found our server. A {mods.mention} will '
                           f'be with you to let you in momentatily. \n \n **Note: We are not veterinarians and cannot '
                           f'provide sound medical advice for your cat. If this is an emergency, please contact your '
                           f'veterinarian ASAP.**')
        print("User is invisible")


@bot.event
async def on_member_update(before, after):
    role_log = int(os.getenv('role_log'))
    role_channel = bot.get_channel(role_log)
    if before.roles != after.roles:
        roles_before = [role.name for role in before.roles]
        roles_after = [role.name for role in after.roles]
        if len(before.roles) < len(after.roles):
            diff = [role for role in roles_after if role not in roles_before]
            await role_channel.send(f"A role for {before.name} has been added. Role added is {''.join(diff)}")
        else:
            diff = [role for role in roles_before if role not in roles_after]
            await role_channel.send(f"A role for {before.name} has been removed. Role removed is {''.join(diff)}")

@bot.command()
async def call_mods(ctx):
    server = bot.get_guild(guild_id)
    mods = server.get_role(581921256920842241)
    await ctx.channel.send(f'Test call for {mods.mention}')

bot.run(bot_token)
