import discord
from discord.ext import commands
import os
import sys
import json
from datetime import datetime,timedelta
import keep_alive
from loguru import logger
from core.time import time_info #時間戳記 時間 UTC+8
import asyncio
import requests

intents = discord.Intents.all()

with open('setting.json', 'r', encoding='utf8') as jfile:
    jdata = json.load(jfile)

bot = commands.Bot(command_prefix=commands.when_mentioned_or(jdata['command_prefix']),intents = intents)
start_time = datetime.now()

@bot.event
async def on_ready():
    log(f'{bot.user} | Ready!')
    activity = discord.Activity(type=discord.ActivityType.watching,name = "WARFRAME的資料")
    await bot.change_presence(activity=activity)
    while True:
        await asyncio.sleep(40)
        requests.get("http://127.0.0.1:8080/")
#------------------------------------------------------------------------------
bot.remove_command('help') #移除原有的help選單 help選單放在common.py內
#------------------------------help清單-----------------------------------------
#help指令
@bot.command(name="help" , aliases=['幫助' , '機器人功能' , 'HELP'] ,description=f"展示`command`的幫助信息\n若要翻頁 請輸入{jdata['command_prefix']}help all 頁數", brief="展示幫助列表")
async def help(ctx, command:str="all", page:int=1):
  fields = 0
  embed = discord.Embed(title="幫助列表",color=0xccab2b)
  if command == "all":
    for command in bot.commands:
      if command.brief != None:
        if (page-1)*25<fields<=page*25-1:
          embed.add_field(name=f"{jdata['command_prefix']}{command.name}", value=command.brief, inline=True)
        fields += 1
    embed.set_footer(text=f"第{page}/{int((fields-fields%25)/25+1)}頁")
    await ctx.send(embed=embed)
  elif command in commands.values():
    for botcommand in bot.commands:
      if command == "common" and botcommand.cog_name == None:
        if (page-1)*25<fields<=page*25-1:
          embed.add_field(name=f"{jdata['command_prefix']}{botcommand.name}", value=botcommand.brief)
        fields += 1
      for ext,tag in commands.items():
        if tag == command and ext == botcommand.cog_name:
          if (page-1)*25<fields<=page*25-1:
            embed.add_field(name=f"{jdata['command_prefix']}{botcommand.name}", value=botcommand.brief)
          fields += 1
    embed.set_footer(text=f"第{page}/{int((fields-fields%25)/25+1)}頁")
    await ctx.send(embed=embed)
  else:
    for botcommand in bot.commands:
      if botcommand.name == command:
        aliases = botcommand.name
        params = ""
        for param in botcommand.clean_params:
          params += f"<{param}>"
        for alias in botcommand.aliases:
          aliases += f"|{alias}"
        embed.add_field(name=f"{jdata['command_prefix']}[{aliases}] {params}",value=botcommand.description)
        await ctx.send(embed=embed)
        return
    await ctx.send("找不到您要問的呢")
#-----------------以下為機器人基本模組載入卸載列出下載功能區域建議不要隨意更改------------
@bot.command(name='status', aliases=['debug'],brief="除錯信息",description="回報當前機器人狀態信息進行除錯")
async def status(ctx):
  if await bot.is_owner(ctx.message.author):
    embed = discord.Embed(title="目前狀態:")
    embed.add_field(name="目前延遲",value=f"{round(bot.latency*1000)}ms",inline=False)
    perms = ">>> "
    for name,value in ctx.channel.permissions_for(ctx.me):
      if value == True:
        perms += name + '\n'
    embed.add_field(name="本機權限",value=perms,inline=True)
    exts = ">>> "
    for ext in bot.extensions:
      exts += ext.replace("cmds.","")+'\n'
    embed.add_field(name="已載入模組",value=exts,inline=True)
    uptime = datetime.now()-start_time
    embed.set_footer(text=f"目前版本：v2.5.6 在線時間:{uptime.days}天{int(uptime.seconds/3600)}小時{int(uptime.seconds%3600/60)}分{uptime.seconds%3600%60}秒")
    await ctx.send(embed=embed)
  else:
    await ctx.send(embed=discord.Embed(title="權限不足",description='本指令只提供給伺服器傭有者 \n本伺服器擁有者為 <@' + str(ctx.guild.owner_id) + '>'))

@bot.command(name= 'load', aliases=['載入' , '載入模組' , '啟用'], brief="載入機器人模組", description = f"此功能為載入機器人模組使用\n使用方法：{jdata['command_prefix']}load [模組名稱]")
async def load(ctx, extension:str ='Null'):
  if ctx.author.id == jdata['owner']:
    if extension == 'Null':
      await ctx.send(NullMod())
    else:
      try:
        bot.load_extension(F'cmds.{extension}')
        await ctx.send(f'\n已加載：{extension}')
        print('\n---------------------------------\n' + time_info.UTC_8() + f'\n已加載 {extension}\n---------------------------------\n')
      except Exception as e:
        await ctx.send(f"組件加載失敗\n```cs\n{e}```")
        logger.error(f'load error: {str(e)}')
  else:
      await ctx.send(InsufficientPermissions())

@bot.command(name= 'unload', aliases=['卸載' , '卸載模組' , '停用'], brief="卸載機器人模組", description = f"此功能為卸載機器人模組使用\n{jdata['command_prefix']}unload [模組名稱]")
async def unload(ctx, extension:str='Null'):
  if ctx.author.id == jdata['owner']:
    if extension == 'Null':
      await ctx.send(NullMod())
    else:
      try:
        bot.unload_extension(F'cmds.{extension}')
        await ctx.send(f'\n已卸載：{extension}')
        print('\n---------------------------------\n' + time_info.UTC_8() + f'\n已卸載 {extension}\n---------------------------------\n')
      except Exception as e:
        await ctx.send(f"組件卸載失敗\n```cs\n{e}```")
        logger.error(f'unload error: {str(e)}')
  else:
      await ctx.send(InsufficientPermissions())


@bot.command(name= 'reload', aliases=['重載' , '重載模組' , '重新載入模組', '重新加載', '重啟' , '重新載入'], brief="重載機器人模組", description = f"此功能為重啟機器人模組使用\n{jdata['command_prefix']}reload [模組名稱]")
async def reload(ctx, extension:str ='Null'):
  if ctx.author.id == jdata['owner']:
    if extension == 'Null':
      await ctx.send(NullMod())
    else:
      try:
        bot.reload_extension(F'cmds.{extension}')
        await ctx.send(f'\n已重新載入：{extension}')
        print('\n---------------------------------\n' + time_info.UTC_8() + f'\n已重新載入 {extension}\n---------------------------------\n')
      except Exception as e:
        await ctx.send(f"組件重新載入失敗\n```cs\n{e}```")
        logger.error(f'reload error: {str(e)}')
  else:
      await ctx.send(InsufficientPermissions())

#機器人關閉系統--------------------------------------------   

@bot.command(name= 'disconnect', aliases=['disable' , 'shutdown' , '關閉機器人' , '關機' , '關閉'], brief="關閉機器人", description = "此功能為關閉機器人")
async def turn_off_bot(ctx):
  if ctx.message.author.id == jdata['owner']:
    print(f"-----------------------------------------\n{time_info.UTC_8()}\n機器人已關閉" + "\n-----------------------------------------")
    await ctx.send(time_info.UTC_8() + '\n機器人已關閉') #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    await bot.close()
  else:
    await ctx.send(InsufficientPermissions())

@bot.event
async def on_disconnect():
    requests.get("http://127.0.0.1:8080/")
    fp = open('./log/' + 'system.log', 'a',encoding='utf8')
    fp.write(f"{time_info.UTC_8()}\n------機器人已關閉------\n")
    print(f"-----------------------------------------\n{time_info.UTC_8()}\n機器人已關閉" + "\n-----------------------------------------")
    fp.close()
#---------------------------------------------------------

class InsufficientPermissions(Exception):
  def __str__(self):
    return '權限不足 本指令只提供給BOT擁有者 \n擁有者為 <@' + jdata["owner"] + '>'
class NullMod(Exception):
  def __str__(self):
    return '此處不可為空 請輸入組件名稱'

#系統錯誤紀錄
@bot.event
async def on_command_error(ctx, error):
    logger.error(f'error: {str(error)}')


def set_logger():
    log_format = (
        '{time:YYYY-MM-DD HH:mm:ss} |'
        '<lvl>{level: ^9}</lvl>| '
        '{message}'
    )
    logger.add(sys.stderr, level='INFO', format=log_format)
    logger.add(
        './log/system.log',
        rotation='7 day',
        retention='30 days',
        level='INFO',
        encoding='UTF-8',
        format=log_format
    )

def log(msg):
    logger.info(msg)

#------------把cmd內的所有模組做載入--------------
for filename in os.listdir('./cmds'):
    if filename.endswith('.py'):
        bot.load_extension(f'cmds.{filename[:-3]}')

commands = {}
for extension in bot.extensions:
  package = extension
  name = extension[5:]
  tags = getattr(__import__(package, fromlist=[name]), name)      
  try:
    commands[name] = tags.tag
  except:
    pass

if __name__ == "__main__":
    set_logger()
    keep_alive.keep_alive()
    bot.run(jdata['TOKEN'])