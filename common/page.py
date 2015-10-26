#!encoding=utf-8


import common.proxy
import socket
import urllib.request
import logging

timeout = 10
socket.setdefaulttimeout(timeout)

"""
author: sunder
date: 2015/10/25
function: 获取网页，
            普通（匿名无代理）获取网页 fetch()
            需登录信息获取网页 auth_fetch()
            匿名使用代理获取 proxy_fetch()

"""


class Page:
    def __init__(self, url):
        self.url = url

    """
        获取需要登录的网页
    """
    def auth_fetch(self, a_url):
        username = input('input username: ')
        password = input('input password: ')
        password_mgr = urllib.request.HTTPPasswordMgrWithDefaultRealm()
        password_mgr.add_password(None, self.url, username, password)
        handler = urllib.request.HTTPBasicAuthHandler(password_mgr)
        opener = urllib.request.build_opener(handler)
        html_bytes = opener.open(a_url).read()
        return html_bytes

    """
        获取不需要登录的网页
    """

    def fetch(self):
        user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        values = {'name' : 'Michael Foord',
                  'location' : 'Northampton',
                  'language' : 'Python' }
        headers = { 'User-Agent' : user_agent }

        data = urllib.parse.urlencode(values)
        data = data.encode('utf-8')
        req = urllib.request.Request(self.url, data, headers)
        with urllib.request.urlopen(req) as response:
            the_page = response.read()
        return the_page

    """
        用代理获取不需要登录的网页,一个代理失效时，自动切换另一个代理
    """

    def proxy_fetch(self, proxies_queue):
        # 用proxy获取网页
        headers = {'Content-type': 'application/x-www-form-urlencoded',
                   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                   'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.1 '
                                 '(KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1'}

        # 是否重新获取代理
        if proxies_queue.qsize() < 1:
            logging.debug('重新获取代理')
            p = common.proxy.Proxy('proxies.dat')
            proxies_queue = p.get_from_web()
        # 当前代理
        protocol, proxy = proxies_queue.get().split('=')
        seg = proxy.split(':')
        proxy_map = {seg[0]: seg[1]}
        try:
            # 用代理获取网页
            logging.debug('正在获取 %s' % self.url)
            proxy_support = urllib.request.ProxyHandler(proxy_map)
            opener = urllib.request.build_opener(proxy_support)
            html_bytes = opener.open(self.url).read()
            logging.info('获取成功 %s' % self.url)
            proxies_queue.put(protocol + '=' + proxy)
            return html_bytes
        except Exception as e:
            # 检查代理，代理是否可用
            if check_proxy(protocol + '=' + proxy):
                # 代理可用
                proxies_queue.put(protocol + '=' + proxy)
                logging.info('网址有误 %s' % self.url)
                logging.debug(e)
                return False
            else:
                # 代理不可用
                logging.info('待验证网址 %s ' % self.url)
                return False


def check_proxy(proxy):
    protocol, proxy = proxy.split('=')
    seg = proxy.split(':')
    proxy_map = {}
    try:
        proxy_support = urllib.request.ProxyHandler(proxy_map)
        opener = urllib.request.build_opener(proxy_support)
        html = opener.open('http://www.baidu.com').read()
        return True
    except Exception as e:
        return False



