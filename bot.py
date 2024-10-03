# bot.py
import os
from dotenv import load_dotenv
import openai
from index import getDB
from openai import OpenAI

import discord
from discord.ext import commands


load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
RIOT_API_KEY = os.getenv('RIOT_API_KEY')
openai.api_key = os.getenv("OPENAI_API_KEY")

intents = discord.Intents.default()
intents.message_content = True  # Enable the message content intent

# 2
bot = commands.Bot(command_prefix='$roast', intents=intents) #this can change to something else later

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    if message.content.lower() == 'ping':
        await message.channel.send('pong')
    
    await bot.process_commands(message)

client = OpenAI()
@bot.command(name='me', help="roast your op.gg")
async def ask(ctx, who):
    stats = await getDB(who)
    print(stats)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
        {"role": "system", "content": "You are a vulgar league of legends comedian"},
        {"role": "user", "content": "Roast my stats in one sentence: " + stats + ", mention numbers such as average deaths per game"}
        ]
    )
    msg = response.choices[0].message.content
    await ctx.send(msg)
bot.run(DISCORD_TOKEN)