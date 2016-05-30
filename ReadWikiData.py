from Classes import *
from Functions import *
from os import listdir
players = {}
ships = {}
piles = {}

files = listdir('wikidata/')

nicks = {}
with open('charnames.txt') as f:
    for line in f:
        line = line.split('&')
        nicks[line[1]] = line[0].strip('\n')
squadd = {}
with open('charnames.txt') as f:
    for line in f:
        line = line.split('&')
        squadd[line[1]] = line[2].strip('\n')

for file in files:
    f = open('wikidata/'+file)
    text = f.read().replace('\n','').split("====")
    name = text[0].strip()
    print(name)
    nick = nicks[name]
    sq = squadd[name]
    infantry = text[30]
    infantry = infantry.split('*')
    try:
        infantry.remove('')
    except Exception:
        #print(infantry)
        pass
    crossbow=""
    grenade=""
    blunderbuss=[]
    blunderind = 0
    for i, thing in enumerate(infantry):
        if "|" in thing:
            infantry[i] = thing[thing.find('|')+1:].replace(']]]','')
        else:
            infantry[i] = thing.replace(']]]', '').replace('[[[equip:', '')
        if 'crossbow' in thing.lower():
            crossbow+=infantry[i+1]+', ' +infantry[i+2]+', ' +infantry[i+3]+', ' +infantry[i+4]
            infantry.remove(infantry[i + 1])
            infantry.remove(infantry[i + 1])
            infantry.remove(infantry[i + 1])
            infantry.remove(infantry[i + 1])
        elif 'grenade' in thing.lower():
            grenade+=infantry[i+1]+', ' +infantry[i+2]+', ' +infantry[i+3]
            infantry.remove(infantry[i + 1])
            infantry.remove(infantry[i + 1])
            infantry.remove(infantry[i + 1])
    shipstuff = text[23]
    shipstuff = shipstuff.split('*')
    try:
        shipstuff.remove('')
    except Exception:
        #print(shipstuff)
        pass
    if len(shipstuff)==0:
        shipname = "Mk 1 Casket"
    elif "casket" in shipstuff[0].lower() or "grease" in shipstuff[0].lower() or "stich" in shipstuff[0].lower():
        shipname = shipstuff[0].replace(']]]', '').replace('[[[equip:', '')
    else:
        shipname = "Mk 1 Casket"
    for i, thing in enumerate(shipstuff):
        if "|" in thing:
            shipstuff[i] = thing[thing.find('|')+1:].replace(']]]','')
        else:
            shipstuff[i] = thing.replace(']]]', '').replace('[[[equip:', '')
        if 'blunderbuss' in thing.lower():
            blunderbuss.append("")
            while True:
                blunderbuss[blunderind] += shipstuff[i + 1] + ', '
                if shipstuff[i + 1].endswith(' '):
                    shipstuff.remove(shipstuff[i + 1])
                else:
                    shipstuff.remove(shipstuff[i + 1])
                    blunderind+=1
                    break


    addPlayer(name,sq,players,nick=nick)

    addShip(name+"'s "+shipname, sq, ships)

    for stuff in infantry:
        if 'crossbow' in stuff.lower():
            addItem(stuff, name, 1, crossbow, players, piles, ships)
        elif 'grenade' in stuff.lower():
            addItem(stuff, name, 1, grenade, players, piles, ships)
        else:
            addItem(stuff, name, 1, '', players,piles,ships)
    blunderind=0
    for stuff in shipstuff:
        if 'blunderbuss' in stuff.lower():
            addItem(stuff, name+"'s "+shipname, 3, blunderbuss[blunderind].strip(', '), players, piles, ships)
            blunderind+=1
        else:
            addItem(stuff, name+"'s "+shipname, 3, '', players, piles, ships)
save('import',players,piles,ships)