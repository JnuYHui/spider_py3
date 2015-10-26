#! coding=utf-8


from queue import Queue
import urllib.request
import re
import logging
logging.basicConfig(filename='proxy.log', filemode='w', level=logging.DEBUG)


"""
author: sunder
date: 2015/10/25
function: renew proxies from http://www.xici.net.co/ and write it to proxies.dat
            get proxies from proxies.dat
"""


class Proxy:
    def __init__(self, filename):
        self.proxies_filename = filename

    """
    从网站上重新获取代理
    """
    def get_from_web(self):
        of = open(self.proxies_filename, 'w')
        for position in ['nn','wn']:
            web_url = "http://www.xici.net.co/" + position
            web_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
            logging.info(u"正在从%s获取代理" % web_url)
            # 存放所有的代理
            proxies_list = []
            try:
                # 获取网页
                req = urllib.request.Request(url=web_url, headers=web_headers)
                html = urllib.request.urlopen(req).read()
                html = str(html)
                # 解析
                boxes = re.findall('<tr class=".*?">.*?</tr>', html, re.DOTALL)
                for box in boxes:
                    exp = r'<td>(.*?)</td>'
                    items = re.findall(exp, box, re.DOTALL)
                    # 存放一个代理
                    proxy = {}
                    proxy['ip'] = items[2]
                    proxy['port'] = items[3]
                    proxy['position'] = items[4]
                    proxy['anonymous'] = items[5]
                    proxy['type'] = items[6]
                    items[7] = re.search(r'title="(.*)"',items[7]).group(1)
                    proxy['speed'] = items[7]
                    items[8] = re.search(r'title="(.*)"',items[8]).group(1)
                    proxy['delay'] = items[8]
                    proxy['date'] = items[9]
                    proxies_list.append(proxy['type']+'='+proxy['ip']+':'+proxy['port'])
                    # 写入文件
                    of.write('%s=%s:%s\n' % (proxy['type'], proxy['ip'], proxy['port']))
            except Exception as e:
                logging.info(e)
            finally:
                logging.info(u"获取了%d个代理" % len(proxies_list))
                of.close()
                return list2queue(proxies_list)

    """
    从proxies.dat中读入proxies，并返回
    """
    def get_from_file(self):
        # 读入proxy
        proxies_list = []
        try:
            logging.debug('open proxies.dat')
            f = open(self.proxies_filename, 'r')
            for line in f:
                proxies_list.append(line.strip())
            f.close()
            logging.debug('close proxies.dat')
            return list2queue(proxies_list)
        except IOError as e:
            logging.debug('open proxies.dat failed')
            logging.debug(e)
            logging.debug('转为从网络获取代理')
            p = Proxy(self.proxies_filename)
            proxies_list = p.get_from_web()
            return list2queue(proxies_list)


def list2queue(a_list):
    q = Queue(len(a_list))
    for element in a_list:
        q.put(element)
    return q

