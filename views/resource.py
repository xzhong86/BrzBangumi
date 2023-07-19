
import os
import pywebio
#from pywebio.pin import  *
#from pywebio.input import  *
from pywebio.output import  *
from pywebio.session import local as web_local
from humanize import naturalsize

from utils.resource import mikan_rss

@use_scope("main", clear=True)
def resource_page():
    am = web_local.ani_man

    items = []
    dl_lst = mikan_rss.getList()
    for info in dl_lst:
        size = naturalsize(info.download.length, binary=True)
        tab = put_table([
            ["Item", "Value"],
            ["title", info.title],
            ["pubdate", info.pdate],
            ["link", info.link],
            ["size", size],
            ["download url", info.download.url]
        ])
        items.append(tab)

    put_column(items)

