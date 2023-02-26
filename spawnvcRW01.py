#spawnvcRW01

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

@bot.event
async def on_voice_state_update(member, before, after):
    print(f"\nactivity detected {datetime.datetime.now()} {member.display_name}")
    
    if after.channel is not None and after.channel.name == 'COD':
        category = after.channel.category
        if '#' in member.display_name:
            mnn = member.display_name[0:member.display_name.find('#')]
        else: mnn = member.display_name    
        new_channel = await category.create_voice_channel(f"CODX {mnn}") 
        await member.move_to(new_channel)
        print(f"member moved {datetime.datetime.now()}")

    if before.channel is not None and 'CODX' in str({before.channel}):
        if len(before.channel.members) == 0:
            await before.channel.delete()
            print(f"channel deleted {datetime.datetime.now()}")
        else:
            bcmdn = before.channel.members[0].display_name
            if '#' in bcmdn:
                mnn = bcmdn[0:bcmdn.find('#')]
                bcmdn=mnn
            await before.channel.edit(name = f"CODX {bcmdn}")
            print(f"channel renamed {datetime.datetime.now()}")

# PC deploy
#bot.run(os.getenv('TOKEN'))

#railway deploy 
bot.run(os.environ['TOKEN'])

# invite https://discord.com/api/oauth2/authorize?client_id=1079357107771551814&permissions=16777232&scope=bot
