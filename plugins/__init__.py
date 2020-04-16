from discord import channel
from discord.ext.commands import bot
from importlib import import_module
from importlib import reload
import json

with open("settings.json") as f:
    settings = json.load(f)


class Context:
    def __init__(self, ctx):
        self.channel = ctx.channel
        self.author = str(ctx.author.name)
        self.author_id = str(ctx.author.id)
        self.server = str(ctx.guild)
        self.content = str(ctx.content)
        self.id = str(ctx.id)
        self.mention_everyone = str(ctx.mention_everyone)
        self.mentions = str(ctx.mentions)
        self.type = str(ctx.type)


class Container:
    def __init__(self):
        self.__plugins = dict()

    def load(self, name:str) -> bool:
        try:
            module = import_module(name=f"plugins.{name}")
            if name in self.__plugins:
                module = reload(module=module)
            if 'module' not in dir(module):
                print(f"Failed to load {name} (object 'module' not found)")
                return False
            module = module.module
            if issubclass(Plugin, type(module)):
                print(f"Failed to load {name} (invalid type of module)")
                return False

            self.__plugins[name] = module
            print(f"Plugin {name} successfully loaded")
            return True
        except ModuleNotFoundError:
            print(f"Failed to load {name} (name of module not found)")
            return False

    async def call(self, channel:channel, ctx: Context, bot: bot.Bot, args: list, globals, plugins):
        if ctx.author in settings['IgnoreNames']:
            return True
        for name in self.__plugins:
            if args[0] == self.__plugins[name].prefix:
                await self.__plugins[name].on_call(channel=channel, ctx=ctx, bot=bot, args=args[1:], globals=globals, plugins=self)
                return True
        return False

    def unload(self, name:str):
        del self.__plugins[name]

    def list(self) -> list:
        return [name for name in self.__plugins]

    def info(self):
        output = '```'
        for name in self.__plugins:
            output += f'{name}({self.__plugins[name].ver})\n'
        return output[:-1]+'```'

class HelpDoc:
    def __init__(self, name):
        self.__name = name
        self.__list = []

    def add(self, row:str):
        self.__list.append(row)

    def __str__(self):
        result = f"```Help for '{self.__name}' \n"
        for row in self.__list:
            result += f" - {row}\n"
        return result[:-1] + '```'

class Plugin:
    def __init__(self, prefix, ver='1.0') -> None:
        self.prefix = prefix
        self.ver = ver

    async def on_call(self, channel:channel, ctx: Context, bot:bot.Bot, args: list, globals:list, plugins:Container) -> None:
        await channel.send(f"Plugin with Prefix {self.prefix} was called")