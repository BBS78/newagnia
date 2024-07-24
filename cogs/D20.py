import discord
from discord.ext import commands
from tinydb import TinyDB, Query
from easy_pil import Font
import requests
import pandas as pd
import random


# БД бота
db = TinyDB('./json/database.json', encoding='utf-8')
User = Query()

# Класс команды
class D20(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("D20.py is ready")

    # Команда
    @commands.command(aliases=['d'])
    async def d20(self, ctx, *args):
        try:
            msg = ctx.message.content
            msg_split = msg.split()
            if '+' in msg:
                new_msg = msg.split('+')
                add_num = int(new_msg[1])
            elif '-' in msg:
                new_msg = msg.split('-')
                add_num = 0 - int(new_msg[1])
            else:
                add_num = 0

            random_number = random.randint(1, 20)

            embed = discord.Embed(
                title=f' {ctx.author.id} бросил кубик...',
                description='',
                color=discord.Color.dark_green()
            )    

            # embed.set_image(url=f"attachment://profile_image_{user_id_for_filename}.png")
            # await ctx.send(file=file, embed=embed, view=Buttons(user_id, ctx))


            await ctx.send(f'Детали: [{msg} ({random_number})]\n## {random_number+add_num}')
        except Exception as e:
            await print(f'{e}')

        

async def setup(client):
    await client.add_cog(D20(client))
