import discord
import pickle
import configparser
import random
import time
from datetime import datetime, timedelta, timezone
import sys
import asyncio
import re

global JST
global Youbi
global OldYoubi
global Limit

with open('Temp/OldYoubi.binaryfile', 'rb')as Box_OldYoubi:
    OldYoubi = pickle.load(Box_OldYoubi)

JST = timezone(timedelta(hours=9))

Youbi = datetime.now(tz=JST).strftime('%w')

if OldYoubi == Youbi:
    with open('Temp/Limit.binaryfile', 'rb')as Box_Limit:
        Limit = pickle.load(Box_Limit)
    print("本日起動済みの為、本日の履歴から復元します。")

else:
    Limit = []
    OldYoubi = Youbi
    with open('Temp/Limit.binaryfile', 'wb')as Box_Limit:
        pickle.dump(Limit, Box_Limit)

    with open('Temp/OldYoubi.binaryfile', 'wb')as Box_OldYoubi:
        pickle.dump(OldYoubi, Box_OldYoubi)
    print("本日は起動していないためリセットしました。")

#接続に必要なオブジェクト生成
client = discord.Client()

#ファイル操作に必要なあれこれ
ini = configparser.ConfigParser(strict=False)

#設定ファイル読み込み
ini.read('./config.ini', encoding='utf-8')

#Tokenの読み込み
Token = (ini.get('Bot', 'Token'))

#Adminの読み込み
Admin = (ini.get('Bot', 'Admin'))

@client.event
async def on_ready():
    print(f'次のBotが起動しました: {client.user.name}')
    print(f'Bot ID: {client.user.id}')
    await client.change_presence(activity=discord.Game(name="現在稼働中！"))

@client.event
async def on_message(message):
    global JST
    global Youbi
    global OldYoubi
    global Limit

    Result = ["大吉","吉", "中吉", "小吉", "末吉", "凶"]

    if message.author.bot:
        return

    if OldYoubi != Youbi:
        Limit = []
        OldYoubi = Youbi
        with open('Temp/Limit.binaryfile', 'wb')as Box_Limit:
            pickle.dump(Limit, Box_Limit)

        with open('Temp/OldYoubi.binaryfile', 'wb')as Box_OldYoubi:
            pickle.dump(OldYoubi, Box_OldYoubi)

    if message.content in ["!kuso", "!ks"]:
        if message.author.id in Limit:
            await message.channel.send("1日1回しか引けません。")
            return
        
        else:
            Limit.append(message.author.id)
            with open('Temp/Limit.binaryfile', 'wb')as Box_Limit:
                pickle.dump(Limit, Box_Limit)
            Temp = await message.channel.send("あなたの運勢は...")
            await asyncio.sleep(3)
            await Temp.edit(content=f"あなたの運勢は...**{random.choice(Result)}**です。")
            return

    
    if message.content.startswith("/relimit"):
        if str(message.author.id) in Admin:
            Temp = int(re.sub(r"\D", "", message.content))
            if Temp in Limit:
                Limit.remove(Temp)
                await message.channle.send(f"<@{Temp}> の制限を解除しました。")
                return
            
            else:
                await message.channel.send(f"<@{Temp}> は制限されていません。")


client.run(Token)