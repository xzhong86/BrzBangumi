
import argparse

from utils import config
from utils import anime
from utils import file_manager

def __init__():
    am = anime.getManager()

def copy_files():
    am = anime.getManager()
    file_manager.scan_files(am)
    file_manager.copy_files(am)


def call_func(func_name, opts):
    new_name = func_name.translate(str.maketrans("-", "_"))
    names = [ new_name, func_name ]
    exclusive = [ 'main', '__init__' ]
    func = None
    for name in names:
        obj = globals().get(name)
        #is_local = name in dir()
        if callable(obj):
            func = obj
            break
    if not func:
        print(f"Error: {func_name} not exist or not callable")
    elif name in exclusive:
        print(f"Error: bad command '{func_name}'")
    else:
        func()


def main():
    parser = argparse.ArgumentParser(prog="Bangumi-CLI", description="command line tool")
    parser.add_argument('command')
    parser.add_argument('-u', '--user USER', help='set user, default(zpzhong)')
    parser.add_argument('--anime-dir DIR', help='set anime root dir')
    parser.add_argument('--download-dir DIR', help='set download dir')
    parser.add_argument('--use-cache', action='store_true')
    parser.add_argument('--do-test', action='store_true')
    opts = parser.parse_args()

    #config.update(opts)
    print(opts)
    cfg = config.get()
    if opts.do_test: cfg.do_test = True

    cmd = opts.command
    call_func(cmd, opts)


if __name__ == '__main__':
    print("test cli ...")
    main()

