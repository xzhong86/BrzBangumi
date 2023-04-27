
import os
import time
import datetime
import json
import yaml

class AnimeInfo:

    def __init__(self):
        tt   = time.time()
        date = datetime.datetime.fromtimestamp(tt)
        season = int(date.month / 4) + 1
        self.curr_season = str(date.year) + 'Q' + str(season)
        if season > 1:
            self.prev_season = str(date.year) + 'Q' + str(season - 1)
        else:
            self.prev_season = str(date.year - 1) + 'Q4'

        self.datafile = self.curr_season + ".json"

        use_test = True
        if os.path.isfile(self.datafile):
            fh = open(self.datafile)
            self.data = json.load(fh)
        elif use_test:
            self.data = yaml.load(open("test-data.yaml"))
        else:
            self.data = dict(season = self.curr_season, list = [])

    def getAnimeList(self):
        return self.data['list']

    def addOrUpdateInfo(self, info):
        name = info['name']
        kw   = info['keywords'] # fail if not exist
        lst  = self.data['list']
        found = False
        for ani in lst:
            if [ani['name'] == name]:
                ani['keywords'] = kw
                # other keys
                found = True
        if not found:
            lst += info

        return lst


    def removeInfo(self, name):
        new = [e for e in self.data['list'] if e['name'] != name]
        self.data['list'] = new
        return new

    def guessName(self, desc):
        for ani in self.data['list']:
            for kw in ani['keywords']:
                if desc.find(kw) >= 0:
                    return ani['name']
        return None

