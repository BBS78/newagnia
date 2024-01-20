import discord
from discord.ext import commands
from tinydb import TinyDB, Query
from easy_pil import Canvas, Editor, Font, load_image_async

# БД бота
db = TinyDB('./json/database.json', encoding='utf-8')
User = Query()

# Класс команды
class Setname(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Setname.py is ready")

    # Команда
    @commands.command(aliases=['sn'])
    async def setname(self, ctx, arg):
        user_id = f"<@{ctx.author.id}>"
        font_50 = Font("patterns/Jost-Bold.ttf", size=50)
        text_size = font_50.getsize(arg)
        if text_size[0] <= 480:
            db.update({"username": arg}, User.user_id == user_id)
            embed = discord.Embed(
                title='✅ Успешно',
                description=f'Имя персонажа было успешно изменено на "{arg}"',
                color=discord.Color.green()
            )
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title='❌ Неудача',
                description=f'Данное имя слишком длинное, попробуйте что-то покороче.',
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)


        

async def setup(client):
    await client.add_cog(Setname(client))
