import sys
import qtawesome
import json
from traceback import print_exc
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import UserTableList

class UserTypeBox(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    #   主界面UI
    def initUI(self):
        #   主窗口大小
        self.windowX = 400
        self.windowY = 220
        self.resize(self.windowX, self.windowY)

        #   窗口标题
        self.setWindowTitle('添加')

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
        self.QuitButton.setGeometry(self.windowX-30,10,20,20)
        self.QuitButton.setToolTip("退出")
        self.QuitButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.QuitButton.clicked.connect(self.close)

        #   最小化按钮
        self.MinimizeButton = QPushButton(qtawesome.icon('fa.minus', color='white'),"",self)
        self.MinimizeButton.setStyleSheet("background-color:rgba(135,206,250,0)")
        self.MinimizeButton.setIconSize(QSize(20, 20))
        self.MinimizeButton.setGeometry(self.windowX-60,10,20,20)
        self.MinimizeButton.setToolTip("最小化")
        self.MinimizeButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.MinimizeButton.clicked.connect(self.showMinimized)

        #   装饰文字
        self.MonthLabel = QLabel(self)
        self.MonthLabel.setText("您需要对哪类用户进行编辑：")
        self.MonthLabel.setFont(QFont("黑体",10))
        self.MonthLabel.setStyleSheet("background-color:rgba(135,206,250,0);color:white")
        self.MonthLabel.setGeometry(10,10,250,20)

        #   教师用户编辑
        self.TeacherButton = QPushButton(qtawesome.icon('fa.coffee', color='white'),"教师用户编辑",self)
        self.TeacherButton.setStyleSheet("background-color:rgba(65,105,225,0.9);border:0px;border-radius:5px;color:white")
        self.TeacherButton.setIconSize(QSize(20, 20))
        self.TeacherButton.setGeometry((self.windowX-140)/2,70,140,30)
        self.TeacherButton.setToolTip("教师编辑")
        self.TeacherButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.TeacherButton.clicked.connect(self.TeacherUserTable)

        #   学生用户编辑
        self.StudentButton = QPushButton(qtawesome.icon('fa.graduation-cap', color='white'),"学生用户编辑",self)
        self.StudentButton.setStyleSheet("background-color:rgba(123,104,238,0.9);border:0px;border-radius:5px;color:white")
        self.StudentButton.setIconSize(QSize(20, 20))
        self.StudentButton.setGeometry((self.windowX-140)/2,130,140,30)
        self.StudentButton.setToolTip("学生编辑")
        self.StudentButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.StudentButton.clicked.connect(self.StudentUserTable)

        #   鼠标事件初始化
        self._tracking = False
        self._startPos = None
        self._endPos = None

    def TeacherUserTable(self):
        self.UserTableList=UserTableList.UserTable("teacher")
        self.UserTableList.show()
        self.close()

    def StudentUserTable(self):
        self.UserTableList=UserTableList.UserTable("student")
        self.UserTableList.show()
        self.close()

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
    window = UserTypeBox()
    #   显示主窗口
    window.show()
    sys.exit(app.exec_())