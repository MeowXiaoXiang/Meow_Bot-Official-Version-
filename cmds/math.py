import discord
from discord.ext import commands
import os
from core.classes import Cog_Extension
import json
with open('setting.json','r',encoding='utf8') as jset:
    jdata = json.load(jset)
msgid = int()
mathClick = 0
gameStatus = 0
gameMember = []
gameNember = int()
gameRound = 0

def gameReaction(emoji):
    emojilist={
        '1️⃣':'1',
        '2️⃣':'2',
        '3️⃣':'3'
    }
    return emojilist.get(emoji, None)

def msgidchan(a):
    global msgid
    msgid = int(a)

class math(Cog_Extension):
    tag="Game"
    @commands.Cog.listener()
    async def on_raw_reaction_add(self,pl):
        global mathClick,msgid,gameMember,gameStatus,gameNember,gameRound
        if pl.user_id != 737611092653637684 and pl.message_id == msgid and str(pl.emoji) == '👊' and mathClick == 0 and pl.member.id not in gameMember:
            print('successful')
            guild = self.bot.get_guild(pl.guild_id)
            channel = guild.get_channel(pl.channel_id)
            msg = await channel.fetch_message(msgid)
            await msg.delete()
            mathClick = 1
            gameMember.append(pl.member.id)
            await channel.send('遊戲開始\n玩家<@'+str(gameMember[0])+'> 和 <@'+str(gameMember[1])+'>')
            msg = await channel.send('<@'+str(gameMember[0])+'>的回合\n目前數字：'+str(gameNember))
            msgidchan(msg.id)
            await msg.add_reaction('1️⃣')
            await msg.add_reaction('2️⃣')
            await msg.add_reaction('3️⃣')

        if mathClick == 1 and pl.message_id == msgid:
            guild = self.bot.get_guild(pl.guild_id)
            channel = guild.get_channel(pl.channel_id)
            msg = await channel.fetch_message(msgid)
            if pl.user_id == gameMember[gameRound]:
                gameNember = gameNember - int(gameReaction(str(pl.emoji)))
                gameRound += 1
                if gameRound == 2:
                    gameRound = 0
            if pl.user_id != 737611092653637684:
                await msg.remove_reaction(pl.emoji, pl.member)
            if gameNember > 0:
                await msg.edit(content='<@'+str(gameMember[gameRound])+'>的回合\n目前數字：'+str(gameNember))
            else:
                await msg.edit(content='勝者是：<@'+str(gameMember[gameRound])+'>')
                await msg.clear_reactions()
                mathClick = 0
                msgid = int()
                gameNember = int()
                gameStatus = 0
                gameRound = 0
                gameMember = []
        pass
    @commands.command()
    async def mathleave(self,ctx):
        global msgid,mathClick,gameStatus,gameMember,gameNember,gameRound
        await ctx.message.delete()
        message = await ctx.message.channel.fetch_message(msgid)
        await message.delete()
        msgid = int()
        mathClick = 0
        gameStatus = 0
        gameMember = []
        gameNember = int()
        gameRound = 0

    @commands.command(name="math" , aliases=['MATH' , 'Math'] ,description="兩人輪流點數字表情來拿走數字,最後數字歸0的輸", brief="拿取數字遊戲")
    async def math(self,ctx, num: int = 20):
        global msgid,gameMember,gameStatus,gameNember
        await ctx.message.delete()
        if gameStatus == 0:
            if str(num).isdigit():
                if int(num) >= 20 and int(num) <= 50 :
                    msg = await ctx.send('玩家<@'+ str(ctx.author.id) +'>開始遊戲math：{} \n挑戰者請點擊下列圖標 {}mathleave 可取消遊戲'.format(num,jdata['command_prefix']))
                    await msg.add_reaction('👊')
                    msgid = msg.id
                    gameMember.append(ctx.author.id)
                    gameStatus = 1
                    gameNember = int(num)
                else:
                    await ctx.send(jdata['command_prefix']+'math [數字20~50]')
        else:
            await ctx.send('遊戲已開始')

def setup(bot):
    bot.add_cog(math(bot))