#spawnvcRW05-0

import os
from datetime import datetime, timedelta
import time

import discord
#from discord.ext import commands

# uncomment the 2 lines below for PC deploy
# comment the 2 lines below for railway deploy
#from dotenv import load_dotenv
#load_dotenv('spammytest.env')

intents = discord.Intents().all()
#intents = discord.Intents().default()
#client = discord.Client(intents=intents)
#intents = discord.Intents(members=True, voice_states=True, value=True)

client = commands.Bot(command_prefix='?', intents=intents)

Hours = -5


@client.command()
async def restart(ctx):
    message = client.guilds[0].name + ' server is restarting'
    print(message)
    await ctx.send(message)
    print(message)
    member = client.guilds[0].get_member(425437217612103684)
    await member.send(message)
    os.execv(sys.executable, ['python'] + sys.argv)
    #await client.close()
    #await client.logout()

os.getenv('TOKEN')


@client.command()
async def ping(ctx):
    embed = discord.Embed(description=(f'Pong!'),  colour=discord.Colour.purple())
    print('pong sent')
    await ctx.send(embed=embed)

@client.command()
async def latency(ctx):
    await ctx.send (f" {client.latency}")









@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))
    print('Connected to server: {}'.format(client.guilds[0].name))

    print('\n\rMember of Guid')
    
    for guild in client.guilds:
        print('\n\r' f"{guild.name}")

        adjustmentsMade = False
        channels = guild.voice_channels
        
        # Remove empty VCX channels
        for channel in channels:
            #print('start channel name = ' + channel.name)
            if (channel.name.startswith('VCX') and len(channel.members) == 0):
                await channel.delete()
                adjustmentsMade = True
                print('deleted ' + channel.name)

        # move members out of MakeNewChannel channel   
        for channel in channels:
            if ((f"{channel.name}"== 'MakeNewChannel') and (len(channel.members)) != 0):
                #print(channel.name)
                lenChannelMembers = len(channel.members)
                while len(channel.members) > 0:
                    mncMember =  channel.members[0]
                    name = f"VCX {mncMember.display_name.split('#')[0]}"
                    movedToChannel = await channel.category.create_voice_channel(name)
                    await mncMember.move_to(movedToChannel)
                    adjustmentsMade = True
                    print('channel ' + name + ' created moved ' + mncMember.name)

        message = ('adjustments made = 'f"{adjustmentsMade} on {guild.name} server")
        print('\n\rfinished cleaning up ' + message)
                    
        member = client.guilds[0].get_member(425437217612103684)
        print('sending message')
        await member.send(message)

    

@client.event
async def on_voice_state_update(member, before, after):
    print(f"\n\r01 --> {datetime.now() + timedelta(hours=ZuluDiff)} activity detected \
{member.display_name.split('#')[0]} (member name) {member.name}")
##    print(f"{datetime.now() + timedelta(hours=ZuluDiff)} before  {before.channel}")
##    print(f"{datetime.now() + timedelta(hours=ZuluDiff)} after  {after.channel}")
##    if after.channel:
##        print(f"Muted: {after.mute}")
##        print(f"Deafened: {after.deaf}")
##        print(f"Self Mute: {after.self_mute}")
##        print(f"Self Deaf: {after.self_deaf}")
##    else:
##        print(f"{member.name} left the voice channel.")
    
    if after.channel is not None and after.channel.name == "MakeNewChannel":
        category = after.channel.category
        name = f"VCX {member.display_name.split('#')[0]}"
        channel = await category.create_voice_channel(name)
        await member.move_to(channel)
        print(f"02 --> {datetime.now() + timedelta(hours=ZuluDiff)}  name new channel {channel}")
 
    if before.channel is not None and 'VCX' in str({before.channel}):
        memberName = f"VCX {member.display_name.split('#')[0]}"
        if len(before.channel.members) == 0:
            await before.channel.delete()
            print(f"03 --> {datetime.now() + timedelta(hours=ZuluDiff)} channel {before.channel} deleted")
        else:
            beforeChannel = f"{before.channel}"
            if((f"{before.channel}") != (f"{after.channel}")):
                newName = f"VCX {before.channel.members[0].display_name.split('#')[0]}"
                await before.channel.edit(name=newName)
                print(f"04 --> {datetime.now() + timedelta(hours=ZuluDiff)} before channel  {beforeChannel}  renamed to {newName}")



# PC deploy
#bot.run(os.getenv('TOKEN'))

#railway deploy 
bot.run(os.environ['TOKEN'])

# invite https://discord.com/api/oauth2/authorize?client_id=1079357107771551814&permissions=16777232&scope=bot
