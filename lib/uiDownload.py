
import dlSource
from downloader import Downloader
from humanize import naturalsize

import pywebio
from pywebio.input import *
from pywebio.output import *


class DlPage:

    def __init__(self, scope):
        self.dl_list = dlSource.getList()
        self.dl = Downloader()
        self.scope = scope

    def doDownload(self, info):
        print("download for ", info.title, ", hash id: ", info.hashid)
        toast("Download " + info.title)  # message
        self.dl.download(info.magnet)

    def dlPage(self):
        for item in self.dl_list:

            def dl_func(it=item):  # get a closure function
                self.doDownload(it)

            button = put_button("download", onclick=dl_func)
            size = naturalsize(item.download.length, binary=True)
            put_row([
                put_text(item.title),
                put_text(size),
                button
            ], size='7fr 1fr 2fr')

        return

    def main(self):
        with use_scope(self.scope, clear=True):
            self.dlPage()

        return

