import discord
from discord.ext import commands
from discord.ext.commands import Bot
from discord.voice_client import VoiceClient
import random
import asyncio
import os
import time

bot = commands.Bot("-")

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    await bot.change_presence(game=discord.Game(name="|BA| -help", type = 3))

@bot.command(pass_context=True)
async def echo(ctx, *, echo: str):
    """
    Echo.
    """
    await bot.delete_message(ctx.message)
    await bot.say(":thumbsup: | " + echo)

@bot.command(pass_context=True)
async def userinfo(ctx, user: discord.Member):
    """
    User Info.
    """
    embed = discord.Embed(title="{}'s info".format(user.name), description="Important Info.", color=0xffff00)
    embed.add_field(name="ID", value=user.id, inline=True)
    embed.add_field(name="Joined At", value=user.joined_at)
    embed.add_field(name="Account Created", value=user.created_at.__format__('%A, %d. %B %Y @ %H:%M:%S'))
    embed.set_thumbnail(url=user.avatar_url)
    await bot.say(embed=embed)

@bot.command(pass_context=True)
async def serverinfo(ctx):
    """
    Server Info.
    """
    embed = discord.Embed(name="{}'s info".format(ctx.message.server.name), description="Important Info.", color=0xffff00)
    embed.set_author(name="🏆 ZeusCoreService 🏆 ")
    embed.add_field(name="Owner", value=ctx.message.server.owner, inline=True)
    embed.add_field(name="ID", value=ctx.message.server.id, inline=True)
    embed.add_field(name="Roles", value=len(ctx.message.server.roles), inline=True)
    embed.add_field(name="Emojis", value=len(ctx.message.server.emojis))
    embed.set_thumbnail(url=ctx.message.server.icon_url)
    await bot.say(embed=embed)

@bot.command(pass_context=True)
async def warn(ctx, userName: discord.Member ,*, reason: str):
    """
    Warn's the user.
    """
    if "Moderator" in [role.name for role in ctx.message.author.roles] or ctx.message.author.server_permissions.administrator:
        embed = discord.Embed(title="Warned", description="{} You have been Warned. Reason: **{}**".format(userName.mention, reason), color=0xff0006)
        embed.set_thumbnail(url=userName.avatar_url)
        embed.set_author(name=ctx.message.author.name, icon_url=ctx.message.author.avatar_url)
        await bot.say(embed=embed)
        await bot.send_message(userName, "You Have Been Warned. Reason: {}".format(reason))
    else:
        await bot.say("{} :x: You are not allowed to use this command!".format(ctx.message.author.mention))

@bot.command(pass_context=True)
@commands.has_permissions(manage_messages=True)
async def delete(ctx, number):
    """
    Delete's messages.
    """
    msgs = []
    number = int(number)
    async for x in bot.logs_from(ctx.message.channel, limit = number):
        msgs.append(x)
    await bot.delete_messages(msgs)
    embed = discord.Embed(title=f"{number} messages deleted", description="Wow, somebody's been spamming", color=0xff0006)
    test = await bot.say(embed=embed)
    await asyncio.sleep(10)
    await bot.delete_message(test)

@bot.command(pass_context=True)
async def kick(ctx, member: discord.Member):
    """
    Kick's the user.
    """
    if ctx.message.author.server_permissions.administrator or ctx.message.author.id == '397745647723216898':
        try:
            await bot.kick(member)
            await bot.say("Succesfully kicked!")
        except discord.errors.Forbidden:
            await bot.say(":x: You have no premission!")
    else:
        await bot.say(":x: You have no premission!")

@bot.command(pass_context=True)
async def ban(ctx, member: discord.Member):
    """
    Ban's the user.
    """
    if ctx.message.author.server_permissions.administrator or ctx.message.author.id == '397745647723216898':
        try:
            await bot.ban(member)
            await bot.say(":thumbsup: Succesfully banned!")
        except discord.errors.Forbidden:
            await bot.say(":x: You have no premission!")

@bot.command(pass_context=True)
async def c_mute(ctx, member: discord.Member):
    """
    Chat Mute's the user.
    """
    if ctx.message.author.server_permissions.administrator != True:
        return await bot.say(":x: You have no premission!")
    role = discord.utils.get(ctx.message.server.roles, name="Chat Mute")
    await bot.add_roles(member, role)
    embed = discord.Embed(title="Chat Muted", description="You have been **Chat Muted**", color=0xff0006)
    embed.set_thumbnail(url=member.avatar_url)
    embed.set_author(name=ctx.message.author.name, icon_url=ctx.message.author.avatar_url)
    await bot.say(embed=embed)

@bot.command(pass_context=True)
async def c_unmute(ctx, member: discord.Member):
    """
    Chat UnMute's the user.
    """
    if ctx.message.author.server_permissions.administrator != True:
        return await bot.say(":x: You have no premission!")
    role = discord.utils.get(ctx.message.server.roles, name="Chat Mute")
    await bot.remove_roles(member, role)
    embed = discord.Embed(title="Member UnMuted", description="{} Has been **UnMuted**".format(member.mention), color=0x00ff00)
    embed.set_author(name=member.name, icon_url=member.avatar_url)
    embed.set_thumbnail(url=member.avatar_url)
    embed.set_author(name=ctx.message.author.name, icon_url=ctx.message.author.avatar_url)
    await bot.say(embed=embed)

@bot.command(pass_context=True)
async def v_mute(ctx, member: discord.Member):
    """
    Voice Mute's the user.
    """
    if ctx.message.author.server_permissions.administrator != True:
        return await bot.say(":x: You have no premission!")
    role = discord.utils.get(ctx.message.server.roles, name="Voice Mute")
    await bot.add_roles(member, role)
    embed = discord.Embed(title="Voice Muted", description="You have been **Voice Muted**", color=0xff0006)
    embed.set_thumbnail(url=member.avatar_url)
    embed.set_author(name=ctx.message.author.name, icon_url=ctx.message.author.avatar_url)
    await bot.say(embed=embed)

@bot.command(pass_context=True)
async def v_unmute(ctx, member: discord.Member):
    """
     Voice UnMute's the user.
    """
    if ctx.message.author.server_permissions.administrator != True:
        return await bot.say(":x: You have no premission!")
    role = discord.utils.get(ctx.message.server.roles, name="Voice Mute")
    await bot.remove_roles(member, role)
    embed = discord.Embed(title="Member UnMuted", description="{} Has been **UnMuted**".format(member.mention), color=0x00ff00)
    embed.set_author(name=member.name, icon_url=member.avatar_url)
    embed.set_thumbnail(url=member.avatar_url)
    embed.set_author(name=ctx.message.author.name, icon_url=ctx.message.author.avatar_url)
    await bot.say(embed=embed)

bot.run("NTQyNzEzNDcyNzk5MjExNTQw.DzyA3Q.GWh7djd57PNBvu1GDabpdSvMWFg")
