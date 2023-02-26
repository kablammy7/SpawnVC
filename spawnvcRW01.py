#spawnvcRW02

import os
import datetime
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

@bot.event
async def on_voice_state_update(member, before, after):
    print(f"\n{datetime.now() + timedelta(hours=Hours)} activity detected  {member.display_name}")
    
    if after.channel is not None and after.channel.name == 'MakeNewChannel':
        category = after.channel.category
        if '#' in member.display_name:
            mnn = member.display_name[0:member.display_name.find('#')]
        else: mnn = member.display_name    
        new_channel = await category.create_voice_channel(f"VCX {mnn}") 
        await member.move_to(new_channel)
        print(f"{datetime.now() + timedelta(hours=Hours)} member moved")

    if before.channel is not None and 'VCX' in str({before.channel}):
        if len(before.channel.members) == 0:
            await before.channel.delete()
            print(f"{datetime.now() + timedelta(hours=Hours)} channel deleted")
        else:
            bcmdn = before.channel.members[0].display_name
            if '#' in bcmdn:
                mnn = bcmdn[0:bcmdn.find('#')]
                bcmdn=mnn
            await before.channel.edit(name = f"VCX {bcmdn}")
            print(f"{datetime.now() + timedelta(hours=Hours)} channel renamed")
            
# PC deploy
#bot.run(os.getenv('TOKEN'))

#railway deploy 
bot.run(os.environ['TOKEN'])

# invite https://discord.com/api/oauth2/authorize?client_id=1079357107771551814&permissions=16777232&scope=bot
