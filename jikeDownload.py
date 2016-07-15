# -*- coding: utf-8 -*-

import re
# import urllib2
import sys
import os
import urllib.request
import time
from win32com.client import Dispatch
import json
from bs4 import BeautifulSoup
import unicodedata
import requests

class Jikexueyuan:
    def __init__(self):
        self.indexurl = "http://www.jikexueyuan.com/course/"
        self.videoIDs = []
        self.videoIndexUrls = []
        self.subjects = []
        self.courselinks = []
        self.headers = {"Host": "www.jikexueyuan.com",
           "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36",
           "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
           "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6", "Accept-Encoding": "gzip, deflate, sdch",
           "Cookie": "sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2215512cea00e16d-07715ae6f130f2-3e64430f-1fa400-15512cea00f12c%22%7D; stat_uuid=1464899398170995176561; gr_user_id=d5127d9b-7957-4111-bcf4-0e1270e1aacf; channel=invite_100w_sharebutton_copy1; uname=weibo_ghs67rkt; uid=5251552; code=IJ5U1A; authcode=8284BHV9gX9woKXPu5BgJ8GdaMOOsrg7SmqNGWf7%2BfTNd71511PjNKUEwmmbBPPSCzqN2qUG71SO%2FaFqZbPFaWIzrG%2BcobsogzkeR9Hnq2xOE6%2BhQ%2FhMTBItCalVXNFaGNk; level_id=3; is_expire=0; domain=7945634172; connect.sid=s%3AVEtWm53fTpgq3VYc7VLZRqAyBd_C3-nw.6xaZhereKo9OluFHVosMPLOxPWafogplN6fKEYjyxGg; stat_fromWebUrl=; stat_ssid=1469241512589; stat_huodong=huodong%3Djiuye_web_shouye_banner_0910; looyu_id=0dfcfe6bda5811166dcc449b512d6b1e5b_20001269%3A5; Hm_lvt_f3c68d41bda15331608595c98e9c3915=1468328460,1468435354,1468493700,1468573043; Hm_lpvt_f3c68d41bda15331608595c98e9c3915=1468573646; _ga=GA1.2.259333669.1464899374; _gat=1; undefined=; stat_isNew=0; QINGCLOUDELB=7e36c8b37b8339126ed93010ae808701d562b81daa2a899c46d3a1e304c7eb2b|V4iny|V4ilb; gr_session_id_aacd01fff9535e79=80da58a9-0eb2-4d78-8814-1cd912fc5b9e; gr_cs1_80da58a9-0eb2-4d78-8814-1cd912fc5b9e=uid%3A5251552; _99_mon=%5B0%2C0%2C0%5D; looyu_20001269=v%3A3d798e55baaf0f37c486ede3e939018993%2Cref%3A%2Cr%3A%2Cmon%3Ahttp%3A//m9100.talk99.cn/monitor%2Cp0%3Ahttp%253A//www.jikexueyuan.com/",
           "Connection": "keep-alive"}
        self.title = ""
        self.path = ""
        self.msgs = []

    def GetHtml(self, url):
        """
        获取页面源码
        """
        r = requests.get(url, headers=self.headers)
        return r.text

    def GetAllVideoIDs(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        pattern = re.compile(u'\u2605')
        #print(html)
        #playbox = soup.find_all("div", {"id":"lessonvideo-box"})[0]
        self.title = soup.find_all("h1")[0].text
        print(self.title)
        videopage = soup.find("div", {"id":"simTestContent2"})
        for link in videopage.find_all("a"):
            self.courselinks.append(link['href'])
            self.subjects.append(link.text)
            print (link['href'])
            print (link.text)

    def GetVideoUrl(self):
        x = 0
        for url in self.courselinks:
            soup = BeautifulSoup(self.GetHtml(url), 'html.parser')
            video = soup.find_all("video")[0]
            videourl = video.find("source").get("src")
            print(videourl)
            filepath = "E:/迅雷下载/jike/Android/" + self.title + "/"
            filename = self.title + " " + self.subjects[x] + ".mp4"
            self.createThunderDownload(videourl, filename, filepath)
            time.sleep(10)
            x += 1

    def createThunderDownload(self, downurl, downfilename, downpath):
        o = Dispatch("ThunderAgent.Agent.1")
        print(downfilename)
        if downurl:
            course_path = os.getcwd()
        try:
            o.AddTask(downurl, downfilename, downpath, "", "", -1, 0, 5)
            o.CommitTasks()
            print(downurl)
        except Exception:
            print(Exception.message)
            print("AddTask is fail!")

    def run(self):
        classID = 1435
        url = self.indexurl + str(classID) + ".html"
        #print (url)
        shtml = self.GetHtml(url)
        print (shtml)
        self.GetAllVideoIDs(shtml)
        self.GetVideoUrl()


if __name__ == '__main__':
    Jikexueyuan = Jikexueyuan()
    Jikexueyuan.run()
