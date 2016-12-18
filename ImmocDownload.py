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


class Immoc:
    def __init__(self):
        self.indexurl = "http://www.imooc.com/learn/"
        self.videoIDs = []
        self.videoIndexUrls = []
        self.subjects = []
        self.headers = {
            'User_Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'}
        self.title = ""
        self.path = ""
        self.msgs = []

    def GetHtml(self, url):
        """
        获取页面源码
        """
        request = urllib.request.Request(url, headers=self.headers)
        return urllib.request.urlopen(request).read().decode('utf-8', 'ignore')

    def GetAllVideoIDs(self, html):
        soup = BeautifulSoup(str(html), 'html.parser')
        pattern = re.compile(u'\u2605')
        self.title = soup.find("h2", {"class": "l"}).text
        for link in soup.find_all("a", {"class": "J-media-item"}):
            vurl = link['href'].split("/")
            if vurl[1] == "video":
                self.videoIDs.append(vurl[2])
                tx = link.text
                tb = tx.strip()
                ts = tb[0: -8]
                self.subjects.append(ts)

    def GetVideoUrl(self):
        x = 0
        for vID in self.videoIDs:
            url = "http://www.imooc.com/course/ajaxmediainfo/?mid=" + vID + "&mode=flash";
            response = urllib.request.urlopen(url)
            rawdata = str(response.read())
            rdata = rawdata[2: len(rawdata) - 1]
            data = json.loads(rdata)
            videourl = data["data"]["result"]["mpath"][2]
            videourl = videourl.replace('\/', '/')
            print(videourl)
            filepath = "E:/迅雷下载/Imooc/" + self.title + "/"
            filename = self.title + " " + str(x + 1) + " " + self.subjects[x] + ".mp4"
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
        classID = 722
        url = self.indexurl + str(classID)
        shtml = self.GetHtml(url)
        self.GetAllVideoIDs(shtml)
        self.GetVideoUrl()


if __name__ == '__main__':
    immoc = Immoc()
    immoc.run()
