
from downloader import Downloader
from humanize import naturalsize

import AnimeInfo

import pywebio
from pywebio.input import *
from pywebio.output import *

class WebUI:

    def __init__(self):
        self.dl = Downloader()

    def setDlList(self, lst):
        self.dl_list = lst


    def doDownload(self, info):
        print("download for ", info.title, ", hash id: ", info.hashid)
        toast("Download " + info.title)  # message
        self.dl.download(info.magnet)


    def dlPage_v0(self):
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

    def dlPage(self):
        for item in self.dl_list:
            size = naturalsize(item.download.length, binary=True)
            def dl_func(ui=self, it=item):  # get a closure function
                ui.doDownload(it)

            button = put_button("download", onclick=dl_func)
            put_row([
                put_text(item.title),
                put_text(size),
                button
            ], size='7fr 1fr 2fr')
        

    def start(self, cfg):
        port = cfg['port'] or 8123
        ui_func = lambda : self.dlPage()
        pywebio.start_server(ui_func, port=port, debug=True)



    @use_scope("ani-edit", clear=True)
    def aniAddOrEdit(self, anin):
        grp = input_group("Add Anime Info",
                          [
                              input("Name", name='name'),
                              input("Keywords", name='kws')
                          ])
        print(grp['name'], grp['kws'])

    @use_scope("ani-info", clear=True)
    def aniPage(self):
        anin = AnimeInfo.AnimeInfo()

        def ani_add(anin=anin):
            self.aniAddOrEdit(anin)

        put_button("Add", onclick=ani_add)
        for ani in anin.getAnimeList():
            kws = ani['keywords']
            put_row([
                put_text(ani['name']),
                put_text(','.join(kws))
            ])


    def test(self, cfg):
        port = cfg['port'] or 8123
        ui_func = lambda : self.aniPage()
        pywebio.start_server(ui_func, port=port, debug=True)



