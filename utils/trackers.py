

mikan = [
    'tr=http%3a%2f%2fopen.acgtracker.com%3a1096%2fannounce',
    'tr=http%3a%2f%2ft.nyaatracker.com%2fannounce',
    'tr=http%3a%2f%2ftracker.kamigami.org%3a2710%2fannounce',
    'tr=http%3a%2f%2fshare.camoe.cn%3a8080%2fannounce',
    'tr=http%3a%2f%2fopentracker.acgnx.se%2fannounce',
    'tr=http%3a%2f%2fanidex.moe%3a6969%2fannounce',
    'tr=http%3a%2f%2ft.acg.rip%3a6699%2fannounce',
    'tr=https%3a%2f%2ftr.bangumi.moe%3a9696%2fannounce',
    'tr=udp%3a%2f%2ftr.bangumi.moe%3a6969%2fannounce',
    'tr=udp%3a%2f%2ftracker.opentrackr.org%3a1337%2fannounce'
]

kisssub = [
    'tr=http://open.acgtracker.com:1096/announce'
]


def getTrackers():
    trackers = dict(
        mikan = mikan.copy(),
        kisssub = kisssub.copy()
    )
    return trackers

def getMagnet(hashid, site='mikan'):
    trs = getTrackers()[site]
    pfx = 'magnet:?xt=urn:btih:'
    url = pfx + hashid + '&' + '&'.join(trs)
    return url


if __name__ == '__main__':
    url = getMagnet('e63fd7a029f9e614c630307d50cf3d507603142e')
    print(url)

