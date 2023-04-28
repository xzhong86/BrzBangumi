
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

    @use_scope("body", clear=True)
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
        ui_func = lambda : self.aniMain()
        pywebio.start_server(ui_func, port=port, debug=True)



    @use_scope("body", clear=True)
    def aniAddOrEdit(self, anin):
        grp = input_group("Add Anime Info",
                          [
                              input("Name", name='name'),
                              input("Keywords", name='kws')
                          ])
        print(grp['name'], grp['kws'])
        self.infoPage()

    @use_scope("body", clear=True)
    def infoPage(self):
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


    def aniMain(self):
        pywebio.session.set_env(output_max_width="80%")
        put_column([put_scope("head"), put_scope("body")],
                   size="100px minmax={800px}")

        with use_scope("head"):
            put_row([
                put_button("Anime", onclick=lambda : self.infoPage()),
                put_button("Download", onclick=lambda : self.dlPage()),
                None
            ], size="1fr 1fr 9fr")

        self.dlPage()





    def test(self, cfg):
        port = cfg['port'] or 8123
        ui_func = lambda : self.aniPage()
        pywebio.start_server(ui_func, port=port, debug=True)



