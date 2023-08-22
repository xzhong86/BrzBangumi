
import sys
import argparse
import pywebio
from views import home as vhome
from utils import anime

# main
parser = argparse.ArgumentParser(prog='MyBangumi')
parser.add_argument('-p', '--port', type=int, default=8091)
args = parser.parse_args()

try:
    p = args.port
    pywebio.start_server(vhome.view, port=p, debug=True, cdn=False)

except KeyboardInterrupt:
    print("User Interrupt, exit.")
    anime.saveAllOpened()
    sys.exit(0)

