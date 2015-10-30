#! coding=utf-8
__author__ = 'SunderLab'

import re


class Parser:
    @staticmethod
    def get_title(content):
        title = re.findall('<title>(.*?)</title>', content, re.DOTALL)[0]
        return title

    @staticmethod
    def get_basic_info(content):
        try:
            basic_info = re.findall(r'<div class="basic-info">(.*?)</div>', content, re.DOTALL)[0]
        except IndexError as e:
            print('没有 info box')
            return {}
        item_name = re.findall(r'<dt class="basicInfo-item name">(.*?)</dt>', basic_info, re.DOTALL)
        item_value = re.findall(r'<dd class="basicInfo-item value">(.*?)</dd>', basic_info, re.DOTALL)
        info = {}
        if len(item_value) == len(item_name):
            for i in range(0, len(item_name)):
                key = item_name[i]
                value = item_value[i]
                #  清洗
                key = key.replace('&nbsp;', '')
                value = value.replace('\n', '')
                info[key] = value
        return info

    @staticmethod
    def get_body(content):
        paragraphs = re.findall(r'<div class="para">(.*?)</div>', content, re.DOTALL)
        body = ''
        for para in paragraphs:
            body += para + '\n'
        body = body.replace('&quot;', '"')
        return body

if __name__ == '__main__':
    f = open('d:/test/baikefile/95985.html')
    content = ''
    for line in f:
        content += line

    title = Parser.get_title(content)
    print(title)
    basic_info = Parser.get_basic_info(content)
    print(basic_info)
    body = Parser.get_body(content)
    print(body)


