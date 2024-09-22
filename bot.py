# bot.py
import os
import random
from dotenv import load_dotenv
import openai
from openai import OpenAI

import discord
from discord.ext import commands

openai.api_key = os.getenv("OPENAI_API_KEY")

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
intents = discord.Intents.default()
intents.message_content = True  # Enable the message content intent

# 2
bot = commands.Bot(command_prefix='!roast', intents=intents) #this can change to something else later

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
@bot.command(name='me', help="rioast your op.gg")
async def ask(ctx, who):

    #first take all information from op.gg
    #then feed it into chatgpt
    

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[

        ]
    )
    msg = response.choices[0].message.content
    await ctx.send(msg)
bot.run(TOKEN)