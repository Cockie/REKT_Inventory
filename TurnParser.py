try:
    from BeautifulSoup import BeautifulSoup
except ImportError:
    from bs4 import BeautifulSoup
from urllib import request


def stripComment(mess):
    while '((' in mess:
        mess = mess.replace(mess[mess.find('(('):mess.find('))') + 2], '')
    return mess


def removeTags(mess):
    mess = mess.replace('<span style="text-decoration: underline">', '')
    mess = mess.replace('</span>', '')
    return mess


def splitInLines(mess):
    return mess.replace('<br/>', '\n')


url = "http://forums.ltheory.com/viewtopic.php?p=127522#p127522"
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

req = request.Request(url, data=None, headers=head)
try:
    r = request.urlopen(req, timeout=15)
except Exception:
    pass
# print(r.geturl())
htmlstr = r.read()
# print(r.geturl())

try:
    htmlstr = htmlstr.decode()
except Exception as e:
    htmlstr = str(htmlstr)
# htmlstr = htmlstr.replace('\t', '').replace('\n', '')

# parse html

parsed_html = BeautifulSoup(htmlstr)
commands = []
actions = []
startat = 0
links = [str(tag.find_all('a')[0]) for tag in parsed_html.body.find_all('p', attrs={'class': 'author'})]
auths = [tag.find_all('a')[1].text for tag in parsed_html.body.find_all('p', attrs={'class': 'author'})]
posts = parsed_html.body.find_all('div', attrs={'class': 'content'})
commanding = False
for i, link in enumerate(links):
    links[i] = link[link.find('"'):link.find('">')].replace(link[link.find('&amp'):link.find('#')], '').strip(
        '"').strip('.')
    if links[i][links[i].find('#'):] == url[url.find('#'):]:
        startat = i
links = links[startat:]
auths = auths[startat:]
posts = posts[startat:]
for stuff in posts:
    for underlined in stuff.find_all('span', attrs={'style': "text-decoration: underline"}):
        underlined = removeTags(stripComment(str(underlined)))
        underlined = splitInLines(underlined)
        for line in underlined.splitlines():
            line = line.replace('\n', '').strip()
            if line is not "":
                if line.startswith('"'):
                    commanding = True
                if commanding:
                    commands.append(line)
                else:
                    actions.append(line)
                if line.endswith('"'):
                    commanding = False

print("COMMANDS:")
for stuff in commands:
    print(stuff)
print("ACTIONS")
for stuff in actions:
    print(stuff)
