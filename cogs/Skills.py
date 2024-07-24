import discord
from discord.ext import commands
from discord.ui import Button, View
from tinydb import TinyDB, Query
import random
from easy_pil import Canvas, Editor, Font, load_image_async
from cogs.Profile import current_userdata

# БД бота
db = TinyDB('./json/database.json', encoding='utf-8')
User = Query()

async def skills_info(ctx, user_id):
    try: 
        userdata = {
            "user_class": current_userdata(user_id, "user_class"),
            "skills": current_userdata(user_id, "skills")
        }
        embed = discord.Embed(
            title='🌀 Способности персонажа',
            description='',
            color=discord.Color.light_grey()
        ) 
        embed.set_author(name=f"{ctx.author.display_name}", icon_url=f"{ctx.author.display_avatar}")
        skills = userdata["skills"]
        counter = 0
        for i in skills:
            counter += 1
            if i["skill_type"] != "passive":
                skill_type = f'Перезарядка: {i["skill_type"]} \n Используйте кнопки для активации'
                embed.add_field(name=f'[{counter}] {i["skill_name"]}', value=f'{i["skill_properties"]}\n{skill_type}', inline=False)
        for i in skills:
            if i["skill_type"] == "passive":
                skill_type = f'Это пассивная способность'
                embed.add_field(name=f'{i["skill_name"]}', value=f'{i["skill_properties"]}\n{skill_type}', inline=False)

        embed.set_footer(text="Импользуйте !use [номер скилла]")
        return embed
    except Exception as e:
        await ctx.send(f"An error occurred in skills_info: {e}")    


# Класс команды
class Skills(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Skills.py is ready")

    # Команда
    @commands.command(aliases=['sk'])
    async def skills(self, ctx):
        try:
            user_id = f"<@{ctx.author.id}>"

            async def on_button_click(interaction):
                try:
                    skill_name = interaction.component.label
                    await interaction.response.send_message(f'Способность **"{skill_name}"** использована')  
                except Exception as e:
                    print(f"An error occurred: {e}")

            sk_info = await skills_info(ctx, user_id)
            await ctx.send(embed=sk_info)
        except Exception as e:
            await ctx.send(f"An error occurred in skills command: {e}")
        

async def setup(client):
    await client.add_cog(Skills(client))