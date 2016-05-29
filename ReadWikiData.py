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
    print(infantry)
    addPlayer(name,'1',players,nick=nick)
save('import',players,piles,ships)