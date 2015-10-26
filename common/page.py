#!encoding=utf-8

from queue import Queue
import common.proxy
import threading
import random
import urllib.request
from urllib.error import URLError
import logging
logging.basicConfig(filename='page.log', filemode='w', level=logging.DEBUG)

"""
author: sunder
date: 2015/10/25
function: 获取网页，
            普通（匿名无代理）获取网页 fetch()
            需登录信息获取网页 auth_fetch()
            匿名使用代理获取 proxy_fetch()

"""

lock = threading.Lock()
class Page:
    def __init__(self, url):
        self.url = url
        print(url)

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
        logging.debug(u'开始获取网页' + self.url)
        headers = {'Content-type': 'application/x-www-form-urlencoded',
                   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                   'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.1 '
                                 '(KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1'}
        if proxies_queue.qsize() < 1:
            p = common.proxy.Proxy('proxies.dat')
            proxies_queue = p.get_from_web()
            # logging.debug('缺少代理')
            # return False
        loop_times = 0
        while loop_times < 3:
            protocol, proxy = proxies_queue.get().split('=')
            logging.debug('\t%d-loops, proxy is: %s ' % (loop_times + 1, proxy))
            seg = proxy.split(':')
            proxy_map = {seg[0]: seg[1]}
            try:
                # 用代理获取网页
                proxy_support = urllib.request.ProxyHandler(proxy_map)
                opener = urllib.request.build_opener(proxy_support)
                html_bytes = opener.open(self.url).read()
                logging.debug('获取成功')
                proxies_queue.put(protocol + '=' + proxy)
                return html_bytes
            except URLError as e:
                if hasattr(e, 'reason'):
                    loop_times += 1
                    print('We failed to reach a server.')
                    print('Reason: ', e.reason)
                elif hasattr(e, 'code'):
                    print('The server couldn\'t fulfill the request.')
                    print('Error code: ', e.code)
                    print('无法获取%s' % self.url)
                    logging.debug('获取失败')
                    return False
                logging.debug(e)
                if check_proxy(protocol + '=' + proxy):
                    proxies_queue.put(protocol + '=' + proxy)
        print('无法获取%s' % self.url)
        logging.debug('获取失败')
        return False


def check_proxy(proxy):
    proxies_queue = Queue(1)
    proxies_queue.put(proxy)
    p = Page('www.baidu.com')
    if p.proxy_fetch(proxies_queue):
        return True
    else:
        return False


def list_del(a_list, element_number):
    lock.acquire()
    a_list.remove(element_number)
    lock.release()


def list_random_chose(proxies_list):
    lock.acquire()
    # 随机选择一个代理
    proxy_num = random.randint(0, len(proxies_list) - 1)
    proxy_info = proxies_list[proxy_num].split('=')
    proxy = {proxy_info[0]: proxy_info[1]}
    lock.release()
    return [proxy, proxy_num]


    """
        用代理获取需要登录的网页
    """

    # def proxy_auth_fetch(self, a_url, proxies_list):
    #     logging.info('fetch %s' % self.url)
    #
    #     looptimes = 0  # 循环次数
    #     while looptimes < 3:
    #         try:
    #             # 随机使用一个代理
    #             randnum = random.randint(0, len(proxieslist) - 1)
    #             proxyinfo = proxieslist[randnum].split('=')
    #             proxy = {proxyinfo[0]: proxyinfo[1]}
    #             logging.debug('proxy: %s' % proxieslist[randnum])
    #             proxy_handler = urllib2.ProxyHandler(proxy)
    #             opener = urllib2.build_opener(cookie_handler, proxy_handler)
    #             r = opener.open(req)
    #             html = r.read()
    #             logging.info('fetch succeed %r' % r.code)
    #             return html
    #         except Exception as e:
    #             logging.debug(e)
    #             del proxieslist[randnum]
    #     logging.error('fetch failed')
    #     return False

