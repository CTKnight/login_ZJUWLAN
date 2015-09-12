__author__ = 'ctknight'
# reference:http://blog.jobbole.com/77878/
import http.cookiejar
import urllib.request
import urllib.parse


# loginURL = 'https://net.zju.edu.cn/mobile5.html'
# loginURL is invalid,use requestURL instead
requestURL = 'https://net.zju.edu.cn/cgi-bin/srun_portal'
UA = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36'
# static vars
username = ''
password = ''
# initiate values

try:
    f = open('values.txt', 'r+')
except FileNotFoundError:
    f = open('values.txt', 'w')
    f.close()
# check values.txt


def storeValues():
    global username, password

    f = open('values.txt', 'r+')
    f.write(username + ':' + password)


# for storing username and password

def readValues():
    global username, password

    f = open('values.txt', 'r+')
    s = f.read()
    if s:
        # check s
        username, password = s.split(':')
    else:
        inputValues()


# for reading stored values

def inputValues(*, passwordError=False):
    global username, password
    if not username:

        username = input('请输入用户名:')
        password = input('请输入密码:')
        storeValues()
    elif passwordError:

        username = input('请检查用户名后再次输入:')
        password = input('请检查密码后再次输入:')
        storeValues()
    else:
        return 'unknown args'

# for reading user's input

readValues()

# input username and password
values = {'username': username,
          'password': password,
          'action': 'login',
          'ac_id': 5,
          'is_ldap': 1,
          'type': 2,
          'local_auth': 1}
# store them in a dict
# thanks to Fiddler2
data = urllib.parse.urlencode(values).encode(encoding='UTF8')
# encode them
cookie = http.cookiejar.CookieJar()
handler = urllib.request.HTTPCookieProcessor(cookie)
opener = urllib.request.build_opener(handler)
opener.addheaders = [('User-agent', UA)]
# cookie and header stuff
urllib.request.install_opener(opener)
request = urllib.request.Request(requestURL, data)
url = opener.open(request)
page = url.read()

# open requesturl and cookie will be collected automatically by cookiejar
