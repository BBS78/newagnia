import discord  # Подключаем библиотеку
from discord import Intents
from discord.ext import commands, tasks
from discord.ui import Button, View
from itertools import cycle
from tinydb import TinyDB, Query
# import random
import os
import asyncio
# import requests
# import json
# import datetime
from datetime import datetime, timedelta
# import re
import asyncio
from tinydb import TinyDB, Query
from PIL import Image, ImageDraw, ImageFont
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
# import time

# БД бота
db = TinyDB('./json/database.json', encoding='utf-8')
User = Query()

# Префикс бота
client = commands.Bot(command_prefix='!', intents=discord.Intents.all())
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

@tasks.loop(hours=24)
async def write_time():
    def days_until(target_date):
        import datetime  # Importing datetime module within the function
        
        try:
            target_date = datetime.datetime.strptime(target_date, '%Y-%m-%d').date()
            today = datetime.date.today()
            delta = target_date - today
            return delta.days
        except Exception as e:
            print(f"An error occurred while calculating days until: {e}")
            return None
    
    try:
        print("Debugging: Starting loop iteration...")  # Debugging statement
        
        channel = client.get_channel(1160890397355163773)
        await channel.send(f'<@830285571599499284> ты сдаешь НЕМЕТЕ 5 июня: через **{days_until("2024-06-05")} дней**\n\n<@996353781300215868> ты сдаешь НЕМЕТЕ 6 июня: через **{days_until("2024-06-06")} дней**\n\n<@631567239690190849> ты сдаешь НЕМЕТЕ 10 июня: через **{days_until("2024-06-10")} дней**\n\n<@513321766928777227> ты сдаешь НЕМЕТЕ 12 июня: через **{days_until("2024-06-12")} дней**\n\nhttps://www.youtube.com/watch?v=iGb3Rl7V9oc')
        print("Debugging: Loop iteration completed.")  # Debugging statement
    except Exception as e:
        print(f"An error occurred during the loop iteration: {e}")

# Отчет о запуске 
@client.event
async def on_ready():
    await client.tree.sync()
    print(f'{client.user} готов к работе!')
    change_status.start()
    write_time.start()

# Подключение команд
async def load():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await client.load_extension(f'cogs.{filename[:-3]}')

# Заруск бота
async def main():
    async with client:
        await load()
        # await client.start('token')
        await client.start('token')
asyncio.run(main())