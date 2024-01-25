import discord
from discord.ext import commands
from tinydb import TinyDB, Query
from easy_pil import Canvas, Editor, Font, load_image_async
from cogs.Inventory import inventory_info

# ТЕКУЩИЕ ОЧКИ
def current_userdata(user_id, k):
    # БД бота
    db = TinyDB('./json/database.json', encoding='utf-8')
    User = Query()
    resalts = db.search(User.user_id == user_id)
    return resalts[0][k]

# Кнопки
class Buttons(discord.ui.View):
    def __init__(self, user_id, ctx):
        super().__init__(timeout=None)
        self.user_id = user_id
        self.ctx = ctx

    @discord.ui.button(label="[1] Инвентарь", style=discord.ButtonStyle.blurple)
    async def inventory(self, interaction: discord.Interaction, Button: discord.ui.Button):
        try:
            user_id = f"<@{interaction.user.id}>"
            username = str(interaction.user.display_name)
            i_info = await inventory_info(self.ctx, user_id, username)  

            await interaction.response.send_message(file=i_info[0], embed=i_info[1])  
        except Exception as e:
            print(f"An error occurred: {e}")


    @discord.ui.button(label="[2] Питомцы", style=discord.ButtonStyle.blurple)
    async def pets(self, interaction: discord.Interaction, Button: discord.ui.Button):
        try:
            pass
        except Exception as e:
            print(f"An error occurred: {e}")


    @discord.ui.button(label="[3] Достижения", style=discord.ButtonStyle.blurple)
    async def achievements(self, interaction: discord.Interaction, Button: discord.ui.Button):     
        try:
            pass
        except Exception as e:
            print(f"An error occurred: {e}")

async def profile_info(ctx, user_id):
    try:
        # Получаем инфу
        userdata = {
            "username": current_userdata(user_id, "username"),
            "user_class": current_userdata(user_id, "user_class"),
            "lvl": current_userdata(user_id, "lvl"),
            "exp": current_userdata(user_id, "exp"),
            "max_exp": current_userdata(user_id, "max_exp"),
            "health": current_userdata(user_id, "health"),
            "max_health": current_userdata(user_id, "max_health"),
            "coins": current_userdata(user_id, "coins")
        }
        background = Editor("images/profile_bg.png")
        coin = Editor("images/coin.png")
        profile_image = await load_image_async(ctx.author.display_avatar.url)
        profile = Editor(profile_image).resize((182, 182))

        # Подключаем шрифты
        font_50 = Font("patterns/Jost-Bold.ttf", size=50)
        font_30 = Font("patterns/Jost-Medium.ttf", size=30)
        font_30_bold = Font("patterns/Jost-Bold.ttf", size=30)
        font_18 = Font("patterns/Jost-Medium.ttf", size=18)


        background.paste(profile, (63, 70))
        background.rectangle((63, 70), width=182, height=182, outline="#ffffff", stroke_width=10)
        background.text((264, 70), userdata["username"], font=font_50, color="white")
        background.text((264, 127), f"{userdata['user_class']}  ◊  ", font=font_30, color="white")
        text_size = font_30.getsize(f"{userdata['user_class']}  ◊  ")
        background.text(((264 + text_size[0]), 127), f"{userdata['lvl']} lvl  ", font=font_30, color="#FFB043")
        text_size = font_30.getsize(f"{userdata['user_class']}  ◊  {userdata['lvl']} lvl  ")
        background.text(((264 + text_size[0]), 127), f"◊  {userdata['coins']}", font=font_30, color="white")
        text_size = font_30.getsize(f"{userdata['user_class']}  ◊  {userdata['lvl']} lvl  ◊  {userdata['coins']} ")
        background.paste(coin, (264 + text_size[0], 127))

        background.rectangle((264, 170), width=326, height=30, fill="#23272A", radius=20)
        background.bar(
            (264, 170),
            max_width=326,
            height=30,
            percentage=(userdata["health"])/(userdata["max_health"])*100,
            fill="#E64A55",
            radius=20,
        )

        background.rectangle((264, 220), width=326, height=30, fill="#23272A", radius=20)
        background.bar(
            (264, 220),
            max_width=326,
            height=30,
            percentage=(userdata["exp"])/(userdata["max_exp"])*100,
            fill="#F5BD5E",
            radius=20,
        )

        background.text((600, 180), f"{userdata['health']}/{userdata['max_health']} HP", font=font_18, color="white")
        background.text((600, 230), f"{userdata['exp']}/{userdata['max_exp']} EXP", font=font_18, color="white")

        background.text((63, 280), f"Последние достижения", font=font_30_bold, color="white")
        background.text((63, 330), "{Нет достижений}", font=font_30_bold, color="#888888")
        user_id_for_filename = str(user_id).replace("<", "").replace(">", "").replace("@", "")
        file_path = f'images/profile_image_{user_id_for_filename}.png' 
        background.save(file_path) 
        file = discord.File(file_path, filename=f"profile_image_{user_id_for_filename}.png")
        embed = discord.Embed(
            title='⚔️ Профиль пользователя',
            description='',
            color=discord.Color.light_grey()
        )    

        embed.set_image(url=f"attachment://profile_image_{user_id_for_filename}.png")
        await ctx.send(file=file, embed=embed, view=Buttons(user_id, ctx))

        if userdata['user_class'] == "Класс не выбран":
            embed = discord.Embed(
                title='Класс не выбран',
                description=f'Вы можете выбрать класс для персонажа используя команду !myclass',
                color=discord.Color.yellow()
            )
            await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"An error occurred in profile_info: {e}")

# Класс команды
class Profile(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Profile.py is ready")

    # Команда
    @commands.command(aliases=['p'])
    async def profile(self, ctx):
        try:
            # БД бота
            db = TinyDB('./json/database.json', encoding='utf-8')
            User = Query()
            username = str(ctx.author.display_name)
            user_id = f"<@{ctx.author.id}>"
            # Добавляем в БД если нету
            if not db.search(User.user_id == user_id):
                db.insert({"username": username, # Ник 
                        "user_id": user_id, # Айди
                        "user_class": "Класс не выбран",
                        "lvl": 0, # Уровень
                        "exp": 0, # Опыт
                        "max_exp": 100, # Опыт до следующего уровня
                        "health": 10, # Текущее здоровье
                        "max_health": 10, # Максимальное здоровье
                        "coins": 0, # Монеты пользователя
                        "01": "None",
                        "02": "None",
                        "03": "None",
                        "inventary": [] 
                            })    
            await profile_info(ctx, user_id)
        except Exception as e:
            await ctx.send(f"An error occurred in the profile command: {e}")

async def setup(client):
    try:
        await client.add_cog(Profile(client))
    except Exception as e:
        print(f"An error occurred while adding the Profile cog: {e}")
