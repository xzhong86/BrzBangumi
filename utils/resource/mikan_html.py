
import re
import bs4
from urllib.parse import urljoin
from ostruct import OpenStruct

from utils import config
from utils import cache
from utils import html_tools

MAP_en2chs = dict(update_time='更新时间', fansub='字幕组',
                  bangumi_name='番组名', size='大小', download='下载')
MAP_chs2en = { v:k for k,v in MAP_en2chs.items() }

# beautiful soup,
#  select(): tag.class-value, tag#id-value, #id-value, .class-value
#  find(tag, class_="name", id="name"): 

def scan_home_page():
    mk_home  = "https://mikanani.me/"
    text = cache.getUrlContent(mk_home, None)
    soup = bs4.BeautifulSoup(text, "xml")
    an_info_list = soup.select('#sk-body .sk-bangumi .an-info-group')

    re_id = re.compile(r"/([0-9]+)$")
    animes = []
    for info in an_info_list:
        aref = info.find("a", class_="an-text")
        if not aref:
            #print("no element of a.an-text")
            #print(info)
            continue
        title = aref.text
        url   = aref.get('href')
        mk_id = re_id.search(url).group(1)
        if not url.startswith("http"):
            url = urljoin(mk_home, url)
        animes.append(OpenStruct(title=title, url=url, mk_id=mk_id))

    print(f"Found {len(animes)} animes in MiKan home page.")

    return animes

def parse_anime_page(ani):
    text = cache.getUrlContent(ani.url, None)
    soup = bs4.BeautifulSoup(text, "xml")

    title    = soup.find('p', class_='bangumi-title')
    if not title:
        print(f"get title failed in {url} for {ani.title}")
        return
    title = title.text.strip()
    if title != ani.title:
        print(f"title mismatch: {title} != {ani.title}")
        return

    ani.info = []
    for info in soup.find_all('p', class_='bangumi-info'):
        ai = OpenStruct(text=info.text, link=None)
        if info.find('a'):
            ai.link = info.find('a').get('href')
            if ai.link.find("bgm.tv/subject") > 0:
                ani.bgm_url = ai.link
        ani.info.append(ai)

    return

def get_download_list(ani):
    text = cache.getUrlContent(ani.url, None)
    soup = bs4.BeautifulSoup(text, "xml")

    dl_list = []
    for table in soup.find_all('table'):
        tab = html_tools.parse_table(table)
        if '下载' in tab.title:
            dl_list = dl_list + tab.data

    return dl_list

def parse_list_page(index = 1):
    if index <= 0 or index > 3000:
        print(f"bad page index {index}")
        return None

    url = 'https://mikanani.me/Home/Classic/' + str(index)
    text = cache.getUrlContent(ani.url, 600)
    soup = bs4.BeautifulSoup(text, "xml")

    dl_lst = []
    for tabx in soup.select('div#sk-body table'):
        tab = html_tools.parse_table(tabx)
        if '下载' not in tab.title:
            continue
        for item in tab.title:
            if item not in MAP_chs2en.keys():
                print(f"unkown title '{item}'")

        table_title = [ MAP_chs2en[t] for t in tab.title ]
        for data_row in tab.data:
            for name, dat in zip(table_title, data_row):
                dl_lst.append(dat)

    return dl_lst


if __name__ == "__main__":
    animes = scan_home_page()
    parse_anime_page(animes[0])

