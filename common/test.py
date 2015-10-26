#! encoding=utf-8

import common.page
import common.proxy
import logging
logging.basicConfig(filename='page.log', filemode='w', level=logging.DEBUG)


class PageTest:
    @staticmethod
    def test_fetch():
        a_url = 'http://www.kekenet.com/'
        page = common.page.Page(a_url)
        html = page.fetch()
        html = html.decode('utf-8', 'ignore')
        html = html.encode('gbk', 'ignore')
        html = html.decode('gbk', 'ignore')
        print(html)

    @staticmethod
    def test_auth_fetch():
        a_url = 'http://www.zhihu.com/people/ceng-xiang-rong'
        page = common.page.Page('www.zhihu.com')
        html = page.auth_fetch(a_url)
        html = html.decode('utf-8', 'ignore')
        html = html.encode('gbk', 'ignore')
        html = html.decode('gbk', 'ignore')
        print(html)

    @staticmethod
    def test_proxy_fetch():
        p = common.proxy.Proxy('proxies.dat')
        proxies_list = p.get_from_file()
        proxies_list = ['http=10.10.10:1', 'http=2.2.26:12']
        page = common.page.Page('http://baike.baidu.com/subview/3077/11247674.htm')
        html = page.proxy_fetch(proxies_list)
        html = html.decode('utf-8', 'ignore')
        html = html.encode('gbk', 'ignore')
        html = html.decode('gbk', 'ignore')
        print(html)


class ProxyTest:
    @staticmethod
    def test_get_from_web():
        p = common.proxy.Proxy('proxies.dat')
        proxies = p.get_from_web()
        print(proxies)

    @staticmethod
    def test_get_form_file():
        p = common.proxy.Proxy('proxies.dat')
        proxies = p.get_from_file()
        print(proxies)

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    # PageTest.test_fetch()
    # PageTest.test_auth_fetch()
    PageTest.test_proxy_fetch()
    # ProxyTest.test_get_form_file()



