# MafiaBot

MafiaBot is a simple python project using [discord.py](https://github.com/Rapptz/discord.py) wrapper that automates a "Mafia" game within Discord with simple commands. This is made for a 13-16 player game (ideal is 15), but the code can be adjusted to any room's liking. This bot assumes [these rules](https://docs.google.com/document/d/1yG_dGVLW_MjwEmiXDeizOm_Bm2U310kb7wsSDbfzXlk/edit?usp=sharing) over Zoom. The mafia game will still require one 'host' to enforce rules, use timers, and move along gameplay. A timer web application to assist the host can be found [here](http://advancedmod.com/mafia/) This bot allows the 'host' to also play along with the other mafia members as the bot will only deliver neutral news to the host without giving away information.

Strongly recommend pairing with a 15-Way Zoom call.

## Notes and Considerations

1. The creator of the discord channel can not play in this game as they have full rights to every channel and can therefore see every role. If you are a Discord server owner who would like to play, I suggest creating a secondary account for mafia play (while logging out on your admin account). Other admins must be removed from the "administrator" group, as these players will also see every channel regardless of permissions - though you may manually add all privileges separately.
2. MafiaBot must be given "administrator" permission to function.

## Installation

1. Create and add a bot called "MafiaBot" to your discord server (tutorials for this can be found elsewhere). Give it "administrator"
2. Create a role called "MafiaPlayer" on your discord server.
3. Create the following private discord text channels in your server (they must be named exactly as described unless you manually change code): 'hostcommands', 'paritycop', 'mafia', 'vig', 'medic', and 'deadchat'. Also create a private 'mafiaplayers' channel and allow "MafiaPlayer" role to read and send messages in this chat. Finally, create a **public** text channel called 'mafiasignup' (ideally set send messages permission of everyone to no)
4. **IMPORTANT**: Assign every user who wishes to play in your discord channel a nickname with all lowercase letters ('zach' or 'john' for example).
5. Get all ID's for every channel created above and your server. You will need to go into settings, enable developer options, then right click your channels and server to get their ID's. You will also need your "Bot Token"
6. Using a search and replace tool (Notepad, Notepad++, etc), open MafiaV[x].py and replace the following text strings with their respective ID's you have collected and your bot token with the bottoken string shown below. For example, my gathered mafia channel ID is 716819081738715674, so I would replace "mafiaid" in the MafiaV[x].py provided with "716819081738715674":
 
```bash
mafiaid
hostcommandsid
paritycopid
vigid
medicid
deadchatid
mafiasignupid
mafiaplayersid
bottoken
```

## Usage & How to Play

Run the MafiaBot script (MafiaV[x].py) - Instructions can be found [here](https://www.pythoncentral.io/execute-python-script-file-shell/)

Host types !start in the 'hostcommands' room to play the game. A sign-up message is created, users sign up by reacting with a thumbs up. Once all users have signed up, host tells everyone to go to sleep and types !assign followed by !night to start the game. Instruct all users to use discord 'nicknames' on the right-side discord display list when asked for names from the bot. Detailed instructions on night actions and lynching can be found below.

### Mafia Host Commands:

!hostgo - Enters user into the hostcommands room - the only room where other host commands will work except !hoststop

!hoststop - Rescinds host status and exits hostcommands room. Use when you're done as host

!start - Creates a sign-up message that players react to in order to sign up

!assign - Assigns roles to players who reacted to the Mafia Sign Up message. You use this command only once per game, **to be used after everyone has reacted to signup message**

!night - The command you will use as host every night. This sends requests for night actions and returns the results of the night without giving any information as to roles. **NOTE: This must be used after !assign to enter into the first night**

!lynch - Type this to lynch a player on behalf of town (during daytime). The bot will ask for a nickname.

!purge - Can be used to clear all text chats involved in mafia (only the rooms you have created for mafia). This is automatically done at the end of every game if there were no errors and a win state was achieved for either mafia or town.

!end - Can be used to end an incomplete mafia game early. This can also be used before instructing users to type !mafia as a good preventative measure to clear bot values for a fresh game. This is automatically run when a mafia game is played to completion with no errors and a win state is achieved.

## General Gameflow

0. (Opt.) Type !end to reset all variables and ensure a clean slate before starting a game.
1. Type !start and instruct all players to react to Mafia Sign up message to enlist in the mafia game.
2. Tell everyone to go to bed.
2. Type !assign in hostcomands room to assign all roles. When done, type !night to send requests for action
3. Once you have received results from night, wake up everyone and share the news
4. Type !lynch if a successful lynch occurs, you will be prompted by the bot for a name
5. Repeat the !night command process and !lynch process until a win is reached.

6. (Opt.) Type !end if the game didn't complete with a win condition from the bot i.e. "all mafia are dead" or "mafia has won"
7. (Opt.) Type !purge to clear chat logs from all rooms except general chat and mafiaroom
