from plugins import Plugin
from plugins import Context
from plugins import Container
from plugins import channel
from plugins import HelpDoc
from discord.ext.commands.bot import Bot
import sys

admins = [] # Put Admin names here

class Admin(Plugin):
    async def on_call(self, channel:channel, ctx: Context, bot:Bot, args: list, globals:list, plugins:Container) -> None:
        channel = ctx.channel
        if ctx.author not in admins:
            await channel.send(f"Sorry, you have no permission to execute this command")
            return
        try:
            if args[0] == 'help':
                helpdoc = HelpDoc(self.prefix)
                helpdoc.add('load <module_name>')
                helpdoc.add('unload <module_name>')
                helpdoc.add('post <channel_id> <information>')
                helpdoc.add('stop')
                helpdoc.add('plugins')
                await channel.send(str(helpdoc))
            # elif args[0] == 'test':
            #     await channel.send(f"ctx: {globals['raw_ctx'].author.id}")
            elif args[0] == 'post':
                if args[1] == 'help':
                    await channel.send(f"`post <channel_id> <information>`")
                try:
                    int(args[1])
                    if int(args[1]) != eval(args[1]):
                        return
                except:
                    return
                try:
                    channel = bot.get_channel(int(args[1]))
                    await channel.send(args[2])
                except:
                    pass
            elif args[0] == 'load':
                try:
                    if len(args) != 2:
                        await channel.send(f"`load <module_name>`")
                    elif plugins.load(args[1]):
                        await channel.send(f"Successfully loaded {args[1]}")
                    else:
                        await channel.send(f"Failed to load {args[1]}")
                except Exception as exc:
                    await channel.send(f"Failed to load {args[1]} ({exc})")
            elif args[0] == 'unload':
                if len(args) != 2:
                    await channel.send(f'`unload <module_name>`')
                elif args[1] not in plugins.list():
                    await channel.send(f'Module "{args[1]}" is not loaded')
                else:
                    plugins.unload(args[1])
            elif args[0] == 'plugins':
                await channel.send(plugins.info())

            elif args[0] == 'stop':
                await channel.send(f"Server Manager is offline")
                sys.exit(0)

        except IndexError:
            pass
module = Admin('admin')
