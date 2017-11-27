# -*- coding: gbk -*-

import re
# import urllib2
import sys
import os
import urllib.request
import time
#from win32com.client import Dispatch
from bs4 import BeautifulSoup

# reload(sys)
# sys.setdefaultencoding('utf-8')

class MaiZi:
    def __init__(self):
        # 麦子学院 视频初始地址
        # self.indexurl = 'http://www.maiziedu.com/course/list/?catagory=all&career=all&sort_by=&page='
        self.indexurl = 'http://www.maiziedu.com/course/'
        # 视频列表
        self.videolist = []
        # 视频索引地址
        self.videoIndexUrls = []
        # headers
        self.headers = {
            'User_Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2522.0 Safari/537.36'}
        # 全部视频urls
        self.AllVideoUrls = []
        self.AllFileNames = []
        self.courseTitle = ""
    def GetHtml(self, url):
        """
        获取页面源码
        """
        request = urllib.request.Request(url, headers=self.headers)
        return urllib.request.urlopen(request).read().decode('utf-8', 'ignore')

    def Allurls(self, html):
        """
        获取当前页面urls
        """
        soup = BeautifulSoup(str(html), 'html.parser')
        pattern = re.compile(u'\u2605')
        ul = soup.find("ul", {"class": "lesson-lists"})
        links = ul.find_all("a")
        for link in links:
            url = link["href"]
        #url = url.replace("/course/","")
        #url = url.replace("/","")
        #print (url)
            title = link.find_all("span")[0].text
        #print (title)
            urlinfo = []
            urlinfo.append(title)
            urlinfo.append(url)

            #urlsinfo = re.findall('$lessonUrl = (.*?).mp4', html, re.S)
            #print (urlsinfo)
        #for urlinfo in urlsinfo:
            print (urlinfo)
            self.videoIndexUrls.append(urlinfo)
        self.courseTitle = soup.find("h1").text
        print (self.courseTitle)
    def GetAllVideoUrls(self, html):
        """
        获取当前html内的所有视频Url
        """
        urls = re.findall('<li .*?>\s*<a href="(.*?)".*?lesson_id=\d*>(.*?)</a>', html, re.S)
        for url in urls:
            # print (url)
            self.AllVideoUrls.append(list(url))

    def GetVideoList(self, html):
        """
        获取视频地址
        """
        video = re.search('lessonUrl = "(.*)?.mp4',html)
        #soup = BeautifulSoup(str(html), 'html.parser')
        #pattern = re.compile(u'\u2605')
        #video = soup.find_all("source")[0]
        print (video.group(0)[13:])
        return video.group(0)[13:]
        #return re.findall('<source src="(.*?)" type=\'video/mp4\'/>', html, re.S)

    def createThunderDownload(self, downurl, downfilename, downpath):
        o = Dispatch("ThunderAgent.Agent.1")

        if downurl:
            course_path = os.getcwd()
        try:
            o.AddTask(downurl, downfilename, downpath, "", "", -1, 0, 5)
            o.CommitTasks()

        except Exception:
            print(Exception.message)
            print("AddTask is fail!")

    def Schedule(self, downloadSize, dataSize, remotelyfileSize):
        '''
        downloadSize:已经下载的数据块
        dataSize:数据块的大小
        remotelyFileSize:远程文件的大小
       '''
        per = 100.0 * downloadSize * dataSize / remotelyFileSize
        if per > 100:
            per = 100

        print(u'currently download percentage:%.2f%%\r' % per, )

    def run(self):
        courseID = 964
        url = self.indexurl + str(courseID)
        print (url)
        self.Allurls(self.GetHtml(url))
        x = 1
        for videoIndexurl in self.videoIndexUrls:
            title = videoIndexurl[0]
            url = 'http://www.maiziedu.com' + videoIndexurl[1]
            print(title, url)
            filepath = "E:/迅雷下载/" + self.courseTitle + "/"
            print (filepath)
            #self.AllVideoUrls.clear()
            #self.AllFileNames.clear()
            #shtml = self.GetHtml(url)
            #self.GetAllVideoUrls(shtml)
            # os.mkdir(title)
            #x=1
            #for VideoUrlin in self.AllVideoUrls:
                #title = VideoUrlin[1]
            #    if not re.search('\d', VideoUrlin[0]):
            #        url = 'http://www.maiziedu.com/' + videoIndexurl[1]
            #    else:
                #url = 'http://www.maiziedu.com/' + VideoUrlin[0]
                #print (url)
                #title = title.replace('.&nbsp;', ' ').strip()

            filename = self.courseTitle + ' ' + str(x) + ' ' + title + '.mp4'
            print (filename)
                #self.AllFileNames.append(filename)
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
            #time.sleep(15)
            x+=1
                # self.AllVideoUrls.append(video)
                # sq = re.findall('\d+.mp4',video,re.S)
                # fn = re.sub('\d+.mp4','',video)
                # print (videonum[0])
                # print (video)
                #print(self.AllFileNames)
                # for VideoUrl in self.AllVideoUrls:
                #   print (VideoUrl + '/n')
                # x=1
                # for filename in self.AllFileNames:
                #   if len(sq)>5:
                #       if x<10:
                #           print (fn + '0' + str(x) + '.mp4\n')
                #       else:
                #           print (fn + str(x) + '.mp4\n')
                #  else:
                #     print (fn + str(x) + '.mp4\n')
                # x += 1
                # urllib.urlretrieve(video, filename, self.Schedule)



if __name__ == '__main__':
    maizi = MaiZi()
    maizi.run()
