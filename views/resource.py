
import os
import pywebio
#from pywebio.pin import  *
#from pywebio.input import  *
from pywebio.output import  *
from pywebio.session import local as web_local
from humanize import naturalsize
from functools import partial
import itertools

from utils import file_manager
from utils import downloader
from utils.resource import mikan_rss

glb_downloader = None
def do_download(info):
    global glb_downloader
    if not glb_downloader:
        glb_downloader = downloader.get()

    glb_downloader.download(info.magnet)
    toast(f"download: {info.title}")

def show_file_list(ani):
    def time_str(dt):
        return dt.strftime("%y-%m-%d %H:%M")

    tbl = put_table([[ "time", "file" ]] +
                    [ [ time_str(fi.time) , fi.name] for fi in ani.files ])

    popup("Downloaded Files", [ tbl ], size="large")
    return

def show_download_list(dl_lst, am):
    info_list = []
    for info in dl_lst:
        ani = am.findAnimeByKwds(info.title)
        if ani:
            info.anime = ani
            files_idx = [ fi.index for fi in ani.files ]
            ani_idx = ani.guessIndex(info.title) or "XX"
            if ani_idx not in files_idx:
                info_list.append(info)

    web_items = []
    info_list.sort(key=lambda i: i.anime.name)
    for ani, grp_lst in itertools.groupby(info_list, lambda i: i.anime):
        #max_idx = max([fi.index for fi in ani.files]) if len(ani.files) > 0 else 0
        idx_lst = ",".join([ str(fi.index) for fi in ani.files ])
        cols = [ ]
        cols.append(put_row([
            put_text(f"{ani.name} - {idx_lst}"),
            None,
            put_button("list", onclick=partial(show_file_list, ani), small=True),
        ], size="auto auto auto"))
        for info in grp_lst:
            size = naturalsize(info.download.length, binary=True)
            cols.append(put_row([
                put_button("Download", onclick=partial(do_download, info), small=True),
                None,
                put_text(f"{size} {info.title}"),
            ], size="80px 10px auto"))
        content = put_column(cols)
        style(content, 'border: 1px solid; border-radius: 8px; padding: 4px; margin: 3px')
        web_items.append(content)

    put_column(web_items, size=" ".join(["auto" for n in web_items]))


def get_dl_list():
    lst = mikan_rss.getList(npage=2)
    if not lst:
        toast("failed, read from cache")
        lst = mikan_rss.getList(npage=2, read_cache=True)

    return lst

@use_scope("main", clear=True)
def resource_page():
    am = web_local.ani_man
    res = file_manager.scan_files(am)
    dl_lst = get_dl_list()

    if not dl_lst:
        put_error("Get Download resource failed.")
        return

    items = []
    show_download_list(dl_lst, am)

    put_markdown("## Others")
    for info in dl_lst:
        size = naturalsize(info.download.length, binary=True)
        ani = am.findAnimeByKwds(info.title)
        if not ani:
            ani_name = ani.name if ani else "unknown"
            ani_idx = ani and ani.guessIndex(info.title) or "XX"
            tab = put_table([
                ["Item", "Value"],
                ["title", info.title],
                ["info", f"{info.pdate}, {size}"],
                ["link", info.link],
                #["download url", info.download.url],
                ["anime", ani_name + " - " + str(ani_idx) ]
            ])
            items.append(tab)

    put_column(items, size=' '.join(['auto' for x in items]))

