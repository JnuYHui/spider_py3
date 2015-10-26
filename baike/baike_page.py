#! coding=utf-8

import threading
import common.page
import common.proxy
import logging
logging.basicConfig(filename='page.log', filemode='w', level=logging.DEBUG)

"""
author: sunder
date: 2015/10/25
function: 获取百度百科信息
"""


class Baike:
    def __init__(self):
        logging.basicConfig(level=logging.DEBUG)
        # 获取代理
        logging.info(u'获取代理')
        p = common.proxy.Proxy('proxies.dat')
        self.proxies_list = p.get_from_file()

    def fetch(self, min_id, max_id):
        for page_id in range(min_id, max_id):
            # 获取
            page_id = str(page_id)
            url = 'http://baike.baidu.com/view/' + page_id + '.htm'
            page = common.page.Page(url)
            html = page.proxy_fetch(self.proxies_list)
            if html:
                # 转码
                html = html.decode('utf-8', 'ignore')
                html = html.encode('gbk', 'ignore')
                html = html.decode('gbk', 'ignore')
                # 写出
                outfile = 'd:/test/baikefile/' + page_id + '.html'
                f = open(outfile, 'w')
                f.write(html)
                f.close()
        logging.debug(u'任务完成'+str(min_id)+"~"+str(max_id))

    def multi_thread_fetch(self, min_id, max_id):
        total = max_id - min_id
        part = int(total / 3)
        bk = Baike()
        t1 = threading.Thread(target=bk.fetch, args=(min_id, min_id + part))
        # t2 = threading.Thread(target=bk.fetch, args=(min_id + part, min_id + 2*part))
        # t3 = threading.Thread(target=bk.fetch, args=(min_id + 2*part, max_id))
        t1.start()
        # t2.start()
        # t3.start()
        t1.join()
        # t2.join()
        # t3.join()

if __name__ == '__main__':
    bk = Baike()
    bk.multi_thread_fetch(30014, 50000)
    # bk.fetch(4000, 4010)
