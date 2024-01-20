import discord
from discord.ext import commands
from tinydb import TinyDB, Query
from easy_pil import Canvas, Editor, Font, load_image_async

# БД бота
db = TinyDB('./json/database.json', encoding='utf-8')
User = Query()


class Buttons(discord.ui.View):
    def __init__(self, user_id):
        super().__init__(timeout=None)
        self.user_id = user_id

    @discord.ui.button(label="[1] Воин", style=discord.ButtonStyle.blurple)
    async def warrior(self, interaction: discord.Interaction, Button: discord.ui.Button):
        db = TinyDB('./json/database.json', encoding='utf-8')
        User = Query()
        current_class = db.search(User.user_id == self.user_id)[0]["user_class"]
        if current_class != "Класс не выбран":
            embed = discord.Embed(
                title='❌ Неудача',
                description=f'Вы уже выбрали класс {current_class}а',
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed)            
            return
        try:
            db.update({"user_class": "Воин"},User.user_id == self.user_id)
            db.update({"max_health": 30},User.user_id == self.user_id)
            db.update({"health": 30},User.user_id == self.user_id)
            embed = discord.Embed(
                title='',
                description=f'',
                color=discord.Color.green()
            )
            embed.set_image(url=f"attachment://Classes-table-warrior.png")
            file = discord.File("images/Classes-table-warrior.png", filename="Classes-table-warrior.png")
            await interaction.response.send_message(embed=embed, file=file)
        except Exception as e:
            print(f"An error occurred: {e}")

    @discord.ui.button(label="[2] Маг", style=discord.ButtonStyle.blurple)
    async def wizzard(self, interaction: discord.Interaction, Button: discord.ui.Button):
        db = TinyDB('./json/database.json', encoding='utf-8')
        User = Query()
        current_class = db.search(User.user_id == self.user_id)[0]["user_class"]
        if current_class != "Класс не выбран":
            embed = discord.Embed(
                title='❌ Неудача',
                description=f'Вы уже выбрали класс {current_class}а',
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed)            
            return        
        try:
            db.update({"user_class": "Маг"},User.user_id == self.user_id)
            db.update({"max_health": 15},User.user_id == self.user_id)
            db.update({"health": 15},User.user_id == self.user_id)
            embed = discord.Embed(
                title='',
                description=f'',
                color=discord.Color.green()
            )
            embed.set_image(url=f"attachment://Classes-table-wizzard.png")
            file = discord.File("images/Classes-table-wizzard.png", filename="Classes-table-wizzard.png")
            await interaction.response.send_message(embed=embed, file=file)
        except Exception as e:
            print(f"An error occurred: {e}")

    @discord.ui.button(label="[3] Разбойник", style=discord.ButtonStyle.blurple)
    async def rogue(self, interaction: discord.Interaction, Button: discord.ui.Button):
        db = TinyDB('./json/database.json', encoding='utf-8')
        User = Query()
        current_class = db.search(User.user_id == self.user_id)[0]["user_class"]
        if current_class != "Класс не выбран":
            embed = discord.Embed(
                title='❌ Неудача',
                description=f'Вы уже выбрали класс {current_class}а',
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed)            
            return        
        try:
            db.update({"user_class": "Разбойник"}, User.user_id == self.user_id)
            db.update({"max_health": 13},User.user_id == self.user_id)
            db.update({"health": 13},User.user_id == self.user_id)
            embed = discord.Embed(
                title='',
                description=f'',
                color=discord.Color.green()
            )
            embed.set_image(url=f"attachment://Classes-table-rogue.png")
            file = discord.File("images/Classes-table-rogue.png", filename="Classes-table-rogue.png")
            await interaction.response.send_message(embed=embed, file=file)
        except Exception as e:
            print(f"An error occurred: {e}")


# Класс команды
class Myclass(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Myclass.py is ready")

    # Команда
    @commands.command(aliases=['mc'])
    async def myclass(self, ctx):
        try:
            user_id = f"<@{ctx.author.id}>"
            current_class = db.search(User.user_id == user_id)[0]["user_class"]
            if current_class == "Класс не выбран":
                embed = discord.Embed(
                    title='',
                    description=f'',
                    color=discord.Color.light_grey()
                )
                embed.set_image(url=f"attachment://Classes-table.png")
                file = discord.File("images/Classes-table.png", filename="Classes-table.png")
                await ctx.send(embed=embed, file=file, view=Buttons(user_id))
            else:
                embed = discord.Embed(
                    title='❌ Неудача',
                    description=f'Вы уже выбрали класс {current_class}а',
                    color=discord.Color.red()
                )
                await ctx.send(embed=embed)
        except Exception as e:
            print(f"An error occurred: {e}")


async def setup(client):
    await client.add_cog(Myclass(client))
