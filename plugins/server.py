from plugins import Plugin
from plugins import Context
from plugins import Container
from plugins import channel
from plugins import HelpDoc
from discord.ext.commands.bot import Bot
from threading import Thread
from asyncio import sleep as delay
from mcrcon import MCRcon
import socket
import sys
from posts import get

addr = '0.0.0.0' # Post Service IP address


def status():
    s = get(addr, 'status')
    s = s.split()[-1].lower()
    return s if s != "staging" else 'starting'

class Server(Plugin):
    def __init__(self, prefix):
        super().__init__(prefix)
        self.status = status()

    async def shutdown(self, mc: MCRcon):
        def warn(sec):
            arg = str([
                {"text": "Server will be stopped in ", "color": "gold"},
                {"text": str(sec), "color": "red"},
                {"text": f" second{'s' if sec > 1 else ''}", "color": "gold"}
            ]).replace("'", '"')
            return f"tellraw @a {arg}"

        sound = """playsound minecraft:entity.chicken.egg music @a 0 0 0 10000 0.1"""

        mc.command("""title @a subtitle {"text":"in 15 seconds", "color":"red"}""")
        mc.command("""title @a title {"text":"Server will be closed", "color":"gold"}""")
        mc.command(warn(15))
        mc.command(sound)
        await delay(10)
        for i in range(5):
            mc.command(sound)
            mc.command(warn(5 - i))
            await delay(1)
        mc.command("""playsound minecraft:block.beacon.deactivate music @a 0 0 0 1000 2""")
        await delay(2)
        mc.command("stop")
        await delay(2)

    async def __stop_server(self, channel:channel, ctx:Context):
        self.status = 'stopping'
        try:
            s = socket.socket()
            s.settimeout(3)
            s.connect(("server address", 25565))
            s.close()
            mc = MCRcon('server address', '**********')
            mc.connect()
            await self.shutdown(mc)
            mc.disconnect()
        except:
            await channel.send('> :warning: **Couldn\'t connect to mc-server. Shutting down directly**')
        thread = Thread(target=get, args=(addr, 'shutdown'))
        thread.start()
        await channel.send(
            "> :octagonal_sign: **Stopping server**"
        )
        while thread.is_alive():
            await delay(0.5)
        await channel.send('> :octagonal_sign: **Server is stopped**')
        self.status = 'terminated'

    async def on_call(self, channel: channel, ctx: Context, bot: Bot, args: list, globals: list,
                      plugins: Container) -> None:
        channel = ctx.channel
        if args[0] == 'help':
            helpdoc = HelpDoc(self.prefix)
            helpdoc.add('status')
            helpdoc.add('start')
            helpdoc.add('stop')
            await channel.send(helpdoc)

        elif args[0] == 'status':
            s = status()
            self.status = s
            await channel.send(
                f"> :{'white_check_mark' if s in ('running', 'starting') else 'octagonal_sign'}: **Server is {s}**"
            )

        elif args[0] == 'start':
            s = status()
            self.status = s
            if s == 'running' or self.status == 'running':
                await channel.send(
                    '> :warning: **Server is already started**'
                )
            elif s == 'stopping' or self.status == 'running':
                await channel.send(
                    '> :warning: **You can\'t start the server while it\'s stopping**'
                )
            else:
                await channel.send(
                    "> :white_check_mark: **Yep, server is starting..**"
                )
                Thread(target=get, args=(addr, 'start')).start()
                self.status = 'running'
        elif args[0] == 'stop':
            s = status()
            if s == 'terminated':
                await channel.send(
                    '> :warning: **Server is already stopped**'
                )
            elif s == 'stopping':
                await channel.send(
                    '> :warning: **Server is stopping**'
                )
            else:
                bot.loop.create_task(self.__stop_server(channel=channel, ctx=ctx))


module = Server('server')

