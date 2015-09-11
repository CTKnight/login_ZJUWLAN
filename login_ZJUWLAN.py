__author__ = 'ctknight'
import http.cookiejar
import urllib.request
import urllib.parse
# reference:http://blog.jobbole.com/77878/
loginURL = 'https://net.zju.edu.cn/mobile5.html'
requestURL = 'https://net.zju.edu.cn/cgi-bin/srun_portal'
UA = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36'
# static vars
username = ''
password = ''

# for storing username and password
def storeValues():
    global username
    global password
    f = open('values.txt', 'r+')
    f.write(username + ':' + password)


def inputValues(*, passwordError=False):
    global username, password
    if not username:

        username = input('请输入用户名:')
        password = input('请输入密码:')

    elif passwordError:

        username = input('请检查用户名后再次输入:')
        password = input('请检查密码后再次输入:')
    else:
        return 'unknown args'


inputValues()
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

# open loginurl and cookie will be collected automatically by cookiejar
