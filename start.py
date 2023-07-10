
import sys
import pywebio
from views import home as vhome


def main():
    vhome.view()

try:
    pywebio.start_server(main, port=8091, debug=True)

except KeyboardInterrupt:
    print("User Interrupt, exit.")
    sys.exit(0)
