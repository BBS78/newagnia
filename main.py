import discord  # Подключаем библиотеку
from discord.ext import commands, tasks
from discord.ui import Button, View
from itertools import cycle
from tinydb import TinyDB, Query
import random
import os
import asyncio
import requests
import json
import datetime
from datetime import datetime, timedelta
import re
import asyncio
from tinydb import TinyDB, Query
from PIL import Image, ImageDraw, ImageFont
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import time

# БД бота
db = TinyDB('./json/database.json', encoding='utf-8')
User = Query()

# Префикс бота
client = commands.Bot(command_prefix='.', intents=discord.Intents.all())
client.remove_command('help')
# Статусы бота
def read_bot_status():
    with open("patterns/status.txt", "r", encoding="utf-8") as file:
        status_list = file.read().splitlines()
    return status_list

bot_status = cycle(read_bot_status())
@tasks.loop(seconds=60)
async def change_status():
    await client.change_presence(activity=discord.Game(next(bot_status)))

# Отчет о запуске 
@client.event
async def on_ready():
    await client.tree.sync()
    print(f'{client.user} готов к работе!')
    change_status.start()

# Подключение команд
async def load():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await client.load_extension(f'cogs.{filename[:-3]}')

# Заруск бота
async def main():
    async with client:
        await load()
        await client.start('MTEyMjk1MDg4OTU5NDk2MTk5NQ.GxI0yA.4SnhRJFStMr9TNoj96NLOmE6GZh4aRS-iCeoDE')
asyncio.run(main())