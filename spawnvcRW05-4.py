
#spawnvcPC05-4.py

import os
import asyncio
from datetime import datetime, timedelta
import time
import discord
from discord.ext import commands
from reportlab.pdfgen import canvas
from discord.ext import commands, tasks
from reportlab.pdfgen import canvas
import re


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
patternGetInt = r"^\D\D(\d{2})"













client.command()
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


##@client.command()
##async def lvc(ctx):
##    guild = ctx.guild
##    voice_channels = guild.voice_channels
##    channel_list = ""
##    for channel in voice_channels:
##        members = channel.members
##        member_list = [member.display_name for member in members]
##        member_string = ", ".join(member_list) if member_list else "None"
##        channel_list += f"{channel.name}: {member_string}\n"
##    await ctx.send(channel_list)























#########################           on ready            #########################





@client.event
async def on_ready():

    print ('\n\rLogged in as {0.user}'.format(client))
    print(f'Connected to {len(client.guilds)} guilds')

    for guild in client.guilds:
        print ('Connected to server: {}'.format(guild.name))

    for guild in client.guilds:
        print ('\n\r' f"Guild = [{guild.name}]")

        adjustmentsMade = False
        channels = guild.voice_channels
        
        # Remove empty VC channels
        for channel in channels:
            #print ('start channel name = ' + channel.name)
            if (channel.name.startswith('VC') and len(channel.members) == 0):
                await channel.delete()
                adjustmentsMade = True
                print (f"Guild [{guild.name}] deleted [{channel.name}]")
                # Get the target channel to place the sorted channels after
                target_channel = discord.utils.get(guild.voice_channels, name="MakeNewChannel")

                # Get all voice channels in the guild
                all_channels = guild.voice_channels

                # Get the index of the target channel in the list of all channels
                target_index = all_channels.index(target_channel)

                # Get the "VC" channels and sort them alphabetically
                vc_channels = sorted([c for c in all_channels if c.name.startswith("VC")], key=lambda c: c.name)

                # Update the channel positions in the guild to place the "VC" channels after the target channel
                for i, c in enumerate(vc_channels):
                    await c.edit(position=target_index+i+1)

                # Print the sorted voice channels (optional)
                for c in all_channels:
                    print(c.name)

        # move members out of MakeNewChannel channel   
        for channel in channels:
            if ((f"{channel.name}"== 'MakeNewChannel') and (len(channel.members)) != 0):
                #print (channel.name)
                lenChannelMembers = len(channel.members)
                while len(channel.members) > 0:
                    mncMember =  channel.members[0]


                    existingChannels = [c for c in channel.guild.voice_channels if c.name.startswith("VC")]
                
                    newChannelNumber = getNewChannelNumber(existingChannels)

                    newChannelName = f"VC{newChannelNumber:02} {mncMember.display_name.split('#')[0]}"

                    movedToChannel = await channel.category.create_voice_channel(newChannelName)
                    await mncMember.move_to(movedToChannel)
                    adjustmentsMade = True
                    print (f"Guild [{guild.name}] channel [{newChannelName}] created moved [{mncMember.name}]")

        message = ('adjustments made = 'f"{adjustmentsMade} on {guild.name} server")
        print ('\n\rfinished cleaning up ' + message)
                    
        member = client.guilds[0].get_member(425437217612103684)
        print ('sending message')
        await member.send(message)







        
    print ('exiting on_ready now')
    exit



























##################        functions           ###########################



def truncate_datetime (dt):
    dt_str = str(dt)
    period_index = dt_str.rfind(".")
    if period_index != -1:
        dt_str = dt_str[:period_index]
    return dt_str


def getNewChannelNumber (existingChannels):

    takenNumbers = []
    for channel in existingChannels:
        match = re.match(patternGetInt, channel.name)
        if match:
            number = int(match.group(1))
            takenNumbers.append(number)
    
    newChannelNumber = 0
    while newChannelNumber in takenNumbers:
        newChannelNumber += 1
        
    return newChannelNumber




























@client.event
async def on_voice_state_update(member, before, after):

    

#     print(f"\n\r01 --> {datetime.now() + timedelta(hours=ZuluDiff)} activity detected {member.display_name.split('#')[0]} (member name) {member.name}")
##    print (f"{before.channel}    VC {member.display_name.split('#')[0]}")
##    print (f"{after.channel}       MakeNewChannel")
##    
##    print (f"{before.channel}" == f"VC {member.display_name.split('#')[0]}")
##    print (f"{after.channel}" != "MakeNewChannel")
##
##    if (f"{before.channel}" == f"VC {member.display_name.split('#')[0]}") and \
##    (f"{after.channel}" != "MakeNewChannel"):
        
#     print (f"\n\r01 --> {datetime.now() + timedelta(hours=ZuluDiff)} activity detected {member.display_name.split('#')[0]} (member name) {member.name}")


    guild = member.guild

    memberDisplayName = member.display_name.split('#')[0]
    memberName = member.name

    if after.channel is not None and after.channel.name == "MakeNewChannel":
        category = after.channel.category
        existingChannels = [c for c in after.channel.guild.voice_channels if c.name.startswith("VC")]
        newChannelNumber = getNewChannelNumber(existingChannels)
        newChannelName = f"VC{newChannelNumber:02} {member.display_name.split('#')[0]}"

        channel = await category.create_voice_channel(newChannelName)
        await member.move_to(channel)
        print (f"01 --> {truncate_datetime(datetime.now() + timedelta(hours=ZuluDiff))} Guild [{guild.name}] [{memberDisplayName}] - [{memberName}] move to new channel [{channel}]")
 
    if before.channel is not None and 'VC' in str({before.channel}):
        #memberName = f"VC[int(re.match(patternGetInt, channel.name).group(1))] {member.display_name.split('#')[0]}"
        if len(before.channel.members) == 0:
            await before.channel.delete()
            print (f"02 --> {truncate_datetime(datetime.now() + timedelta(hours=ZuluDiff))} Guild [{guild.name}] [{memberDisplayName}] - [{memberName}] vacated channel [{before.channel}] deleted")

            # Get the target channel to place the sorted channels after
            target_channel = discord.utils.get(guild.voice_channels, name="MakeNewChannel")

            # Get all voice channels in the guild
            all_channels = guild.voice_channels

            # Get the index of the target channel in the list of all channels
            target_index = all_channels.index(target_channel)

            # Get the "VC" channels and sort them alphabetically
            vc_channels = sorted([c for c in all_channels if c.name.startswith("VC")], key=lambda c: c.name)

            # Update the channel positions in the guild to place the "VC" channels after the target channel
            for i, c in enumerate(vc_channels):
                await c.edit(position=target_index+i+1)

            # Print the sorted voice channels (optional)
            for c in all_channels:
                print(c.name)

        else:
            beforeChannel = f"{before.channel}"
            if((f"{before.channel}") != (f"{after.channel}")):
                newName = f"VC{(re.match(patternGetInt, str(beforeChannel)).group(1))} {before.channel.members[0].display_name.split('#')[0]}"
                await before.channel.edit(name=newName)
                print (f"03 --> {truncate_datetime(datetime.now() + timedelta(hours=ZuluDiff))} Guild [{guild.name}] [{memberDisplayName}] - [{memberName}] before channel [{beforeChannel}] renamed to [{newName}]")
 

# PC deploy
#client.run(os.getenv('TOKEN'))

#railway deploy 
client.run(os.environ['TOKEN'])

# https://discord.com/api/oauth2/authorize?client_id=1079357107771551814&permissions=16787472&scope=bot%20applications.commands
