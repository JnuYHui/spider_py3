#! coding=utf-8

import threading
import common.page
import common.proxy
import logging


"""
author: sunder
date: 2015/10/25
function: 获取百度百科信息
"""


class Baike:
    def __init__(self):
        # 获取代理
        logging.info('获取代理')
        p = common.proxy.Proxy('proxies.dat')
        self.proxies_queue = p.get_from_file()

    def fetch(self, min_id, max_id):
        for page_id in range(min_id, max_id):
            # 获取
            page_id = str(page_id)
            url = 'http://baike.baidu.com/view/' + page_id + '.htm'
            page = common.page.Page(url)
            html = page.proxy_fetch(self.proxies_queue)
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
                logging.debug('写入完成 %s' % page_id)
        logging.info('子任务完成 '+str(min_id)+"~"+str(max_id))

    @staticmethod
    def multi_thread_fetch(min_id, max_id):
        total = max_id - min_id
        part = int(total / 3)
        bk = Baike()
        t1 = threading.Thread(target=bk.fetch, args=(min_id, min_id + part))
        t2 = threading.Thread(target=bk.fetch, args=(min_id + part, min_id + 2*part))
        t3 = threading.Thread(target=bk.fetch, args=(min_id + 2*part, max_id))
        t1.start()
        t2.start()
        t3.start()
        t1.join()
        t2.join()
        t3.join()
        logging.info('完成')

    @staticmethod
    def multi_thread_fetch(min_id, max_id, thread_num):
        total = max_id - min_id
        part = int(total / thread_num)
        bk = Baike()
        my_thread = []
        # 创建线程
        for i in range(0, thread_num):
            if i == thread_num - 1:
                a = min_id + i*part
                b = max_id
                t = threading.Thread(target=bk.fetch, args=(min_id + i*part, max_id))
            else:
                a = min_id + i*part
                b = min_id + (i + 1)*part
                t = threading.Thread(target=bk.fetch, args=(min_id + i*part, min_id + (i + 1)*part))
            my_thread.append(t)
        # 启动线程
        for t in my_thread:
            t.start()
            logging.info('%d 线程启动' % t.ident)
        for t in my_thread:
            t.join()
        logging.info('完成')

if __name__ == '__main__':
    # 设置输出日志格式
    logging.basicConfig(filename='baike.log',
                        filemode='w',
                        level=logging.INFO,
                        format='%(asctime)s:%(levelname)s:%(message)s')
    # bk = Baike()
    # bk.fetch(4000, 4010)
    # Baike.multi_thread_fetch(90000, 150000)
    Baike.multi_thread_fetch(150300, 200000, 6)


