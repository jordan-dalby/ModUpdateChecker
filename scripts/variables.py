import discord
import os

API_KEY = os.environ["API_KEY"]
BOT_TOKEN = os.environ["BOT_TOKEN"]
MOD_IDS = os.environ["MOD_IDS"].split(",")
CHANNEL_ID = int(os.environ["CHANNEL_ID"])
DEBUG_CHANNEL_ID = int(os.environ["DEBUG_CHANNEL_ID"])
MESSAGE_TEMPLATE = os.environ["MESSAGE_TEMPLATE"]
ANNOUNCE_MESSAGES = os.environ["ANNOUNCE_MESSAGES"].lower() == "true"

DEBUG_MODE = os.environ["DEBUG_MODE"].lower() == "true"

sleeptime = 300
version_re = r"\b(\d+)\.zip$"

filepath = os.path.abspath(__file__)
filepath = os.path.join(os.path.dirname(filepath), "latest.txt")
mod_info_url = "https://api.curseforge.com/v1/mods/{}"
changelog_base_url = "https://api.curseforge.com/v1/mods/{}/files/{}/changelog"
headers = {"x-api-key": API_KEY}

intents = discord.Intents.default()
