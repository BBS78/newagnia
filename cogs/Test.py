import discord
from discord.ext import commands
from tinydb import TinyDB, Query
from easy_pil import Font
import requests
import pandas as pd


# БД бота
db = TinyDB('./json/database.json', encoding='utf-8')
User = Query()

# Класс команды
class Test(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Test.py is ready")

    # Команда
    @commands.command(aliases=['t'])
    async def test(self, ctx, *args):
        try:
            url = 'https://docs.google.com/spreadsheets/d/1OKJR2xuqr2Cp8CRlkfXWBSx8zY8I5m9bn77LpbICLnQ/edit?usp=sharing'  # Replace with your Google Sheets link
            html = requests.get(url).content
            df_list = pd.read_html(html)
            df = df_list[-1]  # Assuming the relevant table is the last one
            df.to_csv('my_data.csv')  # Save the data to a CSV file

            # await ctx.send(data[0])
        except Exception as e:
            await print(f'{e}')

        

async def setup(client):
    await client.add_cog(Test(client))
