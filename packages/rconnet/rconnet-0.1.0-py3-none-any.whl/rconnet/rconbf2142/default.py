from rconnet.tcpclient import TCPClient
from rconnet.settings import Settings
from rconnet.maplist import MapList
from rconnet.banmanager import BanManager
import re

class Player():
    def __init__(self, client, id, nick, key=None, address=None, port=None, **kwargs):
        self._client = client
        self.id = id
        self.nick = nick
        self.key = key
        self.address = address
        self.port = port
        for option, value in kwargs.items():
            setattr(self, option, value)

    def __int__(self):
        return self.id

    def __str__(self):
        return self.nick

    def kick(self):
        return self._client.rcon_invoke("exec admin.kickPlayer %s" % self.id)

    def ban(self, period="perm"):
        return self._client.rcon_invoke("exec admin.banPlayer %s %s" % (self.id, period))

    def ban_key(self, period="perm"):
        if self.key is None: raise Exception("The player %s does not have a key" % (self.id))
        return self._client.rcon_invoke("exec admin.banPlayerKey %s %s" % (self.id, period))

class Default(TCPClient):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.settings = Settings(self)
        self.maplist = MapList(self)
        self.banmanager = BanManager(self)

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if not self.is_closed():
            self.close()

    @property
    def users(self):
        return [user.replace(" ", "").split(":") for user in self.rcon_invoke("users").split("\n")[1:]]

    def __get_players(self):
        rawData = self.rcon_invoke('exec admin.listplayers')
        if rawData is None: return None
        pattern1 = re.compile(r'''^Id:\ +(\d+)\ -\ (.*?)\ is\ remote\ ip:\ (\d+\.\d+\.\d+\.\d+):(\d+)''', re.VERBOSE)
        pattern2 = re.compile(r'''(?:.*hash:\ (\w{32}))?''', re.VERBOSE)
        players = {}

        i = 0
        for line in rawData.split("\n"):
            if i == 0:
                matches = pattern1.findall(line)
                if len(matches) != 0:
                    p_id = int(matches[0][0])

                    players[p_id] = Player(self, p_id, matches[0][1], address=matches[0][2], port=matches[0][3])

            elif i == 1:
                matches = pattern2.findall(line)
                players[p_id].key = matches[0]

            i ^= 1

        if len(players) < 1: return None

        return players

    @property
    def players(self):
        return self.__get_players()

    def run_next_level(self):
        return self.rcon_invoke("exec admin.runNextLevel")

    def run_level(self, name: str, game_mode: str, size: int):
        return self.rcon_invoke("exec admin.runLevel %s %s %s" % (name, game_mode, size))

    def current_level(self):
        return self.rcon_invoke("exec admin.currentLevel")

    def set_next_level(self, id: int):
        return self.rcon_invoke("exec admin.nextLevel %s" % id)

    def restart_map(self):
        return self.rcon_invoke("exec admin.restartMap")

    def say(self, message):
        return self.rcon_invoke("exec game.sayall \"%s\"" % message)