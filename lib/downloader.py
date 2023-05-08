
import qbittorrentapi as qbit

DefaultConf = dict(
    host='192.168.1.6',
    port=8080,
    #username="admin",
    #password="adminadmin",
)

class Downloader:

# conf example:
# conf = dict(
#     host="localhost",
#     port=8080,
#     username="admin",
#     password="adminadmin",
# )
    def __init__(self, conf=None):
        cfg = DefaultConf.copy()
        if (conf):
            cfg.update(conf)
        self.no_connect = True
        self.cfg    = cfg
        if self.no_connect:
            return
        print("create qbitorrent client")
        self.client = qbit.Client(**cfg)
        self.connect()
        self.showVersion()
        self.logout()

    def connect(self):
        if (self.no_connect or self.client.is_logged_in):
            return

        try:
            print("connect to qbitorrent ...")
            self.client.auth_log_in(username=self.cfg.get('username'),
                                    password=self.cfg.get('password'))
            return True
        except qbit.LoginFailed as e:
            print(e)
            return False

    def showVersion(self):
        client = self.client
        print(f"qBittorrent: {client.app.version}")
        print(f"qBittorrent Web API: {client.app.web_api_version}")

    def logout(self):
        self.client.auth_log_out()

    def download(self, url):
        print("download: ", url)
        if self.no_connect:
            return

        self.connect()
        res = self.client.torrents_add(urls=[url], category='acg',
                                       save_path='/data/share/qbittorrent/')
        if (res != "Ok."):
            print("add torrent failed. ", res)
        self.logout()

    def test_download(self, url):
        print("download: ", url)
        cfg = self.cfg
        client = qbit.Client(**cfg)
        if client.torrents_add(urls=url) != "Ok.":
            print("add torrent failed. ", res)
        
        #with qbit.Client(host=cfg['host'], port=['port']) as client:
        #    if client.torrents_add(urls=url) != "Ok.":
        #        print("add torrent failed. ", res)
            #client.torrents_add(urls=url, category='acg',
            #                    save_path='/data/share/qbittorrent/')


# standalone test
if __name__ == '__main__':
    #dl = Downloader(dict(host='192.168.1.6', port=8080))
    dl = Downloader()
    dl.showVersion()
    ts = dl.client.torrents_info()
    print(type(ts))
    for tr in ts:
        print(tr)
        break

    # this works
    res = dl.client.torrents_add(urls="magnet:?xt=urn:btih:91dab8240f052f1276ba7936971d027dd21833a1&tr=http%3a%2f%2ft.nyaatracker.com%2fannounce&tr=http%3a%2f%2ftracker.kamigami.org%3a2710%2fannounce&tr=http%3a%2f%2fshare.camoe.cn%3a8080%2fannounce&tr=http%3a%2f%2fopentracker.acgnx.se%2fannounce&tr=http%3a%2f%2fanidex.moe%3a6969%2fannounce&tr=http%3a%2f%2ft.acg.rip%3a6699%2fannounce&tr=https%3a%2f%2ftr.bangumi.moe%3a9696%2fannounce&tr=udp%3a%2f%2ftr.bangumi.moe%3a6969%2fannounce&tr=http%3a%2f%2fopen.acgtracker.com%3a1096%2fannounce&tr=udp%3a%2f%2ftracker.opentrackr.org%3a1337%2fannounce")
    print(res)

