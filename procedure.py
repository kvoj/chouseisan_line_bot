import requests
import chouseisanlib as Chlib

def handle_string(string):
    slist = string.split('\n')
    cmd = slist[0]
    vals = slist[1:]

    chousei = Chlib.Chouseisan()

    if 'create' == cmd:
        name = vals[0]
        comment = vals[1]
        kouho = '\n'.join(vals[2:])
        return chousei.create_schedule(name, comment, kouho)


