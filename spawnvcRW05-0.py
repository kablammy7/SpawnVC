#spawnvcPC05-0
import os
import asyncio
from datetime import datetime, timedelta
import time
import discord
from discord.ext import commands


# uncomment the 2 lines below for PC deploy
# comment the 2 lines below for railway deploy
#from dotenv import load_dotenv
#load_dotenv('spammytest.env')

intents = discord.Intents().all()
#intents = discord.Intents().default()
#intents = discord.Intents(members=True, voice_states=True, value=True)
#client = discord.Client(intents=intents)
client = commands.Bot(command_prefix='?', intents=intents)

ZuluDiff = -5


@client.command()
async def restart(ctx):

    message = client.guilds[0].name + ' server is restarting'
    print (message)
    await ctx.send(message)
    print (message)
    member = client.guilds[0].get_member(425437217612103684)
    await member.send(message)
    os.execv(sys.executable, ['python'] + sys.argv)
    #await client.close()
    #await client.logout()


@client.command()
async def ping(ctx):

    embed = discord.Embed(description=(f'Pong!'),  colour=discord.Colour.purple())
    print ('pong sent')
    await ctx.send(embed=embed)


@client.command()
async def latency(ctx):

    await ctx.send (f" {client.latency}")


@client.event
async def on_message(message):

    if message.content.startswith('!move'):
        member_name = message.content.split()[1] # extract member name
        channel_name = message.content.split()[2] # extract channel name

        # find the member and voice channel objects by their names
        member = discord.utils.get(message.guild.members, name=member_name)
        voice_channel = discord.utils.get(message.guild.voice_channels, name=channel_name)

        if member is None:
            await message.channel.send(f"Could not find a member named {member_name}")
            return

        if voice_channel is None:
            await message.channel.send(f"Could not find a voice channel named {channel_name}")
            return

        # move the member to the specified voice channel
        await member.move_to(voice_channel)
        await message.channel.send(f"Moved {member_name} to {channel_name}")







#********************************* on ready *******************





@client.event
async def on_ready():

    print ('Logged in as {0.user}'.format(client))
    print ('Connected to server: {}'.format(client.guilds[0].name))

    print ('\n\rMember of Guid')
    
    for guild in client.guilds:
        print ('\n\r' f"{guild.name}")

        adjustmentsMade = False
        channels = guild.voice_channels
        
        # Remove empty VCX channels
        for channel in channels:
            #print ('start channel name = ' + channel.name)
            if (channel.name.startswith('VCX') and len(channel.members) == 0):
                await channel.delete()
                adjustmentsMade = True
                print ('deleted ' + channel.name)

        # move members out of MakeNewChannel channel   
        for channel in channels:
            if ((f"{channel.name}"== 'MakeNewChannel') and (len(channel.members)) != 0):
                #print (channel.name)
                lenChannelMembers = len(channel.members)
                while len(channel.members) > 0:
                    mncMember =  channel.members[0]
                    name = f"VCX {mncMember.display_name.split('#')[0]}"
                    movedToChannel = await channel.category.create_voice_channel(name)
                    await mncMember.move_to(movedToChannel)
                    adjustmentsMade = True
                    print ('channel ' + name + ' created moved ' + mncMember.name)

        message = ('adjustments made = 'f"{adjustmentsMade} on {guild.name} server")
        print ('\n\rfinished cleaning up ' + message)
                    
        member = client.guilds[0].get_member(425437217612103684)
        print ('sending message')
        await member.send(message)

    

@client.event
async def on_voice_state_update(member, before, after):

    print(f"\n\r01 --> {datetime.now() + timedelta(hours=ZuluDiff)} activity detected \
{member.display_name.split('#')[0]} (member name) {member.name}")
##    print (f"{before.channel}    VCX {member.display_name.split('#')[0]}")
##    print (f"{after.channel}       MakeNewChannel")
##    
##    print (f"{before.channel}" == f"VCX {member.display_name.split('#')[0]}")
##    print (f"{after.channel}" != "MakeNewChannel")
##
##    if (f"{before.channel}" == f"VCX {member.display_name.split('#')[0]}") and \
##    (f"{after.channel}" != "MakeNewChannel"):
        
    print (f"\n\r01 --> {datetime.now() + timedelta(hours=ZuluDiff)} activity detected \
{member.display_name.split('#')[0]} (member name) {member.name}")

    if after.channel is not None and after.channel.name == "MakeNewChannel":
        category = after.channel.category
        name = f"VCX {member.display_name.split('#')[0]}"
        channel = await category.create_voice_channel(name)
        await member.move_to(channel)
        print (f"02 --> {datetime.now() + timedelta(hours=ZuluDiff)}  move to new channel {channel}")
 
    if before.channel is not None and 'VCX' in str({before.channel}):
        memberName = f"VCX {member.display_name.split('#')[0]}"
        if len(before.channel.members) == 0:
            await before.channel.delete()
            print (f"03 --> {datetime.now() + timedelta(hours=ZuluDiff)} vacated channel {before.channel} deleted")
        else:
            beforeChannel = f"{before.channel}"
            if((f"{before.channel}") != (f"{after.channel}")):
                newName = f"VCX {before.channel.members[0].display_name.split('#')[0]}"
                await before.channel.edit(name=newName)
                print (f"04 --> {datetime.now() + timedelta(hours=ZuluDiff)} before channel {beforeChannel} renamed to {newName}")
 

        

# PC deploy
#client.run(os.getenv('TOKEN'))

#railway deploy 
client.run(os.environ['TOKEN'])

# https://discord.com/api/oauth2/authorize?client_id=1079357107771551814&permissions=16787472&scope=bot%20applications.commands
