import random
from time import sleep
import os

samtale = ["Guro Samtale", "Glenn Mer samtale", "Thomas Litt samtale til", "Me is typing..." "Me jeg er på venstresiden", "AleksanderGustavsson siste samtalebit", "Bot5 is typing...", "Bot5 litt samtale", "Bot4 is typing...", "Bot4 enig med det", "Bot3 is typing...", "Bot3 ikke enig med det"]

clear = lambda: os.system('cls')
clear()




def bordered(arr):
    size = os.get_terminal_size()
    text = arr.split()[0]
    mefinder = "Me"
    w = ""

    for _ in range(int(size.columns)-len(arr)-1):
        w += " "
    wl = w
    for _ in range(len(arr)-len(text)-1):
        wl += " "
    
    exclbot = ' '.join(arr.split()[1:])
    lines = text.splitlines()
    width = max(len(s) for s in lines)
    res = ['┌' + '─' * width + '┐']
    if mefinder in text:
        res = [wl + '┌' + '─' * width + '┐']
    for s in lines:
        if mefinder not in text:
            res.append('│' + (s + ' ' * width)[:width] + '│' + "  " + exclbot)
        else:
            res.append(w[2:] + exclbot + "  " + '│' + (s + ' ' * width)[:width] + '│')
        
    if mefinder in text:
        res.append(wl + '└' + '─' * width + '┘')
    else:
        res.append('└' + '─' * width + '┘')
    return '\n'.join(res)
        

fullsamtale = []
for x in samtale:
    print(bordered(x))
    sleep(1)
    if "is typing" not in x:
        fullsamtale.append(x)
    else:
        sleep(3)
        clear()
        for y in fullsamtale:
            print(bordered(y))


