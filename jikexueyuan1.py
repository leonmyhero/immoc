#定向爬取极客学院视频，原本只有年费VIP只能下载，经过分析，只要找个免费体验VIP即可爬取所有视频
#涉及的基本技术：python xpath 正则 com+
#通过python调用迅雷从组件，实现自动创建文件夹和自动添加批量下载任务，前提要成功安装迅雷和迅雷组件
#思路：path路径爬取所有标签-》搜索页面所有该课程分类-》课程页面获取课程明细-》正则分析视频地址
#极客学院的一直在改进，可能需要自己改进

import requests from lxml
import etree
import re
import sys, os, glob, time
import scrapy

reload(sys) sys.setdefaultencoding("utf-8")

#baesurl = "http://www.jikexueyuan.com/search/s/q_"
#base_path = "f:/jike/"
#heanders Cookie需要自己抓取，否则只能抓取到免费课程
headers = { "Host": "www.jikexueyuan.com", "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,/;q=0.8", "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3", "Accept-Encoding": "gzip, deflate", "Cookie": "ga=GA1.2.1700377703.1438173034; Hmlvtf3c68d41bda15331608595c98e9c3915=1438173034; MECHATLVTime=1438179151498; MECHATCKID=cookieVal=006600143817303272961295; statssid=1438985023415; statuuid=1438173038588973692017; connect.sid=s%3AWt8IWWxkVZ6zlhop7HpbG-vtXqtwIAs.QC1tYy4qV1bHOMDN0UTUfScLKFncl4NY5zAk1SS17Kw; QINGCLOUDELB=37e16e60f0cd051b754b0acf9bdfd4b5d562b81daa2a899c46d3a1e304c7eb2b|VbjfT|VbjfT; Hmlpvtf3c68d41bda15331608595c98e9c3915=1438179151; statisNew=0; statfromWebUrl=; gat=1; uname=jike76; uid=2992598; code=SMapFI; authcode=d572TzIvHFXNIVNXcNf4vI5lv1tQlyEknAG4m0mDQmvMRPa4VhDOtJXOSfO%2BeVFVPzra8M1sEkEzxqLX9qRgS6nWhd5VMobbDpeqvJ726i54TqMoDo81P4OlhQ", "Connection": "keep-alive" }

class jikeautodown: basepath = "" baseurl = "" coursetag = "" courseid = ""

def __init__(self, base_path, base_url):
    if base_path and base_url:
        self.base_path = base_path
        self.base_url = base_url
        self.get_tags()
    else:
        print("base_path and base_url is all must needed!")
        return

def run(self):
    self.get_tags()
get_tags 获取所有便签
def get_tags(self):
    url = "http://www.jikexueyuan.com/path/"
    tag_html = requests.get(url).text.decode("utf-8").encode("GB18030")
    tag_etree = etree.HTML(tag_html)
    tag_lists = [str(tag).rstrip("/")[str(tag).rstrip("/").rindex("/") + 1:] for tag in
                 tag_etree.xpath('/html/body/div[1]/div[4]/div/div[3]/div/a/@href') if tag]
    if tag_lists:
        for tag in tag_lists:
            print(tag)
            self.course_tag = tag
            self.get_total_page(tag)
get_tags 获取课程所有页面 课程分页是js生成不好直接抓取，所以就暴力了
def get_total_page(self, tag):
    if tag:
        for page in range(1, 50):
            page_url = self.base_url + tag + "?pageNum=%d" % page
            # print(page_url)
            page_html = requests.get(page_url, headers=headers).text.decode("utf-8").encode("GB18030")
            # print(page_html)
            no_userMenu = re.search(r"userMenu", page_html, re.S)
            if no_userMenu is None:
                print("please check the cookies")
                return
            no_search = re.search(r"no-search", page_html, re.S)
            if no_search:
                print("the tag ;%s,%d is biggest page" % (tag, page - 1))
                # return page_url_lists
                break
            else:
                # page_url_lists.append(page_url)
                self.get_course_pages(page_url)
                # print(page_url)
getcoursepages 获取课程详细页面
def get_course_pages(self, tag_url):
    if tag_url:
        print("the tag_url:%s " % tag_url)
        course_page_lists = self.get_xpath_lists(tag_url, headers,
                                                 '//*[@id="changeid"]/ul/li/div/div[2]/h5/a/@href')
        if course_page_lists:
            for course_page_url in course_page_lists:
                self.get_down_urls(course_page_url)
getdownurls通过正则获取视频下载地址
def get_down_urls(self, course_page_url):
    if course_page_url:
        self.course_id = course_page_url[course_page_url.rindex("/") + 1:course_page_url.rindex(".")]
        # print(course_page_url)
        print("             course_id:%s %s" % (self.course_id, course_page_url))
        course_down_lists = self.get_xpath_lists(course_page_url, headers,
                                                 '//*[@class="video-list"]/div[2]/ul/li/div/h2/a/@href')
        if course_down_lists:
            for course_down_url in course_down_lists:
                course_down_html = requests.get(course_down_url, headers=headers).text.decode("utf-8").encode(
                    "GB18030")
                course_down = re.findall(r'source src="(.*?)"', course_down_html, re.S)
                if course_down:
                    print("                     %s" % course_down[0])
                    if self.addTasktoXunlei(course_down[0]):
                        # print("                     %s is add success!" % course_down[0])
                        print("                     is add success!")
                        time.sleep(5)
getfilelists创建文件夹
def get_file_lists(self, course_tag, course_id):
    course_path = ""
    if self.base_path and os.path.exists(self.base_path) == False:
        try:
            os.mkdir(self.base_path)
        except Exception:
            print("error :%s" % Exception.message)
            return
    if course_tag and os.path.exists(self.base_path + course_tag) == False:
        try:
            os.mkdir(self.base_path + course_tag)
            # print("%s dir is create success!" % (self.base_path + course_tag))
        except Exception:
            print("dir is create error,the error is %s" % Exception.message)

    tmp = self.base_path + course_tag + "\\" + str(course_id)
    if course_id and os.path.exists(tmp) == False:
        try:
            os.mkdir(tmp)
            course_path = tmp
            # print("%s dir is create success!" % tmp)
        except Exception:
            print("dir is create error,the error is %s" % Exception.message)
            return
    else:
        course_path = tmp
    return course_path
getxpathlists 专门解析xpath，不用每次都写
def get_xpath_lists(self, url, headers, xpath):
    try:
        html = requests.get(url, headers=headers).text.decode("utf-8").encode("GB18030")
        tree = etree.HTML(html)
        lists = [str(plist) for plist in tree.xpath(xpath) if plist]
    except Exception:
        print("get xpath list is error is :%s" % Exception.message)
        return
    return lists
addTasktoXunlei 添加迅雷任，必须安装迅雷，还需要对迅雷设置默认不提醒，否则就需要手动点击确定了
def addTasktoXunlei(self, down_url):
    flag = False
    from win32com.client import Dispatch
    o = Dispatch("ThunderAgent.Agent.1")
    # http: // cv3.jikexueyuan.com / 201508011650 / a396d5f2b9a19e8438da3ea888e4cc73 / python / course_776 / 01 / video / c776b_01_h264_sd_960_540.mp4
    if down_url:
        course_infos = str(down_url).replace(" ", "").replace("http://", "").split("/")
        course_path = self.get_file_lists(self.course_tag, self.course_id)
        try:
            o.AddTask(down_url, course_infos[len(course_infos)-1], course_path, "", "http://cv3.jikexueyuan.com", 1, 0, 5)
            o.CommitTasks()
            flag = True
        except Exception:
            print(Exception.message)
            print("                     AddTask is fail!")
    return flag



if __name__ == "__main__":
    myjike = jike_auto_down("f:\\jike\\", "http://www.jikexueyuan.com/search/s/q_")
    myjike.run()
 
