
import os
import re
from os.path import basename
from datetime import datetime, timedelta
from ostruct import OpenStruct

from utils import config

class FileInfo:
    def __init__(self, dirpath, filename):
        self.path = os.path.join(dirpath, filename)
        self.name = basename(filename)
        st = os.stat(self.path)
        self.time = datetime.fromtimestamp(st.st_mtime)
        self.index = None

    def isfile(self):
        return os.path.isfile(self.path)


def get_files(ddir):
    files = []
    print(f"scan dir {ddir} ...")
    for file in os.listdir(ddir):
        fi = FileInfo(ddir, file)
        if fi.isfile():
            files.append(fi)

    re_ext = re.compile(r'.+\.(mp4|mkv)')
    files = list(filter(lambda fi: re_ext.match(fi.name), files))

    files.sort(key=lambda fi: fi.time, reverse=True)
    return files

def dist_files(am, files):
    print(f"{len(files)} to distribute...")
    for ani in am.animes:
        ani.files = []  # clear
    res = OpenStruct(others=[], conflicts=[])
    for fi in files:
        belong = []
        for ani in am.animes:
            if ani.matchKeyWords(fi.name):
                fi.index = ani.guessIndex(fi.name)
                ani.files.append(fi)
                belong.append(ani)
                break
        #print(f"file: {fi.name}, belong={len(belong)}")
        if len(belong) == 0:
            res.others.append(fi)
        if len(belong) > 1:
            res.conflicts.append([fi, belong])

    for ani in am.animes:
        if len(ani.files) > 0:
            ani.update_time = ani.files[0].time
        else:
            ani.update_time = datetime.now() - timedelta(days=90)

    return res

def scan_files(ani_man):
    files = get_files(config.get().download_dir)
    res = dist_files(ani_man, files)
    return res

def copy_files(ani_man):
    ani_root = config.get().anime_dir
    os.makedirs(ani_root, exist_ok=True)
    import shutil
    for ani in ani_man.animes:
        dir_name = ani.season + "-" + ani.name
        ani_dir  = os.path.join(ani_root, dir_name)
        os.makedirs(ani_dir, exist_ok=True)
        for fi in ani.files:
            print(f"copy {fi.path} into {ani_dir}")
            shutil.copy2(fi.path, ani_dir)

    return

