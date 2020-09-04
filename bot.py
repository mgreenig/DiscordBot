# bot.py
import os
import re
from get_recent_matches import get_recent_score, club_links

import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if '?score' in message.content:
        club = re.sub('^\?score(\s)+', '', message.content)
        score = get_recent_score(club)
        await message.channel.send(score)

client.run(TOKEN)