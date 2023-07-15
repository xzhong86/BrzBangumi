
from pywebio.pin import  *
from pywebio.input import  *
from pywebio.output import  *
from pywebio.session import local as web_local

from functools import partial

from utils import anime

def put_season_select(ani):
    from datetime import datetime
    dt = datetime.now()
    opts = []
    for year in range(dt.year-3, dt.year+1):
        opts = opts + [ f"{year}-Q{n}" for n in range(1, 5) ]
    cur_season = int((dt.month - 1) / 3) + 1   # 1-4
    for n in range(0, 4 - cur_season):
        opts.pop()
    opts.reverse()
    if not ani.season or ani.season in opts:
        return put_select("anime_season", options=opts[0:12], value=ani.season)
    else:
        return put_input("anime_season", value=ani.season, readonly=True)

def show_edit_anime(ani):
    ani_items = []
    for attr in ani.attrs:
        key  = attr.key
        value = getattr(ani, key)
        
        if key == 'season':
            ani_items.append([attr.desc, put_season_select(ani)])
        else:
            ani_items.append([attr.desc, put_input('anime_' + key, value=value)])

    tbl_items = [ ["Item", "Detials" ] ]
    tbl_items = tbl_items + ani_items
    items = put_column([
        put_table(tbl_items),
        put_button("Update", onclick=partial(do_update_anime, ani))
    ])
    popup("Edit Anime Information:", items,
          size="normal")
    
def do_update_anime(ani):
    for item in ani.attr_keys:
        ani.setAttr(item, pin['anime_' + item])

    glb_ani_man.saveData()
    close_popup()
    home_page()


@use_scope("main", clear=True)
def add_anime(opts):
    fname = opts.get('fname')
    if fname:
        put_text(fname)

    ani = anime.AnimeInfo("dummy")
    if opts.get('keyword'):
        ani.kwds.append(opts['keyword'])
    info = input_group("Anime Info", [
        input(a.desc, name=a.key, value=getattr(ani, a.key)) for a in ani.attrs        
    ])
    for key in ani.attr_keys:
        ani.setAttr(key, info[key])

    am = anime.getManager(web_local.user)
    am.add(ani)
    am.saveData()

    if opts.get('callback'):
        opts['callback']()
    else:
        home_page()
