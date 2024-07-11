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


def normalize_lookalike_letters(text):
    # Extended mapping from lookalike letters to English alphabets
    lookalike_mapping = {
        # Russian Cyrillic letters
        'а': 'a', 'А': 'A', 'б': 'b', 'Б': 'B', 'в': 'v', 'В': 'V',
        'г': 'g', 'Г': 'G', 'д': 'd', 'Д': 'D', 'е': 'e', 'Е': 'E',
        'ё': 'e', 'Ё': 'E', 'ж': 'zh', 'Ж': 'ZH', 'з': 'z', 'З': 'Z',
        'и': 'i', 'И': 'I', 'й': 'j', 'Й': 'J', 'к': 'k', 'К': 'K',
        'л': 'l', 'Л': 'L', 'м': 'm', 'М': 'M', 'н': 'n', 'Н': 'N',
        'о': 'o', 'О': 'O', 'п': 'p', 'П': 'P', 'р': 'r', 'Р': 'R',
        'с': 's', 'С': 'S', 'т': 't', 'Т': 'T', 'у': 'u', 'У': 'U',
        'ф': 'f', 'Ф': 'F', 'х': 'kh', 'Х': 'KH', 'ц': 'ts', 'Ц': 'TS',
        'ч': 'ch', 'Ч': 'CH', 'ш': 'sh', 'Ш': 'SH', 'щ': 'shch', 'Щ': 'SHCH',
        'ъ': '', 'Ъ': '', 'ы': 'y', 'Ы': 'Y', 'ь': '', 'Ь': '',
        'э': 'e', 'Э': 'E', 'ю': 'yu', 'Ю': 'YU', 'я': 'ya', 'Я': 'YA',

        # Greek letters
        'α': 'a', 'Α': 'A', 'β': 'b', 'Β': 'B', 'γ': 'g', 'Γ': 'G',
        'δ': 'd', 'Δ': 'D', 'ε': 'e', 'Ε': 'E', 'ζ': 'z', 'Ζ': 'Z',
        'η': 'n', 'Η': 'N', 'θ': 'th', 'Θ': 'TH', 'ι': 'i', 'Ι': 'I',
        'κ': 'k', 'Κ': 'K', 'λ': 'l', 'Λ': 'L', 'μ': 'm', 'Μ': 'M',
        'ν': 'n', 'Ν': 'N', 'ξ': 'x', 'Ξ': 'X', 'ο': 'o', 'Ο': 'O',
        'π': 'p', 'Π': 'P', 'ρ': 'r', 'Ρ': 'R', 'σ': 's', 'Σ': 'S',
        'τ': 't', 'Τ': 'T', 'υ': 'u', 'Υ': 'U', 'φ': 'f', 'Φ': 'F',
        'χ': 'ch', 'Χ': 'CH', 'ψ': 'ps', 'Ψ': 'PS', 'ω': 'o', 'Ω': 'O',

        # Latin extended letters
        'á': 'a', 'Á': 'A', 'à': 'a', 'À': 'A', 'â': 'a', 'Â': 'A',
        'ä': 'a', 'Ä': 'A', 'ã': 'a', 'Ã': 'A', 'å': 'a', 'Å': 'A',
        'æ': 'ae', 'Æ': 'AE', 'ç': 'c', 'Ç': 'C', 'é': 'e', 'É': 'E',
        'è': 'e', 'È': 'E', 'ê': 'e', 'Ê': 'E', 'ë': 'e', 'Ë': 'E',
        'í': 'i', 'Í': 'I', 'ì': 'i', 'Ì': 'I', 'î': 'i', 'Î': 'I',
        'ï': 'i', 'Ï': 'I', 'ñ': 'n', 'Ñ': 'N', 'ó': 'o', 'Ó': 'O',
        'ò': 'o', 'Ò': 'O', 'ô': 'o', 'Ô': 'O', 'ö': 'o', 'Ö': 'O',
        'õ': 'o', 'Õ': 'O', 'ø': 'o', 'Ø': 'O', 'œ': 'oe', 'Œ': 'OE',
        'ú': 'u', 'Ú': 'U', 'ù': 'u', 'Ù': 'U', 'û': 'u', 'Û': 'U',
        'ü': 'u', 'Ü': 'U', 'ý': 'y', 'Ý': 'Y', 'ÿ': 'y', 'Ÿ': 'Y',
        'ĵ': 'j', 'Ĵ': 'J', 'ğ': 'g', 'Ğ': 'G', 'ş': 's', 'Ş': 'S',  # Turkish
        'ő': 'o', 'Ő': 'O', 'ű': 'u', 'Ű': 'U',  # Hungarian

        # Phonetic symbols and others
        'ʙ': 'B', 'ʏ': 'Y', 'ʀ': 'R', 'ᴍ': 'M', 'ᴀ': 'A',
        'ʃ': 'sh', 'ʒ': 'zh',  # Phonetic symbols
        'ℬ': 'B', 'ℰ': 'E', 'ℒ': 'L', 'ℳ': 'M', 'ℙ': 'P', 'ℛ': 'R',
        'Ⅽ': 'C', 'Ⅾ': 'D', 'Ⅿ': 'M', 'Ⅹ': 'X',

        # Enclosed Alphanumeric
        '⒜': 'a', '⒝': 'b', '⒞': 'c', '⒟': 'd', '⒠': 'e',
        '⒡': 'f', '⒢': 'g', '⒣': 'h', '⒤': 'i', '⒥': 'j',
        '⒦': 'k', '⒧': 'l', '⒨': 'm', '⒩': 'n', '⒪': 'o',
        '⒫': 'p', '⒬': 'q', '⒭': 'r', '⒮': 's', '⒯': 't',
        '⒰': 'u', '⒱': 'v', '⒲': 'w', '⒳': 'x', '⒴': 'y',
        '⒵': 'z'
    }

    # Replace lookalike characters in the text
    normalized_text = ''.join(lookalike_mapping.get(char, char) for char in text)

    return normalized_text


def message_cleanup(_msg: str, space_js: bool) -> str:
    msg = _msg.split(" ")
    cleaned_msg = []
    replace_by = "javascript" if "javascript" in msg else "js"
    for i in msg:
        if i in J_SLURS:
            cleaned_msg.append(i.replace(replace_by, "`J-slur`"))
        else:
            cleaned_msg.append(i)
    _msg = " ".join(cleaned_msg)

    if "java" in _msg and "script" in _msg:
        _msg = _msg.replace("java", "`J-Slur`")
    elif space_js:
        _msg = _msg.replace(" ", "").replace("javascript", "`J-Slur`")
    return _msg


async def js_slur_handler(ctx: discord.Message, message: str, space_check: bool) -> None:
    webhook = await ctx.channel.create_webhook(name=str(ctx.author))
    reply = await ctx.reply(
        "the J-slur can only be used in <#1259208950390329475>!!!!!!!!!!!!!! "
        "<:1982manface:1259491829712289822><:1982manface:1259491829712289822>"
    )
    await webhook.send(
        content=message_cleanup(message, space_check),
        username=f"{str(ctx.author.display_name)} - {str(ctx.author)}",
        avatar_url=ctx.author.avatar.url
    )
    await asyncio.sleep(1)
    await reply.delete()
    await ctx.delete()
    await webhook.delete()


async def js_slur_checker(ctx: discord.Message) -> None:
    if ctx.channel.id != 1259208950390329475:
        regex = re.sub(r'[^a-zA-ZА-Яа-яЁё0-9\s]', '', ctx.content)
        msg = normalize_lookalike_letters(regex.lower())
        slur_used = False
        js_space_check = "javascript" in msg.replace(" ", "")
        for i in J_SLURS:
            if i in msg.split(" ") or "javascript" in msg or ("java" in msg and "script" in msg) or js_space_check:
                slur_used = True

        if slur_used:
            await js_slur_handler(ctx, msg, js_space_check)


# MAIN BOT
@bot.event
async def on_ready() -> None:
    logger.debug("BOT RUNNING")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="J-slurs"))


@bot.event
async def on_message(ctx: discord.Message) -> None:
    await js_slur_checker(ctx)
    await bot.process_commands(ctx)


@bot.command()
async def ping(ctx) -> None:
    latency = bot.latency * 1000
    await ctx.reply(f"{latency:.2f}ms")


load_dotenv()
bot.run(os.environ.get("TOKEN"))
