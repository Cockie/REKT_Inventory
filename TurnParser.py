try:
    from BeautifulSoup import BeautifulSoup
except ImportError:
    from bs4 import BeautifulSoup
from urllib import request

nicks = {}
with open('charnames.txt') as f:
    for line in f:
        line = line.split('&')
        nicks[line[0]] = line[1].strip('\n')


class Character():
    name = ""
    nick = ""
    commands = []
    actions = []

    def __init__(self, name, nick):
        self.name = name
        self.nick = nick
        self.commands = []
        self.actions = []

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


def stripComment(mess):
    while '((' in mess:
        mess = mess.replace(mess[mess.find('(('):mess.find('))') + 2], '')
    return mess


def removeTags(mess):
    mess = mess.replace('<span style="text-decoration: underline">', '')
    mess = mess.replace('<span style="font-weight: bold">', '')
    mess = mess.replace('<span style="font-style: italic">', '')
    mess = mess.replace('</span>', '')
    return mess


def splitInLines(mess):
    return mess.replace('<br/>', '\n')


# url = "http://forums.ltheory.com/viewtopic.php?p=127522#p127522"
url = "http://forums.ltheory.com/viewtopic.php?f=29&t=5151#p127522"
if 'start' not in url:
    url = url.replace('#', '&start=1#')

head = {'User-Agent': 'Chrome/35.0.1916.47'}
'''if forumusername != "" and forumpw != "":
    url = "http://forums.ltheory.com/ucp.php?mode=login"
    payload = {"username": forumusername, \
               "password": forumpw, \
               'redirect': 'index.php', \
               'sid': '', \
               'login': 'Login'}
    try:
        p = session.post(url, headers=head, data=payload, timeout=5)
    except Exception:
        pass

    try:
        r = session.get(res[0], headers=head, timeout=15)
    except Exception as e:
        print(e)
        return
    htmlstr = r.text'''
htmlstr = ""
prevhtmlstr = ""
keepgoing = True
while keepgoing:
    print(url)
    req = request.Request(url, data=None, headers=head)
    try:
        r = request.urlopen(req, timeout=15)
    except Exception:
        print("Internet error, please try again")
        break
    htmlstr = r.read()
    # replace weird things by unicode
    try:
        htmlstr = htmlstr.decode()
    except Exception as e:
        htmlstr = str(htmlstr)

    # make new url for next attempt
    startIndicator = int(url[url.find('start=') + 6:url.find('#')])
    newstart = startIndicator + 15
    url = url.replace('start=' + str(startIndicator), 'start=' + str(newstart))

    # parse html
    parsed_html = BeautifulSoup(htmlstr)
    prev_parsed_html = BeautifulSoup(prevhtmlstr)
    if prevhtmlstr != "":
        if parsed_html.body.find('div', attrs={'class': 'content'}).text == prev_parsed_html.body.find('div', attrs={
            'class': 'content'}).text:
            # we reached the end of the thread
            keepgoing = False
            break
        else:
            prevhtmlstr = htmlstr
    else:
        prevhtmlstr = htmlstr
    parsed_html.blockquote.decompose()
    links = [str(tag.find_all('a')[0]) for tag in parsed_html.body.find_all('p', attrs={'class': 'author'})]
    auths = [tag.find_all('a')[1].text for tag in parsed_html.body.find_all('p', attrs={'class': 'author'})]
    posts = parsed_html.body.find_all('div', attrs={'class': 'content'})

    # find actual starting post
    startat = 0
    for i, link in enumerate(links):
        links[i] = link[link.find('"'):link.find('">')].replace(link[link.find('&amp'):link.find('#')], '').strip(
            '"').strip('.')
        if links[i][links[i].find('#'):] == url[url.find('#'):]:
            startat = i
    # cut of unneeded parts of the array
    links = links[startat:]
    auths = auths[startat:]
    posts = posts[startat:]

    chars = {}
    commanding = False
    # pars posts
    for j, stuff in enumerate(posts):
        # check if char is in
        if auths[j] not in chars.keys():
            chars[auths[j]] = Character(nicks[auths[j]], auths[j])

        for underlined in stuff.find_all('span', attrs={'style': "text-decoration: underline"}):
            underlined = removeTags(stripComment(str(underlined)))
            underlined = splitInLines(underlined)
            underlined = underlined.splitlines()
            for i, line in enumerate(underlined):
                line = line.replace('\n', '').strip()
                if line is not "":
                    if line.startswith('"'):
                        commanding = True
                    if commanding:
                        chars[auths[j]].addCommand(line)
                    else:
                        chars[auths[j]].addAction(line)
                    if line.endswith('"'):
                        commanding = False

for nick, people in chars.items():
    print(people.name)
    people.printCommands()
    people.printActions()
    print('-------')
