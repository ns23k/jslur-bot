import asyncio
import os
import re
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='.', intents=intents)

J_SLURS = ["javascript", "js"]


def normalize_lookalike_letters(text):
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


def js_slur_handler(ctx: discord.Message, message: str):
    pass


def js_slur_checker(ctx: discord.Message):
    msg = normalize_lookalike_letters(re.sub(r'[^a-zA-Z0-9\s]+', '', ctx.content).lower())
    slur_used = False
    for i in J_SLURS:
        if i in msg.split(" ") or "javascript" in msg:
            slur_used = True

    if slur_used:
        js_slur_handler(ctx, msg)


bot.run(os.environ.get("TOKEN"))
