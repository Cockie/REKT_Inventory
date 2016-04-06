# -*- coding: utf-8 -*-
"""
Created on Sat Aug 29 21:59:42 2015

@author: Cornflakes & Dinosawer
"""

import tkinter
from tkinter import *
from tkinter import ttk
import pickle as pickle
import jsonpickle
from collections import OrderedDict
import datetime
import sys

# global variables

skillsDict = {"Charisma": 0, "Intuition": 1, "Handiwork": 2, "Conventional Weapons": 3, "Unconventional Weapons": 4,
              "Exotic": 5, "General Knowledge": 6, "Auxiliary": 7}
statsDict = {"Energy": 0, "Durability": 1, "Maneuverability": 2, "Hacking Systems": 3, "Computer": 4, "PSI Unit": 5,
             "Robotics": 6, "Engines": 7}

players = {}
ships = {}
piles = {}
tree = 0
details = 0
detailbuttonfr = 0


# functions
def transfer(source, target, item):
    buffer = source.takeitem(item)
    target.giveitem(buffer)


def addPlayer(player, squad):
    global players
    newplayer = actor(player, extra=squad)
    players[player] = newplayer
    updateTree()


def addPile(pile):
    global piles
    newpile = actor(pile)
    piles[pile] = newpile
    updateTree()


def addShip(ship, squad):
    global ships
    newship = actor(ship, extra=squad)
    ships[ship] = newship
    updateTree()


def addItem(nitem, owner, typ, nammo):
    global players
    global piles
    global ships
    if typ == 1:
        item(nitem, players[owner], ammo=nammo)
    elif typ == 2:
        item(nitem, piles[owner], ammo=nammo)
    else:
        item(nitem, ships[owner], ammo=nammo)
    updateTree()


def addDamage(ndamage, owner, typ):
    global players
    global piles
    global ships
    if typ == 1:
        modificator(ndamage, players[owner])
    elif typ == 2:
        modificator(ndamage, piles[owner])
    else:
        modificator(ndamage, ships[owner])
    updateTree()


def deleteSelected():
    global tree
    global players
    global piles
    global ships
    selected = tree.item(tree.focus())
    if selected['values'] != '':
        try:
            parenttype = tree.item(tree.parent(tree.focus()))['values'][0]
        except Exception:
            pass
        if parenttype == 'Players':
            parent = players[tree.item(tree.parent(tree.focus()))['text']]
        elif parenttype == 'Ships':
            parent = ships[tree.item(tree.parent(tree.focus()))['text']]
        elif parenttype == 'Piles':
            parent = piles[tree.item(tree.parent(tree.focus()))['text']]
        if selected['values'][0] == 'Item':
            item = parent.getitemfromid(tree.focus())
            parent.takeitem(item)
        if selected['values'][0] == 'Damage':
            item = parent.getmodfromname(selected['text'])
            parent.takemod(item)
        elif selected['values'][0] == 'Players':
            players.pop(selected['text'])
        elif selected['values'][0] == 'Piles':
            piles.pop(selected['text'])
        elif selected['values'][0] == 'Ships':
            ships.pop(selected['text'])
    updateTree()


def updateTree():
    global tree
    global data
    updateLists()
    allstuff = OrderedDict({"Players": players, "Piles": piles, "Ships": ships})
    allstuff.move_to_end('Piles')
    allstuff.move_to_end('Ships')
    collapsed = {}
    for child in tree.get_children():
        for entity in tree.get_children(child):
            temp = tree.item(entity)
            collapsed[temp['text']] = True if (temp['open'] == 1 or temp['open'] == 'true') else False
        tree.delete(child)
    for key in allstuff:
        idr = tree.insert('', 'end', text=key + ":", values=("", ""), open=True)
        for playah in sorted(list(sorted(list(allstuff[key].values()), key=lambda t: t.name)), key=lambda t: t.extra):
            opened = True
            try:
                opened = collapsed[playah.name]
            except Exception:
                pass
            idc = tree.insert(idr, 'end', text=playah.name, values=(key, playah.extra, ""), open=opened)
            playah.id = idc
            if len(playah.inventory) != 0:
                for stuff in sorted(list(playah.inventory), key=lambda t: t.ammo, reverse=True):
                    idi = tree.insert(idc, 'end', text=stuff.name, values=("Item", "", stuff.ammo), open=True)
                    stuff.id = idi
            if len(playah.modificators) != 0:
                for stuff in playah.modificators:
                    idi = tree.insert(idc, 'end', text=stuff.name, values=("Damage", "", ""), open=True)
                    stuff.id = idi


def updateLists():
    for key, value in players.items():
        players[value.name] = players.pop(key)
    for key, value in piles.items():
        piles[value.name] = piles.pop(key)
    for key, value in ships.items():
        ships[value.name] = ships.pop(key)


def updateDetails(event):
    global inf
    global tree
    global details
    global detailbuttonfr
    detailbuttonfr.destroy()
    detailbuttonfr = ttk.Frame(detailframe, width=100, height=100)
    detailbuttonfr.pack(fill=BOTH, expand=1)
    selected = tree.item(tree.focus())
    parent = tree.item(tree.parent(tree.focus()))['text']
    try:
        parenttype = tree.item(tree.parent(tree.focus()))['values'][0]
    except Exception:
        pass
    if selected['values'] != '':
        renameb = Button(detailbuttonfr, text='Rename')
        renameb.pack(fill=BOTH, expand=1)
        if selected['values'][0] == 'Item':
            if parenttype == 'Players':
                parentobj = players[parent]
            elif parenttype == 'Ships':
                parentobj = ships[parent]
            else:
                parentobj = piles[parent]
            details.set(parentobj.getitemfromid(tree.focus()).info())
            renameb.config(command=lambda: EditPopup(root, parentobj.getitemfromid(tree.focus()).rename, "New name?",
                                                     currentv=selected['text']))
            ammob = Button(detailbuttonfr, text='Change Ammo',
                           command=lambda: EditPopup(root, parentobj.getitemfromid(tree.focus()).changeammo,
                                                     "New ammo?", currentv=selected['values'][2]))
            ammob.pack(fill=BOTH, expand=1)
            ownb = Button(detailbuttonfr, text='Change Owner',
                          command=lambda: OwnerPopup(root, parentobj.getitemfromid(tree.focus()), parentobj))
            ownb.pack(fill=BOTH, expand=1)
        elif selected['values'][0] == 'Damage':
            if parenttype == 'Players':
                parentobj = players[parent]
            elif parenttype == 'Ships':
                parentobj = ships[parent]
            else:
                parentobj = piles[parent]
            details.set(parentobj.getmodfromname(selected['text']).info())
            renameb.config(
                command=lambda: EditPopup(root, parentobj.getmodfromname(selected['text']).rename, "New name?",
                                          currentv=selected['text']))
        elif selected['values'][0] == 'Players':
            details.set(players[selected['text']].info())
            renameb.config(command=lambda: EditPopup(root, players[selected['text']].rename, "New name?",
                                                     currentv=selected['text']))
            extb = Button(detailbuttonfr, text='Change Squad',
                          command=lambda: EditPopup(root, players[selected['text']].changeextra, "New Squad?",
                                                    currentv=selected['values'][1]))
            extb.pack(fill=BOTH, expand=1)
            killb = Button(detailbuttonfr, text='Kill', command=lambda: KillPopup(root, players[selected['text']]))
            killb.pack(fill=BOTH, expand=1)
        elif selected['values'][0] == 'Ships':
            details.set(ships[selected['text']].info())
            renameb.config(
                command=lambda: EditPopup(root, ships[selected['text']].rename, "New name?", currentv=selected['text']))
            extb = Button(detailbuttonfr, text='Change Squad',
                          command=lambda: EditPopup(root, ships[selected['text']].changeextra, "New Squad?",
                                                    currentv=selected['values'][1]))
            extb.pack(fill=BOTH, expand=1)
        elif selected['values'][0] == 'Piles':
            details.set(piles[selected['text']].info())
            renameb.config(
                command=lambda: EditPopup(root, piles[selected['text']].rename, "New name?", currentv=selected['text']))
        root.update_idletasks()


def save():
    global players
    global piles
    global ships
    f1 = open('players', 'wb')
    f2 = open('piles', 'wb')
    f3 = open('ships', 'wb')
    pickle.dump(players, f1)
    pickle.dump(piles, f2)
    pickle.dump(ships, f3)
    f1.close()
    f2.close()
    f3.close()
    # backup
    timestr = datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y")
    f1 = open('players' + '_' + timestr, 'wb')
    f2 = open('piles' + '_' + timestr, 'wb')
    f3 = open('ships' + '_' + timestr, 'wb')
    pickle.dump(players, f1)
    pickle.dump(piles, f2)
    pickle.dump(ships, f3)
    f1.close()
    f2.close()
    f3.close()
    f4 = open("players.json", "w")
    f5 = open("piles.json", "w")
    f6 = open("ships.json", "w")
    teststr = jsonpickle.encode(players)
    f4.write(teststr)
    teststr = jsonpickle.encode(piles)
    f5.write(teststr)
    teststr = jsonpickle.encode(ships)
    f6.write(teststr)
    f4.close()
    f5.close()
    f6.close()


def stop():
    save()
    root.destroy()


# main loop
def main():
    updateLists()
    updateTree()
    root.protocol('WM_DELETE_WINDOW', stop)
    root.mainloop()


class actor(object):
    name = ""
    skills = {}
    stats = {}
    modificators = []
    inventory = []
    extra = ""

    def __init__(self, name, extra=""):
        self.name = name
        self.modificators = []
        self.inventory = []
        self.skills = {}
        self.stats = {}
        self.extra = extra
        for i in statsDict:
            self.stats[i] = 0
        for i in skillsDict:
            self.skills[i] = 0

    def hasitem(self, item):
        if self.inventory.count(item) >= 1:
            return 1
        else:
            return 0

    def getitemfromname(self, itemname):
        for item in self.inventory:
            if item.name.strip() == itemname.strip():
                return item
        return 0

    def getitemfromid(self, itemid):
        for item in self.inventory:
            if item.id.strip() == itemid.strip():
                return item
        return 0

    def getmodfromname(self, modname):
        for mod in self.modificators:
            if mod.name.strip() == modname.strip():
                return mod
        return 0

    def takeitem(self, item):
        if item in self.inventory:
            item.owner = 0
            return self.inventory.remove(item)

    def takemod(self, item):
        if item in self.modificators:
            item.owner = 0
            return self.modificators.remove(item)

    def giveitem(self, item):
        self.inventory.append(item)

    def givemod(self, mod):
        self.modificators.append(mod)

    def listitems(self, tree, self_id):
        items_id = self_id + " " + "Items"
        tree.insert(self_id, end, items_id, text="Items")
        for i in self.inventory:
            tree.insert(items_id, end, text=self.inventory[i].name)

    def listmodificators(self, tree, self_id):
        modificators_id = self_id + " " + "Modificators"
        tree.insert(self_id, end, modificators_id, text="Modificators")
        for i in self.modificators:
            tree.insert(modificators_id, end, text=self.modificators[i].name)

    def info(self):
        message = "Name: " + self.name + "\n"
        message += "Inventory:\n"
        for item in self.inventory:
            message += "* " + item.name + "\n"
        message += "Damage:\n"
        for item in self.modificators:
            message += "* " + item.name + "\n"
        return message

    def rename(self, newname):
        self.name = newname

    def changeextra(self, newextra):
        self.extra = newextra


class item(object):
    name = ""
    skills = {}
    stats = {}
    owner = 0
    ammo = ""

    def __init__(self, name, owner, ammo=""):
        self.name = name
        self.owner = owner
        owner.giveitem(self)
        self.skills = {}
        self.stats = {}
        self.ammo = ammo
        for i in statsDict:
            self.stats[i] = 0
        for i in skillsDict:
            self.skills[i] = 0

    def info(self):
        message = "Name: " + self.name + "\n"
        message += "Owner: " + self.owner.name + "\n"
        message += "Ammo: " + self.ammo + "\n"
        return message

    def rename(self, newname):
        self.name = newname

    def changeammo(self, newammo):
        self.ammo = newammo


class modificator(object):
    name = ""
    skills = {}
    stats = {}
    owner = 0

    def __init__(self, name, owner):
        self.name = name
        self.owner = owner
        owner.givemod(self)
        self.skills = {}
        self.stats = {}
        for i in statsDict:
            self.stats[i] = 0
        for i in skillsDict:
            self.skills[i] = 0

    def info(self):
        message = "Name: " + self.name + "\n"
        message += "Owner: " + self.owner.name + "\n"
        return message

    def rename(self, newname):
        self.name = newname


# Tree object
class treebox(object):
    def __init__(self, parent, Name=None):
        self.frame = ttk.Frame(parent)
        Grid.rowconfigure(parent, 0, weight=1)
        Grid.columnconfigure(parent, 0, weight=1)
        if Name is not None:
            self.label = ttk.Label(self.frame, text=Name)
            self.label.grid(column=0, row=0)
        self.tree = ttk.Treeview(self.frame)
        self.tree.grid(column=0, row=1, sticky="nsew")
        self.yscrollbar = ttk.Scrollbar(self.frame, orient=VERTICAL, command=self.tree.yview)
        self.yscrollbar.grid(column=1, row=1, sticky="ns")
        self.xscrollbar = ttk.Scrollbar(self.frame, orient=HORIZONTAL, command=self.tree.xview)
        self.xscrollbar.grid(column=0, row=3, sticky="we")
        self.tree.configure(xscrollcommand=self.xscrollbar.set, yscrollcommand=self.yscrollbar.set)
        for x in range(1):
            Grid.columnconfigure(self.frame, x, weight=1)
        for y in range(1, 2):
            Grid.rowconfigure(self.frame, y, weight=1)

    def pack(self):
        self.frame.grid(column=0, row=0, sticky="nsew")

    def destroy(self):
        self.frame.destroy()


# Popup windows
class PlayerPopup():
    def __init__(self, parent):
        top = self.top = Toplevel(parent)
        top.bind("<Return>", self.ok)
        Label(top, text="Player name?").pack()

        self.e = Entry(top)
        self.e.pack(padx=5)

        Label(top, text="Squad?").pack()

        self.e2 = Entry(top)
        self.e2.pack(padx=5)

        b = Button(top, text="Okay", command=self.ok)
        b.pack(pady=5)

    def ok(self, event=0):
        addPlayer(self.e.get(), self.e2.get())
        self.top.destroy()


class PilePopup():
    def __init__(self, parent):
        top = self.top = Toplevel(parent)
        top.bind("<Return>", self.ok)
        Label(top, text="Pile name?").pack()

        self.e = Entry(top)
        self.e.pack(padx=5)

        b = Button(top, text="Okay", command=self.ok)
        b.pack(pady=5)

    def ok(self, event=0):
        addPile(self.e.get())
        self.top.destroy()


class ShipPopup():
    def __init__(self, parent):
        top = self.top = Toplevel(parent)
        top.bind("<Return>", self.ok)
        Label(top, text="Ship name?").pack()

        self.e = Entry(top)
        self.e.pack(padx=5)

        Label(top, text="Squad?").pack()

        self.e2 = Entry(top)
        self.e2.pack(padx=5)

        b = Button(top, text="Okay", command=self.ok)
        b.pack(pady=5)

    def ok(self, event=0):
        addShip(self.e.get(), self.e2.get())
        self.top.destroy()


class ItemPopup():
    def __init__(self, parent):
        global tree
        global players
        global piles
        global ships
        selected = tree.item(tree.focus())
        types = {'Players': 1, 'Piles': 2, 'Ships': 3}

        top = self.top = Toplevel(parent)
        top.bind("<Return>", self.ok)
        Label(top, text="parent?").pack()
        self.v = IntVar()
        try:
            self.v.set(types[selected['values'][0]])
        except Exception:
            self.v.set(1)
        self.box1 = Radiobutton(top, text="Player", variable=self.v, value=1, command=self.newselection)
        self.box2 = Radiobutton(top, text="Pile", variable=self.v, value=2, command=self.newselection)
        self.box3 = Radiobutton(top, text="Ship", variable=self.v, value=3, command=self.newselection)
        self.box1.pack(padx=5)
        self.box2.pack(padx=5)
        self.box3.pack(padx=5)

        self.playerbox = ttk.Combobox(top)
        try:
            if selected['values'][0] == 'Piles':
                self.box2.select()
                self.playerbox['values'] = sorted(list(piles.keys()))
                self.playerbox.set(selected['text'])
            elif selected['values'][0] == 'Ships':
                self.box3.select()
                self.playerbox['values'] = sorted(list(ships.keys()))
                self.playerbox.set(selected['text'])
            elif selected['values'][0] == 'Players':
                self.box1.select()
                self.playerbox['values'] = sorted(list(players.keys()))
                self.playerbox.set(selected['text'])
            else:
                self.box1.select()
                self.playerbox['values'] = sorted(list(players.keys()))
        except Exception:
            self.box1.select()
            self.playerbox['values'] = sorted(list(players.keys()))
        self.playerbox.pack(padx=5)
        Label(top, text="Item name?").pack()

        self.e = Entry(top)
        self.e.pack(padx=5)
        Label(top, text="Ammo?").pack()

        self.e2 = Entry(top)
        self.e2.pack(padx=5)

        b = Button(top, text="Okay", command=self.ok)
        b.pack(pady=5)

    def ok(self, event=0):
        addItem(self.e.get(), self.playerbox.get(), self.v.get(), self.e2.get())
        self.top.destroy()

    def newselection(self):
        value = self.v.get()
        if value == 1:
            self.playerbox['values'] = sorted(list(players.keys()))
        elif value == 2:
            self.playerbox['values'] = sorted(list(piles.keys()))
        else:
            self.playerbox['values'] = sorted(list(ships.keys()))


class DamagePopup():
    def __init__(self, parent):
        global tree
        global players
        global piles
        global ships
        selected = tree.item(tree.focus())
        types = {'Players': 1, 'Piles': 2, 'Ships': 3}
        top = self.top = Toplevel(parent)
        top.bind("<Return>", self.ok)
        Label(top, text="parent?").pack()
        self.v = IntVar()
        try:
            self.v.set(types[selected['values'][0]])
        except Exception:
            self.v.set(1)
        self.box1 = Radiobutton(top, text="Player", variable=self.v, value=1, command=self.newselection)
        self.box2 = Radiobutton(top, text="Pile", variable=self.v, value=2, command=self.newselection)
        self.box3 = Radiobutton(top, text="Ship", variable=self.v, value=3, command=self.newselection)
        self.box1.pack(padx=5)
        self.box2.pack(padx=5)
        self.box3.pack(padx=5)

        self.playerbox = ttk.Combobox(top)

        try:
            if selected['values'][0] == 'Piles':
                self.box2.select()
                self.playerbox['values'] = sorted(list(piles.keys()))
                self.playerbox.set(selected['text'])
            elif selected['values'][0] == 'Ships':
                self.box3.select()
                self.playerbox['values'] = sorted(list(ships.keys()))
                self.playerbox.set(selected['text'])
            elif selected['values'][0] == 'Players':
                self.box1.select()
                self.playerbox['values'] = sorted(list(players.keys()))
                self.playerbox.set(selected['text'])
            else:
                self.box1.select()
                self.playerbox['values'] = sorted(list(players.keys()))
        except Exception:
            self.box1.select()
            self.playerbox['values'] = sorted(list(players.keys()))
        self.playerbox.pack(padx=5)
        Label(top, text="Item name?").pack()

        self.e = Entry(top)
        self.e.pack(padx=5)

        b = Button(top, text="Okay", command=self.ok)
        b.pack(pady=5)

    def ok(self, event=0):
        addDamage(self.e.get(), self.playerbox.get(), self.v.get())
        self.top.destroy()

    def newselection(self):
        value = self.v.get()
        if value == 1:
            self.playerbox['values'] = sorted(list(players.keys()))
        elif value == 2:
            self.playerbox['values'] = sorted(list(piles.keys()))
        else:
            self.playerbox['values'] = sorted(list(ships.keys()))


class EditPopup():
    def __init__(self, parent, func, mess, currentv=""):
        self.func = func
        top = self.top = Toplevel(parent)
        top.bind("<Return>", self.ok)
        Label(top, text=mess).pack()
        self.e = Entry(top)
        self.e.pack(padx=5)
        self.e.insert(0, currentv)

        b = Button(top, text="Okay", command=self.ok)
        b.pack(pady=5)

    def ok(self, event=0):
        self.func(self.e.get())
        updateTree()
        self.top.destroy()


class OwnerPopup():
    def __init__(self, parent, item, prowner):
        self.item = item
        self.prowner = prowner
        top = self.top = Toplevel(parent)
        top.bind("<Return>", self.ok)
        Label(top, text="parent?").pack()
        self.v = IntVar()
        self.v.set(1)
        self.box1 = Radiobutton(top, text="Player", variable=self.v, value=1, command=self.newselection)
        self.box1.select()
        self.box2 = Radiobutton(top, text="Pile", variable=self.v, value=2, command=self.newselection)
        self.box3 = Radiobutton(top, text="Ship", variable=self.v, value=3, command=self.newselection)
        self.box1.pack(padx=5)
        self.box2.pack(padx=5)
        self.box3.pack(padx=5)

        self.playerbox = ttk.Combobox(top)
        self.playerbox['values'] = list(players.keys())
        self.playerbox.pack(padx=5)

        b = Button(top, text="Okay", command=self.ok)
        b.pack(pady=5)

    def ok(self, event=0):
        self.prowner.takeitem(self.item)
        value = self.v.get()
        if value == 1:
            nowner = players[self.playerbox.get()]
        elif value == 2:
            nowner = piles[self.playerbox.get()]
        else:
            nowner = ships[self.playerbox.get()]
        self.item.owner = nowner
        nowner.giveitem(self.item)
        updateTree()
        self.top.destroy()

    def newselection(self):
        value = self.v.get()
        if value == 1:
            self.playerbox['values'] = list(players.keys())
        elif value == 2:
            self.playerbox['values'] = list(piles.keys())
        else:
            self.playerbox['values'] = list(ships.keys())


class KillPopup():
    def __init__(self, parent, player):
        self.player = player
        top = self.top = Toplevel(parent)
        top.bind("<Return>", self.ok)
        Label(top, text="Location?").pack()
        self.e = Entry(top)
        self.e.pack(padx=5)

        b = Button(top, text="Okay", command=self.ok)
        b.pack(pady=5)

    def ok(self, event=0):
        players.pop(self.player.name)
        piles[self.e.get()] = self.player
        item(self.player.name + "'s corpse", self.player)
        self.player.name = self.e.get()
        updateTree()
        self.top.destroy()


try:
    f1 = open('players', 'rb')
    f2 = open('piles', 'rb')
    f3 = open('ships', 'rb')
    players = pickle.load(f1)
    piles = pickle.load(f2)
    ships = pickle.load(f3)
    f1.close()
    f2.close()
    f3.close()
except Exception:
    sys.exit("Error: Invalid savefile")

# main frame
root = Tk()
root.minsize(1000, 400)
root.wm_title("REKT Inventory Manager 1.3")
img = PhotoImage(file='logo.gif')
root.tk.call('wm', 'iconphoto', root._w, img)

details = StringVar()
details.set("Details!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

# windows
window = ttk.Panedwindow(root, orient=HORIZONTAL)
window.pack(fill=BOTH, expand=1)

# frames
buttonframe = ttk.Frame(window, width=100, height=100)
window.add(buttonframe, weight=0)
mainframe = ttk.Frame(window, width=200, height=100)
window.add(mainframe, weight=1)
detailframe = ttk.Frame(window, width=200, height=100)
window.add(detailframe, weight=1)

# tree
InTree = treebox(mainframe, "Input")
columns = ('type', 'squad', 'info')
InTree.tree['columns'] = columns
InTree.tree.column('type', width=80)
InTree.tree.column('squad', width=100)

InTree.pack()
tree = InTree.tree

# detail frame
inf = Label(detailframe, textvariable=details, anchor='nw', relief=SUNKEN, justify=LEFT)
inf.pack(fill=BOTH, expand=1)
detailbuttonfr = ttk.Frame(detailframe)
detailbuttonfr.pack(fill=BOTH, expand=1)

tree.bind("<Button-1>", updateDetails)
tree.bind("<ButtonRelease-1>", updateDetails)

for col in columns:
    InTree.tree.heading(col, text=col)
# Button frame
addpb = Button(buttonframe, text='Add player', anchor="w", command=lambda: PlayerPopup(root))
addpb.pack(fill=BOTH, expand=1)
addplb = Button(buttonframe, text='Add pile', anchor="w", command=lambda: PilePopup(root))
addplb.pack(fill=BOTH, expand=1)
addshb = Button(buttonframe, text='Add ship', anchor="w", command=lambda: ShipPopup(root))
addshb.pack(fill=BOTH, expand=1)
addib = Button(buttonframe, text='Add item', anchor="w", command=lambda: ItemPopup(root))
addib.pack(fill=BOTH, expand=1)
adddb = Button(buttonframe, text='Add damage', anchor="w", command=lambda: DamagePopup(root))
adddb.pack(fill=BOTH, expand=1)
addib = Button(buttonframe, text='Delete selected', anchor="w", command=deleteSelected)
addib.pack(fill=BOTH, expand=1)
saveb = Button(buttonframe, text='Save', anchor="w", command=save)
saveb.pack(fill=BOTH, expand=1)
quitb = Button(buttonframe, text='Save and Quit', anchor="w", command=stop)
quitb.pack(fill=BOTH, expand=1)
quitb2 = Button(buttonframe, text='Quit without Saving', anchor="w", command=root.destroy)
quitb2.pack(fill=BOTH, expand=1)

main()
