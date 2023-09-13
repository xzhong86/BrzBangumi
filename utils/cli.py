
from utils import anime
from utils import file_manager

def __init__():
    am = anime.getManager()
    return

def copy_files():
    am = anime.getManager()
    file_manager.scan_files(am)
    file_manager.copy_files(am)


if __name__ == '__main__':
    print("test cli ...")
    copy_files()

