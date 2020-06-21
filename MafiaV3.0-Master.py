#!/usr/bin/env python3
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
import asyncio

#init variables
client = discord.Client()
users = []
nicks = []
randomvalue = []
permitted = "hostcommands"
mafiaList = []
staticMafiaList = []
parityMemList = []
vigMemList = []
medicMemList = []
townList = []
gameStart = 0
mafiakills = 0
killsRemaining = 3
medicSaved = "blank"
vigShot = "blank"
parityCheck = "blank"
lynchSuccess = "blank"
parityCheckList = []
killsList = []
medicSavedList = []
didVigShoot = 0
gameEnd = 0
staticTownList = []
signup = 0
signupmessage = None
playerList = []
startingKillPower = 0
nightCounter = 0
staticMedicSavedList = []

#botlogin
@client.event # event decorator
async def on_ready():
    print(f"We have logged in as {client.user}")
    print(discord.__version__)
    channel = client.get_channel(hostcommandsid)


@client.event
async def on_message(message):
    #Enables !mafia command
    if "!start" in message.content.lower() and str(message.channel) in permitted:
        #globals
        global staticMedicSavedList
        global signupmessage
        global nightCounter
        global staticTownList
        global townList
        global medicSavedList
        global gameStart
        global gameEnd
        global mafiakills
        global mafiaList
        global killsRemaining
        global medicSaved
        global vigShot
        global parityCheck
        global parityCheckList
        global medicMemList
        global parityMemList
        global vigMemList
        global killsList
        global didVigShoot
        global playerList
        global lynchSuccess
        global startingKillPower
        ###
        gameStart = 1
        channel = client.get_channel(mafiasignupid)
        gameString = "----------------------------------------------\nSign-Up for Mafia by Reacting with a 👍\n----------------------------------------------"
        await channel.send(gameString)

    if "Sign-Up for Mafia by Reacting with a 👍" in message.content and 'MafiaBot' in str(message.author):
        signupmessage = message.id

    #Starts the game and assigns all roles
    if "!assign" in message.content.lower() and str(message.channel) in permitted:
        await message.channel.send("Assigning roles...Please wait.")
        channel = client.get_channel(mafiasignupid)
        role = get(channel.guild.roles, name="MafiaPlayer")
        message = await channel.fetch_message(signupmessage)
        for reaction in message.reactions:
            async for user in reaction.users():
                if user not in users:
                    playerList.append(user)
                    userList = await addPlayer(user, role)
                    users.append(userList[0])
                    randomvalue.append(userList[1])
                    nicks.append(userList[2])
        #sort lists and put smallest number first
        zipped_lists = zip(randomvalue, users, nicks)
        sorted_pairs = sorted(zipped_lists)
        tuples = zip(*sorted_pairs)
        randomvalue_, users_, nicks_ = [ list(tuple) for tuple in tuples]
        mafiaList = await assignMafia(users_)
        vigMemList = await assignVig(users_)
        medicMemList = await assignMedic(users_)
        parityMemList = await assignParity(users_)
        townList = await assignTown(users_, mafiaList)
        staticMafiaList.extend(mafiaList)
        staticTownList.extend(townList)
        channel = client.get_channel(hostcommandsid)
        await channel.send("Roles have been assigned.")
        channel = client.get_channel(deadchatid)
        await channel.send(f"""Mafia List: {mafiaList}\nVig: {vigMemList[0]}\nMedic: {medicMemList[0]}\nParity Cop: {parityMemList[0]}""")

    if "!night" in message.content.lower() and str(message.channel) in permitted:
        await message.channel.send("Sending night actions to all roles and collecting data. Please wait")
        nightCounter = nightCounter + 1

        #sets kills
        await killPower(nightCounter)

        #Mafia Part
        while killsRemaining is not 0:
            mafiaStuff = await mafiaNight(mafiakills)
        if killsRemaining is 0:
            channel = client.get_channel(mafiaid)
            await channel.send("All shots fired. Goodnight")
            await asyncio.sleep(random.randint(15, 25))
        ###

        #Medic Part
        while medicSaved == "blank" and len(medicMemList) > 0:
            medicSaved = await medicNight()
        if len(medicMemList) is 0:
            medicSaved = 'no'
            await asyncio.sleep(random.randint(4, 8))
            
        ###

        #Vig Part
        while vigShot == "blank" and len(vigMemList) > 0 and didVigShoot is 0:
            vigShot = await vigNight()
        if len(vigMemList) is 0 or didVigShoot is 1:
            vigShot = 'no'
            await asyncio.sleep(random.randint(4, 8))

        ###

        #Parity Cop Part
        while parityCheck == "blank" and len(parityMemList) > 0:
            parityCheck = await parityNight()
        if parityCheck != "blank":
            parityCheckList.append(parityCheck)
        if len(parityMemList) is 0:
            parityCheck = 'no'

        ###

        #Host Reception
        channel = client.get_channel(hostcommandsid)
        if vigShot != 'no':
            killsList.append(vigShot)
        if medicSaved != 'no':
            medicSavedList.append(medicSaved)
        #remove medic save from kills and then remove duplicates
        for name in medicSavedList:
            if name in killsList:
                killsList.remove(name)
        killsList = list(dict.fromkeys(killsList))
        #removes from channels and updates lists
        await shotPlayers(killsList)
        random.shuffle(killsList)
        await channel.send(f"""The following players are dead: {killsList}""")
        if len(mafiaList) is 0:
            await channel.send("The game is over. Town has won")
            await asyncio.sleep(5)
            await gameEnd()
        if len(mafiaList) >= len(townList):
            await channel.send("The game is over. Mafia has won")
            await asyncio.sleep(5)
            await gameEnd()
        #resets !night variables and lists
        killsList.clear()
        medicSavedList.clear()
        vigShot = 'blank'
        medicSaved = 'blank'
        parityCheck = 'blank'
        killsRemaining = mafiakills

        ###

    #Lynching
    if "!lynch" in message.content.lower() and str(message.channel) in permitted:
        
        #Lynch actions
        while lynchSuccess == "blank":
            lynchSuccess = await lynchedPlayer()
        if lynchSuccess != "blank":
            await shotPlayers(killsList)
            channel = client.get_channel(hostcommandsid)
            await channel.send(f"""{killsList[0]} has been lynched.""")

        #clear kill list and check for wins
        killsList.clear()
        lynchSuccess = "blank"
        if len(mafiaList) >= len(townList):
            channel = client.get_channel(hostcommandsid)
            await channel.send(f"""Game over. Mafia wins.""")
            await asyncio.sleep(5)
            await gameEnd()
        if len(mafiaList) is 0:
            channel = client.get_channel(hostcommandsid)
            await channel.send(f"""Game over. Mafia is dead. Town wins.""")
            await asyncio.sleep(5)
            await endGame()


    #!end game
    if "!end" in message.content.lower() and str(message.channel) in permitted or gameEnd is 1:
        gameEnd = 0
        await endGame()

    #Controls who goes into host commands room
    if "!hostgo" in message.content.lower():
        channel = client.get_channel(hostcommandsid)
        await channel.set_permissions(message.author, read_messages=True, send_messages=True)
    if "!hoststop" in message.content.lower():
        channel = client.get_channel(hostcommandsid)
        await channel.set_permissions(message.author, read_messages=False, send_messages=False)
    
    #purge channels
    if "!purge" in message.content.lower() and str(message.channel) in permitted:
        await purge()
 

    #RNG Host Mode
    if "!rng" in message.content.lower() and str(message.channel) in permitted:
        await message.channel.send("Sending !start command...")

    if "!list" in message.content.lower() and str(message.channel) in permitted and 'MafiaBot' not in str(message.author):
        rngMafia = []
        rngParity = ''
        rngMedic = ''
        rngVig = ''
        channel = client.get_channel(mafiasignupid)
        message = await channel.fetch_message(signupmessage)
        for reaction in message.reactions:
            async for user in reaction.users():
                playerList.append(user.display_name)
        random.shuffle(playerList)
        for x in range(6):
            if x < 3:
                rngMafia.append(playerList[x])
            elif x == 3:
                rngParity = playerList[x]
            elif x == 4:
                rngMedic = playerList[x]
            elif x == 5:
                rngVig = playerList[x]
        channel = client.get_channel(hostcommandsid)
        await channel.send(f"""Mafia List: """)
        await channel.send(f"""{rngMafia}""")
        await channel.send(f"""Parity Cop: """)
        await channel.send(f"""{rngParity}""")
        await channel.send(f"""Vig: """)
        await channel.send(f"""{rngVig}""")
        await channel.send(f"""Medic: """)
        await channel.send(f"""{rngMedic}""")

    if "!botoff" in message.content.lower():
        channel = client.get_channel(hostcommandsid)
        await channel.send("MafiaBot Offline")
        quit()















###Self-Contained Functions###

#Adds player to MafiaPlayer/Signedup channel by assigning MafiaPlayer role
async def addPlayer(user, role):
    uservalue = random.randint(1, 5000)
    await user.add_roles(role)
    return user, uservalue, user.display_name

async def assignMafia(userslist):
    global townList
    templist = []
    for i in range(3):
        channel = client.get_channel(mafiaid)
        await channel.set_permissions(userslist[i], read_messages=True, send_messages=True)
        templist.append(userslist[i])
    return templist

async def assignVig(userslist):
    templist = []
    channel = client.get_channel(vigid)
    await channel.set_permissions(userslist[3], read_messages=True, send_messages=True)
    templist.append(userslist[3])
    return templist

async def assignMedic(userslist):
    templist = []
    channel = client.get_channel(medicid)
    await channel.set_permissions(userslist[4], read_messages=True, send_messages=True)
    templist.append(userslist[4])
    return templist

async def assignParity(userslist):
    templist = []
    channel = client.get_channel(paritycopid)
    await channel.set_permissions(userslist[5], read_messages=True, send_messages=True)
    templist.append(userslist[5])
    return templist

async def assignTown(userslist, mafiaList):
    templist = []
    for user in users:
        if user not in mafiaList:
            templist.append(user)
    return templist

async def killPower(nightCounter):
    global mafiakills
    global killsRemaining
    #Kill Power for 15MAN
    if len(playerList) is 15:
        if nightCounter is 1:
            mafiakills = 2
            killsRemaining = 2
        elif nightCounter is not 1 and len(mafiaList) < 3:
            mafiakills = 1
            killsRemaining = 1
        elif nightCounter is not 1 and len(mafiaList) is 3:
            mafiakills = 2
            killsRemaining = 2
    #Kill power for 14man
    if len(playerList) is 14:
        if nightCounter is 1:
            mafiakills = 1
            killsRemaining = 1
        elif nightCounter is not 1 and len(mafiaList) is 3:
            mafiakills = 2
            killsRemaining = 2
        elif nightCounter is not 1 and len(mafiaList) < 3:
            mafiakills = 1
            killsRemaining = 1
    #Kill power for 13 man
    if len(playerList) is 13:
        if nightCounter is 1:
            mafiakills = 1
            killsRemaining = 1
        elif nightCounter is 2:
            if len(mafiaList) is 3:
                mafiakills = 1
                killsRemaining = 1
            elif len(mafiaList) < 3:
                mafiakills = 0
                killsRemaining = 0
        elif nightCounter > 2 and len(mafiaList) is 3:
            mafiakills = 2
            killsRemaining = 2
        elif nightCounter > 2 and len(mafiaList) < 3:
            mafiakills = 1
            killsRemaining = 1
    #Kill power for 17 man
    if len(playerList) is 16:
        if nightCounter is 1:
            mafiakills = 3
            killsRemaining = 3
        elif nightCounter is not 1 and len(mafiaList) is 3:
            mafiakills = 2
            killsRemaining = 2
        elif nightCounter is not 1 and len(mafiaList) < 3:
            mafiakill = 1
            killsRemaining = 1

async def medicNight():
    global staticMedicSavedList
    x = len(staticMedicSavedList)
    yesnoList = ['yes', 'no']
    channel = client.get_channel(medicid)
    await channel.send(f"""Who would you like to save from one bullet?""")
    msg = await client.wait_for('message', check=lambda message: message.content.lower() in nicks and "medic" in str(message.channel) and str(message.author.display_name) != message.content.lower())
    if len(staticMedicSavedList) > 0:
        if msg.content.lower() == staticMedicSavedList[x-1]:
            await channel.send("You cannot save the same person twice in a row.")
            return "blank"
    nameString = msg.content.lower()
    await channel.send(f"""Would you like to save {nameString}?""")
    msg2 = await client.wait_for('message', check=lambda message: message.content.lower() in yesnoList and "medic" in str(message.channel))
    if msg2.content.lower() == 'yes':
        await channel.send(f"""{nameString} has been saved. Goodnight.""")
        staticMedicSavedList.append(nameString)
        return nameString
    elif msg2.content.lower() == 'no':
        await channel.send(f"""{nameString} has not been saved.""")
        return "blank"

async def vigNight():
    global didVigShoot
    global killsList
    yesnoList = ['yes', 'no']
    channel = client.get_channel(vigid)
    await channel.send(f"""Would you like to shoot someone tonight?""")
    msg = await client.wait_for('message', check=lambda message: message.content.lower() in yesnoList and "vig" in str(message.channel))
    yesnoString = msg.content.lower()
    if yesnoString == 'no':
        await channel.send("Goodnight.")
        return 'no'
    elif yesnoString == 'yes':
        await channel.send(f"""Who would you like to shoot?""")
        msg2 = await client.wait_for('message', check=lambda message: message.content.lower() in nicks and "vig" in str(message.channel))
        nameString = msg2.content.lower()
        await channel.send(f"""{nameString} has been shot. Goodnight.""")
        didVigShoot = 1
        killsList.append(nameString)
        return nameString

async def parityNight():
    global parityCheckList
    yesnoList = ['yes', 'no']
    channel = client.get_channel(paritycopid)
    await channel.send(f"""Who would you like to check tonight?""")
    msg = await client.wait_for('message', check=lambda message: message.content.lower() in nicks and "paritycop" in str(message.channel))
    nameString = msg.content.lower()
    await channel.send(f"""Would you like to check {nameString}?""")
    msg2 = await client.wait_for('message', check=lambda message: message.content.lower() in yesnoList and "paritycop" in str(message.channel))
    if msg2.content.lower() == 'yes':
        if len(parityCheckList) < 1:
            await channel.send(f"""{nameString} has been added as your first check. Goodnight.""")
            return nameString
        elif len(parityCheckList) >= 1:
            x = len(parityCheckList)
            tempLastString = "'{}'".format(parityCheckList[x-1])
            tempNameString = "'{}'".format(nameString)
            if (tempLastString in str(staticMafiaList) and tempNameString not in str(staticMafiaList)) or (tempLastString not in str(staticMafiaList) and tempLastString in str(staticMafiaList)):
                await channel.send(f"""{nameString} is different from {parityCheckList[x-1]}""")
                return nameString
            else:
                await channel.send(f"""{nameString} is the same as {parityCheckList[x-1]}""")
                return nameString
    elif msg2.content.lower() == 'no':
        return "blank"

async def mafiaNight(mafiakills):
    global killsList
    global killsRemaining
    yesnoList = ['yes', 'no']
    yesVotes = 0
    yesList = []
    channel = client.get_channel(mafiaid)
    await channel.send(f"""Mafia has {killsRemaining} kills. Please enter a name""")
    msg = await client.wait_for('message', check=lambda message: message.content.lower() in nicks and "mafia" in str(message.channel))
    nameString = msg.content.lower()
    await channel.send(f"""Would you like to shoot {nameString}?""")
    while yesVotes < len(mafiaList):
        msg2 = await client.wait_for('message', check=lambda message: message.content.lower() in yesnoList and "mafia" in str(message.channel) and message.author not in yesList)
        if msg2.content.lower() == 'yes':
            yesList.append(msg2.author)
            yesVotes = yesVotes + 1
            await channel.send(f"""{nameString} now has {yesVotes} yes votes. {len(mafiaList) - yesVotes} more votes needed""")
        elif msg2.content.lower() == 'no':
            yesVotes = 20
            await channel.send("Vote failed.")
    if yesVotes is len(mafiaList):
        killsRemaining = killsRemaining - 1
        killsList.append(nameString)
        yesList.clear()
        return killsRemaining
    elif yesVotes is 20:
        yesList.clear()
        yesVotes = 0
        return killsRemaining

async def shotPlayers(killsList):
    global mafiakills
    for name in killsList:
        channel = client.get_channel(mafiaplayersid)
        user = get(channel.members, display_name=name)
        tempName = "'{}'".format(user.display_name)
        if tempName in str(mafiaList):
            mafiaList.remove(user)
        elif tempName in str(medicMemList):
            medicMemList.remove(user)
        elif tempName in str(vigMemList):
            vigMemList.remove(user)
        elif tempName in str(parityMemList):
            parityMemList.remove(user)
        if tempName in str(townList):
            townList.remove(user)

        #remove from channels
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
    return None

async def lynchedPlayer():
    global killsList
    yesnoList = ['yes', 'no']
    channel = client.get_channel(hostcommandsid)
    await channel.send("Who would you like to lynch?")
    msg = await client.wait_for('message', check=lambda message: message.content.lower() in nicks and "hostcommands" in str(message.channel))
    nameString = msg.content.lower()
    await channel.send(f"""Would you like to lynch {nameString}?""")
    msg2 = await client.wait_for('message', check=lambda message: message.content.lower() in yesnoList and "hostcommands" in str(message.channel))
    if msg2.content.lower() == 'yes':
        killsList.append(nameString)
        return "no"
    elif msg2.content.lower() == 'no':
        await channel.send(f"""{nameString} has not been lynched.""")
        return "blank"

async def purge():
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
    #commands nstuff
    channel = client.get_channel(mafiasignupid)
    await channel.purge(limit=100)
    #hostcommands channel
    channel = client.get_channel(hostcommandsid)
    await channel.purge(limit=100)
    await channel.send("Channels purged")

async def endGame():
    #clear mafiaplayer role
    channel = client.get_channel(hostcommandsid)
    roleM = get(channel.guild.roles, name="MafiaPlayer")
    await channel.send("Ending game and resetting roles... Please wait")
    channel = client.get_channel(mafiaplayersid)
    for user in channel.members:
        for role in channel.guild.roles:
            if role.name == 'MafiaPlayer':

                await user.remove_roles(roleM)
                #clear all channels
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

    #clear variables and lists
    global didVigShoot
    global vigShot
    staticMafiaList.clear()
    mafiaList.clear()
    users.clear()
    nicks.clear()
    townList.clear()
    staticTownList.clear()
    medicSavedList.clear()
    randomvalue.clear()
    killsList.clear()
    parityCheckList.clear()
    parityMemList.clear()
    vigMemList.clear()
    medicMemList.clear()
    mafiakills = 0
    killsRemaining = 0
    didVigShoot = 0
    gameStart = 0
    gameEnd = 0
    medicSaved = "blank"
    vigShot = "blank"
    parityCheck = "blank"
    playerList.clear()
    await purge()
    channel = client.get_channel(hostcommandsid)
    await channel.send("Game has ended and roles reset.")
    return None


client.run("bottoken")
