import json
from discord.ext import commands
from plugins import Container, Context
from shlex import split
import sys
import time

# Read Settings
with open('./settings.json', 'r') as f:
    setting = json.load(f)

# Init
bot = commands.Bot(command_prefix='!')
bot.remove_command('help')
sys.path.append('.')
plugins = Container()

global starttime
starttime = 0

@bot.event
async def on_ready():
    global starttime
    channel = bot.get_channel(setting["MainChannel"])
    plugins.load('admin')
    if starttime == 0:
        await channel.send("```>> Server Manager is Online <<```")
        starttime += 1

@bot.event
async def on_message(ctx):
    raw_ctx = ctx
    ctx = Context(ctx)
    print(ctx.author, ':', ctx.content)
    channel = bot.get_channel(setting["MainChannel"])
    called = 0
    if ctx.author in setting["IgnoreNames"]:
        return
    await plugins.call(channel=channel, ctx=ctx, bot=bot, args=split(ctx.content), globals=locals(), plugins=plugins)




if __name__ == '__main__':
    time.sleep(5)
    bot.run(setting["BotToken"])
