#spawnvcRW04-4

import os
from datetime import datetime, timedelta
import time

import discord
#from discord.ext import commands

# uncomment the 2 lines below for PC deploy
# comment the 2 lines below for railway deploy
#from dotenv import load_dotenv
#load_dotenv('.env')

#intents = discord.Intents(messages=True, members=True, guilds=True, typing=True)

intents = discord.Intents().all()
bot = discord.Client(intents=intents)

# bot = commands.Bot(command_prefix='!', intents=intents)

Hours = -5

def formatDisplayName(bcmdn: str):
    if '#' in bcmdn:
        mnn = bcmdn[0:bcmdn.find('#')]
    else: mnn = bcmdn
    return mnn

@bot.event
async def on_voice_state_update(member, before, after):
    bcmdn = member.display_name
    
    mnn = formatDisplayName(bcmdn)
    
    print(f"\n\r{datetime.now() + timedelta(hours=Hours)} activity detected  {mnn} 01")
    print(f"{datetime.now() + timedelta(hours=Hours)} before  {before.channel} 00")
    print(f"{datetime.now() + timedelta(hours=Hours)} after  {after.channel} 00")
    print("before and after channel names not equal -> pass ? ")
    print((f"{before.channel}") != (f"{after.channel}"))
    
    bcmdn = member.display_name
    mnn = formatDisplayName(bcmdn)
    print((f"VCX {mnn}  {after.channel} equal -> block ?"))
    print((f"VCX {mnn}") == (f"{after.channel}"))
    
    if ((f"{before.channel}") != (f"{after.channel}")) and (f"VCX {mnn}")  != (f"{after.channel}"):
        if ((after.channel is not None and after.channel.name == 'MakeNewChannel') or
            (before.channel is not None and before.channel.name == 'MakeNewChannel') and
            (f"VCX {mnn}" != after.channel)):
            print(f"{datetime.now() + timedelta(hours=Hours)} after  {after.channel} 02")
            category = after.channel.category

            new_channel = await category.create_voice_channel(f"VCX {mnn}")
            time.sleep(.3);
            await member.move_to(new_channel)
            time.sleep(.3);
            print(f"{datetime.now() + timedelta(hours=Hours)} member moved 03")

        if before.channel is not None and 'VCX' in str({before.channel}):
            print(f"{datetime.now() + timedelta(hours=Hours)} before  {before.channel} 04")
            if len(before.channel.members) == 0:
                await before.channel.delete()
                time.sleep(.3);
                print(f"{datetime.now() + timedelta(hours=Hours)} channel deleted 05")
            else:
                bcmdn = before.channel.members[0].display_name

                mnn = formatDisplayName(bcmdn)
                
                print(f"{datetime.now() + timedelta(hours=Hours)} before  {before.channel} 06")
                await before.channel.edit(name = f"VCX {mnn}")
                time.sleep(.3);
                print(f"{datetime.now() + timedelta(hours=Hours)} channel renamed VCX {mnn} 07")
        
    print(f"{datetime.now() + timedelta(hours=Hours)} before  {before.channel} 08")
    print(f"{datetime.now() + timedelta(hours=Hours)} after  {after.channel} 09")
            
# PC deploy
#bot.run(os.getenv('TOKEN'))

#railway deploy 
bot.run(os.environ['TOKEN'])

# invite https://discord.com/api/oauth2/authorize?client_id=1079357107771551814&permissions=16777232&scope=bot
