
import os

class Config:
    def __init__(self):
        self.user = "zpzhong"
        self.datadir  = "./data"
        self.datafile = self.inDataDir("anime-data.json")
        self.download_dir = "/data/share/qbittorrent"
        self.anime_dir = "/data/share/anime"
        self.use_cache = True
        self.cache_dir = "./cache"
        self.do_test = False

    def inDataDir(self, path):
        return os.path.join(self.datadir, path)

    def getDataPath(self, path = None):
        if path:
            return self.inDataDir(path)
        return self.datadir


config = Config()
def get():
    return config

def set(cfg):
    global config
    config = cfg

