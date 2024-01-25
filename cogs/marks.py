import discord
from discord.ext import commands
from tinydb import TinyDB, Query
from easy_pil import Canvas, Editor, Font, load_image_async
import asyncio
import datetime
from datetime import datetime, timedelta

# БД бота
db = TinyDB('./json/database.json', encoding='utf-8')
User = Query()

# Класс команды
class Marks(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Marks.py is ready")

    @commands.Cog.listener()
    async def on_message(self, ctx):
        if ctx.channel.id == 1193647715398205560:
            if ctx.author.id == 1122950889594961995 or ctx.author.id == 1021098227342254220:
                return
            if ctx.content.startswith('.'):
                return
            pom_emoji = ["<:pom:678849691403943965>", "<:checkpom:890586910509125664>", "🍅", "<:pomWin:744085631772262430>",
                            ":pomWin:", ":checkpom:", ":pom:", "🍊"]
            check_emoji = ["<:d3:806171597174079559>", "✅", ":d3:", ":d3_NY:", ":d3_NY2:", "<:d3_NY2:1179729870281003098>", "<:d3_NY:1179727889789370429>"]
            fire_emoji = ["🔥"]
            relax_emoji = ["<:relax:795944514262663198>", "🛡️", ":relax:"]

            emoji_lists = [relax_emoji, pom_emoji, fire_emoji, check_emoji]
            if any(any(r in ctx.content for r in emoji_list) for emoji_list in emoji_lists):
                user_id = f'<@{ctx.author.id}>'
                msg_split = ctx.content.split()
                resalt = ["Записала "]
                db = TinyDB('./json/database.json', encoding='utf-8')
                user_info = db.search(User.user_id == user_id)
                categories = []
                categories_id = []
                # Добавляем названия категорий если есть
                for category_key in ["01", "02", "03"]:
                    category_value = user_info[0].get(category_key)
                    if category_value != "None":
                        category_values = category_value.split(" ")
                        categories_id.append(category_key)
                        categories.append(category_values[0])
                # 1) ПРОВЕРКА КАТЕГОРИИ
                category_name = "Null"
                if categories != []:
                    for index, element in enumerate(msg_split):
                        if element in categories:
                            category_name = element
                # 2) ПОИСК ОТМЕТОК
                num_pom, num_check, num_fire, num_relax = 0, 0, 0, 0
                for index, element in enumerate(msg_split):  
                    if element in (pom_emoji):
                        resalt.append(f"{int(msg_split[index - 1])} {element} ")
                        num_pom = int(msg_split[index - 1])
                    
                    if element in (check_emoji):
                        resalt.append(f"{int(msg_split[index - 1])} {element} ")
                        num_check = int(msg_split[index - 1])

                    if element in (fire_emoji):
                        resalt.append(f"{int(int(msg_split[index - 1])*1.15)} {element}(+15%) ")
                        num_fire = int(int(msg_split[index - 1])*1.15)

                    if element in (relax_emoji):
                        resalt.append(f"{int(msg_split[index - 1])} {element} ")
                        num_relax = int(msg_split[index - 1])
                # 3) ОПРЕДЕЛЕНИЕ ЧИСЛА
                try:
                    msg = ctx.content.split(" за ")
                    if len(msg) == 2:
                        sign_date = msg[1]
                    else:
                        month_names = {
                            1: 'января',
                            2: 'февраля',
                            3: 'марта',
                            4: 'апреля',
                            5: 'мая',
                            6: 'июня',
                            7: 'июля',
                            8: 'августа',
                            9: 'сентября',
                            10: 'октября',
                            11: 'ноября',
                            12: 'декабря'
                        }

                        current_date = datetime.now()
                        day = current_date.day
                        month = current_date.month
                        year = current_date.year

                        sign_date = f"{day} {month_names[month]} {year}"           
                except Exception as e:
                    await ctx.channel.send(f"somethong wrong: {e}")
                # 4) ЗАПИСЬ ОТМЕТОК в БД
                mdb = TinyDB('./json/marksdb.json', encoding='utf-8')
                mdb.insert({"user_id": user_id,
                            "markdate": sign_date,
                            "num_pom": num_pom,
                            "num_check": num_check,
                            "num_fire": num_fire,
                            "num_relax": num_relax
                            })
                # 5) Запись опыта пользователя
                db = TinyDB('./json/database.json', encoding='utf-8')
                user_exp = db.search(User.user_id == user_id)[0]['exp']
                user_max_exp = db.search(User.user_id == user_id)[0]['max_exp']
                user_lvl = db.search(User.user_id == user_id)[0]['lvl']
                user_coins = db.search(User.user_id == user_id)[0]['coins']


                user_exp = int(num_pom + num_check + num_fire + (num_relax*0.2) + user_exp)
                
                while user_exp >= user_max_exp: # если достиг нового уровня
                    user_exp -= user_max_exp
                    user_max_exp *= 1.15
                    user_lvl += 1 
                    user_coins += user_lvl * 2
                    # Тут должен быть эмбед с картинкой

                db.update({"exp": int(user_exp)}, User.user_id == user_id)
                db.update({"max_exp": int(user_max_exp)}, User.user_id == user_id)
                db.update({"lvl": int(user_lvl)}, User.user_id == user_id)
                db.update({"coins": int(user_coins)}, User.user_id == user_id)
                # 6) Запись отметок для гарнизона (В будущем)
                #
                # 
                # 7) Запись отдыха для гарнизона (В будущем)
                resalt = " ".join(resalt)
                bot_message = await ctx.reply(f"{resalt} за {sign_date}")   
                await asyncio.sleep(5)  
                await bot_message.delete()
            

        

async def setup(client):
    await client.add_cog(Marks(client))