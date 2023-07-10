
import hashlib
from utils import database
from utils import config

def get_str_hash(_str, len = 8):
    hash_str = hashlib.md5(_str.encode('utf-8')).hexdigest()
    len = 16 if len > 16 else len
    len = 8  if len < 8  else len
    return hash_str[0:len]

class AnimeInfo:
    def __init__(self, name):
        self.name = name
        self.hash_id = get_str_hash(name, 12)

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
            self.animes.append(ani)

    def add(self, ani):
        self.animes.append(ani)

    def saveData(self):
        udata = {}
        for ani in self.animes:
            data = dict(name=ani.name, hash_id=ani.hash_id)
            udata[ani.hash_id] = data
        print("save data...")
        self.db.saveUserData(udata)


def getManager(_user = None):
    user = _user or config.get().user
    return AnimeManager(user)

