
from downloader import Downloader
from humanize import naturalsize

import pywebio
from pywebio.output import *

class WebUI:

    def __init__(self):
        self.dl = Downloader()

    def setDlList(self, lst):
        self.dl_list = lst


    def doDownload(self, info):
        print("download for ", info.title)
        toast("Download " + info.title)  # message
        self.dl.download(info.download.url)


    def dlPage(self):
        for item in self.dl_list:
            size = naturalsize(item.download.length, binary=True)
            #dl_func = lambda : self.doDownload(item)
            def dl_func(ui=self, it=item):
                ui.doDownload(it)
                
            put_table([
                ['Title', item.title],
                ['Url',   item.download.url],
                ['Size',  size],
                ['Download', put_button("download", onclick=dl_func)]
            ])


    def start(self, cfg):
        port = cfg['port'] or 8123
        ui_func = lambda : self.dlPage()
        pywebio.start_server(ui_func, port=port, debug=True)

