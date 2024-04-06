import asyncio
import variables
import os
from discord.ext import commands
from data_fetcher import create_initial_db, fill_initial_data_db, check_for_updates_db

bot = commands.Bot(command_prefix='-', intents=variables.intents)

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    channel = bot.get_channel(variables.CHANNEL_ID)
    debug = bot.get_channel(variables.DEBUG_CHANNEL_ID)
    await debug.send(f"Bot is online.")
    await create_initial_db()
    await fill_initial_data_db(variables.MOD_IDS, variables.mod_info_url, variables.headers, debug)
    await asyncio.sleep(10)
    await check_for_updates_db(channel, debug, variables.MOD_IDS, variables.mod_info_url, variables.headers,
                                variables.changelog_base_url, variables.sleeptime)

bot.run(variables.BOT_TOKEN)