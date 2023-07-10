
import os
import pywebio
from pywebio.pin import  *
from pywebio.input import  *
from pywebio.output import  *
from pywebio.session import local as web_local

from functools import partial
#from more_itertools import batched

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
    put_column(ani_items)

def put_anime_brief(ani):
    put_text(ani.name)

def show_add_anime():
    items = put_column([
        put_row([put_text("name"), put_input("anime_name")]),
        put_button("Submit", onclick=do_add_anime)
    ])
    popup("Add Anime Information:",
          items,
          size="normal")

def do_add_anime():
    name = pin.anime_name
    ani  = anime.AnimeInfo(name)
    glb_ani_man.add(ani)
    glb_ani_man.saveData()
    close_popup()
    home_page()
