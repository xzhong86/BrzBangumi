
import hashlib
from utils import database
from utils import config

def get_str_hash(_str, len = 8):
    hash_str = hashlib.md5(_str.encode('utf-8')).hexdigest()
    len = 16 if len > 16 else len
    len = 8  if len < 8  else len
    return hash_str[0:len]

class Attr:
    def __init__(self, key, desc, default):
        self.key, self.desc, self.default = key, desc, default

class AnimeInfo:
    def __init__(self, name):
        self.attrs = [
            Attr('name',   'anime name', ''),
            Attr('bgm_id', 'bangumi.tv id', 0),
            Attr('mk_id',  'mikan id', 0),
            Attr('kwds',   'key words', [])
        ]
        self.attr_keys = [ a.key for a in self.attrs ]
        self.attr_dict = { a.key : a for a in self.attrs }

        for attr in self.attrs:
            self.setAttr(attr.key, attr.default)

        self.setAttr('name', name)

    def setAttr(self, name, value):
        setattr(self, name, value)
        if (name == 'name' and value):
            self.hash_id = get_str_hash(value, 12)

    def getData(self):
        return { item : getattr(self, item) for item in self.attr_keys }

    def loadData(self, data):
        for item in self.attr_keys:
            default = self.attr_dict[item].default
            self.setAttr(item, data.get(item) or default)


class AnimeManager:
    def __init__(self, user):
        self.user = user
        self.db = database.init(config.get().datafile, user)
        self.animes = []
        self.initAnimes()

    def initAnimes(self):
        udata = self.db.getUserData()
        for key, info in udata.items():
            name = info['name']
            ani  = AnimeInfo(name)
            ani.loadData(info)
            self.animes.append(ani)

    def add(self, ani):
        self.animes.append(ani)

    def saveData(self):
        udata = {}
        for ani in self.animes:
            data = ani.getData()
            udata[ani.hash_id] = data
        print("save data...")
        self.db.saveUserData(udata)


def getManager(_user = None):
    user = _user or config.get().user
    return AnimeManager(user)

