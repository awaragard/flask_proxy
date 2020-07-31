import sys

from os.path import dirname, realpath, join

resource_dir = dirname(realpath(__file__))


def get_resource(name):
    return join(resource_dir, name)

def get_ust_exe():
    binary = "user-sync-bugfix.exe" if 'win' in sys.platform.lower() else "user-sync"
    return join(resource_dir, binary)
