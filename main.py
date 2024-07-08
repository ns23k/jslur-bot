import asyncio
import os
import re
import discord
from discord.ext import commands
from dotenv import load_dotenv
from loguru import logger

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='.', intents=intents)

logger = logger

J_SLURS = ["javascript", "js"]


def normalize_lookalike_letters(text) -> str:
    # Define a mapping from lookalike letters to English alphabets
    lookalike_mapping = {
        'а': 'a', 'А': 'A',  # Cyrillic
        'е': 'e', 'Е': 'E',  # Cyrillic
        'о': 'o', 'О': 'O',  # Cyrillic
        'с': 'c', 'С': 'C',  # Cyrillic
        'р': 'p', 'Р': 'P',  # Cyrillic
        'у': 'y', 'У': 'Y',  # Cyrillic
        'х': 'x', 'Х': 'X',  # Cyrillic
        'І': 'I', 'і': 'i',  # Ukrainian
        'ѣ': 'e',  # Old Slavonic
        'ϲ': 'c',  # Greek
        'Ι': 'I', 'i': 'i',  # Greek
        'Β': 'B', 'ν': 'v',  # Greek
        'Κ': 'K', 'κ': 'k',  # Greek
        'Μ': 'M', 'μ': 'm',  # Greek
        'Ν': 'N', 'η': 'n',  # Greek
        'Ο': 'O', 'ο': 'o',  # Greek
        'Ρ': 'P', 'ρ': 'p',  # Greek
        'Τ': 'T', 'τ': 't',  # Greek
        'Υ': 'Y', 'υ': 'y',  # Greek
        'Χ': 'X', 'χ': 'x',  # Greek
        'ϒ': 'Y', 'ϓ': 'y',  # Greek
        'Ϗ': 'P',  # Greek
        'Ḁ': 'A', 'ḁ': 'a',  # Latin
        'ƀ': 'b', 'ƃ': 'b',  # Latin
        'Č': 'C', 'č': 'c',  # Latin
        'Ð': 'D', 'ð': 'd',  # Latin
        'Ë': 'E', 'ë': 'e',  # Latin
        'Ɣ': 'Y', 'ɣ': 'y',  # Latin
        'İ': 'I', 'ı': 'i',  # Latin
        'Ḳ': 'K', 'ḳ': 'k',  # Latin
        'ƛ': 'L', 'λ': 'l',  # Latin
        'Ň': 'N', 'ň': 'n',  # Latin
        'Ö': 'O', 'ö': 'o',  # Latin
        'Ʀ': 'R', 'ɼ': 'r',  # Latin
        'Ť': 'T', 'ť': 't',  # Latin
        'Ū': 'U', 'ū': 'u',  # Latin
        'Ǔ': 'U', 'ǔ': 'u',  # Latin
        'Ẃ': 'W', 'ẃ': 'w',  # Latin
        'Ÿ': 'Y', 'ÿ': 'y',  # Latin
        'Ž': 'Z', 'ž': 'z',  # Latin
        'ʙ': 'B', 'ᴍ': 'M', 'ʀ': 'R', 'ʏ': 'Y',  # Phonetic Symbols
        'Ⅽ': 'C', 'Ⅾ': 'D', 'Ⅿ': 'M', 'Ⅹ': 'X',  # Roman Numerals
        'ℬ': 'B', 'ℰ': 'E', 'ℒ': 'L', 'ℳ': 'M',  # Script
        'ℙ': 'P', 'ℛ': 'R', 'ℭ': 'C', 'ℯ': 'e',  # Script
        'ℹ': 'i', 'ℽ': 'y',  # Script
        '⒜': 'a', '⒝': 'b', '⒞': 'c', '⒟': 'd', '⒠': 'e',  # Enclosed Alphanumeric
        '⒡': 'f', '⒢': 'g', '⒣': 'h', '⒤': 'i', '⒥': 'j',  # Enclosed Alphanumeric
        '⒦': 'k', '⒧': 'l', '⒨': 'm', '⒩': 'n', '⒪': 'o',  # Enclosed Alphanumeric
        '⒫': 'p', '⒬': 'q', '⒭': 'r', '⒮': 's', '⒯': 't',  # Enclosed Alphanumeric
        '⒰': 'u', '⒱': 'v', '⒲': 'w', '⒳': 'x', '⒴': 'y',  # Enclosed Alphanumeric
        '⒵': 'z',  # Enclosed Alphanumeric
    }

    normalized_text = ''.join(lookalike_mapping.get(char, char) for char in text)

    return normalized_text


def message_cleanup(msg: str) -> str:
    msg = msg.split(" ")
    cleaned_msg = []
    replace_by = "javascript" if "javascript" in msg else "js"
    for i in msg:
        if i in J_SLURS:
            cleaned_msg.append(i.replace(replace_by, "J-slur"))
    return " ".join(cleaned_msg)


async def js_slur_handler(ctx: discord.Message, message: str) -> None:
    webhook = await ctx.channel.create_webhook(name=str(ctx.author))
    reply = await ctx.reply(
        "the J-slur can only be used in <#1259208950390329475>!!!!!!!!!!!!!! "
        "<:1982manface:1259491829712289822><:1982manface:1259491829712289822>"
    )
    await webhook.send(
        content=message_cleanup(message),
        username=str(ctx.author),
        avatar_url=ctx.author.avatar.url
    )
    await asyncio.sleep(2)
    await reply.delete()


async def js_slur_checker(ctx: discord.Message) -> None:
    if ctx.channel.id != 1259208950390329475:
        msg = normalize_lookalike_letters(re.sub(r'[^a-zA-Z0-9\s]+', '', ctx.content).lower())
        slur_used = False
        for i in J_SLURS:
            if i in msg.split(" ") or "javascript" in msg:
                slur_used = True

        if slur_used:
            await js_slur_handler(ctx, msg)


# MAIN BOT
@bot.event
async def on_ready() -> None:
    logger.debug("BOT RUNNING")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="J-slurs"))


@bot.event
async def on_message(ctx: discord.Message) -> None:
    await js_slur_checker(ctx)


@bot.command()
async def ping(ctx) -> None:
    latency = bot.latency * 1000
    await ctx.reply(f"{latency:.2f}ms")

load_dotenv()
bot.run(os.environ.get("TOKEN"))
