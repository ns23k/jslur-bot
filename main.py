import asyncio
import os
import re
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='.', intents=intents)


@bot.event
async def on_ready():
    print("running")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="J-slurs"))


@bot.command()
async def ping(ctx):
    latency = bot.latency * 1000
    await ctx.reply(f'{latency:.3f}ms')


@bot.event
async def on_message(ctx):
    slurs = ["js", "javascript", "Javascript", "Jаvаscript"]
    content = re.sub(r'[^a-zA-Z0-9\s]+', '', ctx.content)
    if (any(word in content.lower().split(" ") for word in slurs) or (
            "javascript" in content.lower() or "Jаvаscript" in content.lower())) and ctx.channel.id != 1259208950390329475:
        await ctx.reply(
            "the J-slur can only be used in <#1259208950390329475>!!!!!!!!!!!!!! "
            "<:1982manface:1259491829712289822><:1982manface:1259491829712289822>"
        )
        await asyncio.sleep(1)
        await ctx.delete()
    await bot.process_commands(ctx)


bot.run(os.environ.get("TOKEN"))
