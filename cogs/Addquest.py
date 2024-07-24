import discord
from discord.ext import commands
from tinydb import TinyDB, Query
from easy_pil import Font
import pandas as pd
import asyncio

# БД бота
db = TinyDB('./json/database.json', encoding='utf-8')
User = Query()


async def create_channel(ctx):
    guild = ctx.guild
    author = ctx.message.author
    new_channel = await guild.create_text_channel(f'{author.global_name}-channel')
    
    overwrite = discord.PermissionOverwrite(read_messages=True)
    await new_channel.set_permissions(author, overwrite=overwrite)
    await new_channel.set_permissions(guild.default_role, read_messages=False)

    await ctx.send(f'Channel "{author.global_name}-channel" created successfully and unlocked only for {author.global_name}!')

    await new_channel.send(f'Привет, <@{ctx.author.id}>, давай начнем создание твоего супер-пупер квеста!')
    return new_channel

# Класс команды
class Addquest(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Addquest.py is ready")

    # Команда
    @commands.command(aliases=['aq'])
    async def addquest(self, ctx, *args):
        try:
            # create channel
            new_channel = await create_channel(ctx)
            await asyncio.sleep(1) 
            await new_channel.send("1. Напиши название квеста, оно будет отображено в верхушке инфографики, а также в моих напоминалках.")

            @commands.Cog.listener()
            async def on_message(self, ctx):
                await new_channel.send(ctx)
            # if len(args) == 0:
            #     embed = discord.Embed(
            #         title=':warning: Подсказка',
            #         description=f'Для создания личного квеста укажите через пробел следущее:',
            #         color=discord.Color.yellow()
            #     )
            #     embed.add_field(name='Название квеста', value='Используйте кавычки чтобы указать больше чем одно слово, например: "Улучшаю сон"', inline=False)
            #     embed.add_field(name='Cсылка на изображение', value='Это должна быть прямая ссылка на изображение, рекомендую использовать для этого сервис [imgbb](https://ru.imgbb.com/). Пример ссылки: https://i.ibb.co/dtYCkL2/Fjall-Armor.webp', inline=False)
            #     embed.add_field(name='Конечная цель', value='Это должно быть числовое значение. Например, если ваша конечная цель 10 книг, укажите число 10.', inline=False)
            #     embed.add_field(name='Кол-во монет за выполнение', value='Это должно быть числовое значение. Награды больше 10 монет требуют подтверждения админа.', inline=False)
            #     embed.add_field(name='Кол-во опыта за выполнение', value='Это должно быть числовое значение. Награды больше 250 опыта требуют подтверждения админа.', inline=False)
            #     embed.add_field(name='Урон по персонажу за НЕвыполнение', value='Это должно быть числовое значение.', inline=False)     

            #     embed.add_field(name='Комментарий (необязательно)', value='Вы можете написать описание квеста обернув его в кавычки.', inline=False) 

            #     embed.add_field(name='Пример полной команды', value='`!aq "Улучшаю сон" https://i.ibb.co/fnkyQM1/sleep.gif 30 10 200 5 "описание"`', inline=False)
                     

            #     file = discord.File(f'images/quest_body.png', filename=f"quest_body.png")
            #     embed.set_image(url=f"attachment://quest_body.png") 
            #     await ctx.send(file=file, embed=embed)
        except Exception as e:
            await print(f'{e}')

        

async def setup(client):
    await client.add_cog(Addquest(client))
