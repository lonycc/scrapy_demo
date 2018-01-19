# coding=utf-8
from hashlib import md5
from json import loads
from base64 import b64encode, b64decode
import re
import sys
import urllib.request
from urllib.parse import urljoin, urlencode
import http.cookiejar

def hash_md5(str_input):
    return md5(str_input.encode('utf-8')).hexdigest()

def from_jsonp(jsonp_str):
    jsonp_str = jsonp_str.strip()
    return loads(jsonp_str[1:-1])

def strip_tags(html_str):
    dr = re.compile(r'<[^>]+>', re.S)
    return dr.sub('', html_str)

def selectExists(lists):
    for i in lists:
        if i:
            return i
    return None

def getEncodeKey():
    """获取煎蛋网加密key"""
    html = crawlHtml('http://jandan.net/ooxx')
    js_reg = re.findall(r'src="//cdn.jandan.net/static/min/[\w\d\.]+.js"', html)
    js_url = 'https:' + js_reg[0][5:-1]
    js_html = crawlHtml(js_url)
    app_secret = re.findall(r'c=[\w\d\_]+\(e,"[\w\d]+"\);', js_html)
    return app_secret[0].split('"')[1]

def crawlHtml(url, referer='https://jandan.net/', host='jandan.net'):
    """获取页面源码"""
    cookie_support = urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar())
    #proxy_support = urllib.request.ProxyHandler({"http":"115.159.50.56:8080"})
    opener = urllib.request.build_opener(cookie_support, urllib.request.HTTPHandler)
    urllib.request.install_opener(opener)
    opener.addheaders = [('User-agent', 'Mozilla/5.0'), ('Accept', '*/*'), ('Referer', referer), ('Host', host)]
    try:
        urlop = opener.open(url)
        html = urlop.read().decode('utf-8')
        urlop.close()
        return html
    except Exception as e:
        print(e, url)
        sys.exit(0)

def extractPic(n, x):
    """由图片hash获取真实地址"""
    k = 'DECODE'
    f = 0
    x = hash_md5(x)
    w = hash_md5(x[0:16])
    u = hash_md5(x[16:32])
    t = n[0:4]
    r = w + hash_md5(w + t)
    n = n[4:]
    m = b64decode(n)
    h = [i for i in range(256)]
    q = [ord(r[j%len(r)]) for j in range(256)]
    o = 0
    for i in range(256):
        o = (o + h[i] + q[i]) % 256
        tmp = h[i]
        h[i] = h[o]
        h[o] = tmp
    v = o = 0
    l = ''
    for i in range(len(m)):
        v = (v + 1) % 256
        o = (o + h[v]) % 256
        tmp = h[v]
        h[v] = h[o]
        h[o] = tmp
        l += chr(ord(chr(m[i])) ^ (h[(h[v] + h[o]) % 256]))
    return l[26:]


class TransCookie(object):
    '''cookie字符串转为字典'''
    def __init__(self, cookie)
        self.cookie = cookie

    def String2Dict(self):
        itemDict = {}
        items = self.cookie.split(';')
        for item in items:
            key = item.split('=')[0].strip()
            value = item.split('=')[1]
            itemDict[key] = value
        return itemDict

if __name__ == '__main__'
    cookie = input('输入字符串格式的cookie')
    tc = TransCookie(cookie)
    print(tc)
    print(tc.String2Dict())
