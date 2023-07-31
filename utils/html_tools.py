
import bs4
from ostruct import OpenStruct

def get_mixed_data(dat):
    info = OpenStruct(text = dat.text)
    info.link = []
    info.magnet = None
    for a in dat.find_all('a'):
        if a.get('href'):
            info.link.append(a.get('href'))
        for attr, val in a.attrs.items():
            if val.startswith('magnet:'):
                info.magent = val
    #print(info)
    return info

def parse_table(table):
    """table is BS4 object"""
    title = [ th.text for th in table.select('thead tr th') ]
    data = []
    for tr in table.select('tbody tr'):
        row = [ get_mixed_data(td) for td in tr.select('td') ]
        data.append(row)
    return OpenStruct(title=title, data=data)

