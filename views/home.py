
import os
import pywebio
from pywebio.pin import  *
from pywebio.input import  *
from pywebio.output import  *
from pywebio.session import local as web_local

from functools import partial
from more_itertools import batched

from utils import anime

glb_ani_man = None

def view():
    pywebio.session.set_env(output_max_width="80%")

    put_column([put_scope("menu"), None, put_scope("main")],
               size="1fr 0.3fr 13fr")

    global glb_ani_man
    glb_ani_man = anime.getManager()
    home_page()

@use_scope("main", clear=True)
def home_page():
    put_row([
        put_button("Add", onclick=show_add_anime)
    ])
    anime_list = glb_ani_man.animes
    ani_items = [ put_anime_brief(ani) for ani in anime_list ]
    #put_column(ani_items)
    put_column([
        put_row(r) for r in batched(ani_items, 2)
    ])

def put_anime_brief(ani):
    brief = put_row([
        put_text("Picture"),
        put_column([
            put_text(ani.name),
            put_text(f"bangumi.tv {ani.bgm_id}, mikan {ani.mk_id}"),
            put_text("key words: " + ', '.join(ani.kwds)),
        ]),
        put_column([
            put_button("Edit", onclick=lambda:toast("edit")),
        ])
    ], size="1fr 4fr 1fr")
    style(brief, 'border: 1px solid; border-radius: 8px; padding: 5px; margin: 4px')
    return brief

def show_add_anime():
    ani = anime.AnimeInfo("dummy")
    ani_items = [
        [attr.desc, put_input('anime_' + attr.key)] for attr in ani.attrs
    ]
    tbl_items = [ ["Item", "Detials" ] ]
    tbl_items = tbl_items + ani_items
    items = put_column([
        put_table(tbl_items),
        put_button("Submit", onclick=do_add_anime)
    ])
    popup("Add Anime Information:",
          items,
          size="normal")

def do_add_anime():
    ani = anime.AnimeInfo(pin.anime_name)
    for item in ani.attr_keys:
        ani.setAttr(item, pin['anime_' + item])

    glb_ani_man.add(ani)
    glb_ani_man.saveData()
    close_popup()
    home_page()
