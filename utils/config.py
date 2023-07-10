
class Config:
    def __init__(self):
        self.datafile = "./data/anime-data.json"
        self.user = "zpzhong"


config = Config()
def get():
    return config

def set(cfg):
    global config
    config = cfg

