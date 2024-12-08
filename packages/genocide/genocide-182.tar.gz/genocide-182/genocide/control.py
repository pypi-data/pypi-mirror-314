# This file is placed in the Public Domain.
# pylint: disable=C0115,C0116,C0415,R0903,R0912,R0915,W0105,W0718,E0402


"main"


import sys


from .object  import Config, parse
from .persist import NAME
from .runtime import Client, Commands, Event, errors, later, scan, wrap


Cfg  = Config()


class CLI(Client):

    def __init__(self):
        Client.__init__(self)
        self.register("command", command)

    def raw(self, txt):
        print(txt)


def command(bot, evt):
    parse(evt, evt.txt)
    if "ident" in dir(bot):
        evt.orig = bot.ident
    func = Commands.cmds.get(evt.cmd, None)
    if func:
        try:
            func(evt)
            bot.display(evt)
        except Exception as ex:
            later(ex)
    evt.ready()


def wrapped():
    wrap(main)
    for line in errors():
        print(line)


def srv(event):
    import getpass
    name = getpass.getuser()
    event.reply(TXT % (NAME.upper(), name, name, name, NAME))


def main():
    Commands.add(srv)
    parse(Cfg, " ".join(sys.argv[1:]))
    from .modules import face
    scan(face)
    evt = Event()
    evt.type = "command"
    evt.txt = Cfg.otxt
    csl = CLI()
    command(csl, evt)
    evt.wait()


TXT = """[Unit]
Description=%s
After=network-online.target

[Service]
Type=simple
User=%s
Group=%s
ExecStart=/home/%s/.local/bin/%ss

[Install]
WantedBy=multi-user.target"""


if __name__ == "__main__":
    wrapped()
