
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
        for ani in anin.getAnimeList():
            kws = ani['keywords']
            put_row([
                put_text(ani['name']),
                put_text(','.join(kws))
            ])


    def main(self):
        with use_scope(self.scope, clear=True):
            self.infoPage()
