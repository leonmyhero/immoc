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

class Imooc:
    def __init__(self):
        self.indexurl = "http://www.imooc.com/course/list?page="
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
        for li in soup.find_all("li", {'class':"course-one"}):
            a = li.find("a")
            self.courseID = re.findall("\d+", a['href'], re.S)[0].replace('\n', '')
            self.courseName = li.find("h5").text.replace('\n', '')
            self.courseComment = li.find("p").text.replace('\n', '')
            if li.find_all("span")[1].text == "更新完毕":
                self.courseCompleted = True
            else:
                self.courseCompleted = False
            imgurl = li.find("img")["src"]
            self.logoFileName = self.courseName.replace("/", "") + imgurl[-4:]
            imgname = self.saveImgFolder + self.logoFileName.replace('"',"")
            self.downLoadImg(imgname, imgurl)
            #print (self.courseID + " " + self.courseName + " " + self.courseComment + " " + str(self.courseCompleted))
            connection = pymysql.connect(host='localhost', user='root', password='', db='immoc', charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
            self.InsertDatabase(connection, self.courseID, self.courseName, self.courseComment, self.courseCompleted, self.logoFileName)

    def InsertDatabase(self, connection, courseID, courseName, courseComment, courseCompleted, logoFileName):
        try:
            cur = connection.cursor()
            sql = "SELECT `id`, `CourseID`, `CourseName`, `CourseCompleted` FROM `course` WHERE `CourseID` = %s and `CourseSouces`=%s and `CourseName`=%s"
            cur.execute(sql, (courseID, "Imooc.com", courseName))
            if cur.rowcount:
                rs = cur.fetchone()
                if rs["CourseCompleted"] != courseCompleted:
                    selectid = rs["CourseID"]
                    sql= "update course set courseCompleted = %s where CourseID = %s"
                    cur.execute (sql, (courseCompleted, selectid))
                    connection.commit()
            else:
                sql = "INSERT INTO `course` (`CourseName`, `CourseSouces`, `CourseCompleted`, `CourseComment`, `CourseID`, `LogoFileName`) VALUES (%s, %s, %s, %s, %s, %s)"
                cur.execute (sql, (courseName, "Imooc.com", courseCompleted, courseComment, courseID, logoFileName))
                connection.commit()
            cur.close()
        except Exception as e:
            connection.rollback()
            raise e
        finally:
            connection.close()

    def downLoadImg(self,imgname, imgURL):
        d = open(imgname, 'wb')
        red = urllib.request.Request(imgURL, headers=self.headers)
        d.write(urllib.request.urlopen(red).read())
        d.close()

    def GetMaxPage(self, html):
        soup = BeautifulSoup(str(html), 'html.parser')
        pattern = re.compile(u'\u2605')
        div = soup.find("div", {"class":"page"})
        for link in div.find_all("a"):
            if link.text == "尾页":
                print (link['href'])
                return int(re.findall("\d+", link['href'], re.S)[0])

    def run(self):
        shtml = self.GetHtml(self.indexurl)
        maxPage = self.GetMaxPage(shtml)
        print (maxPage)
        page = 0
        while page <= maxPage:
            url = self.indexurl + str(page)
            self.GetAllCourseInfo(self.GetHtml(url))
            time.sleep(5)
            page += 1



if __name__ == '__main__':
    imooc = Imooc()
    imooc.run()
