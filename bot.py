import discord
from discord.ext import commands
import requests
import random
import cfg

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='bzl ', intents=intents)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.command()
async def hello(ctx:commands.Context):
    await ctx.send(f'Hi! I am a bot {bot.user}!')

@bot.command()
async def heh(ctx:commands.Context, count_heh = 5):
    await ctx.send("he" * count_heh)

@bot.command()
async def btn(ctx:commands.Context):
    view = discord.ui.View()
    view.add_item(discord.ui.Button(
        style=discord.ButtonStyle.blurple,
        label="Click me",
        custom_id=f"click_me:{ctx.author.id}"
    ))
    await ctx.send(view=view)

@bot.event
async def on_interaction(itr: discord.Interaction):
    data = itr.data
    if not data:
        return
    
    user = itr.user
    
    if data["custom_id"] == f"click_me:{user.id}":
        await itr.response.defer()
        await itr.followup.send(f"hi {user.name}")
        await itr.followup.edit_message(itr.message.id, view=None)

@bot.command()
async def epstein(ctx:commands.Context):
    with open("images/epstein.jpeg", "rb") as f:
        await ctx.send(file=discord.File(f))

def get_meme():    
    url = 'https://meme-api.com/gimme'
    res = requests.get(url)
    data = res.json()
    return data['url'], data['title']

@bot.command()
async def meme(ctx:commands.Context):
    meme, name = get_meme()
    await ctx.send(f"{name}\n{meme}")

bot.run(cfg.token)