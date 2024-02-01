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
            item_mapping = {
                "id01": {"name": "Серебряное кольцо с аквамарином", "points": "+5% опыта"},
                "id02": {"name": "Серебряное кольцо с рубином", "points": "+5% здоровья"},
                "id03": {"name": "Золотой медальон", "points": "+3% золота"},
                "id04": {"name": "Филактерия", "points": "+10% силы"},
                "id05": {"name": "Бронзовое кольцо с аметистом", "points": "+3% защиты"},
                "id06": {"name": "Амулет Клыка", "points": "+2% силы"},
                "id07": {"name": "Клинок гильдии", "points": "+20% силы"},
                "id08": {"name": "Кожаный тардж", "points": "+20% защиты"},
                "id09": {"name": "Шитая одежда", "points": "+15% защиты"},
                "id10": {"name": "Капюшон", "points": "+10% защиты"},
                "id11": {"name": "Кинжал обыкновенный", "points": "+10% силы"},
            }

            if arg in item_mapping:
                item_info = item_mapping[arg]
                item = {"item_id": arg, "name": item_info["name"], "points": item_info["points"]}
                inventory.append(item)
                db.update({"inventory": inventory}, User.user_id == user_id)
                inventory = current_userdata(user_id, "inventory")
                await ctx.send(f'Добавлен предмет "{item_info["name"]}"')
                await ctx.send(f'Инвентарь "{inventory}"')
            else:
                await ctx.send(f'Неизвестный айди')
        except Exception as e:
            await ctx.send(f"An error occurred in test: {e}")

        

async def setup(client):
    await client.add_cog(Test(client))
