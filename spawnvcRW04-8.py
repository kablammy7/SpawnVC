#spawnvcRW04-8

import os
from datetime import datetime, timedelta
import time

import discord
#from discord.ext import commands

# uncomment the 2 lines below for PC deploy
# comment the 2 lines below for railway deploy
#from dotenv import load_dotenv
#load_dotenv('spammytest.env')

intents = discord.Intents(members=True, voice_states=True, value=True)
bot = discord.Client(intents=intents)

Hours = -5

@bot.event
async def on_voice_state_update(member, before, after):
    print(f"\n\r{datetime.now() + timedelta(hours=Hours)} activity detected {member.display_name.split('#')[0]} 01")
    print(f"{datetime.now() + timedelta(hours=Hours)} before  {before.channel} 00")
    print(f"{datetime.now() + timedelta(hours=Hours)} after  {after.channel} 00")
    
    if after.channel is not None and after.channel.name == "MakeNewChannel":
        category = after.channel.category
        name = f"VCX {member.display_name.split('#')[0]}"
        channel = await category.create_voice_channel(name)
        await member.move_to(channel)
        print(f"{datetime.now() + timedelta(hours=Hours)}  name new channel {channel} 02")
 
    if before.channel is not None and 'VCX' in str({before.channel}):
        memberName = f"VCX {member.display_name.split('#')[0]}"
        if len(before.channel.members) == 0:
            await before.channel.delete()
            print(f"{datetime.now() + timedelta(hours=Hours)} {before.channel} deleted  + name + 03")
        else:
            beforeChannel = f"{before.channel}"
            if((f"{before.channel}") != (f"{after.channel}")):
                newName = f"VCX {before.channel.members[0].display_name.split('#')[0]}"
                await before.channel.edit(name=newName)
                print(f"{datetime.now() + timedelta(hours=Hours)} before channel  {beforeChannel}  renamed to {newName} + 04")

# PC deploy
#bot.run(os.getenv('TOKEN'))

#railway deploy 
bot.run(os.environ['TOKEN'])

# invite https://discord.com/api/oauth2/authorize?client_id=1079357107771551814&permissions=16777232&scope=bot
