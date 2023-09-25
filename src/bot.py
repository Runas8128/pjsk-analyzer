import discord
from discord.app_commands import Choice, choices, describe
from discord.ext.commands import Bot, Context

import typing
from uploader import Uploader
from mongoose import Mongoose
import data

bot = Bot('!', help_command=None, intents=discord.Intents.all())

str2Choice = lambda value: Choice(name=value, value=value)

def build_embed(rst):
    embed = discord.Embed(title=f'{rst["title"]} ({rst["diff"]})')
    embed.add_field(name='score', value=str(rst["score"]))
    embed.add_field(name='accuracy', value=f'{rst["acc"]:.2f}%')
    embed.add_field(name='combo', value=str(rst["combo"]))
    embed.add_field(name='====================', value=' ', inline=False)
    for judge in rst["judge"]:
        embed.add_field(name=judge, value=str(rst["judge"][judge]))
    return embed

@bot.tree.command(name='pb', description='해당 채보에 대한 개인 최고 기록을 보여줍니다.')
@describe(music='검색할 악곡입니다.')
@describe(diff='해당 악곡의 난이도입니다. (기본값: MASTER)')
@choices(diff=list(map(str2Choice, data.diff)))
@describe(option='최고 기록의 기준입니다. (정확도/콤보/점수 ; 기본값: 정확도)')
@choices(option=list(map(str2Choice, ["acc", "combo", "score"])))
async def pjsk_pb(interaction: discord.Interaction, music: str, diff: typing.Optional[Choice[str]], option: typing.Optional[Choice[str]]):
    uid = str(interaction.user.id)
    data = { 'title': music, 'diff': diff.value if diff else 'MASTER' }
    if not Mongoose.has(uid, data):
        await interaction.response.send_message('None')
        return
    rst = sorted(Mongoose.get(uid, data), key=lambda data: data[option.value if option else 'acc'], reverse=True)
    await interaction.response.send_message(embed=build_embed(rst[0]))

@pjsk_pb.autocomplete("music")
async def pjsk_pb_music_autocomplete(interaction: discord.Interaction, curr: str):
    return list(map(str2Choice, data.Musics.find(curr)))

def getGoodUnder(data):
    judge = data['judge']
    return judge['good'] + judge['bad'] + judge['miss']

def weightedGoodUnder(data):
    judge = data['judge']
    return judge['good'] + judge['bad'] * 2 + judge['miss'] * 4

@bot.tree.command(name='suggest', description='최고기록이 GOOD 이하 판정의 총합이 가장 작은 순서대로 5개를 가져옵니다.')
async def pjsk_suggest(interaction: discord.Interaction):
    await interaction.response.defer()
    datas = {}
    collected = {}
    for data in Mongoose.get(str(interaction.user.id), {}):
        key = (data['title'], data['diff'])
        if key not in collected:
            collected[key] = getGoodUnder(data)
            datas[key] = data
        else:
            comp = collected[key]
            count = getGoodUnder(data)
            if comp > count:
                collected[key] = count
                datas[key] = data
    result = filter(lambda data: getGoodUnder(data) != 0, datas.values())
    result = sorted(result, key=lambda data: data['acc'], reverse=True)
    result = sorted(result, key=weightedGoodUnder)[:5]
    embed = discord.Embed(title='풀콤 제안 곡 목록')
    for r in result:
        judge = r['judge']
        embed.add_field(
            name=r['title'] + " (" + r['diff'] + ")",
            value='-'.join(map(lambda k: str(judge[k]), ['great', 'good', 'bad', 'miss'])) + f' ({r["acc"]:.2f}%)'
        )
    await interaction.followup.send(embed=embed)

@bot.event
async def on_ready():
    rst = await bot.tree.sync(guild=None)
    data.Musics.load()
    print(f'ready. loaded {len(rst)} commands')

@bot.command()
async def sync(ctx: Context):
    msg = await ctx.reply(
        content='syncing...',
        allowed_mentions=discord.AllowedMentions.none()
    )
    await bot.tree.sync(guild=None)
    await msg.edit(
        content='synced!',
        allowed_mentions=discord.AllowedMentions.none()
    )

# @bot.event
# async def on_message(message: discord.Message):
#     atts = message.attachments
#     if len(atts) == 0 or message.author.bot: return
    
#     await Uploader(message).start()
