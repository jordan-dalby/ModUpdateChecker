Big thanks to the original author for figuring out the API calls & code for that, I simply moved things around and dockerised everything.  
  
This repo was created to be run on UNRAID, however it's still possible to run this manually with docker run and the following environment variables set:  
API_KEY = your curseforge API key  
BOT_TOKEN = your discord bot token  
MOD_IDS = mod id's to track, separated with a comma e.g. 12345678,87654321  
CHANNEL_ID = discord channel ID to send announcements to e.g. 123456789123456  
DEBUG_CHANNEL_ID = discord channel ID to send debug to e.g. 123456789123456  
ANNOUNCE_MESSAGES = should messages sent to the announcement channel be published? True or False  
  
However, I recommend that you use docker-compose instead, to do so, add your information into .env.template, ensuring you keep the single quotations, then rename the file to .env  
  
Original README  
little discord bot which periodically checks if there was an update released for your mods.  
  
If there is an update it posts an embed message into a specified channel together with the changelogs.  
check https://discordpy.readthedocs.io/en/stable/intro.html and https://discordpy.readthedocs.io/en/stable/discord.html for the general discord.py setup guide  
  
The "old" bot can be found in... "oldbot > bot.py"  
  
You need to edit the `secrets.py` where you enter the CF API token and the bot token 
  
Settings can be found in the `statics.py`  
If you want to add additional commands check the `main.py`  
  
to start the bot install the dependencies listed down below and run `python3 main.py`  

### Dependencies:  
  
discord.py   
aiosqlite  
requests  
html2text  


![image](https://i.imgur.com/P1SF2qj.png)
