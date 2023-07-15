
import os
import sys
import re
from os.path import basename

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

def get_files(ddir):
    files = []
    print(f"scan dir {ddir} ...")
    for file in os.listdir(ddir):
        path = os.path.join(ddir, file)
        if os.path.isfile(path):
            files.append(path)

    re_ext = re.compile(r'.+\.(mp4|mkv)')
    for file in files:
        if not re_ext.match(file):
            files.remove(file)

    return files

def dist_files(am, files):
    print(f"{len(files)} to distribute...")
    for ani in am.animes:
        ani.files = []  # clear
    res = OpenStruct(others=[], conflicts=[])
    for file in files:
        belong = []
        for ani in am.animes:
            for kw in ani.kwds:
                if kw and kw in file:
                    ani.files.append(file)
                    belong.append(ani)
                    break
        #print(f"file: {file}, belong={len(belong)}")
        if len(belong) == 0:
            res.others.append(file)
        if len(belong) > 1:
            res.conflicts.append([file, belong])
    return res

@use_scope('main', clear=True)
def downloaded_page():
    ani_man = anime.getManager(web_local.user)
    files = get_files(config.get().download_dir)
    res = dist_files(ani_man, files)

    for ani in ani_man.animes:
        put_column([
            put_text(ani.name),
            put_collapse(f"{len(ani.files)} files:",
                         [ put_text(basename(f)) for f in ani.files ])
        ], size="0.3fr 1fr")

    put_markdown("## Conflicts")
    for info in res.conflicts:
        file, animes = info
        put_markdown(" - " + file)
        for ani in animes:
            put_markdown("   - " + ani.name)
    
    put_markdown("## Others")
    file_items = []
    for file in res.others:
        fname = basename(file)
        item = [ fname,
                 put_button("Belong", onclick=partial(show_belong_pop, fname)) ]
        file_items.append(item)

    put_table([[f"File ({len(file_items)})", "Action"]] + file_items)


def show_belong_pop(fname):
    am = anime.getManager(web_local.user)

    opts = [ dict(label=ani.name, value=ani.hash_id) for ani in am.animes ]
    #edit_anime = anime_info.show_edit_anime
    #ani_tbl = [["Anime", "Edit"]]
    #ani_tbl += [
    #    [ani.name, put_button("Edit", onclick=partial(edit_anime, ani))] for ani in ani_man.animes
    #]
    #pop_tbl = put_table(ani_tbl)
    web_local.cur_fname = fname
    #add_anime = home.show_add_anime
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

def do_add_anime():
    opts = dict(keyword = pin.anime_keyword,
                fname = web_local.cur_fname,
                callback = downloaded_page)
    close_popup()
    anime_info.add_anime(opts)
