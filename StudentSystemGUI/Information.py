
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys
import json
import qtawesome
from traceback import print_exc

class Information(QWidget):
    def __init__(self,DataId):
        super().__init__()
        self.initUI(DataId)
    #   主界面UI
    def initUI(self,DataId):
        #   主窗口大小
        self.windowX = 300
        self.windowY = 480
        self.resize(self.windowX, self.windowY)

        #   设置窗口隐藏背景和边框、去除标题栏
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint)
 
        #   设置透明背景
        self.background = QLabel(self)
        #   85%透明度白色背景，10px大小平滑角
        self.background.setStyleSheet("background-color:rgba(135,206,250,0.9);border:1px;border-radius:10px")
        self.background.setGeometry(0,0,self.windowX,self.windowY)

        #   读取信息文件
        self.LoadLoginData()

        #   退出按钮
        self.QuitButton = QPushButton(qtawesome.icon('fa.times', color='white'),"",self)
        self.QuitButton.setStyleSheet("background-color:rgba(135,206,250,0)")
        self.QuitButton.setIconSize(QSize(20, 20))
        self.QuitButton.setGeometry(270,10,20,20)
        self.QuitButton.setToolTip("退出")
        self.QuitButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.QuitButton.clicked.connect(self.close)

        #   最小化按钮
        self.MinimizeButton = QPushButton(qtawesome.icon('fa.minus', color='white'),"",self)
        self.MinimizeButton.setStyleSheet("background-color:rgba(135,206,250,0)")
        self.MinimizeButton.setIconSize(QSize(20, 20))
        self.MinimizeButton.setGeometry(240,10,20,20)
        self.MinimizeButton.setToolTip("最小化")
        self.MinimizeButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.MinimizeButton.clicked.connect(self.showMinimized)

        #   装饰文字
        self.TitleText = QLabel(self)
        self.TitleText.setText("个人信息")
        self.TitleText.setFont(QFont("黑体",10))
        self.TitleText.setStyleSheet("background-color:rgba(135,206,250,0);color:white")
        self.TitleText.setGeometry(20,15,70,20)

        #   装饰图像
        self.UserHead = QPushButton(qtawesome.icon('fa.address-card', color='white'),"",self)
        self.UserHead.setIconSize(QSize(140,140))
        self.UserHead.setStyleSheet("background-color:rgba(135,206,250,0)")
        self.UserHead.setGeometry(80,70,140,140)
            
        #   用户名字
        self.Name = QLabel(self)
        self.Name.setFont(QFont("黑体",10))
        self.Name.setText("姓名：" + self.LoginData[DataId]["Name"])
        self.Name.setStyleSheet("background-color:rgba(135,206,250,0);color:white")
        self.Name.setGeometry(50,300,200,20)

        #   编号
        self.Num = QLabel(self)
        self.Num.setFont(QFont("黑体",10))
        self.Num.setStyleSheet("background-color:rgba(135,206,250,0);color:white")
        self.Num.setGeometry(50,330,200,20)

        #   性别
        self.Sex = QLabel(self)
        self.Sex.setFont(QFont("黑体",10))
        self.Sex.setText("性别："+self.LoginData[DataId]["Sex"])
        self.Sex.setStyleSheet("background-color:rgba(135,206,250,0);color:white")
        self.Sex.setGeometry(50,360,200,20)

        #   民族
        self.Nation = QLabel(self)
        self.Nation.setFont(QFont("黑体",10))
        self.Nation.setText("民族："+self.LoginData[DataId]["Nation"])
        self.Nation.setStyleSheet("background-color:rgba(135,206,250,0);color:white")
        self.Nation.setGeometry(150,360,200,20)

        #   出生日期
        self.Date = QLabel(self)
        self.Date.setFont(QFont("黑体",10))
        self.Date.setText("出生日期："+self.LoginData[DataId]["Date"])
        self.Date.setStyleSheet("background-color:rgba(135,206,250,0);color:white")
        self.Date.setGeometry(50,390,200,20)

        if(self.LoginData[DataId]["Permission"] == "student"):
            self.Num.setText("学号：" + str(self.LoginData[DataId]["StudentId"]))
        if(self.LoginData[DataId]["Permission"] == "teacher"):
            self.Num.setText("工号：" + str(self.LoginData[DataId]["TeacherId"]))
        if(self.LoginData[DataId]["Permission"] == "admin"):
            self.Num.setText("管理员号：" + str(self.LoginData[DataId]["AdminId"]))


        #   鼠标事件初始化
        self._tracking = False
        self._startPos = None
        self._endPos = None

    #   读取信息文件
    def LoadLoginData(self):
        file = open('./conf/LoginData.json')
        self.LoginData = json.load(file)
        file.close()

    #   重写鼠标按下事件
    def mousePressEvent(self,e:QMouseEvent):
        #   检测鼠标按下左键点击（未放开）
        if e.button() == Qt.LeftButton:
            #   改变监测参数
            self._tracking = True
            #   获取鼠标左键点击位置
            self._startPos = QPoint(e.x(),e.y())

    #   重写鼠标移动事件，让没有标题栏的界面能通过按住界面移动
    def mouseMoveEvent(self,e:QMouseEvent):
        try:
            #   鼠标移动到位置(e.pos())与原来所在的位置(self._startPos)之差（两者的x,y组合起来的参数之差）即为窗口要移动的距离(self._endPos)
            self._endPos = e.pos() - self._startPos
            #   获取窗口位置(self.pos())并移动窗口
            self.move(self.pos() + self._endPos)
        except Exception:
            pass

    #   重写鼠标放开事件
    def mouseReleaseEvent(self,e:QMouseEvent):
        #   检测鼠标松开左键
        if e.button() == Qt.LeftButton:
            #   将重写鼠标事件中用到的参数重新整理好
            self._tracking = False
            self._startPos = None
            self._endPos = None

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Information(DataId="2")
    #   显示主窗口
    window.show()
    sys.exit(app.exec_())