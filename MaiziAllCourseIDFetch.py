# -*- coding: utf-8 -*-

import re
import pymysql.cursors
import sys
import os
import urllib.request
import time
from win32com.client import Dispatch
import json
from bs4 import BeautifulSoup
import unicodedata
try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse
from urllib.parse import urlparse

class Imooc:
    def __init__(self):
        self.indexurl = "http://www.maiziedu.com/course/list/all-all/0-"
        self.courseName = ''
        self.courseComment = ''
        self.courseCompleted = True
        self.headers = {
            'User_Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2522.0 Safari/537.36'}
        self.courseID = ""
        self.logoFileName = ""
        self.saveImgFolder = 'E:/CourseImages/'

    def GetHtml(self, url):
        """
        获取页面源码
        """
        request = urllib.request.Request(url, headers=self.headers)
        return urllib.request.urlopen(request).read().decode('utf-8', 'ignore')

    def GetAllCourseInfo(self, html):
        soup = BeautifulSoup(str(html), 'html.parser')
        pattern = re.compile(u'\u2605')
        ul = soup.find("ul", {"class":"zy_course_list"})
        for li in ul.find_all("li"):
            a = li.find("a")
            self.courseID = re.findall("\d+", a['href'], re.S)[0].replace('\n', '')
            #self.courseName = a.text.replace('\n', '')
            print (self.courseID)

            #p = li.find("p")
            #print (li.find("p", {"class": "font14"}).text)
            self.courseName =li.find("p", {"class": "font14"}).text
            self.courseComment = li.find("p", {"class": "font14"}).text
            print(self.courseName)
            imgurl = li.find("img")["src"]
            print (li.find_all("li")[1])
            if li.find_all("i")[1]["class"] == "VLCico status_end":
                self.courseCompleted = True
            else:
                self.courseCompleted = False
            self.logoFileName = self.courseName.replace("/", "") + imgurl[-4:]
            imgname = self.saveImgFolder + self.logoFileName.replace('"',"")
            imgurl = "http://www.maiziedu.com" + imgurl
            print (imgurl)
            #self.downLoadImg(imgname, imgurl)
            #self.createThunderDownload(imgurl,"",self.saveImgFolder)
            #print (self.courseID + " " + self.courseName + " " + self.courseComment + " " + str(self.courseCompleted))
            connection = pymysql.connect(host='localhost', user='root', password='', db='immoc', charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
            self.InsertDatabase(connection, self.courseID, self.courseName, self.courseComment, self.courseCompleted, self.logoFileName)

    def InsertDatabase(self, connection, courseID, courseName, courseComment, courseCompleted, logoFileName):
        try:
            cur = connection.cursor()
            sql = "SELECT `id`, `CourseID`, `CourseName`, `CourseCompleted` FROM `course` WHERE `CourseID` = %s and `CourseSouces`=%s and `CourseName`=%s"
            cur.execute(sql, (courseID, "maiziedu.com", courseName))
            if cur.rowcount:
                rs = cur.fetchone()
                if rs["CourseCompleted"] != courseCompleted:
                    selectid = rs["CourseID"]
                    sql= "update course set courseCompleted = %s where CourseID = %s"
                    cur.execute (sql, (courseCompleted, selectid))
                    connection.commit()
                sql= "update course set CourseSouces = %s where CourseID = %s"
                cur.execute(sql, ("maiziedu.com", selectid))
                connection.commit()

            else:
                sql = "INSERT INTO `course` (`CourseName`, `CourseSouces`, `CourseCompleted`, `CourseComment`, `CourseID`, `LogoFileName`) VALUES (%s, %s, %s, %s, %s, %s)"
                cur.execute (sql, (courseName, "maiziedu.com", courseCompleted, courseComment, courseID, logoFileName))
                connection.commit()
            cur.close()
        except Exception as e:
            connection.rollback()
            raise e
        finally:
            connection.close()

    def downLoadImg(self,imgname, imgURL):
        parsed_link = urllib.parse.urlsplit(imgURL.encode('utf8'))
        print (parsed_link)
        parsed_link = parsed_link._replace(path=urllib.quote(parsed_link.path))
        print (parsed_link)
        d = open(imgname, 'wb')
        red = urllib.request.Request(parsed_link, headers=self.headers)
        d.write(urllib.request.urlopen(red).read().encode('utf-8'))
        d.close()

    def GetMaxPage(self, html):
        soup = BeautifulSoup(str(html), 'html.parser')
        pattern = re.compile(u'\u2605')
        div = soup.find("div", {"class":"page"})
        for link in div.find_all("a"):
            if link.text == "尾页":
                print (link['href'])
                return int(re.findall("\d+", link['href'], re.S)[0])

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
        page = 1
        #shtml = self.GetHtml(self.indexurl + str(page))
        #maxPage = int(re.findall('<span id="page-pane2">(.*?)</span>', shtml, re.S)[0])
        maxPage = 36
        while page <= maxPage:
            url = self.indexurl + str(page)
            print (url)
            self.GetAllCourseInfo(self.GetHtml(url))
            time.sleep(5)
            page += 1



if __name__ == '__main__':
    imooc = Imooc()
    imooc.run()
