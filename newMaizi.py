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
        self.indexurl = "http://www.maiziedu.com/course/"
        self.videoIDs = []
        self.videoIndexUrls = []
        self.subjects = []
        self.courselinks = []
        self.headers = {"Host": "www.maiziedu.com",
           "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2486.0 Safari/537.36 Edge/13.10586",
           "Accept": "text/html, application/xhtml+xml, image/jxr, */*",
           "Accept-Language": "en-GB, en; q=0.8, zh-Hans-CN; q=0.5, zh-Hans; q=0.3",
           "Cookie": "53gid2=10164662171009; 53revisit=1464624095671; maiziuid=45d9531dbc8eff94663e18e7c3078e07; _gat=1; isLoadPage=loaded; 53gid0=10164662171009; 53gid1=10164662171009; 53uvid=1; onliner_zdfq72111642=0; maiziedu=0ae7pznqgoetz6xblu8ukj0hmoqh8und; responseTimeline=339; SERVERID=4167573bb07fa323552b6b17d0ac903c|1481288032|1481287993; _zg=%7B%22uuid%22%3A%20%2215502661341542-0784e90b93a31e-3e64430f-1fa400-155026613456eb%22%2C%22sid%22%3A%201481288087.968%2C%22updated%22%3A%201481288125.033%2C%22info%22%3A%201481288087973%7D; _ga=GA1.2.696380383.1464624091; Hm_lvt_e3879546912fd4b2d6e909e064d49262=1481288087; Hm_lpvt_e3879546912fd4b2d6e909e064d49262=1481288126; visitor_type=old; 53kf_72111642_keyword=; kf_72111642_keyword_ok=1",
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
        ul = soup.find("ul", {"class": "lesson-lists"})
        links = ul.find_all("a")
        for link in links:
            url = link["href"]
            print(url)
            # url = url.replace("/course/","")
            # url = url.replace("/","")
            # print (url)
            title = link.find_all("span")[0].text
            # print (title)
            urlinfo = []
            urlinfo.append(title)
            urlinfo.append(url)

            # urlsinfo = re.findall('<li><a href="/course/[0-9]{1,4}-[0-9]{1,4}"', html, re.S)
            # print (urlsinfo)
            # for urlinfo in urlsinfo:
            print(urlinfo)
            self.videoIndexUrls.append(urlinfo)
        self.courseTitle = soup.find("h1").text
        print(self.courseTitle)

    def GetVideoList(self, html):
        """
        获取视频地址
        """

        #print (html)
        video = re.findall('http://(.*?)\.mp4', html)[0]
        print (video)
        #soup = BeautifulSoup(str(html), 'html.parser')
        #pattern = re.compile(u'\u2605')
        #video = soup.find_all("video")[0]
        #print (video["src"])
        #print (video)
        #return video["src"]
        return "http://" + video + ".mp4"

    def GetVideoUrl(self):
        x = 0
        for url in self.courselinks:
            soup = BeautifulSoup(self.GetHtml(url), 'html.parser')
            video = soup.find_all("video")[0]
            videourl = video.find("source").get("src")
            print(videourl)
            filepath = "E:/迅雷下载/Maizi/" + self.title + "/"
            filepath = filepath.replace(":","-")
            filename = self.title + " " + self.subjects[x] + ".mp4"
            filename = filename.replace(":","-")
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
        classIDArray = [942, 943, 944]
        for classID in classIDArray:
            #classID = 541
            url = self.indexurl + str(classID) + "/"
            print (url)
            self.videoIndexUrls.clear()


            shtml = self.GetHtml(url)
            #print (shtml)
            self.GetAllVideoIDs(shtml)
            for videoIndexurl in self.videoIndexUrls:
                title = videoIndexurl[0]
                url = 'http://www.maiziedu.com' + videoIndexurl[1]
                print(title, url)
                filepath = "E:/迅雷下载/Maizi/" + self.courseTitle + "/"
                print(filepath)
                # self.AllVideoUrls.clear()
                # self.AllFileNames.clear()
                # shtml = self.GetHtml(url)
                # self.GetAllVideoUrls(shtml)
                # os.mkdir(title)
                # x=1
                # for VideoUrlin in self.AllVideoUrls:
                # title = VideoUrlin[1]
                #    if not re.search('\d', VideoUrlin[0]):
                #        url = 'http://www.maiziedu.com/' + videoIndexurl[1]
                #    else:
                # url = 'http://www.maiziedu.com/' + VideoUrlin[0]
                # print (url)
                # title = title.replace('.&nbsp;', ' ').strip()

                filename = self.courseTitle + title + '.mp4'
                print(filename)
                # self.AllFileNames.append(filename)
                # print (filename)
                # f = open("MaiZi.txt","w",encoding="utf-8")
                # f.write(filename + '\n')
                # f.close()
                # video = self.GetVideoList(shtml)[0]
                # print (video)
                video = self.GetVideoList(self.GetHtml(url))
                print(video)
                self.createThunderDownload(video, filename, filepath)
                # print (re.findall('.com/+.mp4',video,re.S))
                time.sleep(15)


if __name__ == '__main__':
    Jikexueyuan = Jikexueyuan()
    Jikexueyuan.run()
