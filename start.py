
import sys
import pywebio
from views import home as vhome
from utils import anime

def main():
    vhome.view()

try:
    pywebio.start_server(main, port=8091, debug=True)

except KeyboardInterrupt:
    print("User Interrupt, exit.")
    anime.saveAllOpened()
    sys.exit(0)
