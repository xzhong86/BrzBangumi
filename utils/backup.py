
import os
import re
import filecmp
import shutil
from datetime import datetime, timedelta

class FileInfo:
    def __init__(self, dirpath, basename):
        self.dirpath = dirpath
        self.name = basename
        self.path = os.path.join(dirpath, basename)
        self.mtime = os.stat(self.path).st_mtime

    def read_content(self):
        with open(self.path, 'r', encoding='utf-8') as fh:
            return fh.read()


def check_and_backup(filepath):
    dirpath  = os.path.dirname(filepath) or "."
    filename = os.path.basename(filepath)
    fi_curr   = FileInfo(dirpath, filename)

    # start with bak-MM-DD-HH-filename.ext
    re_fname = re.compile('bak-.+-' + filename)
    files = []
    for fname in os.listdir(dirpath):
        if re_fname.match(fname):
            files.append(FileInfo(dirpath, fname))

    files.sort(key=lambda fi: fi.mtime)
    fi_latest = files[-1]

    if filecmp.cmp(fi_curr.path, fi_latest.path, False):
        return    # nothing new

    time_str  = datetime.now().strftime("%m-%d-%H")
    bak_fname = f"bak-{time_str}-{filename}"
    shutil.copyfile(filepath, os.path.join(dirpath, bak_fname))

    files.append(FileInfo(dirpath, bak_fname))
    clean_backup_files(files)

def clean_backup_files(files):
    if len(files) < 8:
        return
    
    for fi in files[0: len(files) - 8]:
        os.unlink(fi.path)


if __name__ == '__main__':
    check_and_backup('anime-data.json')

