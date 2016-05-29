
from GlobVar import *
from Classes import *
import pickle
import sys
import jsonpickle
import datetime

def load(filen):
    try:
        f1 = open(filen + 'players', 'rb')
        f2 = open(filen + 'piles', 'rb')
        f3 = open(filen + 'ships', 'rb')
        players = pickle.load(f1)
        piles = pickle.load(f2)
        ships = pickle.load(f3)
        f1.close()
        f2.close()
        f3.close()
        return players, piles, ships
    except Exception:
        sys.exit("Error: Invalid savefile")

def save(filen, players, piles, ships):
    f1 = open(filen + 'players', 'wb')
    f2 = open(filen + 'piles', 'wb')
    f3 = open(filen + 'ships', 'wb')
    pickle.dump(players, f1)
    pickle.dump(piles, f2)
    pickle.dump(ships, f3)
    f1.close()
    f2.close()
    f3.close()
    # backup
    timestr = datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y")
    f1 = open('backup/' + filen + 'players' + '_' + timestr, 'wb')
    f2 = open('backup/' + filen + 'piles' + '_' + timestr, 'wb')
    f3 = open('backup/' + filen + 'ships' + '_' + timestr, 'wb')
    pickle.dump(players, f1)
    pickle.dump(piles, f2)
    pickle.dump(ships, f3)
    f1.close()
    f2.close()
    f3.close()
    f4 = open(filen + "players.json", "w")
    f5 = open(filen + "piles.json", "w")
    f6 = open(filen + "ships.json", "w")
    teststr = jsonpickle.encode(players)
    f4.write(teststr)
    teststr = jsonpickle.encode(piles)
    f5.write(teststr)
    teststr = jsonpickle.encode(ships)
    f6.write(teststr)
    f4.close()
    f5.close()
    f6.close()

# functions
def transfer(source, target, item):
    buffer = source.takeitem(item)
    target.giveitem(buffer)


def addPlayer(player, squad, players, nick=""):
    newplayer = actor(player, extra=squad, nick=nick)
    players[player] = newplayer



def addPile(pile, piles):
    newpile = actor(pile)
    piles[pile] = newpile


def addShip(ship, squad, ships):
    newship = actor(ship, extra=squad)
    ships[ship] = newship

def addItem(nitem, owner, typ, nammo, players, piles, ships):
    if typ == 1:
        item(nitem, players[owner], ammo=nammo)
    elif typ == 2:
        item(nitem, piles[owner], ammo=nammo)
    else:
        item(nitem, ships[owner], ammo=nammo)


def addDamage(ndamage, owner, typ, players, piles, ships):
    if typ == 1:
        modificator(ndamage, players[owner])
    elif typ == 2:
        modificator(ndamage, piles[owner])
    else:
        modificator(ndamage, ships[owner])