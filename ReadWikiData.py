from Classes import *
from Functions import *
from os import listdir
players = {}
ships = {}
piles = {}

files = listdir('wikidata/')

for file in files:
    f = open('wikidata/'+file)
    text = f.read().replace('\n','').split("====")
    name = text[0]
    try:
        nick = text[34]
    except Exception:
        nick = "NPC"
    infantry = text[30]
    infantry = infantry.split('*')
    try:
        infantry.remove('')
    except Exception:
        print(infantry)
    for i, thing in enumerate(infantry):
        if "|" in thing:
            infantry[i] = thing[thing.find('|')+1:].replace(']]]','')
        else:
            infantry[i] = thing.replace(']]]', '').replace('[[[equip:', '')

    shipstuff = text[23]
    shipstuff = shipstuff.split('*')
    try:
        shipstuff.remove('')
    except Exception:
        print(shipstuff)
    if len(shipstuff)==0:
        shipname = "Casket Mk 1"
    elif "casket" in shipstuff[0].lower() or "grease" in shipstuff[0].lower() or "stich" in shipstuff[0].lower():
        shipname = shipstuff[0].replace(']]]', '').replace('[[[equip:', '')
    else:
        shipname = "Casket Mk 1"
    for i, thing in enumerate(shipstuff):
        if "|" in thing:
            shipstuff[i] = thing[thing.find('|')+1:].replace(']]]','')
        else:
            shipstuff[i] = thing.replace(']]]', '').replace('[[[equip:', '')

    addPlayer(name,'1',players,nick=nick)

    addShip(name+"'s "+shipname, '1', ships)

    for stuff in infantry:
        addItem(stuff, name, 1, '', players,piles,ships)

    for stuff in shipstuff:
        addItem(stuff, name+"'s "+shipname, 3, '', players, piles, ships)
save('import',players,piles,ships)