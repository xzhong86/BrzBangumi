
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


def getRss(url, use_cache=False):
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
    try:
        dt = datetime.datetime.fromisoformat(dstr)
        return dt.timestamp()
    except:
        pass

    try:
        dt = datetime.strptime(dstr, "%Y-%m-%dT%H:%M:%S.%f")
        return dt.timestamp()
    except:
        pass

    return time.time()


def findHashId(info, item):
    regex = re.compile('([0-9a-f]{32,})')
    def getid(url, regex=regex):
        m = regex.search(url)
        return m and m[1]
    res = None
    if (info.download):
        res = getid(info.download.url)
    if (not res and item.link):
        res = getid(item.link)
    return res

def getDlListUrl(url, read_cache=False):
    rss = getRss(url, read_cache)
    lst = []
    if not rss:
        return None
    for item in rss.items:
        info = OpenStruct()
        info.title = item.title.text
        info.link  = item.link.text
        info.pdate = item.pubDate.text
        info.time  = strToTime(info.pdate)

        enclosure  = item.find('enclosure')
        if (enclosure):
            dl = OpenStruct()
            dl.dtype  = enclosure.get('type')
            dl.length = int(enclosure.get('length'))
            dl.url    = enclosure.get('url')
            info.download = dl
            lst.append(info)

        info.hashid = findHashId(info, item)
        info.magnet = trackers.getMagnet(info.hashid, 'mikan')

    return lst

def getList(npage=1, read_cache=False):
    lst = []
    rss_base = "https://mikanani.me/RSS/Classic"
    for index in range(1, npage+1):
        rss_url = f"{rss_base}/{str(index)}"
        res = getDlListUrl(rss_url, read_cache)
        if not res:
            return None
        lst = lst + res

    return lst


def doTest():
    print("doTest")
    rss_url = "https://mikanani.me/RSS/Classic"
    rss = getRss(rss_url)
    dumpRss(rss)


