# MafiaBot

MafiaBot is a simple python project using [discord.py](https://github.com/Rapptz/discord.py) wrapper that automates a "Mafia" game within Discord with simple commands. This is made for a 15 player game, but the code can be adjusted to any room's liking. This bot assumes [these](https://docs.google.com/document/d/1yG_dGVLW_MjwEmiXDeizOm_Bm2U310kb7wsSDbfzXlk/edit?usp=sharing) rules over Zoom. The mafia game will still require one 'host' to enforce rules, use timers, and move along gameplay. This bot allows the 'host' to also play along with the other mafia members as the bot will only deliver neutral news to the host without giving away information.

Strongly recommend pairing with a 15-Way Zoom call.

## Notes and Considerations

1. The creator of the discord channel can not play in this game as they have full rights to every channel and can therefore see every role. If you are a Discord server owner who would like to play, I suggest creating a secondary account for mafia play (while logging out on your admin account). Other admins must be removed from the "administrator" group - though you may manually add all privileges separately.
2. MafiaBot must be given "administrator" permission to function.

## Installation

1. Create and add a bot called "MafiaBot" to your discord server (tutorials for this can be found elsewhere).
2. Create a role called "MafiaPlayer" on your discord server.
3. Create a private discord text channel called "hostcommands" (you may not name this channel differently) and other private text channels for mafia game roles: parity cop, mafia, vig, and medic. These channels can be named however you'd like. Create a private "deadchat" channel so people who've died can chat. Create a private "livemafia" or "mafiaplayers" channel (you may name as desired) and allow "MafiaPlayer" role to read and send messages in this chat.
4. **IMPORTANT**: Assign every user who wishes to play in your discord channel a nickname with all lowercase letters ('zach' or 'john' for example).
5. Get all ID's for every channel created above and your server. You will need to go into settings, enable developer options, then right click your channels and server to get their ID's. You will also need your "Bot Token"
6. Using a search and replace tool (Notepad, Notepad++, etc), open MafiaV[x].py and replace the following text strings with their respective ID's you have collected and your bot token with the bottoken string shown below:
 
```bash
mafiaid
hostcommandsid
paritycopid
vigid
medicid
deadchatid
serverid
bottoken
```

## Usage & How to Play

Run the MafiaBot script (MafiaV[x].py) - Instructions can be found [here](https://www.pythoncentral.io/execute-python-script-file-shell/)

Instruct users to type !mafia to play the game. Instruct users to use discord 'nicknames' on display list when asked for names from the bot.

### Mafia Player Commands:

!mafia - Enters user who enters this command into the mafia game. Every user must type this (in any channel) to be added to the bots calculations and be considered 'in the game'

!human - Sends an anonymous message into general chat that human interaction is needed. Generally, a dead player can become 'host' and takeover the responsibilities of the bot in the event of a broken game state (useful for zoom games).

### Mafia Host Commands:

!hostgo - Enters user into the hostcommands room - the only room where other host commands will work except !hoststop

!hoststop - Rescinds host status and exits hostcommands room. Use when you're done as host

!start - Assigns roles to all mafia players - this command starts the game, **to be used after everyone has typed !mafia**

!night - The command you will use as host every night. This sends requests for night actions and returns the results of the night without giving any information as to roles. **NOTE: This must be used after !start to enter into the first night**

!lynch - Type this to lynch a player on behalf of town. The bot will ask for nickname.

!# - Where # is a number. You will be asked for this command after !start. Usage is self-explanatory in game and sets starting kill power (kills per night) for mafia. !2 is suggested for normal purposes.

!purge - Can be used to clear all text chats involved in mafia (only the rooms you have created for mafia). This is automatically done at the end of every game if there were no errors and a win state was achieved for either mafia or town.

!end - Can be used to end an incomplete mafia game early. This can also be used before instructing users to type !mafia as a good preventative measure to clear bot values for a fresh game. This is automatically run when a mafia game is played to completion with no errors and a win state is achieved.

## General Gameflow

0. (Opt.) Type !end to reset all variables and ensure a clean slate before starting a game.
1. Instruct all players to type !mafia in any channel to enlist in the mafia game (they will know if they are added to the 'mafiaroom' or 'livemafia')
2. Tell everyone to go to bed.
2. Type !start in hostcomands room to assign all roles. Then type !night to send requests for action
3. Once you have received results from night, wake up everyone and share the news
4. Type !lynch if a successful lynch occurs, you will be prompted by the bot for a name
5. Repeat the !night command process and !lynch process until a win is reached.

6. (Opt.) Type !end if the game didn't complete with a win condition from the bot i.e. "all mafia are dead" or "mafia has won"
7. (Opt.) Type !purge to clear chat logs from all rooms except general chat and mafiaroom