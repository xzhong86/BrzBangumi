
import os
import pywebio
from pywebio.pin import  *
from pywebio.input import  *
from pywebio.output import  *
from pywebio.session import local as web_local

from functools import partial
from more_itertools import batched

from views import downloaded
from views import anime_info
from views import resource
from utils import anime
from utils import config

glb_ani_man = None

def view():
    pywebio.session.set_env(output_max_width="80%")

    put_column([put_scope("menu"), None, put_scope("main")],
               size="40px 10px auto")

    global glb_ani_man
    user = config.get().user  # fixme
    web_local.user = user
    web_local.ani_man = anime.getManager(user)
    glb_ani_man = web_local.ani_man
    main_menu()
    home_page()

@use_scope("menu")
def main_menu():
    put_row([
        put_button("Home", home_page),
        put_button("Downloaded", downloaded.downloaded_page),
        put_button("Resource", resource.resource_page)
    ])

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
    edit_page = partial(anime_info.show_edit_anime,
                        dict(anime=ani, callback=home_page))
    brief = put_row([
        put_text("Picture"),
        put_column([
            put_text(ani.name),
            put_text(f"bangumi.tv {ani.bgm_id}, mikan {ani.mk_id}"),
            put_text("key words: " + ', '.join(ani.kwds)),
        ]),
        put_column([
            put_button("Edit", onclick=edit_page),
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
    ani = anime.AnimeInfo(pin.anime_name.strip())
    for item in ani.attr_keys:
        ani.setAttr(item, pin['anime_' + item])

    glb_ani_man.add(ani)
    glb_ani_man.saveData()
    close_popup()
    home_page()

