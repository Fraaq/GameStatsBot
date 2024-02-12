# GameStatsBot
GameStatsBot is an open-source project that includes the code for a Discord bot designed 
to add Source and GoldSource servers to a MongoDB database and provide statistics for those servers. 
The bot is programmed in Python, utilizing the Discord API and dependencies for 
database integration.

## 📋Table of contents
* [Features](#features)
* [How to use it](#how-to-use-it)
* [How to customize bot](#how-to-customize-bot)
* [Commands](#commands)
* [Screenshots](#screenshots)

## ⭐Features
* Easy to customize
* MongoDB database
* Multiple servers support
* Send server's name, ip, map, map thumbnail, player count
* Send all players and their names, scores and playtime
* Send stored information about server

## 📌How to use it 
1. Install python 
2. Install and setup Mongodb or use MongoDB Atlas
3. Download and unzip this repository
4. Install required modules   
```pip install -r requirements.txt```
5. Create file .env and put there your discord token and mongodb login details  
**If you are using mongodb atlas:**  
```MONGODB_STRING='Your-Monhodb-Connection-String'```  
**If you are using normal mongodb**
```
MONGODB_IP_AND_PORT='MongodbIpAndPort'
MONGODB_PASSWORD='MongodbPassword'
```  
**The final .env file should looks like something like this:**
```
DISCORD_TOKEN='YourDiscordToken'
MONGODB_IP_AND_PORT='MongodbIpAndPort'
MONGODB_PASSWORD='MongodbPassword'
```  
6. Run bot.py

## 🔧Players list fix for CS2
1. Install [AuthSessionFix](https://github.com/Source2ZE/AuthSessionFix/releases/) on your CS2 server
2. Install [ServerListPlayersFix](https://github.com/Source2ZE/ServerListPlayersFix/releases/) on your CS2 server

## 💎Commands

**!add_server** (Add game server to the database) | Required role to use this command is **games server manager**  
**!del_server** (Delete server from the database) | Required role to use this command is **games server manager**    
**!servers** (List of all servers from the database)   
**!info** (Stored information about the server from the database)   
**!players** (All players of the server with their names, scores and playtime)   
**!stats** (Stats of the server like game, name, description, map, player count, map thumbnail)   

## 🛠️How to customize the bot
* ### Add thumbnails
  * Your map thumbnail file should be named exactly as the map name (de_mirage.jpg)
  * Upload your thumbnail to the [map-thumbnails/your-game-name/](map-thumbnails)
* ### Add thumbnails for more games
  * You need to create new folder in [map-thumbnails/](map-thumbnails) and the folder should have name exactly
    same as your game name without this characters \\, /, :, *, ?, ", <, >, |   
    If you don't know exactly the game name you can write !stats and the name is in field game.
  * For example if my game is CS2 I will write !stats and there is this name: Counter-Strike 2 
    I will remove the special characters so my game folder inside [map-thumbnails/](map-thumbnails) should look
    like this map-thumbnails/Counter-Strike 2
  
* ### Help messages
  * Edit help messages in [help_messages.json](help_messages.json).
* ### Discord role for managing servers
  * Edit this string ```DISCORD_MANAGE_ROLE``` in [validators.py](validators.py).

## 🖼️Screenshots
  <img src="/screenshots/screen1.png?raw=true" alt="Help command" width="600"/><br>  
  <img src="/screenshots/screen2.png?raw=true" alt="Add server and servers command" width="600"/><br>    
  <img src="/screenshots/screen3.png?raw=true" alt="Stats command" width="600"/><br>   
  <img src="/screenshots/screen4.png?raw=true" alt="Players command" width="600"/><br><br>
  <img src="/screenshots/screen5.png?raw=true" alt="Info command" width="600"/>
