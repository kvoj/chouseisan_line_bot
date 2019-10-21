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
    elif 'total' == cmd:
        url = vals[0]
        vals.append(3)
        number = int(vals[1]) if str(vals[1]).isnumeric() else 3
        return chousei.get_total(url, number)

