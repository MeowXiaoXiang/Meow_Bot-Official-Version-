import discord
from discord.ext import commands
from core.classes import Cog_Extension
from loguru import logger
import json

with open('setting.json', 'r', encoding='utf8') as jfile:
    jdata = json.load(jfile)


class admin(Cog_Extension):
    #清除訊息
    tag = "admin"
    @commands.command(name='clear', aliases=['clean' , '清除'], brief="刪除聊天記錄", description="此功能可以清除指定數量的訊息\n使用方法：clear [指定數量]\n刪除指定數量的聊天記錄")
    async def clear(self,ctx,num:int=0):
      if num == 0:
        await ctx.send(jdata["command_prefix"] + "clear [num] 刪除指定數量的聊天記錄")
      else:
        try:
          if ctx.message.author.id == ctx.guild.owner_id:
              await ctx.channel.purge(limit=int(num)+1)
              print(str(ctx.message.author)+' ---ID '+str(ctx.message.author.id)+'在 << '+str(ctx.channel.name)+' >> 頻道使用了clear指令刪除了'+str(num)+'個對話')
              if int(num)>=10:
                await ctx.send('https://tenor.com/view/explode-blast-blow-nuclear-boom-gif-15025770')
          else:
              await ctx.send('權限不足 本指令只提供給伺服器傭有者 \n本伺服器擁有者為 <@' + str(ctx.guild.owner_id) + '>')
        except discord.errors.Forbidden:
          await ctx.send("機器人權限不足")
          print("機器人本身的權限不足")
          logger.error('error: Missing Permissions (error code: 50013)')
        except:
          await ctx.send("請勿在私人頻道使用這功能")
          print("請勿在私人頻道使用這功能")
   
    
    @commands.command(name= 'sendch', aliases=['向頻道發送訊息'], brief="向頻道發送訊息", description=f"此功能可以操控機器人向頻道發送訊息\n使用方法為：{jdata['command_prefix']}sendch [頻道ID] \n要開啟'外觀->開發者模式'然後對頻道滑鼠右鍵複製ID")
    async def sendch(self,ctx,chid='None',*,msg='None'):
      if chid == 'None' or msg == 'None':
        await ctx.send(f"未給予參數\n使用方法為：{jdata['command_prefix']}sendch [頻道ID] \n要開啟'外觀->開發者模式'然後對頻道滑鼠右鍵複製ID")
      else:
        if ctx.author.id == jdata['owner']:
            ch = self.bot.get_channel(int(chid))
            await ch.send(msg)
        else:
            await ctx.send(admin.InsufficientPermissions())
            
    
    @commands.command(name= 'send', aliases=['私訊'], brief="向用戶發送訊息",description=f"此功能可以直接用機器人私訊目標用戶\n使用方法為：{jdata['command_prefix']}send [用戶ID]\n要開啟'外觀->開發者模式'然後對用戶滑鼠右鍵複製ID")
    async def send(self,ctx,userid='None',*,msg='None'):
      if userid == 'None' or msg == 'None':
        await ctx.send(f"未給予參數\n使用方法為：{jdata['command_prefix']}send [用戶ID]\n要開啟'外觀->開發者模式'然後對用戶滑鼠右鍵複製ID")
      else:
        if ctx.author.id == jdata['owner']:
            if '!' in userid:
                user = str(userid).split('!')
            else:
                user = str(userid).split('@')
            if str.isdigit(user[0]):
                user2 = self.bot.get_user(int(userid))
                await user2.send(msg)
            else:
                user1 = str(user[1]).split('>')
                user2 = self.bot.get_user(int(user1[0]))
                await user2.send(msg)
        else:
            await ctx.send(admin.InsufficientPermissions())

    class InsufficientPermissions(Exception):
      def __str__(self):
        return f'權限不足 本指令只提供給BOT擁有者 \n擁有者為 <@{jdata["owner"]}>'

def setup(bot):
    bot.add_cog(admin(bot))