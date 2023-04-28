

from uiDownload import DlPage
from uiAnime import AniPage

import pywebio
from pywebio.input import *
from pywebio.output import *

class WebUI:

    def __init__(self):
        self.dl_ins   = DlPage("body")
        self.dl_page  = lambda : self.dl_ins.main()
        self.ani_ins  = AniPage("body")
        self.ani_page = lambda : self.ani_ins.main()
        return

    def aniMain(self):
        pywebio.session.set_env(output_max_width="80%")
        put_column([put_scope("head"), put_scope("body")],
                   size="100px minmax={800px}")

        with use_scope("head"):
            put_row([
                put_button("Anime", onclick=self.ani_page),
                put_button("Download", onclick=self.dl_page),
                None
            ], size="1fr 1fr 9fr")

        self.dl_page()


    def start(self, cfg):
        port = cfg['port'] or 8123
        ui_func = lambda : self.aniMain()
        pywebio.start_server(ui_func, port=port, debug=True)

