
class Config:
    def __init__(self):
        self.user = "zpzhong"
        self.datafile = "./data/anime-data.json"
        self.download_dir = "/data/share/qbittorrent"
        self.use_cache = True
        self.cache_dir = "./cache"


config = Config()
def get():
    return config

def set(cfg):
    global config
    config = cfg

