
class Config:
    def __init__(self):
        self.datafile = "./data/anime-data.json"
        self.user = "zpzhong"
        self.download_dir = "/data/share/qbittorrent"


config = Config()
def get():
    return config

def set(cfg):
    global config
    config = cfg

