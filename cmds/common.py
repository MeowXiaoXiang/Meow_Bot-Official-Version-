import discord
from discord.ext import commands
from core.classes import Cog_Extension
import json

with open('setting.json', 'r', encoding='utf8') as jfile:
    jdata = json.load(jfile)

class common(Cog_Extension):
    tag="Common"
    #ping
    @commands.command(name= 'ping', aliases=['延遲' , '機器人延遲' , 'delay'], brief="顯示機器人延遲", description="顯示機器人到Discord的延遲")
    async def ping(self, ctx):
      latency = round(self.bot.latency*1000)
      red = max(0,min(int(255*(latency-50)/1000),255))
      green = 255-red
      color = discord.Colour.from_rgb(r=red,g=green,b=0)
      embed = discord.Embed(title="當前機器人的延遲",description=f'⌛ Ping：{round(self.bot.latency*1000)} 毫秒 (ms)',color=color)
      await ctx.send(embed=embed)

    #說
    @commands.command(name= 'sayd', aliases=['說' , '機器人說'], brief="復讀", description=f"使機器人說話\n使用方法：{jdata['command_prefix']}sayd [訊息]")
    async def sayd(self,ctx,*,value:str='None'):
      if value == 'None':
        await ctx.send(f"未給予參數\n使用方法：{jdata['command_prefix']}sayd [訊息] ")
      else:
          await ctx.message.delete()
          if value != str():
              await ctx.send(value)
    
    @commands.command(name= 'avatar', aliases=['頭貼' , '頭像'], brief="顯示目標用戶的頭像", description=f"此功能可以顯示目標用戶的頭像全圖\使用方法：{jdata['command_prefix']}avatar [用戶ID] \n要開啟'外觀->開發者模式'然後對用戶滑鼠右鍵複製ID")
    async def avatar(self,ctx,userid:str='0'):
      uid2 = userid.split('>')
      uid = int((uid2[0])[-18:])
      user = self.bot.get_user(int(uid))
      if user == None:
        await ctx.send(f"找不到指定用戶\n使用方法：{jdata['command_prefix']}avatar [用戶ID] \n要開啟'外觀->開發者模式'然後對用戶滑鼠右鍵複製ID")
      else:
        asset = user.avatar_url
        await ctx.send(str(asset))
      
def setup(bot):
    bot.add_cog(common(bot))