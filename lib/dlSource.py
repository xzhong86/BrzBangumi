
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

import trackers

UseCache = True
CacheDir = "./cache/"
Debug = False

def getUrlContent(url):
    md5str = hashlib.md5(url.encode()).hexdigest()
    cache_file = os.path.join(CacheDir, md5str)
    effictive_time = 600
    if (UseCache and os.path.isfile(cache_file)):
        mtime = os.path.getmtime(cache_file)
        fsize = os.path.getsize(cache_file)
        if (time.time() - mtime < effictive_time and fsize > 0):
            print("read from cache: ", cache_file)
            content = Path(cache_file).read_text()
            return content

    print("read url: ", url)
    req = requests.get(url)
    text = req.content

    if (UseCache and req.status_code == 200):
        print("write cache file: ", cache_file)
        Path(CacheDir).mkdir(parents=True, exist_ok=True)
        with open(cache_file, 'wb') as fh:
            fh.write(text)
            #fh.close()

    return text


def getRss(url):
    try:
        text   = getUrlContent(url)
        soup   = bs4.BeautifulSoup(text, "xml")
        items  = soup.channel.findAll('item', recursive=False)
        rss    = OpenStruct(soup=soup, items=items)
        rss.title = soup.title.text
        rss.link  = soup.link.text
        rss.version = soup.rss.get('version')
        return rss

    except Exception as e:
        print("Exception when get RSS: ", e)
        raise(e)

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

def getDlListUrl(url):
    rss = getRss(url)
    lst = []
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

def getList():
    rss_url = "https://mikanani.me/RSS/Classic"
    return getDlListUrl(rss_url)

def doTest():
    print("doTest")
    rss_url = "https://mikanani.me/RSS/Classic"
    rss = getRss(rss_url)
    dumpRss(rss)


