import requests
import asyncio
import aiosqlite
import html2text
import re
from datetime import datetime
from variables import ANNOUNCE_MESSAGES, MESSAGE_TEMPLATE, DEBUG_MODE, version_re

db_path = '/db/mod_data.db'

async def create_initial_db():
    async with aiosqlite.connect(db_path) as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS mod_data (
                mod_id INTEGER PRIMARY KEY,
                mod_name TEXT,
                latest_file TEXT,
                latest_date TEXT,
                mod_url TEXT
            )
        ''')
        await db.commit()

async def fill_initial_data_db(mod_ids, mod_info_url, headers, debug):
    async with aiosqlite.connect(db_path) as db:
        for mod_id in mod_ids:
            mod_id = str(mod_id)
            mod_url = mod_info_url.format(mod_id)
            response = requests.get(mod_url, headers=headers)
            if response.status_code == 200:
                response_data = response.json()
                mod_name = response_data['data']['name']
                latest_files = response_data['data']['latestFiles']
                latest_file_info = latest_files[0]
                latest_file = latest_file_info['displayName']
                latest_date = latest_file_info['fileDate']
                mod_cf_url = response_data['data']['links']['websiteUrl']
                cursor = await db.execute('SELECT mod_id FROM mod_data WHERE mod_id = ?', (mod_id,))
                existing_entry = await cursor.fetchone()
                if not existing_entry:
                    await db.execute('''
                        INSERT INTO mod_data (mod_id, mod_name, latest_file, latest_date, mod_url)
                        VALUES (?, ?, ?, ?, ?)
                    ''', (mod_id, mod_name, latest_file, latest_date, mod_cf_url))
                    await db.commit()
            else:
                await debug.send(f"Mod Request failed for Mod ID {mod_id}: {response.status_code}")

async def check_for_updates_db(channel, debug, mod_ids, mod_info_url, headers, changelog_base_url, sleeptime):
    async with aiosqlite.connect(db_path) as db:
        while True:
            update_data = {}
            for mod_id in mod_ids:
                mod_id = str(mod_id)
                mod_url = mod_info_url.format(mod_id)
                response = requests.get(mod_url, headers=headers)
                if response.status_code == 200:
                    response_data = response.json()
                    mod_name = response_data['data']['name']
                    latest_files = response_data['data']['latestFiles']
                    mod_cf_url = response_data['data']['links']['websiteUrl']
                    cursor = await db.execute('SELECT * FROM mod_data WHERE mod_id = ?', (mod_id,))
                    existing_entry = await cursor.fetchone()
                    file_date_old = None
                    if existing_entry:
                        file_date_old = datetime.strptime(existing_entry[3], '%Y-%m-%dT%H:%M:%S.%fZ')
                    update_found = False
                    file_id = None
                    for file_info in latest_files:
                        file_date = file_info['fileDate']
                        current_date = datetime.strptime(file_date, '%Y-%m-%dT%H:%M:%S.%fZ')
                        if file_date_old is None or current_date > file_date_old or DEBUG_MODE:
                            update_found = True
                            file_id = file_info['id']
                            break
                    if update_found:
                        update_data[mod_id] = {
                            "mod-name": mod_name,
                            "latest-file": latest_files[0]['displayName'],
                            "latest-date": latest_files[0]['fileDate'],
                            "mod-url": response_data['data']['links']['websiteUrl']
                        }
                        changelog_url = changelog_base_url.format(mod_id, file_id)
                        changelog_response = requests.get(changelog_url, headers=headers)
                        if changelog_response.status_code == 200:
                            changelog_data = changelog_response.json()
                            changes = changelog_data['data']
                            changes = html2text.html2text(changes, bodywidth=0)
                            changes = changes.replace('\-', '-')
                            version = re.search(version_re, update_data[mod_id]['latest-file'])
                            if version:
                                version = version.group(1)
                            header = f"{mod_name} version {version}" if version else f"A new version of {mod_name}"
                            msg = [
                                f'@everyone {header} has been released. Please update your server and clients.',
                                f'Changes:',
                                f'{changes}',
                                f'\nPlease report any issues.',
                            ]
                            msg = "\n".join(msg)

                            if len(MESSAGE_TEMPLATE) != 0:
                                replacements = {
                                    "{mod_name}": mod_name,
                                    "{version}": version,
                                    "{changes}": changes,
                                    "\\n": "\n"
                                }
                                msg = MESSAGE_TEMPLATE
                                for pattern, replacement in replacements.items():
                                    msg = msg.replace(pattern, replacement)

                            if DEBUG_MODE:
                                await debug.send(msg)
                            else:
                                message = await channel.send(msg)
                                if ANNOUNCE_MESSAGES:
                                    if channel.is_news():
                                        await message.publish()
                        else:
                            await debug.send(
                                f"Changelog Request failed for Mod ID {mod_id}: {changelog_response.status_code}")
                else:
                    await debug.send(f"Mod Request failed for Mod ID {mod_id}: {response.status_code}")
            if update_data:
                for mod_id, data in update_data.items():
                    mod_name = data["mod-name"]
                    latest_file = data["latest-file"]
                    latest_date = data["latest-date"]
                    mod_cf_url = data["mod-url"]
                    cursor = await db.execute('SELECT mod_id FROM mod_data WHERE mod_id = ?', (mod_id,))
                    existing_entry = await cursor.fetchone()
                    if existing_entry:
                        await db.execute('''
                                        UPDATE mod_data
                                        SET mod_name = ?, latest_file = ?, latest_date = ?, mod_url = ?
                                        WHERE mod_id = ?
                                    ''', (mod_name, latest_file, latest_date, mod_cf_url, mod_id))
                    else:
                        await db.execute('''
                                        INSERT INTO mod_data (mod_id, mod_name, latest_file, latest_date, mod_url)
                                        VALUES (?, ?, ?, ?, ?)
                                    ''', (mod_id, mod_name, latest_file, latest_date, mod_cf_url))
                    await db.commit()
            await asyncio.sleep(sleeptime)
