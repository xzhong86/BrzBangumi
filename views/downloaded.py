
import os
import sys
import re
from os.path import basename
from datetime import datetime, timedelta

import pywebio
from pywebio.pin import  *
from pywebio.input import  *
from pywebio.output import  *
from pywebio.session import local as web_local

from functools import partial
from ostruct import OpenStruct

from views import anime_info
from views import home
from utils import config
from utils import anime

class FileInfo:
    def __init__(self, dirpath, filename):
        self.path = os.path.join(dirpath, filename)
        self.name = basename(filename)
        st = os.stat(self.path)
        self.time = datetime.fromtimestamp(st.st_mtime)

    def isfile(self):
        return os.path.isfile(self.path)

def get_files(ddir):
    files = []
    print(f"scan dir {ddir} ...")
    for file in os.listdir(ddir):
        fi = FileInfo(ddir, file)
        if fi.isfile():
            files.append(fi)

    re_ext = re.compile(r'.+\.(mp4|mkv)')
    for fi in files:
        if not re_ext.match(fi.name):
            files.remove(fi)

    files.sort(key=lambda fi: fi.time, reverse=True)
    return files

def dist_files(am, files):
    print(f"{len(files)} to distribute...")
    for ani in am.animes:
        ani.files = []  # clear
    res = OpenStruct(others=[], conflicts=[])
    for fi in files:
        belong = []
        for ani in am.animes:
            for kw in ani.kwds:
                if kw and kw in fi.name:
                    ani.files.append(fi)
                    belong.append(ani)
                    break
        #print(f"file: {fi.name}, belong={len(belong)}")
        if len(belong) == 0:
            res.others.append(fi)
        if len(belong) > 1:
            res.conflicts.append([fi, belong])

    for ani in am.animes:
        if len(ani.files) > 0:
            ani.update_time = ani.files[0].time
        else:
            ani.update_time = datetime.now() - timedelta(days=90)

    return res

@use_scope('main', clear=True)
def downloaded_page():
    ani_man = anime.getManager(web_local.user)
    files = get_files(config.get().download_dir)
    res = dist_files(ani_man, files)

    animes = ani_man.animes.copy()
    animes.sort(key=lambda a: a.update_time, reverse=True)
    put_markdown("## Animes")
    for ani in animes:
        timestr = ani.update_time.strftime("%Y-%m-%d")
        put_column([
            put_markdown(f"### {ani.name}"),
            put_text(f"last update: {timestr}"),
            put_collapse(f"{len(ani.files)} files:",
                         [ put_text(fi.name) for fi in ani.files ])
        ], size="0.3fr 0.3fr 1fr")

    put_markdown("## Conflicts")
    for info in res.conflicts:
        fi, animes = info
        put_markdown(" - " + fi.name)
        for ani in animes:
            put_markdown("   - " + ani.name)
    
    put_markdown("## Others")
    file_items = []
    for fi in res.others:
        item = [ fi.time.strftime("%Y-%m-%d"), fi.name,
                 put_button("Belong", onclick=partial(show_belong_pop, fi.name)) ]
        file_items.append(item)

    put_table([["Time", f"File ({len(file_items)})", "Action"]] + file_items)


def show_belong_pop(fname):
    am = anime.getManager(web_local.user)

    opts = [ dict(label=ani.name, value=ani.hash_id) for ani in am.animes ]
    web_local.cur_fname = fname

    popup("Update Anime Keyword Info",
          [
              put_text(fname),
              put_row([put_text("Keyword"), put_input("anime_keyword")], size="1fr 4fr"),
              put_row([put_text("Anime"), put_select("anime_select", options=opts)], size="1fr 4fr"),
              put_row([put_button("Add", onclick=do_add_anime), put_button("Update", onclick=do_belong_update)])
          ],
          size="normal")

def do_belong_update():
    hash_id = pin.anime_select
    keyword = pin.anime_keyword
    fname   = web_local.cur_fname
    if not keyword in fname:
        toast("Bad keyword not in file name")
        return

    am = anime.getManager(web_local.user)
    ani = am.findAnimeById(hash_id)
    ani.kwds.append(keyword)
    am.saveData()
    close_popup()
    downloaded_page()

def do_add_anime():
    opts = dict(keyword = pin.anime_keyword,
                fname = web_local.cur_fname,
                callback = downloaded_page)
    close_popup()
    anime_info.add_anime(opts)
