skillsDict = {"Charisma": 0, "Intuition": 1, "Handiwork": 2, "Conventional Weapons": 3, "Unconventional Weapons": 4,
              "Exotic": 5, "General Knowledge": 6, "Auxiliary": 7}
statsDict = {"Energy": 0, "Durability": 1, "Maneuverability": 2, "Hacking Systems": 3, "Computer": 4, "PSI Unit": 5,
             "Robotics": 6, "Engines": 7}
class actor(object):
    name = ""
    nick = ""
    skills = {}
    stats = {}
    modificators = []
    inventory = []
    extra = ""
    commands = []
    actions = []

    def __init__(self, name, nick="", extra=""):
        self.name = name
        self.modificators = []
        self.inventory = []
        self.skills = {}
        self.stats = {}
        self.extra = extra
        self.nick = nick
        self.commands = []
        self.actions = []
        for i in statsDict:
            self.stats[i] = 0
        for i in skillsDict:
            self.skills[i] = 0

    def setStat(self, i, stat):
        self.stats[i] = stat

    def setSkill(self, i, stat):
        self.skills[i] = stat

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

    def addAction(self, action):
        self.actions.append(action)

    def addCommand(self, command):
        self.commands.append(command)

    def printActions(self):
        print("ACTIONS")
        for thing in self.actions:
            print(thing)

    def printCommands(self):
        print("COMMANDS:")
        for thing in self.commands:
            print(thing)


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