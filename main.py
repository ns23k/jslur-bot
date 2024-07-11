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


def normalize_lookalike_letters(input_string: str) -> str:
    # Mapping of characters to their base form
    conversion_map = {
        # J mappings
        "J": "J", "Ϳ": "J", "Ј": "J", "Ꭻ": "J", "ᒍ": "J", "ꓙ": "J", "Ʝ": "J", "ꭻ": "J", "Ｊ": "J",

        # A mappings
        "A": "A", "Α": "A", "А": "A", "Ꭺ": "A", "ᗅ": "A", "ᴀ": "A", "ꓮ": "A", "ꭺ": "A", "Ａ": "A", "а": "A",

        # V mappings
        "V": "V", "Ѵ": "V", "٧": "V", "۷": "V", "Ꮩ": "V", "ᐯ": "V", "Ⅴ": "V", "ⴸ": "V", "ꓦ": "V",
        "ꛟ": "V", "Ｖ": "V",

        # S mappings
        "S": "S", "Ѕ": "S", "Տ": "S", "Ꮥ": "S", "Ꮪ": "S", "ꓢ": "S", "Ｓ": "S",

        # C mappings
        "C": "C", "Ϲ": "C", "С": "C", "Ꮯ": "C", "ᑕ": "C", "ℂ": "C", "ℭ": "C", "Ⅽ": "C", "⊂": "C", "Ⲥ": "C",
        "⸦": "C", "ꓚ": "C", "Ｃ": "C", "с": "C",

        # R mappings
        "R": "R", "Ʀ": "R", "ʀ": "R", "Ꭱ": "R", "Ꮢ": "R", "ᖇ": "R", "ᚱ": "R", "ℛ": "R", "ℜ": "R", "ℝ": "R",
        "ꓣ": "R", "ꭱ": "R", "ꮢ": "R", "Ｒ": "R", "г": "R",

        # I mappings
        "I": "I", "Ι": "I", "І": "I", "Ꮖ": "I", "Ⅰ": "I", "Ⲓ": "I", "ꓲ": "I", "Ｉ": "I", "і": "I",

        # P mappings
        "P": "P", "Ρ": "P", "Р": "P", "Ꮲ": "P", "ᑭ": "P", "ᴘ": "P", "ᴩ": "P", "ℙ": "P", "Ⲣ": "P", "ꓑ": "P",
        "ꮲ": "P", "Ｐ": "P", "р": "P",

        # T mappings
        "T": "T", "Τ": "T", "τ": "T", "Т": "T", "Ꭲ": "T", "ᴛ": "T", "⊤": "T", "⟙": "T", "Ⲧ": "T", "ꓔ": "T",
        "ꭲ": "T", "Ｔ": "T"
    }

    # Convert the input string
    converted_string = ''.join(conversion_map.get(char, char) for char in input_string)

    return converted_string


def message_cleanup(_msg: str, space_js: bool) -> str:
    msg = _msg.split(" ")
    cleaned_msg = []
    replace_by = "javascript" if "javascript" in msg else "js"
    for i in msg:
        if i in J_SLURS:
            cleaned_msg.append(i.replace(replace_by, "`J-slur`"))
        else:
            cleaned_msg.append(i)

    __msg = " ".join(cleaned_msg)
    if "java" in _msg and "script" in _msg:
        __msg = __msg.replace("java", "`J-Slur`")
    elif space_js:
        __msg = __msg.replace(" ", "").replace("javascript", "`J-Slur`")
    return __msg


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


CHARACTER_REGEX = re.compile(r'[^\w\sА-Яа-яЁё]')


async def js_slur_check(ctx: discord.Message) -> None:
    if ctx.channel.id == 1259208950390329475:
        return

    normalized_message = normalize_lookalike_letters(CHARACTER_REGEX.sub('', ctx.content).lower())
    normalized_message_no_spaces = normalized_message.replace(" ", "")
    js_space_check = "javascript" in normalized_message_no_spaces

    slur_used = (any(word in normalized_message.split() for word in J_SLURS)
                 or 'javascript' in normalized_message_no_spaces
                 or ('java' in normalized_message_no_spaces and 'script' in normalized_message_no_spaces))

    if slur_used:
        await js_slur_handler(ctx, normalized_message, js_space_check)


# MAIN BOT
@bot.event
async def on_ready() -> None:
    logger.debug("BOT RUNNING")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="J-slurs"))


@bot.event
async def on_message(ctx: discord.Message) -> None:
    await js_slur_check(ctx)
    await bot.process_commands(ctx)


@bot.command()
async def ping(ctx) -> None:
    latency = bot.latency * 1000
    await ctx.reply(f"{latency:.2f}ms")


@bot.event
async def on_message_edit(_, ctx):
    await js_slur_check(ctx)


load_dotenv()
bot.run(os.environ.get("TOKEN"))
