
#from rss_parser import Parser
from pathlib import Path
from ostruct import OpenStruct

import requests
import datetime
import hashlib
import time
import bs4
import os
import re

from utils import config
from utils import trackers
from utils import cache
from utils import LinkList


def getRssInfo(url, use_cache=False):
    try:
        text   = cache.getUrlContent(url, None if use_cache else 600)
        if not text:
            return None
        soup   = bs4.BeautifulSoup(text, "xml")
        items  = soup.channel.findAll('item', recursive=False)
        rss    = OpenStruct(soup=soup, items=items)
        rss.title = soup.title.text
        rss.link  = soup.link.text
        rss.version = soup.rss.get('version')
        return rss

    except Exception as e:
        print("Exception when get RSS: ", e)
        return None

def dumpRss(rss):
    dump_num = 5
    print("RSS title: ", rss.title)
    print("RSS version: ", rss.version)
    for item in rss.items[:dump_num]:
        print("title: ", item.title)
        #print(list(filter(lambda s: s[0] != '_', dir(item))))

def strToTime(dstr):
    def trySafe(dstr, fn):
        try: return fn(dstr)
        except: pass
        return None
    dt =       trySafe(dstr, lambda s: datetime.datetime.fromisoformat(s))
    dt = dt or trySafe(dstr, lambda s: datetime.strptime(s, "%Y-%m-%dT%H:%M:%S.%f"))
    return dt and dt.timestamp() or time.time()

def findHashId(info, item):
    regex = re.compile('([0-9a-f]{32,})')
    def getid(url, regex=regex):
        m = regex.search(url)
        return m and m[1]
    return info.link and getid(info.link)

def getDlInfo(item):   # rss item
    info = OpenStruct()
    info.title = item.title.text
    info.link  = item.link.text
    info.pdate = item.pubDate.text

    enclosure  = item.find('enclosure')
    info.length = int((item.contentLength and item.contentLength.text)
                      or (enclosure and enclosure.get('length'))
                      or '100000000')

    if not info.link and enclosure:
        info.link = enclosure.get('url')

    if not info.pdate:
        info.pdate = datetime.now().isoformat()

    return info

def getDlListUrl(url, read_cache=False):
    rss = getRssInfo(url, read_cache)
    if not rss:
        return None

    lst = []
    for item in rss.items:
        info = getDlInfo(item)
        info.hashid = findHashId(info, item)

        if info.hashid:
            info.magnet = trackers.getMagnet(info.hashid, 'mikan')
            lst.append(info)

    return lst

def getRssUrl(index=1):
    rss_base = "https://mikanani.me/RSS/Classic"
    return f"{rss_base}/{str(index)}"

def getListRss(npage=1, read_cache=False):
    lst = []
    for index in range(1, npage+1):
        rss_url = getRssUrl(index)
        res = getDlListUrl(rss_url, read_cache)
        if not res:
            return None
        lst = lst + res

    return lst

def getList(nday=3):
    linklist = LinkList.LinkList()
    lst = getListRss(npage=2)
    if lst:
        links = [ LinkList.LinkInfo(e) for e in lst ]
        linklist.mergeLinks(links)
    return linklist.getList(nday)


def doTest():
    print("doTest")
    rss = getRssInfo(getRssUrl(1))
    dumpRss(rss)


