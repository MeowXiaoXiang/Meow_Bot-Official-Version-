import discord
from discord.ext import tasks, commands
from core.classes import Cog_Extension
import asyncio
import random
import os
import json

with open('setting.json','r',encoding='utf8') as jset:
    jdata = json.load(jset)
    
game=[[999,999,999,999,999,999,999,999,999,999,999,999,999,999,999]#0
,[999,0,0,0,0,0,0,0,0,0,0,0,0,0,999]#1
,[999,0,0,0,0,0,0,0,0,0,0,0,0,0,999]#2
,[999,0,0,0,0,0,0,0,0,0,0,0,0,0,999]#3
,[999,0,0,101,2,0,0,0,0,0,0,1,0,0,999]#4
,[999,0,0,0,0,0,0,0,0,0,0,0,0,0,999]#5
,[999,0,0,0,0,0,0,0,0,0,0,0,0,0,999]#6
,[999,0,0,0,0,0,0,0,0,0,0,0,0,0,999]#7
,[999,999,999,999,999,999,999,999,999,999,999,999,999,999,999]]#8
gamedef = 88 #最高分數上限 不可大於88 [o]
gamer = 0 #userId [x]
gameStatusMax = 101 #目前尾巴最大值 [x]
reaction=['⬆️','⬇️','➡️','⬅️'] #方向鍵 [o]
directionStatus=3 #判斷方向 [x]
directionStatusIndex = 0 #判斷是否已經轉過彎[x]
messageId= 0 #遊戲訊息ID[x]
channelId = 0 #頻道ID[x]
score = 0 #分數[o?]
def gameReset(): #若要修改參數請改下面這部分[x]為不可修改[o]為可修改
    global game,gamedef,gamer,gameStatusMax,reaction,directionStatus,directionStatusIndex,messageId,channelId,score
    game=[[999,999,999,999,999,999,999,999,999,999,999,999,999,999,999]#0[x]
    ,[999,0,0,0,0,0,0,0,0,0,0,0,0,0,999]#1[x]
    ,[999,0,0,0,0,0,0,0,0,0,0,0,0,0,999]#2[x]
    ,[999,0,0,0,0,0,0,0,0,0,0,0,0,0,999]#3[x]
    ,[999,0,0,101,2,0,0,0,0,0,0,1,0,0,999]#4[x]
    ,[999,0,0,0,0,0,0,0,0,0,0,0,0,0,999]#5[x]
    ,[999,0,0,0,0,0,0,0,0,0,0,0,0,0,999]#6[x]
    ,[999,0,0,0,0,0,0,0,0,0,0,0,0,0,999]#7[x]
    ,[999,999,999,999,999,999,999,999,999,999,999,999,999,999,999]]#8
    gamedef = 88 #最高分數上限 不可大於88 [o]
    gamer = 0 #userId [x]
    gameStatusMax = 101 #目前尾巴最大值 [x]
    reaction=['⬆️','⬇️','➡️','⬅️'] #方向鍵 [o] 若要修改需改def direction & async def on_raw_reaction_add
    directionStatus=3 #判斷方向 [x]
    directionStatusIndex = 0 #判斷是否已經轉過彎[x]
    messageId= 0 #遊戲訊息ID[x]
    channelId = 0 #頻道ID[x]
    score = 0 #分數[o?]

def direction(i):#1⬆️2⬇️3➡️4⬅️
    direction={
        '⬆️':1,
        '⬇️':2,
        '➡️':3,
        '⬅️':4
    }
    return direction.get(i,None)
def block(i):#⬛ = 0,🟥 = 1,🟪 = 2,🟦 = 101~200,🟧 = 999
    if i in range(101,201):
        i=100
    block={
        0:'⬛',
        1:'🟥',
        2:'🟪',
        100:'🟦',
        999:'🟧'
    }
    return block.get(i,None)

def appleNone():
    global score,gamedef
    if gamedef == 0:
        return 'gameOver'
    score+=1
    rannum = random.randint(1,gamedef)
    a=1
    b=1
    for i in range(1,rannum+1):
        b+=1
        if b==14:
            b=1
            a+=1
    while(game[a][b] in  [1,2,999,*range(101,201)]):
        b+=1
        if b==14:
            b=1
            a+=1
        if a>7:
            a=1
    game[a][b] = 1
    gamedef-=1

class snake(Cog_Extension):
    def gameCreate(self):
        message = ''
        a=0
        for i in game:
            for i2 in game[a]:
                message+=block(i2)
            a+=1
            message+='\n'
        return message

    async def my_task(self):
        while True:
            global gameStatusMax,directionStatusIndex,gamedef
            embed=discord.Embed()
            a=0
            c=0
            gameOver = 0
            i22status = 0 #判斷是否已經移動過
            for i in game:
                b=0
                for i2 in game[a]:
                    if i2 == 2 and i22status == 0:
                        game[a][b]=gameStatusMax
                        i22status=1
                        if directionStatus == 1:
                            if game[a-1][b] == 999 or game[a-1][b] in range(101,201):
                                embed.add_field(name="遊戲結束", value="分數：{}".format(score), inline=True)
                                gameOver = 1
                            elif game[a-1][b] == 1:
                                print('貧果被吃掉了')
                                c=1
                                gameStatusMax+=1
                                game[a][b]=gameStatusMax
                                game[a-1][b] =2
                                if appleNone() == 'gameOver':
                                    gameOver = 1
                                    embed.add_field(name="遊戲勝利", value="分數：{}".format(score), inline=True)
                            else:
                                game[a-1][b] =2

                        if directionStatus == 2:
                            if game[a+1][b] == 999 or game[a+1][b] in range(101,201):
                                embed.add_field(name="遊戲結束", value="分數：{}".format(score), inline=True)
                                gameOver = 1
                            elif game[a+1][b] == 1:
                                print('貧果被吃掉了')
                                c=1
                                gameStatusMax+=1
                                game[a][b]=gameStatusMax
                                game[a+1][b] =2
                                if appleNone() == 'gameOver':
                                    gameOver = 1
                                    embed.add_field(name="遊戲勝利", value="分數：{}".format(score), inline=True)
                            else:
                                game[a+1][b] =2

                        if directionStatus == 3:
                            if game[a][b+1] == 999 or game[a][b+1] in range(101,201):
                                embed.add_field(name="遊戲結束", value="分數：{}".format(score), inline=True)
                                gameOver = 1
                            elif game[a][b+1] == 1:
                                print('貧果被吃掉了')
                                c=1
                                gameStatusMax+=1
                                game[a][b]=gameStatusMax
                                game[a][b+1] =2
                                if appleNone() == 'gameOver':
                                    gameOver = 1
                                    embed.add_field(name="遊戲勝利", value="分數：{}".format(score), inline=True)
                            else:
                                game[a][b+1] =2

                        if directionStatus == 4:
                            if game[a][b-1] == 999 or game[a][b-1] in range(101,201):
                                embed.add_field(name="遊戲結束", value="分數：{}".format(score), inline=True)
                                gameOver = 1
                            elif game[a][b-1] == 1:
                                print('貧果被吃掉了')
                                c=1
                                gameStatusMax+=1
                                game[a][b]=gameStatusMax
                                game[a][b-1] =2
                                if appleNone() == 'gameOver':
                                    gameOver = 1
                                    embed.add_field(name="遊戲勝利", value="分數：{}".format(score), inline=True)
                            else:
                                game[a][b-1] =2
                    if c == 0 and i2 in range(101,201):
                        game[a][b]-=1
                        if game[a][b] < 101:
                            game[a][b]=0
                    b+=1
                a+=1
            channel = self.bot.get_channel(channelId)
            editmessage = await channel.fetch_message(messageId)
            embed.set_footer(text=self.gameCreate())
            await editmessage.edit(embed=embed)
            directionStatusIndex = 0
            '''for i in game:
                print(i)
            print('\n')'''
            if gameOver == 1:
                gameReset()
                return
            await asyncio.sleep(1)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self,pl):
        if pl.user_id == gamer and pl.message_id == messageId:
            global directionStatus,directionStatusIndex
            channel = self.bot.get_channel(pl.channel_id)
            message = await channel.fetch_message(messageId)
            if str(pl.emoji) == '⬆️' and directionStatus != 2 and directionStatusIndex == 0:
                directionStatus = direction(str(pl.emoji))
                directionStatusIndex = 1
            elif str(pl.emoji) == '⬇️' and directionStatus != 1 and directionStatusIndex == 0:
                directionStatus = direction(str(pl.emoji))
                directionStatusIndex = 1
            elif str(pl.emoji) == '➡️' and directionStatus != 4 and directionStatusIndex == 0:
                directionStatus = direction(str(pl.emoji))
                directionStatusIndex = 1
            elif str(pl.emoji) == '⬅️' and directionStatus != 3 and directionStatusIndex == 0:
                directionStatus = direction(str(pl.emoji))
                directionStatusIndex = 1
            print(directionStatus)
            await message.remove_reaction(pl.emoji,pl.member)

    @commands.command(name= 'snake', aliases=['貪食蛇'], brief="貪食蛇", description="貪食蛇遊戲")
    async def snake(self,ctx):
        message = ''
        a=0
        for i in game:
            for i2 in game[a]:
                message+=block(i2)
            a+=1
            message+='\n'
        global gamer,messageId,channelId
        if gamer == 0:
            gamer = ctx.message.author.id
            print('s~~~ s~~~ s~~~')
            embed=discord.Embed()
            embed.set_footer(text=message)
            msg = await ctx.send(embed=embed)
            for i in reaction:
                await msg.add_reaction(i)
            messageId = msg.id
            channelId = msg.channel.id
            self.bot.loop.create_task(self.my_task())
        else:
            await ctx.send('已有人開始遊戲')

def setup(bot):
    gameReset()
    bot.add_cog(snake(bot))