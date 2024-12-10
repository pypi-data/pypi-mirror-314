from DrissionPage import Chromium, ChromiumOptions
from DrissionPage.errors import *
import threading
import numpy as np
import time, random

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
            tab.get('https://www.baidu.com')
        # chunks
        self.chunks = np.array_split(np.array(data), num_threads)
        # results
        self.results=[]

    def search_processor(self, tab, url):
        ele = tab.ele('@@id=kw')
        ele.clear()
        ele.input(url+'\n')

    def baidu_index_checker(self, tab_id: str, url: str):
        tab = self.browser.get_tab(tab_id)
        self.search_processor(tab, url)

        # 加载检测
        while True:
            try:
                tab.wait.title_change(url)
                tab.wait.doc_loaded()
                break
            except:
                time.sleep(random.uniform(0.3,0.5))
                tab.back()
                self.browser.clear_cache()
                self.search_processor(tab, url)

        # 正确页面检测
        while True:
            try:
                if url in tab.title:
                    if tab.ele('tag:div@id=wrapper_wrapper'):
                        break
                    else:
                        raise ValueError
                else:
                    raise ValueError
            except ValueError:
                time.sleep(random.uniform(0.3,0.5))
                tab.back()
                self.browser.clear_cache()
                self.search_processor(tab, url)

        div_list = tab.eles('tag:div').get.attrs('mu')
        time.sleep(random.uniform(0.3,0.5))
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
    