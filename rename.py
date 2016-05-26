import os, sys

#for filename in os.listdir("/Users/mingtaozhang/Downloads"):
#    print (filename)
projectName = "Cocos2d-x游戏之七夕女神抓捕计划"
newNames = ['1 - 女神我来了',
'3 - 工具篇(上)',
'6 - 场景篇-场景跳转',
'7 - 战斗UI',
'8 - 摇杆实现一',
'9 - 遥感实现二',
'2 - 游戏展示',
'5 - 场景篇-场景控制器',
'10 - 遥感实现三',
'4 - 工具篇(下)',
'11 - 遥感实现四',
'12 - 角色属性设置一',
'14 - 角色容器类',
'15 - 角色移动一',
'13 - 角色属性设置二',
'17 - 角色AI-绘制攻击框',
'16 - 角色移动二',
'18 - 角色AI 人脸朝向(上)',
'19 - 角色AI人脸朝向(下)',
'20 - 敌人移动',
'21 - 主角攻击',
'22 - 碰撞检测',
'24 - 释放对象',
'23 - 飘血',
'25 - 数据管理类(上)',
'26 - 数据管理类(中)',
'27 - 数据管理类(下)',
'28 - 对白(上)',
'29 - 对白(中)',
'30 - 对白(下)',
'31 - 后记']

targetNames = []
startNum = 472
NumofFiles = 31

folderPath = "/Users/mingtaozhang/Downloads/"

if not os.path.isdir(folderPath + projectName):
    os.makedirs(folderPath + projectName)

for x in range(0,NumofFiles):
    oldname = folderPath + "H_"+ str(startNum+x) + ".mp4"
    newname = folderPath + projectName + "/" + projectName + " " + newNames[x] + ".mp4"
    os.rename(oldname,newname)



