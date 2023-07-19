
import re
import hashlib
from utils import database
from utils import config
from utils import misc

def get_str_hash(_str, len = 8):
    hash_str = hashlib.md5(_str.encode('utf-8')).hexdigest()
    len = 16 if len > 16 else len
    len = 8  if len < 8  else len
    return hash_str[0:len]

IndexPatterns = [ r'\[(\d\d)(v\d)?(集)?\]', r'\s(\d\d)(v\d)?\s*(\[|\()' ]
IndexRePats  = [ re.compile(pat) for pat in IndexPatterns ]
def guess_anime_index(string):
    for re_pat in IndexRePats:
        m = re_pat.search(string)
        if m:
            return m[1]  # return string
    return None


class Attr:
    def __init__(self, key, desc, default):
        self.key, self.desc, self.default = key, desc, default

class AnimeInfo:
    def __init__(self, name):
        self.attrs = [
            Attr('name',   'anime name', ''),
            Attr('bgm_id', 'bangumi.tv id', 0),
            Attr('mk_id',  'mikan id', 0),
            Attr('kwds',   'key words', []),
            Attr('season', 'season', '2023-Q3')
        ]
        self.attr_keys = [ a.key for a in self.attrs ]
        self.attr_dict = { a.key : a for a in self.attrs }

        for attr in self.attrs:
            setattr(self, attr.key, attr.default)

        self.name = name
        self.hash_id = get_str_hash(name, 12)

        self.files = []

    def transAttrValue(self, name, value):
        atype = type(getattr(self, name))
        if atype == str:
            return value
        elif atype == int:
            return int(value) if value else 0
        elif atype == list:
            if type(value) == str:
                return misc.splitStr(value, ',')
            else:
                return value
        else:
            raise "bad type"

    def setAttr(self, name, _value):
        if getattr(self, name) == _value:
            return

        value = self.transAttrValue(name, _value)
        setattr(self, name, value)

        if (name == 'name' and value):
            self.hash_id = get_str_hash(value, 12)

    def matchKeyWords(self, string):
        for kw in self.kwds:
            #if kw and kw in string:
            #    return True
            if misc.keywordMatch(kw, string):
                return True

        return False

    def guessIndex(self, string):
        return guess_anime_index(string)

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

    def findAnimeById(self, hash_id):
        for ani in self.animes:
            if ani.hash_id == hash_id:
                return ani

        return None

    def findAnimeByKwds(self, string):
        for ani in self.animes:
            if ani.matchKeyWords(string):
                return ani

        return None

    def saveData(self):
        udata = {}
        for ani in self.animes:
            data = ani.getData()
            udata[ani.hash_id] = data
        print("save data...")
        self.db.saveUserData(udata)


glb_opened_am = {}
def getManager(_user = None):
    global glb_opened_am
    user = _user or config.get().user
    am = glb_opened_am.get(user)
    if not am:
        am = AnimeManager(user)
        glb_opened_am[user] = am
    return am

def saveAllOpened():
    for user,am in glb_opened_am.items():
        am.saveData()
