__author__ = 'ctknight'
# reference:http://blog.jobbole.com/77878/
import http.cookiejar
import urllib.request
import urllib.parse
import os.path


# loginURL = 'https://net.zju.edu.cn/mobile5.html'
# loginURL is invalid,use loginUrl instead
loginUrl = 'https://net.zju.edu.cn/include/auth_action.php'
logoutUrl = 'https://net.zju.edu.cn/cgi-bin/srun_portal'
UA = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36'
# static vars
username = ''
password = ''
page = ''
requestvalues = {}
extravalues = {}
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
    global username, password, extravalues, requestvalues
    if not username:
        # check empty username
        username = input('username:')
        password = input('password:')
        storeValues()
        setValues()
    elif passwordError:
        initfile()
        username = input('retype username:')
        password = input('retype password:')
        storeValues()
        setValues()
    else:
        return 'unknown args'


# for reading user's input
def request(url, value):
    data = urllib.parse.urlencode(value).encode(encoding='UTF8')
    # encode them
    cookie = http.cookiejar.CookieJar()
    handler = urllib.request.HTTPCookieProcessor(cookie)
    opener = urllib.request.build_opener(handler)
    opener.addheaders = [('User-agent', UA),
                         ('X-Requested-With', 'XMLHttpRequest'),
                         ('Origin', 'https://net.zju.edu.cn'),
                         ('Referer', 'https://net.zju.edu.cn/srun_portal_pc.php?url=http://www.baidu.com/&ac_id=3')]
    # cookie and header stuff
    urllib.request.install_opener(opener)
    request = urllib.request.Request(url, data)
    response = opener.open(request)
    return response.read()
    # open loginUrl and cookie will be collected automatically by cookiejar


def setValues():
    global loginValues, logoutValues
    loginValues = {
        'username': username,
        'password': password,
        'action': 'login',
        'ac_id': 3,
        'save_me': 1,
        'ajax': 1}
    logoutValues = {
        'username': username,
        'password': password,
        'action': 'login',
        'ajax': 1}


# store them in a dict
# thanks to Fiddler2

def checkStatus(page):
    if page.startswith(b'E2532'):
        print('online_num_error')
        # catch online_num_error, try to kick off the other device
        request(logoutUrl, logoutValues)
        # send request to kick off
        page1 = request(loginUrl, loginValues)
        # login again
        checkStatus(page1)


    elif (page.startswith(b'E2901')):
        # check wrong username and password
        print('bad username or password')
        inputValues(passwordError=True)
        page3 = request(loginUrl, requestvalues)
        checkStatus(page3)

    elif page.startswith(b'login_ok'):
        print('%s login successfully!' % (username))
    else:
        print('unknown response:', page)

# let's start!
if not os.path.isfile('values.txt'):
    initfile()
# check values.txt,if it doesn't exist,create one
readValues()
setValues()
page2 = request(loginUrl, loginValues)
checkStatus(page2)
dict()
