import discord
from discord.ext import commands
import pickle
import configparser
import random
import time
from datetime import datetime, timedelta, timezone
import sys
import asyncio
import re

#接続に必要なオブジェクト生成
bot = commands.Bot(command_prefix="!")


with open('Temp/OldYoubi.binaryfile', 'rb')as Box_OldYoubi:
    bot.OldYoubi = pickle.load(Box_OldYoubi)

bot.JST = timezone(timedelta(hours=9))

bot.Youbi = datetime.now(tz=bot.JST).strftime('%w')

if bot.OldYoubi == bot.Youbi:
    with open('Temp/Limit.binaryfile', 'rb')as Box_Limit:
        Limit = pickle.load(Box_Limit)
    print("本日起動済みの為、本日の履歴から復元します。")

else:
    bot.Limit = []
    bot.OldYoubi = bot.Youbi
    with open('Temp/Limit.binaryfile', 'wb')as Box_Limit:
        pickle.dump(bot.Limit, Box_Limit)

    with open('Temp/OldYoubi.binaryfile', 'wb')as Box_OldYoubi:
        pickle.dump(bot.OldYoubi, Box_OldYoubi)
    print("本日は起動していないためリセットしました。")


#ファイル操作に必要なあれこれ
ini = configparser.ConfigParser(strict=False)

#設定ファイル読み込み
ini.read('./config.ini', encoding='utf-8')

#Tokenの読み込み
Token = (ini.get('Bot', 'Token'))

#Adminの読み込み
bot.Admin = (ini.get('Bot', 'Admin'))

bot.Result = ["大吉","吉", "中吉", "小吉", "末吉", "凶"]

@bot.event
async def on_ready():
    print(f'次のBotが起動しました: {bot.user.name}')
    print(f'Bot ID: {bot.user.id}')
    await bot.change_presence(activity=discord.Game(name="現在稼働中！"))

@bot.event
async def on_message(message):

    if message.author.bot:
        return

    if bot.OldYoubi != bot.Youbi:
        bot.Limit = []
        bot.OldYoubi = bot.Youbi
        with open('Temp/Limit.binaryfile', 'wb')as Box_Limit:
            pickle.dump(bot.Limit, Box_Limit)

        with open('Temp/OldYoubi.binaryfile', 'wb')as Box_OldYoubi:
            pickle.dump(bot.OldYoubi, Box_OldYoubi)

    await bot.process_commands(message)
    
@bot.command(name="omikuji",aliases=["mikuji"])
async def omikuji_(ctx):
    if ctx.author.id in bot.Limit:
        await ctx.channel.send("1日1回しか引けません。")

    else:
        bot.Limit.append(ctx.author.id)
        with open('Temp/Limit.binaryfile', 'wb')as Box_Limit:
            pickle.dump(bot.Limit, Box_Limit)
        Temp = await ctx.send(f"{ctx.author.mention} あなたの運勢は...")
        await asyncio.sleep(3)
        await Temp.edit(content=f"{ctx.author.mention} の運勢は...**{random.choice(bot.Result)}**です。")

    
@bot.command(name="relimit")
async def relimit_(ctx,member:commands.MemberConverter):
    if str(ctx.author.id) in bot.Admin:
        if member.id in bot.Limit:
            bot.Limit.remove(member)
            await ctx.send(f"{member.mention} の制限を解除しました。")
        else:
            await ctx.send(f"{member.mention} は制限されていません。")


    else:
        await ctx.send(f"{ctx.author.mention} 管理者権限がありません。")



bot.run(Token)