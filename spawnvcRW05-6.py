
#spawnvcPC05-6.py

import os
import threading
import asyncio
from datetime import datetime, timedelta
import time
import discord
#from discord.ext import commands
from discord.ext import commands, tasks
import re
#from reportlab.pdfgen import canvas



# uncomment the 2 lines below for PC deploy
# comment the 2 lines below for railway deploy
#from dotenv import load_dotenv
#load_dotenv('spammytest.env')

#intents = discord.Intents().all()
#intents = discord.Intents().default()
intents = discord.Intents(members=True, voice_states=True, value=True)
client = discord.Client(intents=intents)
client = commands.Bot(command_prefix='?', intents=intents)







zuluDiff = -5
patternGetInt = r"^\D\D(\d{2})"
channelsData = {}
lockReporting = False
reportNumber = 0
#guildData = {}










#async def my_function():
#    # Do something here
#    print("My function ran!")

## Schedule the function to run every 10 minutes
#async def run_function():
#    while True:
#        await my_function()
#        await asyncio.sleep(10)  





#async def my_coroutine():
#    while True:
#        print("Running my coroutine!")
#        await asyncio.sleep(10)

#def start_loop(loop):
#    asyncio.set_event_loop(loop)
#    loop.run_forever()


#loop = asyncio.new_event_loop()
#thread = threading.Thread(target=start_loop, args=(loop,))
#thread.start()

#asyncio.run(my_coroutine())






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
    lockRorting = False
    reportNumber = 0
    print ('\n\rLogged in as {0.user}'.format(client))
    print(f'Connected to {len(client.guilds)} guilds')

    for guild in client.guilds:
        print ('Connected to server: {}'.format(guild.name))

    for guild in client.guilds:
        print ('\n\r' f"Guild = [{guild.name}]")

        adjustmentsMade = False
        channels = guild.voice_channels
        
        # sort the voice channels
        target_channel = discord.utils.get(guild.voice_channels, name="MakeNewChannel")
        all_channels = guild.voice_channels
        target_index = all_channels.index(target_channel)
        vc_channels = sorted([c for c in all_channels if c.name.startswith("VC")], key=lambda c: c.name)
        for i, c in enumerate(vc_channels):
            await c.edit(position=target_index+i+1)

        # Remove empty VC channels
        for channel in channels:
            #print ('start channel name = ' + channel.name)
            if ((channel.name.startswith('VC')) and (len(channel.members) == 0)):
                await channel.delete()
                adjustmentsMade = True
                print (f"Guild [{guild.name}] deleted [{channel.name}]")

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
                    # sort the voice channels
                    target_channel = discord.utils.get(guild.voice_channels, name="MakeNewChannel")
                    all_channels = guild.voice_channels
                    target_index = all_channels.index(target_channel)
                    vc_channels = sorted([c for c in all_channels if c.name.startswith("VC")], key=lambda c: c.name)
                    for i, c in enumerate(vc_channels):
                        await c.edit(position=target_index+i+1)

        message = ('adjustments made = 'f"{adjustmentsMade} on {guild.name} server")
        print ('\n\rfinished cleaning up ' + message)
                    
        member = client.guilds[0].get_member(425437217612103684)
        print ('sending message')
        await member.send(message)

    


    botGuilds = client.guilds
    print ('guilds set')
    report.start()    # timer task for future use
    
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


















@tasks.loop(seconds = 60) # repeat in 1 minute
async def report():
    
    global reportNumber

    if not lockReporting:
        print ('\n\rreport starting ' + str(reportNumber))
        print('\n\r')
        reportNumber += 1
        for guildName, channels in channelsData.items():
            print(f"Guild : {[guildName]}")
            for channelName, members in channels.items():
                print([channelName], ' '.join(members), sep=' ')
             print('\n\r')  # Print a new line between guilds
    channelsData.clear()
        













    



@client.event
async def on_voice_state_update(member, before, after):

    guild = member.guild
    nlcr = '\n\r'

    memberDisplayName = member.display_name.split('#')[0]
    memberName = member.name
    #if after.channel is not None and before.channel is None:
    
    if (before.channel is None):
        beforeChannel = 'None'
    else: beforeChannel=(f"{before.channel}")
    if (after.channel is None):
        afterChannel = 'None'
    else: afterChannel=(f"{after.channel}")

    if beforeChannel == "MakeNewChannel": nlcr = ''
    print (f"{nlcr}01 --> {truncate_datetime(datetime.now() + timedelta(hours=zuluDiff))} Guild [{guild.name}] [{memberDisplayName}] - [{memberName}] left channel [{beforeChannel}] joined channel {afterChannel}")

    # join MakeNewChannel
    if (after.channel is not None) and (after.channel.name == "MakeNewChannel"):
        category = after.channel.category
        existingChannels = [c for c in after.channel.guild.voice_channels if c.name.startswith("VC")]
        newChannelNumber = getNewChannelNumber(existingChannels)
        newChannelName = f"VC{newChannelNumber:02} {member.display_name.split('#')[0]}"

        channel = await category.create_voice_channel(newChannelName)
        await member.move_to(channel)
        # sort the voice channels
        target_channel = discord.utils.get(guild.voice_channels, name="MakeNewChannel")
        all_channels = guild.voice_channels
        target_index = all_channels.index(target_channel)
        vc_channels = sorted([c for c in all_channels if c.name.startswith("VC")], key=lambda c: c.name)
        for i, c in enumerate(vc_channels):
            await c.edit(position=target_index+i+1)
    
    # channel vacated
    if (before.channel is not None) and ('VC' in str({before.channel})):
        #memberName = f"VC[int(re.match(patternGetInt, channel.name).group(1))] {member.display_name.split('#')[0]}"
        if len(before.channel.members) == 0:
            await before.channel.delete()
            print (f"02 --> {truncate_datetime(datetime.now() + timedelta(hours=zuluDiff))} Guild [{guild.name}] [{memberDisplayName}] - [{memberName}] vacated channel [{before.channel}] deleted") #moved to {after.channel}")

            
        else:
            beforeChannel = f"{before.channel}"
            if((beforeChannel) != (f"{after.channel}")):
                newName = f"VC{(re.match(patternGetInt, str(beforeChannel)).group(1))} {before.channel.members[0].display_name.split('#')[0]}"
                if (f"{before.channel}") != newName:
                    await before.channel.edit(name=newName)
                    print (f"03 --> {truncate_datetime(datetime.now() + timedelta(hours=zuluDiff))} Guild [{guild.name}] [{memberDisplayName}] - [{memberName}] before channel [{beforeChannel}] renamed to [{newName}]")
                else: (f"04 --> {truncate_datetime(datetime.now() + timedelta(hours=zuluDiff))} Guild [{guild.name}] [{memberDisplayName}] - [{memberName}] before channel [{beforeChannel}] moved to [{after.channel}]")
 


    lockReporting = True

    for guild in client.guilds:
        channelsData[guild.name] = {}
        for channel in guild.voice_channels:
            channelsData[guild.name][channel.name] = [member.name for member in channel.members]

    lockReporting = False


    




# PC deploy
#client.run(os.getenv('TOKEN'))

#railway deploy 
client.run(os.environ['TOKEN'])

# https://discord.com/api/oauth2/authorize?client_id=1079357107771551814&permissions=16787472&scope=bot%20applications.commands







