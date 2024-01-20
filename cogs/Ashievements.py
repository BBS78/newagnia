import discord
from discord.ext import commands
from tinydb import TinyDB, Query
from easy_pil import Canvas, Editor, Font, load_image_async

# БД бота
db = TinyDB('./json/database.json', encoding='utf-8')
User = Query()

# Класс команды
class Achievements(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Achievements.py is ready")

    # Команда
    @commands.command(aliases=['a'])
    async def achievements(self, ctx):
        file = discord.File('images/profiletest.png', filename=f"profiletest.png")
        embed = discord.Embed(
            title='⚔️ Профиль пользователя',
            description='',
            color=discord.Color.light_grey()
        )    

        embed.set_image(url=f"attachment://profiletest.png")
        await ctx.send(file=file, embed=embed)
        

        

async def setup(client):
    await client.add_cog(Achievements(client))
