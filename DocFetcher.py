# coding:utf-8
r"""
致力于把在线的文档爬下来变成电子书
包括epub和pdf
"""
import requests
from bs4 import BeautifulSoup


class DocFetcher:

    # 当前链接
    url = None
    # 当前网页源码
    html = None
    # 当前的BeautifulSoup
    soup = None

    def __init__(self, url):
        r"""
        初始化
        :param url:   当前链接
        """
        self.url = url
        self.fetch_html()

    def fetch_html(self):
        r"""
        下载html
        :return:    无
        """
        self.html = requests.get(self.url)
        self.soup = BeautifulSoup(self.html, "html.parser")





