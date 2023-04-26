
from rss_parser import Parser
from pathlib import Path
import requests
import hashlib
import time
import os

UseCache = True
CacheDir = "./cache/"

def getUrlContent(url):
    md5str = hashlib.md5(url.encode()).hexdigest()
    cache_file = os.path.join(CacheDir, md5str)
    if (UseCache and os.path.isfile(cache_file)):
        mtime = os.path.getmtime(cache_file)
        fsize = os.path.getsize(cache_file)
        if (time.time() - mtime < 600 and fsize > 0):
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
        parser = Parser(xml=text, limit=1000)
        #xml    = requests.get(url)
        #parser = Parser(xml=xml.content, limit=1000)
        feed   = parser.parse()
        return feed
    except Exception as e:
        print(e)

def dumpRss(rss):
    dump_num = 5
    print("RSS language: ", rss.language)
    print("RSS version: ", rss.version)
    #print(type(rss.feed))
    for item in rss.feed[:dump_num]:
        print("title: ", item.title)
        #print(dir(item))


def doTest():
    print("doTest")
    rss_url = "https://mikanani.me/RSS/Classic"
    rss = getRss(rss_url)
    dumpRss(rss)


