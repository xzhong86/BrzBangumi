
import pywebio
from pywebio.output import *

def clickTest():
    toast("clicked")

def dlPage(dl_list):
    for item in dl_list:
        put_table([
            ['Title', item.title],
            ['Url',   item.download.url],
            ['Download', put_button("download", onclick=clickTest)]
        ])

def webui(dl_list):
    dlPage(dl_list)


def start(dl_list, cfg):
    port = cfg['port'] or 8123
    ui = lambda : webui(dl_list)
    pywebio.start_server(ui, port=port, debug=True)

