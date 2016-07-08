import os
import pymysql.cursors

notLocateCourse = []


def checkfilename(dir, found):
    connection = pymysql.connect(host='localhost', user='root', password='', db='immoc', charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    try:
        cur = connection.cursor()
        sql = "SELECT `id`, `CourseName`, `CourseCompleted` FROM `course` WHERE `CourseName`=%s"
        cur.execute(sql, (dir))
        if cur.rowcount:
            print (dir + "found")
            sql_insert = "UPDATE `course` SET `Download`= %s WHERE `CourseName`= %s"
            cur.execute(sql_insert, (True, dir))
            connection.commit()
            found = True
        else:
            found = False
    finally:
        cur.close()
        connection.close()


for root, dirs, files in os.walk("//RT-AC3200-76A0/Education"):
    print (root)
    print (dirs)
    for dir in dirs:
        print ("dir" + dir)
        found = False
        checkfilename(dir, found)
        if found == False:
            notLocateCourse.append(dir)

for course in notLocateCourse:
    print (course)


