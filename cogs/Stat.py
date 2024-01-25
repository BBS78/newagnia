import discord
from discord.ext import commands
from tinydb import TinyDB, Query
from easy_pil import Canvas, Editor, Font, load_image_async

async def statistic_info(ctx, user_id, username):
    try:
        # БД бота
        mdb = TinyDB('./json/marksdb.json', encoding='utf-8')
        User = Query()
        # ИНФА ОБ ОТМЕТКАХ
        user_data = mdb.search(User.user_id == user_id)
        all_pom = str(sum(entry["num_pom"] for entry in user_data))
        all_check = str(sum(entry["num_check"] for entry in user_data))
        all_fire = str(sum(entry["num_fire"] for entry in user_data))
        all_relax = str(sum(entry["num_relax"] for entry in user_data))
        # РИСУЕМ КАРТИНКУ
        background = Editor("images/stat_bg.png")
        tomato = Editor("images/tomato.png")
        check = Editor("images/check.png")
        fire = Editor("images/fire.png")
        relax = Editor("images/relax.png")
        # Подключаем шрифты
        font_39 = Font("patterns/Jost-Medium.ttf", size=39)
        x = 158
        y = 257
        space = 80
        linesize = (font_39.getsize(f"{all_pom}")[0]) + (font_39.getsize(f"{all_check}")[0]) + (font_39.getsize(f"{all_fire}")[0]) + (font_39.getsize(f"{all_relax}")[0]) + space*3
        if linesize >= 550: 
            space = 60
        background.text((x, y), all_pom, font=font_39, color="white")
        x = x + (font_39.getsize(f"{all_pom}")[0])+space
        background.paste(tomato, (x-space-4, y-10))
        background.text((x, y), all_check, font=font_39, color="white")
        x = x + (font_39.getsize(f"{all_check}")[0])+space
        background.paste(check, (x-space, y-7))
        background.text((x, y), all_fire, font=font_39, color="white")
        x = x + (font_39.getsize(f"{all_fire}")[0])+space
        background.paste(fire, (x-space-2, y-14))
        background.text((x, y), all_relax, font=font_39, color="white")
        x = x + (font_39.getsize(f"{all_relax}")[0])
        background.paste(relax, (x-2, y-10))
        # Сохранение и вывод файла
        user_id_for_filename = str(user_id).replace("<", "").replace(">", "").replace("@", "")
        file_path = f'images/stat_image_{user_id_for_filename}.png' 
        background.save(file_path)
        file = discord.File(file_path, filename=f"stat_image_{user_id_for_filename}.png")

        embed = discord.Embed(
            title=f'📊 Статистика {username}',
            description='',
            color=discord.Color.light_grey()
        )    

        embed.set_image(url=f"attachment://stat_image_{user_id_for_filename}.png")
        await ctx.send(file=file, embed=embed)

    except Exception as e:
        await ctx.send(f"An error occurred in the statistic_info: {e}")   

# Класс команды
class Stat(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Stat.py is ready")

    # Команда
    @commands.command(aliases=['s'])
    async def stat(self, ctx):
        try:
            username = str(ctx.author.display_name)
            user_id = f"<@{ctx.author.id}>"
            await statistic_info(ctx, user_id, username)
        except Exception as e:
            await ctx.send(f"An error occurred in the statistic command: {e}")
        

        

async def setup(client):
    await client.add_cog(Stat(client))
