import re

class Map():
    def __init__(self, client, id, name, gpm, size):
        self.__client = client
        self.id = id
        self.name = name
        self.gpm = gpm
        self.size = size

    def __repr__(self):
        return "Map(name=%s, gpm=%s, size=%s)" % (self.name, self.gpm, self.size)

    def run(self):
        self.__client.rcon_invoke("exec admin.nextLevel %s" % self.id)
        result = self.__client.rcon_invoke("exec admin.runNextLevel")
        return result

    def set_next(self):
        result = self.__client.rcon_invoke("exec admin.nextLevel %s" % self.id)
        return result

    def remove(self):
        result = self.__client.rcon_invoke("exec mapList.remove %s" % self.id)
        return result

    def __str__(self):
        return self.name

    def __int__(self):
        return self.id

class MapList():
    def __init__(self, client):
        self.__client = client

    def __load(self):
        data = self.__client.rcon_invoke("exec maplist.list")
        list = {}
        pattern = re.compile(r'(\d+): "(\S*?)" (\S*) (\d+)')
        for map in data.split("\n"):
            matches = pattern.findall(map)
            if len(matches) != 0:
                mapID = int(matches[0][0])
                list[mapID] = Map(self.__client, mapID, matches[0][1], matches[0][2], matches[0][3])

        if len(list) < 1: return None
        return list

    @property
    def list(self):
        return self.__load()

    @property
    def total(self):
        return int(self.__client.rcon_invoke("exec mapList.mapCount"))

    @property
    def current(self):
        return self.list.get(int(self.__client.rcon_invoke("exec mapList.currentMap")))

    def clear(self):
        result = self.__client.rcon_invoke("exec mapList.clear")
        return result

    def remove(self, id: int):
        result = self.__client.rcon_invoke("exec mapList.remove %s" % id)
        return result

    def append(self, name: str, game_mode: str, size: int):
        result = self.__client.rcon_invoke("exec mapList.append \"%s\" %s %s" % (name, game_mode, size))
        return result

    def insert(self, id: int, name: str, game_mode: str, size: int):
        result = self.__client.rcon_invoke("exec mapList.insert %s \"%s\" %s %s" % (id, name, game_mode, size))
        return result

    def save(self):
        result = self.__client.rcon_invoke("exec mapList.save")
        return result