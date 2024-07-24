import discord
from discord.ext import commands
from tinydb import TinyDB, Query
from dpy_paginator import paginate

# БД бота
db = TinyDB('./json/database.json', encoding='utf-8')
User = Query()

# Класс команды
class Help(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Help.py is ready")

    # Команда
    @commands.command(aliases=['h'])
    async def help(self, ctx):
        try:
            embed1 = discord.Embed(
                title = "Команды бота #1",
                description='',
                color=discord.Color.blue())
            embed1.add_field(name='!tutorial', value='короткий туториал по серверу', inline=False)
            embed1.add_field(name='!setname, !sn', value='изменить имя персонажа', inline=False)
            embed1.add_field(name='!profile, !p', value='профиль участника', inline=False)
            embed1.add_field(name='!stat, !s', value='статистика отметок', inline=False)
            embed1.add_field(name='!globalstat, !gs', value='статистика сервера', inline=False)
            embed1.add_field(name='!shop, !sh', value='магазин предметов', inline=False)

            embed2 = discord.Embed(
                title = "Команды бота #2",
                description='',
                color=discord.Color.blue())
            embed2.add_field(name='!buy [номер]', value='купить предмет из магазина', inline=False)
            embed2.add_field(name='!inventory, !i', value='инвентарь участника', inline=False)
            embed2.add_field(name='!equip, !e [номер]', value='использовать предмет', inline=False)
            embed2.add_field(name='!trade, !t [пинг] [id предмета] [сумма]', value='предложить обмен участнику', inline=False)
            embed2.add_field(name='!pets', value='питомник участника', inline=False)
            embed2.add_field(name='!feed [номер]', value='покормить питомца', inline=False)
            
            embed3 = discord.Embed(
                title = "Команды бота #3",
                description='',
                color=discord.Color.blue())
            embed3.add_field(name='!achievements, !a', value='достижения участника', inline=False)
            embed3.add_field(name='!quests, !q', value='личные квесты участника', inline=False)
            embed3.add_field(name='!addquest, !aq', value='создать личный квест', inline=False)
            embed3.add_field(name='!duel [пинг] [id питомца]', value='вызвать участника на сражение питомцев', inline=False)
            embed3.add_field(name='!leaders, !l', value='таблица лидеров', inline=False)
            output = paginate(embeds = [embed1, embed2, embed3])
            await ctx.send(embed = output.embed, view = output.view) 
        except Exception as e:
            await ctx.send(f"An error occurred in test: {e}")

async def setup(client):
    await client.add_cog(Help(client))