
#spawnvcRW06-05.py

import os
import threading
import asyncio
from datetime import datetime, timedelta
import time
from xml.dom.expatbuilder import makeBuilder
import discord
from discord.ext import commands
from discord.ext import commands, tasks
import re#import openai
#from reportlab.pdfgen import canvas


# uncomment the 2 lines below for PC deploy
# comment the 2 lines below for railway deploy
#from dotenv import load_dotenv
#load_dotenv('spammytest.env')

#uncomment for PC
#openai.api_key = os.getenv('TOKEN2')
#uncomment for railway
#openai.api_key = os.environ['TOKEN2']

#intents = discord.Intents().all()
#intents = discord.Intents().default()
intents = discord.Intents(members=True, voice_states=True, value=True, message_content = True)
client = discord.Client(intents=intents)
client = commands.Bot(command_prefix='?', intents=intents)





zuluDiff = -5
patternGetInt = r"^\D\D(\d{2})"
channelsData = {}
lockReporting = True
reportNumber = 0
doReport = True
noActivityMinutes = 0
makeNewChannelNames = ['MakeNewSerious', 'MakeNewCasual']
channelPrefixes = ['SC', 'CC']
span = 1
runNumber = 1







































#async def restart(ctx):

#    message = client.guilds[0].name + ' server is restarting'
#    print (message)
#    await ctx.send(message)
#    print (message)
#    member = client.guilds[0].get_member(425437217612103684)
#    await member.send(message)
#    os.execv(sys.executable, ['python'] + sys.argv)
#    #await client.close()
#    #await client.logout()


#@client.command()
#async def ping(ctx):

#    embed = discord.Embed(description=(f'Pong!'),  colour=discord.Colour.purple())
#    print ('pong sent')
#    await ctx.send(embed=embed)


#@client.command()
#async def latency(ctx):

#    await ctx.send (f" {client.latency}")


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





#@client.event
#async def on_message(message):
#    print ('receieved ' + message.content)
#    # Ignore messages sent by the bot itself
#    if message.author == client.user:
#        return

#    if message.content.startswith('chatGPT'):
#        words = message.content.split()
#        words.pop(0)
#        newMessage = " ".join(words)
#        response = openai.Completion.create(
#            engine="davinci",
#            prompt=newMessage,
#            max_tokens=100,
#            n=1,
#            stop=None,
#            temperature=0.5,
#            )
#        response_text = response.choices[0].text.strip()

#        # Send the response back to the member
#        await message.channel.send(response_text)








#########################           on ready            #########################


























































@client.event
async def on_ready():
    
    global lockRorting
    global doReport
    global noActivityMinutes
    global makeNewChannelNames
    global channelPrefixes
    global span
    global runNumber

    adjustmentsMade = False

    print ('\n\rLogged in as {0.user}'.format(client))
    print(f'Connected to {len(client.guilds)} guilds')
    print('executing version spawnvcRW06-05.py')
    
    


    for guild in client.guilds:
        print ('\n\r' f"Guild = [{guild.name}]")
        channelPrefixIndex = 0;

    for makeNewChannelName in makeNewChannelNames:
        channelPrefix = channelPrefixes[channelPrefixIndex]
        channelPrefixIndex += 1
        adjustmentsMade = False

        # set category correspond to channel named 'Voice Channels'
        existingChannelNames = [channel.name for channel in guild.voice_channels]
        category = discord.utils.get(guild.categories, name='Voice Channels')

        if makeNewChannelName not in existingChannelNames:
            await category.create_voice_channel(makeNewChannelName)
            time.sleep(span)

        #Remove empty VC channels
        for channel in guild.voice_channels:
            if channel.name.startswith(channelPrefix) and len(channel.members) == 0:
                if  discord.utils.get(guild.voice_channels, name=channel.name):
                    await channel.delete()
                    time.sleep(span)
                    adjustmentsMade = True
                    print (f"06 --> Guild [{guild.name}] deleted [{channel.name}]")
                else: print ('06 --> A CHANNEL IN LIST BUT NOT PRESENT')
            

        ## move members out of MakeNewChannel channel   
        for channel in guild.channels:
            if (((f"{channel.name}"== makeNewChannelName) and (len(channel.members)) != 0)):
                #print (channel.name)
                lenChannelMembers = len(channel.members)
                while len(channel.members) > 0:
                    mncMember =  channel.members[0]
                    existingChannels = [c for c in channel.guild.voice_channels if c.name.startswith(channelPrefix)]
                    newChannelNumber = getNewChannelNumber(existingChannels)
                    newChannelName = f"{channelPrefix}{newChannelNumber:02} {mncMember.display_name.split('#')[0]}"
                    movedToChannel = await channel.category.create_voice_channel(newChannelName)
                    time.sleep(span)
                    await mncMember.move_to(movedToChannel)
                    time.sleep(span)
                    adjustmentsMade = True
                    print (f"Guild [{guild.name}] channel [{newChannelName}] created moved [{mncMember.name}]")
                        
        # new sort
        verifiedSorted = False
            
        while not verifiedSorted:
            voiceChannels = guild.voice_channels
            MakeNewChannelName = discord.utils.get(voiceChannels, name=makeNewChannelName)
            prefixedChannels = [c for c in voiceChannels if c.name.startswith(channelPrefix)]
            #prefixedChannelNames = [c.name for c in prefixedChannels]
            MakeNewChannelPosition = MakeNewChannelName.position
            
       
            verifiedSorted = True
            print (f'\n\rsort run on voice state update number = {runNumber}')
            runNumber += 1

            sortedVoiceChannels = sorted(prefixedChannels, key=lambda x: x.name)
            for i, voiceChannel in enumerate(sortedVoiceChannels):
                expectedPosition = MakeNewChannelPosition + i + 1
                if voiceChannel.position != expectedPosition:
                    await voiceChannel.edit(position=expectedPosition)
                    time.sleep(span)
                    adjustmentsMade = True
                    verifiedSorted = False

                    print(f"Moved '{voiceChannel.name}' in position {voiceChannel.position} to position {expectedPosition}.")
 

    message = ('adjustments made = 'f"{adjustmentsMade} on {guild.name} server for {makeNewChannelName}")
    print ('finished cleaning up ' + message)
                    
    member = client.guilds[0].get_member(425437217612103684)
    print ('sending message')
    await member.send(message)
    time.sleep(span)

    


    botGuilds = client.guilds
    print ('guilds set')
    #report.start()    # timer task for future use
    
    


    print ('exiting on_ready now')
    exit






    







    #@client.event
    #async def on_message(message):
    #    print(f'{message.author}: {message.content}')











        
## Define the URL of the web server where the log file will be stored
#log_url = "http://kablammy.me/bot.log"

## Define a function that sends a message to both the standard output and the log file
#def log(msg):
#    # Write the message to the standard output
#    print(msg)

#    # Write the message to the log file on the web server
#    requests.post(log_url, data=msg.encode())

## Example usage of the log function
#@client.event
#async def on_message(message):
#    print(' got message')
#    log(f"Received message: {message.content}")

#    # Do other processing here















##################        functions           ###########################



def truncateDatetime (dt):

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
    global doReport
    global noActivityMinutes

    if not lockReporting:
        if doReport:
            print('\r')
            print ('#---------------#        channel report ' + str(reportNumber) + '        #---------------#')
            reportNumber += 1

            for guild_name, guild_channels in channelsData.items():
                print(f"\n\rGuild: [{guild_name}]")
                for channel_name, channel_members in guild_channels.items():
                    if channel_members:
                        print(f"----------->Channel     {channel_name}")
                        for member in channel_members:
                            print(f"-------------->Member-->{member}")
                        print('\r')

                        
            channelsData.clear()
            doReport = False
            noActivityMinutes = 0
        else:
            print('\r')
            print ('No activity for ' + str(noActivityMinutes) + ' minutes')
            noActivityMinutes += 1
    else:
        print ('reporting locked')










    



@client.event
async def on_voice_state_update(member, before, after):
    
    global doReport
    global lockReporting
    showMoves = True
    global makeNewChannelNames
    global channelPrefixes
    global span
    global runNumber

    adjustmentsMade = False


    guild = member.guild
    print (f'\n\rGuild is {guild} ')
    nlcr = '\n\r'

    print ('on voice state update')

    if (before.channel is None):
        beforeChannel = 'None'
    else: beforeChannel=(f"{before.channel}")
    if (after.channel is None):
        afterChannel = 'None'
    else: afterChannel=(f"{after.channel}")

    for index in range(0, 2):
        makeNewChannelName = makeNewChannelNames[index]
        channelPrefix = channelPrefixes[index]

        memberDisplayName = member.display_name.split('#')[0]
        memberName = member.name
        #if after.channel is not None and before.channel is None:
        
        if (beforeChannel != afterChannel):
            if beforeChannel == makeNewChannelName: nlcr = ''
            if showMoves:
                print (f"{nlcr}01 --> {truncateDatetime(datetime.now() + timedelta(hours=zuluDiff))} Guild [{guild.name}] [{memberDisplayName}] - [{memberName}] left channel [{beforeChannel}] joined channel [{afterChannel}]")

            # join MakeNewChannel
            if ((after.channel is not None) and (after.channel.name == makeNewChannelName)):
                category = after.channel.category
                existingChannels = [c for c in after.channel.guild.voice_channels if c.name.startswith(channelPrefix)]
                newChannelNumber = getNewChannelNumber(existingChannels)
                newChannelName = f"{channelPrefix}{newChannelNumber:02} {member.display_name.split('#')[0]}"

                newChannel = await category.create_voice_channel(newChannelName)
                time.sleep(span)
                await member.move_to(newChannel)
                time.sleep(span)
                
    
            # prefixed named channel vacated
            if before.channel is not None and channelPrefix in before.channel.name:
                if len(before.channel.members) == 0:
                    await before.channel.delete()
                    time.sleep(span)
                    if showMoves:
                        print (f"02 --> {truncateDatetime(datetime.now() + timedelta(hours=zuluDiff))} Guild [{guild.name}] [{memberDisplayName}] - [{memberName}] vacated channel [{before.channel}] deleted") #moved to {after.channel}")
                else:
                    beforeChannel = f"{before.channel}"
                    if((beforeChannel) != (f"{after.channel}")):
                        newName = f"{channelPrefix}{(re.match(patternGetInt, str(beforeChannel)).group(1))} {before.channel.members[0].display_name.split('#')[0]}"
                        if before.channel != newName:
                            if len(before.channel.members) == 0:
                                await before.channel.delete()
                                time.sleep(span)
                                adjustmentsMade = True
                                print (f"07 --> Guild [{guild.name}] deleted [{channel.name}]")
                            else: print ('07 --> A CHANNEL IN LIST BUT NOT PRESENT')

                            await before.channel.edit(name=newName)
                            time.sleep(span)
                            if showMoves:
                                print (f"03 --> {truncateDatetime(datetime.now() + timedelta(hours=zuluDiff))} Guild [{guild.name}] [{memberDisplayName}] - [{memberName}] before channel [{beforeChannel}] renamed to [{newName}]")
                        elif showMoves:
                            (f"04 --> {truncateDatetime(datetime.now() + timedelta(hours=zuluDiff))} Guild [{guild.name}] [{memberDisplayName}] - [{memberName}] before channel [{beforeChannel}] moved to [{after.channel}]")
            
            
            #Remove empty VC channels            
            voiceChannels = guild.voice_channels
            prefixedChannels = [c for c in voiceChannels if c.name.startswith(channelPrefix)]
            
            for channel in prefixedChannels:
                if len(channel.members) == 0:
                    await channel.delete()
                    time.sleep(span)
                    adjustmentsMade = True
                    print (f"02 --> Guild [{guild.name}] deleted [{channel.name}]")
                else: print ('02 --> A CHANNEL IN LIST BUT NOT PRESENT')
          
                            
            # new sort
            verifiedSorted = False
            
            while not verifiedSorted:
                voiceChannels = guild.voice_channels
                MakeNewChannelName = discord.utils.get(voiceChannels, name=makeNewChannelName)
                prefixedChannels = [c for c in voiceChannels if c.name.startswith(channelPrefix)]
                #prefixedChannelNames = [c.name for c in prefixedChannels]
                if MakeNewChannelName is not None: 
                    MakeNewChannelPosition = MakeNewChannelName.position
            
       
                    verifiedSorted = True
                    print (f'\n\rsort run on voice state update number = {runNumber}')
                    runNumber += 1

                    sortedVoiceChannels = sorted(prefixedChannels, key=lambda x: x.name)
                    for i, voiceChannel in enumerate(sortedVoiceChannels):
                        expectedPosition = MakeNewChannelPosition + i + 1
                        if voiceChannel.position != expectedPosition:
                            await voiceChannel.edit(position=expectedPosition)
                            time.sleep(span)
                            adjustmentsMade = True
                            verifiedSorted = False

                            print(f"Moved '{voiceChannel.name}' in position {voiceChannel.position} to position {expectedPosition}.")
 
                            
   




        lockReporting = True
    
        #for guild in client.guilds:
        #    channelsData[guild.name] = {}
        #    for channel in guild.voice_channels:
        #        channelsData[guild.name][channel.name] = [member.name for member in channel.members]


        for guild in client.guilds:
            channelsData[guild.name] = {}
            for channel in guild.voice_channels:
                reportedMembers = []
                for reportedMember in channel.members:
                    reportedMembers.append(f"{reportedMember.name} ({reportedMember.display_name})")
                channelsData[guild.name][channel.name] = reportedMembers
                
        lockReporting = False
        doReport = True

    




# PC deploy
client.run(os.getenv('TOKEN'))  

#railway deploy 
#client.run(os.environ['TOKEN'])

# https://discord.com/api/oauth2/authorize?client_id=1079357107771551814&permissions=16787472&scope=bot%20applications.commands




#correct it  channel name does not match anyone in the channel

# stuff







                   


            ## sort the voice channels
            #target_channel = discord.utils.get(guild.voice_channels, name=makeNewChannelName)
            #all_channels = guild.voice_channels
            #target_index = all_channels.index(target_channel)
            #vc_channels = sorted([c for c in all_channels if c.name.startswith(channelPrefix)], key=lambda c: c.name)
            #for i, c in enumerate(vc_channels):
            #    await c.edit(position=target_index+i+1)
            #    time.sleep(span)





            


