
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys
import json
import qtawesome
import LoginWindow
import Information
import StudentScoreTable
from traceback import print_exc
import ScoreAnalyzBox
import DVStudent

class StudentMainWindow(QMainWindow):

    def __init__(self,DataId):
        super().__init__()
        self.initUI(DataId)

    #   主界面UI
    def initUI(self,DataId):

        self.DataId = DataId

        #   主窗口大小
        self.windowX = 725
        self.windowY = 480
        self.resize(self.windowX, self.windowY)

        #   调用居中
        self.center()

        #   窗口标题
        self.setWindowTitle('主界面')

        #   设置窗口隐藏背景和边框、去除标题栏
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint)

        #   设置透明背景
        self.background = QLabel(self)
        #   85%透明度白色背景，10px大小平滑角
        self.background.setStyleSheet("background-color:rgba(135,206,250,0.9);border:1px;border-radius:10px")
        self.background.setGeometry(0,0,self.windowX,self.windowY)

        #   退出按钮
        self.QuitButton = QPushButton(qtawesome.icon('fa.times', color='white'),"",self)
        self.QuitButton.setStyleSheet("background-color:rgba(135,206,250,0)")
        self.QuitButton.setIconSize(QSize(20, 20))
        self.QuitButton.setGeometry(690,10,20,20)
        self.QuitButton.setToolTip("退出")
        self.QuitButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.QuitButton.clicked.connect(self.Quit)

        #   最小化按钮
        self.MinimizeButton = QPushButton(qtawesome.icon('fa.minus', color='white'),"",self)
        self.MinimizeButton.setStyleSheet("background-color:rgba(135,206,250,0)")
        self.MinimizeButton.setIconSize(QSize(20, 20))
        self.MinimizeButton.setGeometry(660,10,20,20)
        self.MinimizeButton.setToolTip("最小化")
        self.MinimizeButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.MinimizeButton.clicked.connect(self.showMinimized)

        #   装饰文字
        self.TitleText = QLabel(self)
        self.TitleText.setText("欢迎！")
        self.TitleText.setFont(QFont("黑体",10))
        self.TitleText.setStyleSheet("background-color:rgba(135,206,250,0);color:white")
        self.TitleText.setGeometry(20,15,50,20)

        #   个人信息按钮
        self.UserDataButton = QPushButton(qtawesome.icon('fa.user-circle', color='white'),"",self)
        self.UserDataButton.setStyleSheet(("background-color:rgba(255,222,173,0.9);border:0px;color:white;border-radius:5px"))
        self.UserDataButton.setIconSize(QSize(40,40))
        self.UserDataButton.setGeometry(35,50,160,400)
        self.UserDataButton.setText("个人信息")
        self.UserDataButton.setFont(QFont("黑体",10))
        self.UserDataButton.setToolTip("查看个人信息")
        self.UserDataButton.setCursor(QCursor(Qt.PointingHandCursor))
        #   查看个人信息
        self.UserDataButton.clicked.connect(self.ShowInformation)

        #   课程成绩查询
        self.UserScoreButton = QPushButton(qtawesome.icon('fa.trophy', color='white'),"",self)
        self.UserScoreButton.setStyleSheet(("background-color:rgba(147,112,219,0.9);border:0px;color:white;border-radius:5px"))
        self.UserScoreButton.setIconSize(QSize(40,40))
        self.UserScoreButton.setGeometry(200,50,160,400)
        self.UserScoreButton.setText("课程成绩")
        self.UserScoreButton.setFont(QFont("黑体",10))
        self.UserScoreButton.setToolTip("查看个人成绩")
        self.UserScoreButton.setCursor(QCursor(Qt.PointingHandCursor))
        #   课程成绩查询
        self.UserScoreButton.clicked.connect(self.ShowScoreTable)

        #   课程成绩分析
        self.ScoreAnalyzButton = QPushButton(qtawesome.icon('fa.area-chart', color='white'),"",self)
        self.ScoreAnalyzButton.setStyleSheet(("background-color:rgba(144,238,144,0.9);border:0px;color:white;border-radius:5px"))
        self.ScoreAnalyzButton.setIconSize(QSize(40,40))
        self.ScoreAnalyzButton.setGeometry(365,50,160,400)
        self.ScoreAnalyzButton.setText("成绩分析")
        self.ScoreAnalyzButton.setFont(QFont("黑体",10))
        self.ScoreAnalyzButton.setToolTip("查看成绩分析")
        self.ScoreAnalyzButton.setCursor(QCursor(Qt.PointingHandCursor))
        #   课程成绩分析
        self.ScoreAnalyzButton.clicked.connect(self.ShowScoreAnalyz)

        #   退出登录
        self.QuitLoginButton = QPushButton(qtawesome.icon('fa.sign-out', color='white'),"",self)
        self.QuitLoginButton.setStyleSheet(("background-color:rgba(219,112,147,0.9);border:0px;color:white;border-radius:5px"))
        self.QuitLoginButton.setIconSize(QSize(40,40))
        self.QuitLoginButton.setGeometry(530,50,160,400)
        self.QuitLoginButton.setText("退出登录")
        self.QuitLoginButton.setFont(QFont("黑体",10))
        self.QuitLoginButton.setToolTip("退出登录")
        self.QuitLoginButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.QuitLoginButton.clicked.connect(self.QuitLogin)

        #   鼠标事件初始化
        self._tracking = False
        self._startPos = None
        self._endPos = None

    #   显示个人信息
    def ShowInformation(self):
        self.Information = Information.Information(self.DataId)
        self.Information.show()

    #   显示个人成绩
    def ShowScoreTable(self):
        self.LoadLoginData()
        self.ScoreTable = StudentScoreTable.StudentTable(self.LoginData["User"][self.DataId]["StudentId"])
        self.ScoreTable.show()

    #   显示成绩分析
    def ShowScoreAnalyz(self):
        self.LoadLoginData()
        self.ScoreAnalyz=ScoreAnalyzBox.ScoreAnalyzBox(self.DataId)
        DVStudent.score_radarChart(self.LoginData["User"][self.DataId]["StudentId"])
        self.ScoreAnalyz.show()

    #   直接退出
    def Quit(self):
        self.close()
        try:
            self.ScoreTable.close()
        except Exception:
            pass
        try:
            self.Information.close()
        except Exception:
            pass
        try:
            self.ScoreAnalyz.close()
        except Exception:
            pass

    #   退出登录
    def QuitLogin(self):
        self.Login = LoginWindow.LoginWindow()
        self.close()
        try:
            self.ScoreTable.close()
        except Exception:
            pass
        try:
            self.Information.close()
        except Exception:
            pass
        try:
            self.ScoreAnalyz.close()
        except Exception:
            pass
        self.Login.show()

    #   读取信息文件
    def LoadLoginData(self):
        file = open('./conf/LoginData.json')
        self.LoginData = json.load(file)
        file.close()            

    #   窗口生成在屏幕中间
    def center(self):
        #   计算显示屏的大小
        screen = QDesktopWidget().screenGeometry()
        #   计算qwidget的窗口大小
        size = self.geometry()
        #   把窗口移动到屏幕正中央
        self.move((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2)

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
    window = StudentMainWindow(2)
    #   显示主窗口
    window.show()
    sys.exit(app.exec_())