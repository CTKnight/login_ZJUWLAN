__author__ = 'ctknight'
# reference:http://blog.jobbole.com/77878/
import http.cookiejar
import urllib.request
import urllib.parse


# loginURL = 'https://net.zju.edu.cn/mobile5.html'
# loginURL is invalid,use requestURL instead
requestURL = 'https://net.zju.edu.cn/cgi-bin/srun_portal'
extraURL = 'https://net.zju.edu.cn/rad_online.php'
UA = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36'
# static vars
username = ''
password = ''
page = ''
# initiate values
def initfile():
    f = open('values.txt', 'w')
    f.close()



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

        username = input('username:')
        password = input('password:')
        storeValues()
    elif passwordError:
        initfile()
        username = input('retype username:')
        password = input('retype password:')
        storeValues()
    else:
        return 'unknown args'

# for reading user's input
def request(url,value):

    data = urllib.parse.urlencode(value).encode(encoding='UTF8')
# encode them
    cookie = http.cookiejar.CookieJar()
    handler = urllib.request.HTTPCookieProcessor(cookie)
    opener = urllib.request.build_opener(handler)
    opener.addheaders = [('User-agent', UA)]
# cookie and header stuff
    urllib.request.install_opener(opener)
    request = urllib.request.Request(url, data)
    response = opener.open(request)
    global page
    page = response.read()
# open requesturl and cookie will be collected automatically by cookiejar

try:
    f = open('values.txt', 'r+')
except FileNotFoundError:
    initfile()
# check values.txt,if it doesn't exist,create one
readValues()

# input username and password
requestvalues = {
    'username': username,
    'password': password,
    'action': 'login',
    'ac_id': 5,
    'is_ldap': 1,
    'type': 2,
    'local_auth': 1}
extravalues = {
    'action':'auto_dm',
    'uid':1,
    'username':username,
    'password':password}
# store them in a dict
# thanks to Fiddler2

request(requestURL,requestvalues)

if page == b'online_num_error':
    print('online_num_error')
    # catch online_num_error, try to kick off the other device
    request(extraURL,extravalues)
    # send request to kick off
    request(requestURL,requestvalues)
    # login again
elif page == b'': #//TODO: check wrong username and password
    ...
else:
    print('%s login successfully!'%(username))

