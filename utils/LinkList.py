
import os
import json
import itertools

import ostruct
from datetime import datetime, timedelta

from utils import config
from utils import misc
from utils import backup

def strToTime(dstr):
    def trySafe(dstr, fn):
        try: return fn(dstr)
        except: pass
        return None
    dt =       trySafe(dstr, lambda s: datetime.datetime.fromisoformat(s))
    dt = dt or trySafe(dstr, lambda s: datetime.strptime(s, "%Y-%m-%dT%H:%M:%S.%f"))
    dt = dt or trySafe(dstr, lambda s: datetime.strptime(s, "%Y-%m-%dT%H:%M:%S"))
    return dt

class LinkInfo:
    def __init__(self, info=None):
        self.attrs = [ 'title', 'link', 'pubdate', 'length', 'magnet' ]
        self.title = None
        self.link  = ""
        self.pubdate = None
        self.length  = 0
        self.magnet  = ""

        if type(info) is ostruct.OpenStruct:
            self.init_ost(info)
        elif type(info) is dict:
            self.init_dict(info)

        dt = strToTime(self.pubdate)
        self.pubdate = dt.isoformat()

    def init_ost(self, info):
        for attr in self.attrs:
            setattr(self, attr, getattr(info, attr))
        if not self.pubdate:
            self.pubdate = info.pdate

    def init_dict(self, info):
        for attr in self.attrs:
            setattr(self, attr, info[attr])

    def to_dict(self):
        return { k : getattr(self, k) for k in self.attrs }


class LinkList:
    def __init__(self):
        self.file_prefix = "linklist-"
        self.data_file = self.getDataFilePath()
        self.links = []
        self.initList()

    def getDataFilePath(self, dt = None):
        if not dt:
            dt = datetime.now()
        fname = dt.strftime(self.file_prefix + "%Y-%m.json")
        return config.get().getDataPath(fname)

    def isDataFile(self, path):
        fname = os.path.basename(path)
        return fname.startswith(self.file_prefix) and fname.endswith(".json")

    def initList(self):
        ddir = os.path.dirname(self.data_file)
        files = [ f for f in os.listdir(ddir) if self.isDataFile(f) ]
        files.sort(reverse=True)
        for fname in files[0:3]:
            path = os.path.join(ddir, fname)
            lst = misc.load_json(path)
            self.mergeLinks([ LinkInfo(i) for i in lst ])
        pass

    def saveList(self):
        links = self.links
        def monthStr(link):
            #dt = datetime.fromisoformat(link.pubdate)
            dt = strToTime(link.pubdate)
            return dt.strftime("%Y-%m")
        for ms, _glst in itertools.groupby(links, monthStr):
            glst  = list(_glst)
            dt    = datetime.fromisoformat(glst[0].pubdate)
            path  = self.getDataFilePath(dt)
            links = [ e.to_dict() for e in glst ]
            backup.check_and_backup(path, 4)
            misc.dump_json(path, links)


    def mergeLinks(self, links):
        links.sort(key=lambda e: e.pubdate)
        ncnt = 0

        if len(self.links) > 0:
            fst = self.links[0]
            for link in links:
                if fst.pubdate < link.pubdate:
                    self.links.insert(0, link)
                    ncnt += 1
                else:
                    break
        else:
            ncnt = len(links)
            self.links = list(reversed(links))

        if (ncnt > 0):
            self.saveList()

        pass

    def getList(self, ndays):
        timeline = datetime.now() - timedelta(days=ndays)
        timestr  = timeline.isoformat()
        lst = []
        for link in self.links:
            if link.pubdate > timestr:
                lst.append(link)
            else:
                break

        return lst

