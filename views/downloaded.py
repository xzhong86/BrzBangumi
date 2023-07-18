
import os
import pywebio
from pywebio.pin import  *
from pywebio.input import  *
from pywebio.output import  *
from pywebio.session import local as web_local

from functools import partial

from views import anime_info
from views import home
from utils import anime
from utils import file_manager


@use_scope('main', clear=True)
def downloaded_page():
    ani_man = anime.getManager(web_local.user)
    res = file_manager.scan_files(ani_man)

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
