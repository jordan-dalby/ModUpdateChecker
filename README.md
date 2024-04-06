# Mod Update Checker
  
Big thanks to the original author for figuring out the API calls & code for that, I simply moved things around and dockerised everything.  
  
This fork does not use embeds, instead opting for a basic message to allow for tagging with @everyone or @here  
  
  
## UNRAID installation  
  
To install into your UNRAID system, you can wget the template XML file into ```/boot/config/plugins/dockerMan/templates-user```  
  
```
cd /boot/config/plugins/dockerMan/templates-user
wget https://raw.githubusercontent.com/jordan-dalby/ModUpdateChecker/main/my-asamodupdatechecker.xml
```  
  
Then go through the usual container creation process and fill in any required variables.  
  
  
## docker-compose  
  
I recommend that you use docker-compose for its simplicity.  
To do so, add your information into .env.template, ensuring you keep the single quotations, then rename the file to .env and run docker-compose up.  
  

## Dockerfile  
  
This repo was created to be run on UNRAID, however it's still possible to run this manually with docker run and the following environment variables set: 
``` 
API_KEY = your curseforge API key  
BOT_TOKEN = your discord bot token  
MOD_IDS = mod id's to track, separated with a comma e.g. 12345678,87654321  
CHANNEL_ID = discord channel ID to send announcements to e.g. 123456789123456  
DEBUG_CHANNEL_ID = discord channel ID to send debug to e.g. 123456789123456  
ANNOUNCE_MESSAGES = should messages sent to the announcement channel be published? True or False  
MESSAGE_TEMPLATE = the message, separated with line breaks \n {mod_name} {version} {changes} \n etc. Leave blank for a default message template.
```
  
You can pass the .env file into docker run by adding --env-file=.env  
  
![example image](https://i.imgur.com/buqdM7I.png)