import discord
from discord.ext import commands
from core.classes import Cog_Extension
import os
import json

with open('setting.json','r',encoding='utf8') as jset:
    jdata = json.load(jset)

messageReactionId=[]
messageId=[]
gamerAndMessageId=[]
gamer=[]
game=[]
def gameOver(i,index):
    messageId.remove(i)
    gamer.remove(game[index][9])
    gamer.remove(game[index][10])
    game.remove(game[index])
def gameRound(i):
    ooxx={
        1:'1️⃣',
        2:'2️⃣',
        3:'3️⃣',
        4:'4️⃣',
        5:'5️⃣',
        6:'6️⃣',
        7:'7️⃣',
        8:'8️⃣',
        9:'9️⃣',
        'o':'⭕',
        'x':'❌',
    }
    return ooxx.get(i,None)
def gameRoundEmoji(i):
    ooxx={
        '1️⃣':1,
        '2️⃣':2,
        '3️⃣':3,
        '4️⃣':4,
        '5️⃣':5,
        '6️⃣':6,
        '7️⃣':7,
        '8️⃣':8,
        '9️⃣':9
    }
    return ooxx.get(i,None)

class ooxx(Cog_Extension):
    tag="Game"
    @commands.Cog.listener()
    async def on_raw_reaction_add(self,pl):
        if pl.message_id in messageReactionId and pl.user_id not in gamer and pl.user_id != self.bot.user.id and str(pl.emoji) == '👊':
            for i in range(0,len(gamerAndMessageId)):
                if gamerAndMessageId[i][1] == pl.message_id:
                    gamerAndMessageId.remove(gamerAndMessageId[i])
            gamer.append(pl.user_id)
            messageReactionId.remove(pl.message_id)
            channel = self.bot.get_channel(pl.channel_id)
            msg = await channel.fetch_message(pl.message_id)
            for i in msg.mentions: #index 0 to 9
                user1 = self.bot.get_user(i.id)
                game.append([i.id])
            user2 = self.bot.get_user(pl.user_id)
            game[len(game)-1].append(pl.user_id)#index 1 to 10
            await msg.delete()
            message=''
            for i in range(1,10):
                game[len(game)-1].insert(i-1,i)
                if i % 3==0:
                    message+='{}\n'.format(gameRound(i))
                else:
                    message+='{}'.format(gameRound(i))
            msg = await channel.send(message)
            for i in range(1,10):#index 0~8
                await msg.add_reaction(gameRound(i))
            await msg.add_reaction('😞')
            game[len(game)-1].append(msg.id)#index 11
            game[len(game)-1].append(0)#index 12
            messageId.append(msg.id)
            await channel.send('遊戲開始<@{}> VS <@{}> 按下😞即投降'.format(user1.id, user2.id))

        if pl.message_id in messageId and pl.user_id != self.bot.user.id:
            messageIdIndex=int()
            for i in range(0,len(messageId)):
                if pl.message_id == i:
                    messageIdIndex = i
            channel = self.bot.get_channel(pl.channel_id)
            msg = await channel.fetch_message(pl.message_id)
            if game[messageIdIndex][12] %2 == 0 and pl.user_id == game[messageIdIndex][9] and str(pl.emoji) != '😞':
                await msg.clear_reaction(pl.emoji)
                game[messageIdIndex].remove(gameRoundEmoji(str(pl.emoji)))
                game[messageIdIndex].insert(gameRoundEmoji(str(pl.emoji))-1,'o')
                game[messageIdIndex][12] += 1
            elif game[messageIdIndex][12] %2 == 1 and pl.user_id == game[messageIdIndex][10] and str(pl.emoji) != '😞':
                await msg.clear_reaction(pl.emoji)
                game[messageIdIndex].remove(gameRoundEmoji(str(pl.emoji)))
                game[messageIdIndex].insert(gameRoundEmoji(str(pl.emoji))-1,'x')
                game[messageIdIndex][12] += 1
            message=''
            a=1
            for i in game[messageIdIndex]:#ooxx遊戲排版
                if a>9:
                    pass
                elif a % 3==0:
                    message+='{}\n'.format(gameRound(i))
                else:
                    message+='{}'.format(gameRound(i))
                a+=1
            #==========================勝利/平局判定================================================
            if game[messageIdIndex][0] == game[messageIdIndex][1] == game[messageIdIndex][2]:#行一
                if game[messageIdIndex][0] =='o':
                    message+='\n{}勝利'.format(self.bot.get_user(game[messageIdIndex][9]))
                else:
                    message+='\n{}勝利'.format(self.bot.get_user(game[messageIdIndex][10]))
                await msg.clear_reactions()
                gameOver(game[messageIdIndex][11],messageIdIndex)
            elif game[messageIdIndex][3] == game[messageIdIndex][4] == game[messageIdIndex][5]:#行二
                if game[messageIdIndex][3] =='o':
                    message+='\n{}勝利'.format(self.bot.get_user(game[messageIdIndex][9]))
                else:
                    message+='\n{}勝利'.format(self.bot.get_user(game[messageIdIndex][10]))
                await msg.clear_reactions()
                gameOver(game[messageIdIndex][11],messageIdIndex)
            elif game[messageIdIndex][6] == game[messageIdIndex][7] == game[messageIdIndex][8]:#行三
                if game[messageIdIndex][6] =='o':
                    message+='\n{}勝利'.format(self.bot.get_user(game[messageIdIndex][9]))
                else:
                    message+='\n{}勝利'.format(self.bot.get_user(game[messageIdIndex][10]))
                await msg.clear_reactions()
                gameOver(game[messageIdIndex][11],messageIdIndex)
            elif game[messageIdIndex][0] == game[messageIdIndex][3] == game[messageIdIndex][6]:#直一
                if game[messageIdIndex][0] =='o':
                    message+='\n{}勝利'.format(self.bot.get_user(game[messageIdIndex][9]))
                else:
                    message+='\n{}勝利'.format(self.bot.get_user(game[messageIdIndex][10]))
                await msg.clear_reactions()
                gameOver(game[messageIdIndex][11],messageIdIndex)
            elif game[messageIdIndex][1] == game[messageIdIndex][4] == game[messageIdIndex][7]:#直二
                if game[messageIdIndex][1] =='o':
                    message+='\n{}勝利'.format(self.bot.get_user(game[messageIdIndex][9]))
                else:
                    message+='\n{}勝利'.format(self.bot.get_user(game[messageIdIndex][10]))
                await msg.clear_reactions()
                gameOver(game[messageIdIndex][11],messageIdIndex)
            elif game[messageIdIndex][2] == game[messageIdIndex][5] == game[messageIdIndex][8]:#直三
                if game[messageIdIndex][2] =='o':
                    message+='\n{}勝利'.format(self.bot.get_user(game[messageIdIndex][9]))
                else:
                    message+='\n{}勝利'.format(self.bot.get_user(game[messageIdIndex][10]))
                await msg.clear_reactions()
                gameOver(game[messageIdIndex][11],messageIdIndex)
            elif game[messageIdIndex][0] == game[messageIdIndex][4] == game[messageIdIndex][8]:#斜\
                if game[messageIdIndex][0] =='o':
                    message+='\n{}勝利'.format(self.bot.get_user(game[messageIdIndex][9]))
                else:
                    message+='\n{}勝利'.format(self.bot.get_user(game[messageIdIndex][10]))
                await msg.clear_reactions()
                gameOver(game[messageIdIndex][11],messageIdIndex)
            elif game[messageIdIndex][2] == game[messageIdIndex][4] == game[messageIdIndex][6]:#斜/
                if game[messageIdIndex][2] =='o':
                    message+='\n{}勝利'.format(self.bot.get_user(game[messageIdIndex][9]))
                else:
                    message+='\n{}勝利'.format(self.bot.get_user(game[messageIdIndex][10]))
                await msg.clear_reactions()
                gameOver(game[messageIdIndex][11],messageIdIndex)
            elif game[messageIdIndex][12] == 9:
                message+='\n平局'
                await msg.clear_reactions()
                gameOver(game[messageIdIndex][11],messageIdIndex)
            #==========================勝利/平局判定================================================
            elif str(pl.emoji) == '😞':#投降用
                async def surr(user1,user2):
                    print(messageIdIndex)
                    await msg.clear_reactions()
                    gameOver(game[messageIdIndex][11],messageIdIndex)
                    return str('\n{}已經投降 {}勝利').format(user1,user2)
                if pl.user_id==game[messageIdIndex][9]:
                    user1 = self.bot.get_user(game[messageIdIndex][9])
                    user2 = self.bot.get_user(game[messageIdIndex][10])
                    message+=await surr(user1,user2)
                elif pl.user_id==game[messageIdIndex][10]:
                    user1 = self.bot.get_user(game[messageIdIndex][10])
                    user2 = self.bot.get_user(game[messageIdIndex][9])
                    message+=await surr(user1,user2)
            await msg.edit(content=message)
            

    @commands.group(name='ooxx', aliases=['圈圈叉叉'], brief="遊戲OOXX", description=f"遊戲OOXX 若沒人陪你一起玩可以輸入{jdata['command_prefix']}ooxx leave")
    async def ooxx(self,ctx):
        if ctx.message.author.id not in gamer:#判斷是否已加入一場遊戲
            msg = await ctx.send('玩家<@'+ str(ctx.author.id) +'>開始遊戲OOXX \n挑戰者請點擊下列圖標 \n若想放棄遊戲請輸入 {}ooxx leave'.format(jdata['command_prefix']))
            await msg.add_reaction('👊')
            gamer.append(ctx.message.author.id)
            messageReactionId.append(msg.id)
            gamerAndMessageId.append([ctx.message.author.id,msg.id])
        else:
            pass

    @ooxx.command()
    async def leave(self,ctx):
        for i in range(0,len(gamerAndMessageId)):
            if gamerAndMessageId[i][0] == ctx.message.author.id:
                msg = await ctx.channel.fetch_message(gamerAndMessageId[i][1])
                await msg.delete()
                gamer.remove(gamerAndMessageId[i][0])
                messageReactionId.remove(gamerAndMessageId[i][1])
                gamerAndMessageId.remove(gamerAndMessageId[i])

def setup(bot):
    bot.add_cog(ooxx(bot))