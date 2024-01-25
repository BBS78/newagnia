import discord
from discord.ext import commands
from tinydb import TinyDB, Query
from easy_pil import Canvas, Editor, Font, load_image_async
from cogs.Profile import current_userdata

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
    async def test(self, ctx, arg):
        try:
            user_id = f"<@{ctx.author.id}>"
            inventory = current_userdata(user_id, "inventory")
            if arg == "id01":
                name = "Серебряное кольцо с аквамарином"
                points = "+5% силы"
            elif arg == "id02":
                name = "Серебряное кольцо с рубином"
                points = "+5% здоровья"
            elif arg == "id03":
                name = "Золотой медальон"
                points = "+3% золота"
            elif arg == "id04":
                name = "Филактерия"
                points = "+10% силы"
            elif arg == "id05":
                name = "Бронзовое кольцо с аметистом"
                points = "+3% защиты"
            elif arg == "id06":
                name = "Амулет Клыка"
                points = "+2% силы"
            item = {"item_id": arg, "name": name, "points": points}
            inventory.append(item)
            db.update({"inventory": inventory}, User.user_id == user_id)
            inventory = current_userdata(user_id, "inventory")
            await ctx.send(f'Добавлен предмет "{name}"')
            await ctx.send(f'Инвентарь "{inventory}"')
        except Exception as e:
            await ctx.send(f"An error occurred in test: {e}")

        

async def setup(client):
    await client.add_cog(Test(client))
