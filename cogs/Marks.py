import discord
from discord.ext import commands
from tinydb import TinyDB, Query
import asyncio
import datetime
from datetime import datetime, timedelta
from cogs.Ashievements import achievements_giver
from cogs.Profile import profile_lvl

client = commands.Bot(command_prefix='!', intents=discord.Intents.all())

async def achievements_check(self, ctx, user_id):
    try:
        mdb = TinyDB('./json/marksdb.json', encoding='utf-8')
        db = TinyDB('./json/database.json', encoding='utf-8')
        User = Query()
        user_achievements = db.search(User.user_id == user_id)[0]["achievements"]
        user_data_marks = mdb.search(User.user_id == user_id)  
        
        all_pom = int(sum(entry["num_pom"] for entry in user_data_marks))
        all_check = int(sum(entry["num_check"] for entry in user_data_marks))
        all_fire = int(sum(entry["num_fire"] for entry in user_data_marks))
        all_relax = int(sum(entry["num_relax"] for entry in user_data_marks))

        text_channel = self.client.get_channel(675993483948982272)
        # ПОМИДОРЫ
        achievements_thresholds = [(100, "01"), (500, "02"), (1000, "03"), (5000, "04")]
        for threshold, achievement_code in achievements_thresholds:
            if all_pom >= threshold and achievement_code not in user_achievements:
                a_giver = await achievements_giver(user_id, achievement_code)
                await text_channel.send(embed=a_giver[0], file=a_giver[1])

        # ОТДЫХ
        achievements_thresholds = [(100, "05"), (500, "06"), (1000, "07"), (5000, "08")]
        for threshold, achievement_code in achievements_thresholds:
            if all_relax >= threshold and achievement_code not in user_achievements:
                a_giver = await achievements_giver(user_id, achievement_code)
                await text_channel.send(embed=a_giver[0], file=a_giver[1])

        # ОГОНЬКИ
        achievements_thresholds = [(100, "09"), (500, "10"), (1000, "11"), (5000, "12")]
        for threshold, achievement_code in achievements_thresholds:
            if all_fire >= threshold and achievement_code not in user_achievements:
                a_giver = await achievements_giver(user_id, achievement_code)
                await text_channel.send(embed=a_giver[0], file=a_giver[1])
        


    except Exception as e:
        print(f"somethong wrong in achievements_check(): {e}")    

# Класс команды
class Marks(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Marks.py is ready")

    @commands.Cog.listener()
    async def on_message(self, ctx):

        if ctx.channel.id == 1193647715398205560 or ctx.channel.id == 715915520498729000:
            try:
                if ctx.author.id == 1122950889594961995 or ctx.author.id == 1021098227342254220:
                    return
                if ctx.content.startswith('.'):
                    return
                pom_emoji = ["<:pom:678849691403943965>", "<:checkpom:890586910509125664>", "🍅", "<:pomWin:744085631772262430>",
                                ":pomWin:", ":checkpom:", ":pom:", "🍊"]
                check_emoji = ["<:d3:806171597174079559>", "✅", ":d3:", ":d3_NY:", ":d3_NY2:", "<:d3_NY2:1179729870281003098>", "<:d3_NY:1179727889789370429>"]
                fire_emoji = ["🔥"]
                relax_emoji = ["<:relax:795944514262663198>", "🛡️", ":relax:"]

                # БД бота
                db = TinyDB('./json/database.json', encoding='utf-8')
                mdb = TinyDB('./json/marksdb.json', encoding='utf-8')
                User = Query()

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
                                "inventary": [],
                                "achievements": []  
                                    })
                except Exception as e:
                    print(f"Не могу добавить в бд:{e}")                 

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
                        print(f"somethong wrong: {e}")
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

                    db.update({"exp": int(user_exp)}, User.user_id == user_id)

                    try:
                        await profile_lvl(self, ctx, user_id)
                    except Exception as e:
                        print(f"An error occurred in profile_lvl update: {e}")
                    # 6) Запись отметок для гарнизона (В будущем)
                    #
                    # 
                    # 7) Запись отдыха для гарнизона (В будущем)

                    # ВЫВОД РЕЗУЛЬТАТОВ:
                    resalt = " ".join(resalt)
                    bot_message = await ctx.reply(f"{resalt} за {sign_date}")   

                    await achievements_check(self, ctx, user_id)
                    await asyncio.sleep(5)  
                    await bot_message.delete()

                    # 8) Ачивки
                    # mdb = TinyDB('./json/marksdb.json', encoding='utf-8')
                    # db = TinyDB('./json/database.json', encoding='utf-8')
                    # User = Query()
                    # user_achievements = db.search(User.user_id == user_id)[0]["achievements"]
                    # user_data_marks = mdb.search(User.user_id == user_id)  
                    
                    # all_pom = int(sum(entry["num_pom"] for entry in user_data_marks))
                    # all_check = int(sum(entry["num_check"] for entry in user_data_marks))
                    # all_fire = int(sum(entry["num_fire"] for entry in user_data_marks))
                    # all_relax = int(sum(entry["num_relax"] for entry in user_data_marks)) 
                    # print(all_pom)
                    # print(user_achievements)
                    # if all_pom >= 100 and "01" not in user_achievements:
                    #     user_achievements.append("01")
                    #     db.update({"achievements": user_achievements}, User.user_id == user_id)
                    #     file = discord.File(f"images/ach-icons/ach-icon-01-msg.png", filename=f"ach-icon-01-msg.png")
                    #     await ctx.reply(f'{user_id} получил достижение', file=file)   
            except Exception as e:
                print(f"Не могу записать отметки: {e}")        

async def setup(client):
    try:
        await client.add_cog(Marks(client))
    except Exception as e:
        print(f"{e}")