import discord
from discord.ext import commands
from tinydb import TinyDB, Query
from easy_pil import Canvas, Editor, Font, load_image_async

# БД бота
db = TinyDB('./json/database.json', encoding='utf-8')
User = Query()

# ТЕКУЩИЕ ОЧКИ
def current_userdata(user_id, k):
    # БД бота
    db = TinyDB('./json/database.json', encoding='utf-8')
    User = Query()
    resalts = db.search(User.user_id == user_id)
    return resalts[0][k]

async def inventory_info(ctx, user_id, username):
    try:
        userdata = {
            "user_class": current_userdata(user_id, "user_class"),
            "lvl": current_userdata(user_id, "lvl"),
            "coins": current_userdata(user_id, "coins"),
            "inventory": current_userdata(user_id, "inventory")
        }

        background = Editor("images/inventory_bg.png")
        profile_image = await load_image_async(ctx.author.display_avatar.url)
        profile = Editor(profile_image).resize((61, 61))
        coin = Editor("images/coin.png").resize((19, 19))

        font_28 = Font("patterns/Jost-Bold.ttf", size=28)
        font_22 = Font("patterns/Jost-Medium.ttf", size=22)

        background.paste(profile, (63, 70))
        background.rectangle((63, 70), width=61, height=61, outline="#ffffff", stroke_width=5)

        background.text((320, 70), username, font=font_28, color="white")

        background.text((138, 111), f"{userdata['user_class']}  ◊  ", font=font_22, color="white")
        text_size = font_22.getsize(f"{userdata['user_class']}  ◊  ")

        background.text(((138 + text_size[0]), 111), f"{userdata['lvl']} lvl  ", font=font_22, color="#FFB043")
        text_size = font_22.getsize(f"{userdata['user_class']}  ◊  {userdata['lvl']} lvl  ")

        background.text(((138 + text_size[0]), 111), f"◊  {userdata['coins']}", font=font_22, color="white")
        text_size = font_22.getsize(f"{userdata['user_class']}  ◊  {userdata['lvl']} lvl  ◊  {userdata['coins']} ")
        background.paste(coin, (138 + text_size[0], 111))

        # Отрисовка предметов
        x = 77
        y = 181

        x_text = 62
        y_text = 267
        y_text_bottom = 289
        counter = 10
        for i in userdata["inventory"]:
            item_pic = Editor(f'images/items/{i["item_id"]}.png')
            background.paste(item_pic, (x, y))

            # Текст
            text = i["points"].split(" ")
            text_size = (font_22.getsize(text[0]))[0]
            x_position = (45-(text_size/2)) + x_text
            background.text((x_position, y_text), text[0], font=font_22, color="#FFB043")

            text_size = (font_22.getsize(text[1]))[0]
            x_position = (45-(text_size/2)) + x_text
            background.text((x_position, y_text_bottom), text[1], font=font_22, color="white")
            
            counter -= 1
            x += 135
            x_text += 135
            if counter == 5:
                x = 77
                y = 340  
                x_text = 62
                y_text = 425
                y_text_bottom = 447           

        user_id_for_filename = str(user_id).replace("<", "").replace(">", "").replace("@", "")
        file_path = f'images/inventory_image_{user_id_for_filename}.png' 
        background.save(file_path) 
        file = discord.File(file_path, filename=f"inventory_image_{user_id_for_filename}.png")

        file = discord.File(f'images/inventory_image_{user_id_for_filename}.png', filename=f"inventory_image_{user_id_for_filename}.png")
        embed = discord.Embed(
            title='🎒 Инвентарь пользователя',
            description='',
            color=discord.Color.light_grey()
        )    

        embed.set_image(url=f"attachment://inventory_image_{user_id_for_filename}.png")
        return file, embed

    except Exception as e:
        await ctx.send(f"An error occurred in the inventory_info: {e}")


# Класс команды
class Inventory(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Inventory.py is ready")

    # Команда
    @commands.command(aliases=['i'])
    async def inventory(self, ctx):
        try:
            user_id = f"<@{ctx.author.id}>"
            username = str(ctx.author.display_name)
            i_info = await inventory_info(ctx, user_id, username)  

            await ctx.send(file=i_info[0], embed=i_info[1])       
        except Exception as e:
            await ctx.send(f"An error occurred in the inventory command: {e}")        

        

async def setup(client):
    await client.add_cog(Inventory(client))
