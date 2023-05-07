
from AnimeInfo import AnimeInfo

import pywebio
from pywebio.input import *
from pywebio.output import *

class AniPage:

    def __init__(self, scope):
        self.scope = scope

        self.anin = AnimeInfo()

    def getFuncScope(self, func):
        def fun(o=self, f=func):
            with use_scope(o.scope, clear=True):
                f()
        return fun

    def aniAddOrEdit(self, anin):
        grp = input_group("Add Anime Info",
                          [
                              input("Name", name='name'),
                              input("Keywords", name='kws')
                          ])
        print(grp['name'], grp['kws'])
        self.infoPage()

    def infoPage(self):
        anin = self.anin

        def ani_add(anin=anin):
            with use_scope(self.scope, clear=True):
                self.aniAddOrEdit(anin)

        put_button("Add", onclick=ani_add)
        #  padding: 6px 0px;
        item_style = "border: 2px solid; border-radius: 15px; margin-top: 10px;"
        #item_style = "outline-style: solid; outline-width: thick; margin-top: 10px; border-radius: 15px;"
        for ani in anin.getAnimeList():
            kws = ani['keywords']
            put_row([
                put_column([
                    put_row([
                        put_text("番剧名").style("font-weight:bold; margin-left: 10px"),
                        put_text(ani['name'])
                    ], size="1fr 4fr"),
                    put_row([
                        put_text("keywords").style("margin-left: 10px"),
                        put_text(','.join(kws))
                    ], size="1fr 4fr")
                ]),
                put_button("Edit", onclick=lambda: toast("edit")).style("center")
            ]).style(item_style)


    def main(self):
        with use_scope(self.scope, clear=True):
            self.infoPage()
