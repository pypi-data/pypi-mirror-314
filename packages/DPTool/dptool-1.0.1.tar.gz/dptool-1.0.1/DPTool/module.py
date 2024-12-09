from DrissionPage import Chromium, ChromiumOptions
from DrissionPage.errors import *
import threading
import numpy as np
import re

class DPTool:
    print('本脚本基于DrissionPage提供API运行\n喜欢本功能请给DrissionPage作者g1879买杯咖啡，支持原作者\nDrissionPage Github: https://github.com/g1879/DrissionPage')
    def __init__(self, data, proxy: str=None, headless: bool=False, num_threads: int=1):
        # initialize
        self.co = ChromiumOptions()
        self.co.no_imgs(True).no_js(True).headless(headless)
        # proxy
        if proxy:
            self.co.set_proxy(f'http://{proxy}')
        else:
            pass
        self.browser = Chromium(addr_or_opts=self.co)
        self.browser.set.retry_times(0)
        # multi
        count = 1
        while count < num_threads:
            self.browser.new_tab()
            count += 1
        for tab in self.browser.get_tabs():
            self.tab_init(tab)
        # chunks
        self.chunks = np.array_split(np.array(data), num_threads)
        # results
        self.results=[]

    def tab_init(self, tab):
        self.browser.clear_cache()
        tab.get('https://www.baidu.com')

    def load_check(self, tab, wait_time):
        while True:
            try:
                tab.wait.doc_loaded(timeout=wait_time)
                break
            except WaitTimeoutError:     
                self.browser.clear_cache()
                tab.refresh()

    def baidu_index_checker(self, tab_id: str, url: str):
        tab = self.browser.get_tab(tab_id)
        ele = tab.ele('@@id=kw')
        ele.clear()
        ele.input(url+'\n')

        # 加载检测
        self.load_check(tab, 10)

        # 正确页面检测
        while True:
            if url in tab.title:
                break
            else:
                self.tab_init(tab)
                ele = tab.ele('@@id=kw')
                ele.clear()
                ele.input(url+'\n')
                self.load_check(tab, 10)

        div_list = tab.eles('tag:div').get.attrs('mu')
        if url in list(filter(None, div_list)):
            return (url, '已收录')
        elif '抱歉，未找到相关结果' in tab.html:
            return (url, '未收录')
        
    def distributor(self, tab_id: str, chunk):
        result = list()
        for index, i in enumerate(chunk):
            result.append(self.baidu_index_checker(tab_id=tab_id, url=i))
        self.results.append(result)
        print(f"网页{tab_id}: 已完成")

    def threads_processor(self):
        threads = []
        for index, tab in enumerate(self.browser.get_tabs()):
            threads.append(threading.Thread(target=self.distributor, args=(tab.tab_id, self.chunks[index])))
            threads[-1].start()
        for thread in threads:
            thread.join()
    