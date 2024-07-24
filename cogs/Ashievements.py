import discord
from discord.ext import commands
from tinydb import TinyDB, Query
from easy_pil import Canvas, Editor, Font, load_image_async
from cogs.Profile import current_userdata
from dpy_paginator import paginate

# БД бота
db = TinyDB('./json/database.json', encoding='utf-8')
server_config = TinyDB('./json/server-config.json', encoding='utf-8')
User = Query()

async def achievements_info(ctx, user_id, username):
    try:
        db = TinyDB('./json/database.json', encoding='utf-8')
        server_config = TinyDB('./json/server-config.json', encoding='utf-8')
        User = Query()

        background = Editor("images/achievements_bg.png")
        locke_icon = Editor("images/locke_icon.png")

        font_48 = Font("patterns/Jost-Bold.ttf", size=48)
        font_14 = Font("patterns/Jost-Bold.ttf", size=14)
        font_10 = Font("patterns/Jost-Medium.ttf", size=10)

        global_achievements = server_config.search(User.global_achievements != [])
        global_achievements = global_achievements[0]['global_achievements']
        user_achievements = db.search(User.user_id == user_id)[0]["achievements"]
        x_border = 50
        y_border = 155
        counter = 0
        page = 1

        percentage = len(user_achievements)/len(global_achievements)*100

        background.text((572, 86), f"{int(percentage)}%", font=font_48, color="#FFC54D")
        for i in global_achievements:
            if i in user_achievements:
                ach_icon = Editor(f"images/ach-icons/ach-icon-{i}-done.png")
            else:
                ach_icon = Editor(f"images/ach-icons/ach-icon-{i}.png")
            counter+=1
            background.paste(ach_icon, (x_border, y_border))

            y_border = y_border+79
            if counter == 4:
                x_border = 290
                y_border = 155
            if counter == 8:
                x_border = 530
                y_border = 155
            if counter == 12:
                page = page + 1

        

        user_id_for_filename = str(user_id).replace("<", "").replace(">", "").replace("@", "")
        file_name = f'achievements_image_{user_id_for_filename}_page{page}.png'
        file_path = f'images/{file_name}' 
        background.save(file_path) 
        file = discord.File(file_path, filename=f"{file_name}")

        file = discord.File(f'images/{file_name}', filename=f"{file_name}")
        embed = discord.Embed(
            title='🏆 Достижения',
            description='',
            color=discord.Color.light_grey()
        )    

        embed.set_image(url=f"attachment://{file_name}")
        return file, embed

    except Exception as e:
        await ctx.send(f"An error occurred in the achievements_info: {e}")

async def achievements_giver(user_id, achiev_id):
    try:
        db = TinyDB('./json/database.json', encoding='utf-8')
        User = Query()
        user_achievements = db.search(User.user_id == user_id)[0]["achievements"] 

        user_achievements.append(f"{achiev_id}")
        db.update({"achievements": user_achievements}, User.user_id == user_id)
        file = discord.File(f"images/ach-icons/ach-icon-{achiev_id}-msg.png", filename=f"ach-icon-{achiev_id}-msg.png")
        embed = discord.Embed(
            title=f'',
            description=f'🏆 {user_id} получил достижение',
            color=discord.Color.green()
        )    
        embed.set_image(url=f"attachment://ach-icon-{achiev_id}-msg.png")
        return embed, file
    except Exception as e:
        await print(f"An error occurred in the achievements_giver: {e}")

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
        try:
            user_id = f"<@{ctx.author.id}>"
            username = str(ctx.author.display_name)
            a_info = await achievements_info(ctx, user_id, username)  

            await ctx.send(file=a_info[0], embed=a_info[1])       
        except Exception as e:
            await ctx.send(f"An error occurred in the achievements command: {e}") 

        

async def setup(client):
    await client.add_cog(Achievements(client))
