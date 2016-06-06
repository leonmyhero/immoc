coding:utf-8
from jkscrapy.items import JkscrapyItem
from scrapy.http import Request
import re
from scrapy.spiders import BaseSpider
from scrapy.selector import Selector
from jkscrapy.settings import *
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

#爬虫
class jikespider(BaseSpider):
    name = "jike"
    baseurl = "http://www.jikexueyuan.com/course/"
    starturls = ["http://www.jikexueyuan.com/"]
    allowed_domains = ["www.jikexueyuan.com", "search.jikexueyuan.com", "jikexueyuan.com"]

    def __init(self):
        self.headers = headers
        self.cookies = cookies
        pass

#爬虫 重写 BaseSpider parse
#-1、在首页中获取标签及课程对应的地址
#-2、eghttp://www.jikexueyuan.com/course/python/
    def parse(self, response):
        s_total = Selector(text=response.body).xpath('//*[@id="pager"]/div[1]/div[1]/ul/li/div/div/div/dl/dd/a/@href').extract()
        if len(s_total) > 0:
            for page in s_total:
                yield Request(page, callback=self.get_course_pages,headers=self.headers,cookies=self.cookies)
        else:
            pass

#爬虫 get_course_pages 获取课程连接
#-1、scrapy Selector xpath 获取课程地址
#-2、eg http://www.jikexueyuan.com/course/1860.html
    def get_course_pages(self, response):
        x_couses = Selector(text=response.body).xpath('//*[@id="changeid"]/ul/li/div[1]/a')
        for x in x_couses:
            try:
                href = x.select('@href').extract()[0]
                title = x.select('img/@title').extract()[0]
                yield Request(href, callback=self.get_course_detail,headers=self.headers,cookies=self.cookies)
            except:
                pass

#爬虫 get_course_detail获取课程
#-1、scrapy Selector xpath 获取课程地址
#-2、eg http://www.jikexueyuan.com/course/271_3.html?ss=1
    def get_course_detail(self, response):
        d_couses = Selector(text=response.body).xpath('//*[@id="pager"]/div[3]/div[2]/div[2]/ul/li/div/h2/a')
        for d in d_couses:
            try:
                href = d.select('@href').extract()[0]
                print(href)
                title = d.select('text()').extract()[0]

# print(" %s %s" % (href, title))
                meta ={}
                meta["href"]= href
                meta["title"]= title
                yieldRequest(href, callback=self.get_down_urls, meta={"meta": meta},headers=self.headers,cookies=self.cookies)
            except:
                pass
#爬虫 get_down_urls获取课程下地址
#-1、正则 获取课程下载地址，这个是调用flash播放地址 尝试过很多方法 最后发现正则可以
#-2、eg http://cv3.jikexueyuan.com/201509071527/df51514a02286dac0b30245eaa4dd166/html5/course_mob/01/video/c271b_03_h264_sd_960_540.mp4
    def get_down_urls(self, response):
        meta = response.meta["meta"]
        course_down = re.findall(r'source src="(.*?)"', response.body, re.S)
        item = JkscrapyItem()
        if course_down:
            item["course_id"] = meta["href"]
            item["course_name"] = meta["title"]
            item["course_path"] = course_down[0]
            yield item
