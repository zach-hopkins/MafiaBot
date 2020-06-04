#!/usr/bin/env python3
# Client ID: 
# Bot Token: 
# Permissions: 

# https://discordapp.com/oauth2/authorize?client_id=714604065199226911&scope=bot&permissions=469773362

#Command List:
#every mafia player must type !mafia until 15 people are in mafiaparty channel
#Host goes into hostcommands and types !gamestart to assign roles
#Host can then type !night for subsequent nights
#Host can type !lynch to lynch player for town
#Any player can type !human after night one in the event of a bug to notify the server that a dead player needs to take over for host

#
from random import seed
from random import random
from random import choice
from random import randrange
import random
import discord
import discord.utils
from discord.ext import commands
from discord.utils import get
import array
import time

#init variables
client = discord.Client()
bot = commands.Bot(command_prefix='!')

townList = []
gameEnd = 0
msgcontent = ''
nightcounter = 0
mafiacomplete = 0
paritycomplete = 0
mediccomplete = 0
vigcomplete = 0
permitted = "hostcommands"
mafiaList = []
staticmafiaList = []
users = []
nicks = []
randomvalue = []
mafiakills = 0
start = 0
startup = 0
correctnamecheck = 0
killsRemaining = 0
nameList = []
medicList = []
timesmafiakilled = 0
vigshot = 0
parityList = []
nightactioninit = 0
paritymemList = []
medicmemList = []
vigmemList = []
ifcounter = 0
onlyOnce = 0
medicRemoved = 0

#botlogin
@client.event # event decorator
async def on_ready():
    print(f"We have logged in as {client.user}")
    print(discord.__version__)

@client.event
async def on_message(message):
    global users
    if "!mafia" in message.content.lower() and message.author not in users:
        role = get(message.channel.guild.roles, name="MafiaPlayer")
        user = message.author
        users.append(message.author)
        randomvalue.append(random.randint(1, 5000))
        global nicks
        nicks.append(message.author.display_name)
        await user.add_roles(role)

    global gameEnd
    if "!end" in message.content.lower() and str(message.channel) in permitted:
        gameEnd = 1
        await message.channel.send("Ending game...Please wait...")

    #adds user to mafiahost room/role
    if "!hostgo" in message.content.lower():
        channel = client.get_channel(hostcommandsid)
        await channel.set_permissions(message.author, read_messages=True, send_messages=True)
    if "!hoststop" in message.content.lower():
        channel = client.get_channel(hostcommandsid)
        await channel.set_permissions(message.author, read_messages=False, send_messages=False)


    #starts mafia game and assigns all roles
    if "!start" in message.content.lower() and str(message.channel) in permitted:
        global onlyOnce
        onlyOnce = 1
        totalPlayers = len(message.channel.members) - 1
        #sort lists and put smallest number first
        zipped_lists = zip(randomvalue, users, nicks)
        sorted_pairs = sorted(zipped_lists)
        tuples = zip(*sorted_pairs)
        randomvalue_, users_, nicks_ = [ list(tuple) for tuple in tuples]
        for i in range(3):
            #mafia
            channel = client.get_channel(mafiaid)
            await channel.set_permissions(users_[i], read_messages=True, send_messages=True)
            global mafiaList
            global nameList
            global townList
            global staticmafiaList
            global paritymemList
            global medicmemList
            global vigmemList
            mafiaList.append(nicks_[i])
            staticmafiaList.append(nicks_[i])
        print(len(users_))
        for name in nicks:
            if name not in mafiaList:
                townList.append(name)
        for i in range(1):
            #parity
            i = i + 3
            channel = client.get_channel(paritycopid)
            await channel.set_permissions(users_[i], read_messages=True, send_messages=True)
            paritymemList.append(nicks_[i])
        for i in range(1):
            #medic
            i = i + 4
            channel = client.get_channel(medicid)
            await channel.set_permissions(users_[i], read_messages=True, send_messages=True)
            medicmemList.append(nicks_[i])
        for i in range(1):
            #vig
            i = i + 5
            channel = client.get_channel(vigid)
            await channel.set_permissions(users_[i], read_messages=True, send_messages=True)
            vigmemList.append(nicks_[i])
        map(str.lower, vigmemList)
        map(str.lower, mafiaList)
        map(str.lower, medicmemList)
        map(str.lower, paritymemList)
        await message.channel.send("Roles have been assigned.")
        

    #hostcommands
        global msgcontent
        await message.channel.send('Enter starting kill power (!integer - ie. "!2" without quotes)')
        msg = await client.wait_for('message', check=lambda message: message.content == '!1' or message.content == '!2' or message.content == '!3')
        msgcontent = msg.content
        global start
        global startup
        global mafiakills
        start = 1
        #mafia
    if "!3" in msgcontent.lower() and start is 1 and permitted in str(message.channel) and onlyOnce == 1:
        mafiakills = 3
        onlyOnce = 0
        await message.channel.send('kill power set')
        start = 0
    elif "!2" in msgcontent.lower() and start is 1 and permitted in str(message.channel) and onlyOnce == 1:
        mafiakills = 2
        onlyOnce = 0
        await message.channel.send('kill power set')
        start = 0
    elif "!1" in msgcontent.lower() and start is 1 and permitted in str(message.channel) and onlyOnce == 1:
        mafiakills = 1
        onlyOnce = 0
        await message.channel.send('kill power set')
        start = 0

        #town lynches
    if "!lynch" in message.content.lower() and permitted in str(message.channel):
        guildString = str(message.guild.members)
        await message.channel.send('Enter name of lynched player')
        msg = await client.wait_for('message', check=lambda message: message.content.lower() in guildString.lower())
        rawString = str(msg.content).lower()
        nameString = "'{}'".format(rawString)
        if nameString.lower() in guildString.lower():
            #remove permissions if user matches string
            user = get(message.channel.guild.members, display_name=rawString)
            #remove mafia kill power if display name in maf list and remove from PR list if PR player
            if (rawString in mafiaList and mafiakills == 2) or (rawString in medicmemList and mafiakills == 2) or (rawString in paritymemList and mafiakills == 2) or (rawString in vigmemList and mafiakills == 2):
                if rawString in mafiaList:
                    mafiakills = mafiakills - 1
                    mafiaList.remove(rawString.lower())
                    print(mafiaList)
                elif rawString in medicmemList:    
                    medicmemList.remove(rawString.lower())
                elif rawString in vigmemList: 
                    vigmemList.remove(rawString.lower())
                elif rawString in paritymemList: 
                    paritymemList.remove(rawString.lower())
            elif (rawString in mafiaList and mafiakills == 1) or (rawString in medicmemList and mafiakills == 1) or (rawString in paritymemList and mafiakills == 1) or (rawString in vigmemList and mafiakills == 1):
                if rawString in mafiaList:
                    mafiaList.remove(rawString.lower())
                    print(mafiaList)
                elif rawString in medicmemList:
                    medicmemList.remove(rawString.lower())
                elif rawString in vigmemList:
                    vigmemList.remove(rawString.lower())
                elif rawString in paritymemList: 
                    paritymemList.remove(rawString.lower())
            if len(mafiaList) < 1:
                await message.channel.send("Game is over - Mafia is dead")
                gameEnd = 1
            if len(mafiaList) >= len(townList):
                await channel.send("Game is over - Mafia wins")
                gameEnd = 1

            #mafia channel
            channel = client.get_channel(mafiaid)
            await channel.set_permissions(user, read_messages=False, send_messages=False)
            #vig channel
            channel = client.get_channel(vigid)
            await channel.set_permissions(user, read_messages=False, send_messages=False)
            #medic channel
            channel = client.get_channel(medicid)
            await channel.set_permissions(user, read_messages=False, send_messages=False)
            #paritycop channel
            channel = client.get_channel(paritycopid)
            await channel.set_permissions(user, read_messages=False, send_messages=False)
            #deadchat channel
            channel = client.get_channel(deadchatid)
            await channel.set_permissions(user, read_messages=True, send_messages=True)
            #success message after lynch
            if len(mafiaList) > 0:
                await message.channel.send(f"""{rawString} has been lynched. Go to sleep""")
        else:
            await message.channel.send("No nickname found. Please type the lynch command and try again")


    

    #normal night actions
    if "!night" in message.content.lower() and permitted in str(message.channel):
        global nightcounter
        global paritycomplete
        global nightactioninit
        global vigcomplete
        global mediccomplete
        nightcounter += 1
        nightactioninit = 1
        if nightcounter is 2:
            if mafiakills == 3:
                mafiakills = mafiakills -1
        await message.channel.send("Sending night actions to all roles and collecting data. Please wait")

        #sending message to all power/mafia roles
        #mafia
        channel = client.get_channel(mafiaid)
        await channel.send(f"""Mafia has {mafiakills} kills tonight. Please enter a name first""")
        #paritycop
        channel = client.get_channel(paritycopid)
        await channel.send(f"""Who would you like to check tonight""")
        #medic
        channel = client.get_channel(medicid)
        await channel.send(f"""Who would you like to save tonight?""")
        #vig
        global vigshot
        if vigshot is 0:
            channel = client.get_channel(vigid)
            await channel.send(f"""Would you like to shoot someone tonight?""")

    #mafia night actions
    if "mafia" in str(message.channel) and 'MafiaBot' not in str(message.author) and nightactioninit is 1:
        global ifcounter
        global killsRemaining
        global nameList
        nameEntered = str(message.content.lower())
        nameString = "'{}'".format(nameEntered)
        guildString = str(message.guild.members)
        yesString = 'yes'
        noString = 'no'
        yesVotes = 0
        correctnamecheck = 0
        ifcounter += 1
        if ifcounter is 1:
            killsRemaining = mafiakills
        if nameString in guildString.lower():
            correctnamecheck = 1
            await message.channel.send(f"""Would you like to shoot {nameString}?""")
            while yesVotes < len(mafiaList):
                msg = await client.wait_for('message', check=lambda message: message.content == yesString or message.content == noString)
                if  str(msg.content).lower() == noString and "mafia" in str(message.channel):
                    yesVotes = 20
                    await message.channel.send("Vote failed, please try another name")
                elif str(msg.content).lower() == yesString and "mafia" in str(message.channel):
                    yesVotes +=1
                    await message.channel.send(f"""{nameString} now has {yesVotes} yes votes. {len(mafiaList) - yesVotes} more votes needed""")
                    if yesVotes is len(mafiaList):
                        nameString = nameString[1:-1]
                        nameList.append(nameString)
                        await message.channel.send(f"""{nameString} has been successfully shot""")
                        killsRemaining = killsRemaining - 1
                        if killsRemaining > 0:
                            await message.channel.send(f"""Mafia has {killsRemaining} shot left. Enter a name.""")
                        else:
                            await message.channel.send(f"""Mafia has fired all shots. Goodnight""")
                            global mafiacomplete
                            mafiacomplete = 1
        elif message.content.lower() not in guildString.lower() and message.content.lower() not in yesString and message.content.lower() not in noString:
            await message.channel.send("No nickname found. Please try again")
        
    #medic night actions
    if "medic" in str(message.channel) and 'MafiaBot' not in str(message.author) and nightactioninit is 1 and mediccomplete is not 1:
        nameEntered = str(message.content.lower())
        nameString = "'{}'".format(nameEntered)
        guildString = str(message.guild.members)
        yesString = 'yes'
        noString = 'no'
        global medicList
        correctnamecheck = 0
        if nameString in guildString.lower():
            correctnamecheck = 1
            await message.channel.send(f"""Would you like to save {nameString}?""")
            msg = await client.wait_for('message', check=lambda message: str(message.content).lower() == yesString or str(message.content).lower() == noString)
            if  str(msg.content).lower() == noString and "medic" in str(message.channel):
                await message.channel.send("Okay. Please enter another name")
            elif str(msg.content).lower() == yesString and "medic" in str(message.channel):
                nameString = nameString[1:-1]
                medicList.append(nameString)
                await message.channel.send(f"""{nameString} has been saved. Goodnight""")
                mediccomplete = 1
        elif nameString not in guildString.lower() and correctnamecheck is 0 and message.content.lower() not in yesString and message.content.lower() not in noString:
            await message.channel.send("No nickname found. Please try again")
    elif len(medicmemList) is 0 and nightactioninit is 1:
        mediccomplete = 1

    #vig night actions
    if "vig" in str(message.channel) and 'MafiaBot' not in str(message.author) and nightactioninit is 1 and vigcomplete is not 1:
        yesString = 'yes'
        noString = 'no'
        guildString = str(message.guild.members)
        msg = message.content
        if  str(msg).lower() == noString and "vig" in str(message.channel):
            await message.channel.send("Goodnight")
            vigcomplete = 1
        elif str(msg).lower() == yesString and "vig" in str(message.channel):
            await message.channel.send(f"""Who would you like to shoot?""")
            msg2 = await client.wait_for('message', check=lambda message: message.content.lower() in guildString.lower())
            if  str(msg2.content).lower() in guildString.lower():
                nameString = str(msg2.content).lower()
                nameList.append(nameString)
                vigshot = 1
                vigcomplete = 1
                await message.channel.send(f"""{nameString} has been shot. Goodnight""")
            elif str(msg2.content).lower() in guildString.lower():
                await message.channel.send("nickname not found. Please try again")
    elif len(vigmemList) is 0 and nightactioninit is 1:
        vigcomplete = 1

    #parity night actions
    if "paritycop" in str(message.channel) and 'MafiaBot' not in str(message.author) and nightactioninit is 1 and paritycomplete is not 1:
        global parityList
        guildString = str(message.guild.members)
        nameEntered = str(message.content.lower())
        nameString = "'{}'".format(nameEntered)
        if nameString in guildString.lower():
            correctnamecheck = 1
            if len(parityList) < 1:
                parityList.append(nameEntered)
                await message.channel.send(f"""{nameString} has been added as your first check. Goodnight""")
                paritycomplete = 1
            elif len(parityList) >= 1:
                x = len(parityList)
                if (parityList[x - 1] in staticmafiaList and nameEntered not in staticmafiaList) or (parityList[x - 1] not in staticmafiaList and nameEntered in staticmafiaList):
                    await message.channel.send(f"""{nameString} is different from {parityList[x - 1]}""")
                    parityList.append(nameEntered)
                    paritycomplete = 1
                else:
                    await message.channel.send(f"""{nameString} is the same as {parityList[x - 1]}""")
                    parityList.append(nameEntered)
                    paritycomplete = 1
        elif nameString not in guildString.lower() and correctnamecheck is 0:
            await message.channel.send("No nickname found. Please try again")
    elif len(paritymemList) is 0 and nightactioninit is 1:
        paritycomplete = 1

    #final message and reset
    if mafiacomplete is 1 and paritycomplete is 1 and vigcomplete is 1 and mediccomplete is 1:
        nightactioninit, mafiacomplete, paritycomplete, vigcomplete, mediccomplete, ifcounter = 0, 0, 0, 0, 0, 0
        random.shuffle(nameList)
        global medicRemoved
        for name in nameList:
            if name in medicList and medicRemoved is 0:
                nameList.remove(name)
                medicRemoved = 1
                #loop to remove mafia kills from PR chat or mafia chat and add to deadchat
        for name in nameList:
            if name.startswith('"') and name.endswith('"'): 
                rawString = name[1:-1]
            else: rawString = name
            user = get(message.channel.guild.members, display_name=rawString)
            if rawString in mafiaList or rawString in medicmemList or rawString in paritymemList or rawString in vigmemList:
                if rawString in mafiaList: 
                    mafiaList.remove(rawString.lower())
                    if mafiakills >= 2:
                        mafiakills = 1
                elif rawString in medicmemList: 
                    medicmemList.remove(rawString.lower())
                elif rawString in vigmemList: 
                    vigmemList.remove(rawString.lower())
                elif rawString in paritymemList: 
                    paritymemList.remove(rawString.lower())
            #mafia channel
            channel = client.get_channel(mafiaid)
            await channel.set_permissions(user, read_messages=False, send_messages=False)
            #vig channel
            channel = client.get_channel(vigid)
            await channel.set_permissions(user, read_messages=False, send_messages=False)
            #medic channel
            channel = client.get_channel(medicid)
            await channel.set_permissions(user, read_messages=False, send_messages=False)
            #paritycop channel
            channel = client.get_channel(paritycopid)
            await channel.set_permissions(user, read_messages=False, send_messages=False)
            #deadchat channel
            channel = client.get_channel(deadchatid)
            await channel.set_permissions(user, read_messages=True, send_messages=True)
        #remove duplicates
        nameList = list(dict.fromkeys(nameList))
        channel = client.get_channel(hostcommandsid)
        await channel.send(f"""The following players are dead {nameList}""")
        if len(mafiaList) is 0:
            await channel.send("Game is over - Mafia is dead")
            gameEnd = 1
        if len(mafiaList) >= len(townList):
            await channel.send("Game is over - Mafia wins")
            gameEnd = 1
        medicRemoved = 0
        medicList.clear()
        nameList.clear()

    if "!purge" in message.content.lower() and str(message.channel) in permitted:
        #mafia channel
        channel = client.get_channel(mafiaid)
        await channel.purge(limit=100)
        #vig channel
        channel = client.get_channel(vigid)             
        await channel.purge(limit=100)
        #medic channel
        channel = client.get_channel(medicid)
        await channel.purge(limit=100)
        #paritycop channel
        channel = client.get_channel(paritycopid)
        await channel.purge(limit=100)
        #hostcommands channel
        channel = client.get_channel(hostcommandsid)
        await channel.purge(limit=100)
        await message.channel.send("Channels purged")
    if gameEnd is 1:
        gameEnd = 0
        #remove mafiaplayer role and then reset channel permissions
        role = get(message.channel.guild.roles, name="MafiaPlayer")
        for user in users:
            await user.remove_roles(role)

        #remove all members from all private channels
        guild = get(client.guilds, id=serverid)
        for user in guild.members:
            if user.name is not 'MafiaBot':
                print(user.name)
                #mafia channel
                channel = client.get_channel(mafiaid)
                await channel.set_permissions(user, read_messages=False, send_messages=False)
                #vig channel
                channel = client.get_channel(vigid)
                await channel.set_permissions(user, read_messages=False, send_messages=False)
                #medic channel
                channel = client.get_channel(medicid)
                await channel.set_permissions(user, read_messages=False, send_messages=False)
                #paritycop channel
                channel = client.get_channel(paritycopid)
                await channel.set_permissions(user, read_messages=False, send_messages=False)
                #deadchat channel
                channel = client.get_channel(deadchatid)
                await channel.set_permissions(user, read_messages=False, send_messages=False)
        
        #clear relevant variables
        timesmafiakilled = 0
        onlyOnce = 0
        staticmafiaList.clear()
        mafiaList.clear()
        users.clear()
        nicks.clear()
        medicList.clear()
        randomvalue.clear()
        nameList.clear()
        parityList.clear()
        paritymemList.clear()
        vigmemList.clear()
        medicmemList.clear()
        mafiakills = 0
        killsRemaining = 0
        nightcounter = 0
        start = 0
        startup = 0
        vigshot = 0
        correctnamecheck = 0
        medicRemoved, nightactioninit, mafiacomplete, paritycomplete, vigcomplete, mediccomplete, ifcounter = 0, 0, 0, 0, 0, 0, 0
        channel = client.get_channel(hostcommandsid)

        #purge chat channels
        #mafia channel
        channel = client.get_channel(mafiaid)
        await channel.purge(limit=100)
        #vig channel
        channel = client.get_channel(vigid)             
        await channel.purge(limit=100)
        #medic channel
        channel = client.get_channel(medicid)
        await channel.purge(limit=100)
        #paritycop channel
        channel = client.get_channel(paritycopid)
        await channel.purge(limit=100)
        #hostcommands channel
        channel = client.get_channel(hostcommandsid)
        await channel.purge(limit=100)
        await channel.send("Game has ended and roles were deleted")


client.run("bottoken")
