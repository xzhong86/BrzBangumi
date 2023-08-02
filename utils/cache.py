
import requests
import hashlib
import time
import os

from pathlib import Path
from utils import config


def getUrlContent(url, effective_time = 600):
    cfg = config.get()
    md5str = hashlib.md5(url.encode()).hexdigest()
    cache_file = os.path.join(cfg.cache_dir, md5str)

    if not effective_time:  # set to 1 year if None
        effective_time = 3600 * 24 * 365
    if (cfg.use_cache and os.path.isfile(cache_file)):
        mtime = os.path.getmtime(cache_file)
        fsize = os.path.getsize(cache_file)
        if (time.time() - mtime < effective_time and fsize > 0):
            print("read from cache: ", cache_file)
            content = Path(cache_file).read_text()
            return content

    print("read url: ", url)
    req = requests.get(url)
    text = req.content

    if (cfg.use_cache and req.status_code == 200):
        print(f"write cache file {cache_file} for {url}")
        Path(cfg.cache_dir).mkdir(parents=True, exist_ok=True)
        with open(cache_file, 'wb') as fh:
            fh.write(text)

    if req.status_code != 200:
        print(f"bad response code: {req.status_code} for {url}")
        return None

    return text

