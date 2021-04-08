import discord
from discord.ext import commands
import random
import json

with open('setting.json', 'r', encoding='utf8') as jfile:
    jdata = json.load(jfile)

errortxt = ('格式不正確，或是未使用有效的正整數',
            f'正確的格式是:\n`{jdata["command_prefix"]}ms <列> <行> <炸彈>`\n\n',
            '你可以不要給予值 直接使用 會給你隨機列、行、炸彈的數量唷。')
errortxt = ''.join(errortxt)

class minesweeper(commands.Cog):
    tag="Game"
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='minesweeper', aliases=['踩地雷' , 'ms'], brief="踩地雷遊戲", description=f"\n{jdata['command_prefix']}ms <列> <行> <炸彈>\n你可以不要給予值 直接使用 會給你隨機列、行、炸彈的數量唷。")
    async def minesweeper(self, ctx, columns = None, rows = None, bombs = None):
        if columns is None or rows is None and bombs is None:
            if columns is not None or rows is not None or bombs is not None:
                await ctx.send(errortxt)
                return
            elif columns is None and rows is None and bombs is None:
                await ctx.send(f'若你想要指定的話：{jdata["command_prefix"]}ms <列> <行> <炸彈>')
                columns = random.randint(4,9)
                rows = random.randint(4,9)
                bombs = columns * rows - 1
                bombs = bombs / 2.5
                bombs = round(random.randint(5, round(bombs)))
            else:
                #若不給參數的話 會給4到13範圍 隨機給行列的數量
                #（（列×行）－1）÷ 2.5
                #這是確保我們網格上的炸彈比例不會太高
                columns = random.randint(4,9)
                rows = random.randint(4,9)
                bombs = columns * rows - 1
                bombs = bombs / 2.5
                bombs = round(random.randint(5, round(bombs)))
        try:
            columns = int(columns)
            rows = int(rows)
            bombs = int(bombs)
        except ValueError:
            await ctx.send(errortxt)
            return
        if columns > 9 or rows > 9:
            await ctx.send('由於Discord限制 列和行的限制為9')
            return
        if columns < 1 or rows < 1 or bombs < 1:
            await ctx.send('提供的數字不可以為0或負值')
            return
        if bombs + 1 > columns * rows:
            await ctx.send(':boom:**爆炸**, 你的炸彈數量不可以比網格還多啦!也不能跟網格一樣多!')
            return
        
        # 在list中用0填滿 來當臨時的網格
        grid = [[0 for num in range (columns)] for num in range(rows)]

        loop_count = 0
        while loop_count < bombs:
            x = random.randint(0, columns - 1)
            y = random.randint(0, rows - 1)
            if grid[y][x] == 0:
                grid[y][x] = 'B'
                loop_count = loop_count + 1
            # 假如炸彈已經隨機選擇 迴圈會在執行一次 
            if grid[y][x] == 'B':
                pass

        # 這個while迴圈 會走過每個點 在臨時的網格
        pos_x = 0
        pos_y = 0
        a = [(0,1),(0,-1),(1,0),(-1,0),(1,1),(-1,1),(1,-1),(-1,-1)]
        while pos_x * pos_y < columns * rows and pos_y < rows:
            adj_sum = 0
            for (adj_y, adj_x) in a:
                #這邊會出現索引錯誤..所以~ 就用try..except直接忽略這個錯誤030
                try:
                    if grid[adj_y + pos_y][adj_x + pos_x] == 'B' and adj_y + pos_y > -1 and adj_x + pos_x > -1:
                        adj_sum = adj_sum + 1
                except Exception as error:
                    pass
            # 由於不想把Bomb變數更改為數字，
            # 迴圈所在的點只在不是"B"的情況下才改變
            if grid[pos_y][pos_x] != 'B':
                grid[pos_y][pos_x] = adj_sum
            # 增加X值 直到超過列數為止
            # 若while中沒有pos_y < columns 會導致索引錯誤
            if pos_x == columns - 1:
                pos_x = 0
                pos_y = pos_y + 1
            else:
                pos_x = pos_x + 1

        # 建構字串準備就緒
        string_builder = []
        for the_rows in grid:
            string_builder.append(''.join(map(str, the_rows)))
        string_builder = '\n'.join(string_builder)
        # 替換數字和表情對應
        string_builder = string_builder.replace('0', '||:zero:||')
        string_builder = string_builder.replace('1', '||:one:||')
        string_builder = string_builder.replace('2', '||:two:||')
        string_builder = string_builder.replace('3', '||:three:||')
        string_builder = string_builder.replace('4', '||:four:||')
        string_builder = string_builder.replace('5', '||:five:||')
        string_builder = string_builder.replace('6', '||:six:||')
        string_builder = string_builder.replace('7', '||:seven:||')
        string_builder = string_builder.replace('8', '||:eight:||')
        final = string_builder.replace('B', '||:bomb:||')

        percentage = columns * rows
        percentage = bombs / percentage
        percentage = 100 * percentage
        percentage = round(percentage, 2)

        embed = discord.Embed(title='\U0001F642 踩地雷 Minesweeper \U0001F635', color=0xC0C0C0)
        embed.add_field(name='列：', value=columns, inline=True)
        embed.add_field(name='行：', value=rows, inline=True)
        embed.add_field(name='整體數量：', value=columns * rows, inline=True)
        embed.add_field(name='\U0001F4A3 數量：', value=bombs, inline=True)
        embed.add_field(name='\U0001F4A3 百分比：', value=f'{percentage}%', inline=True)
        embed.add_field(name='玩家：', value=ctx.author.display_name, inline=True)
        await ctx.send(content=f'\U0000FEFF\n{final}', embed=embed)

    @minesweeper.error
    async def minesweeper_error(self, ctx, error):
        await ctx.send(errortxt)
        return

def setup(bot):
    bot.add_cog(minesweeper(bot))