
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import json
import qtawesome
from traceback import print_exc
import sys
import StudentMainWindow
import TeacherMainWindow
import AdminMainWindow

#   登录界面
class LoginWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    #   登录界面GUI
    def initUI(self):
        #   读取登录文档
        self.LoadLoginData()

        #   窗口大小
        self.windowX = 600
        self.windowY = 250

        self.resize(self.windowX,self.windowY)

        #   将窗口生成在屏幕中间
        self.center()

        #   窗口标题
        self.setWindowTitle('登录')

        #   设置窗口隐藏背景和边框、去除标题栏、强制置顶
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint)
        
        #   设置透明背景
        self.background = QLabel(self)

        #   85%透明度淡蓝色背景，10px大小平滑角
        self.background.setStyleSheet("background-color:rgba(135,206,250,0.85);border:1px;border-radius:10px")
        self.background.setGeometry(0,0,self.windowX,self.windowY)

        #   退出按钮
        self.QuitButton = QPushButton(qtawesome.icon('fa.times', color='white'),"",self)
        self.QuitButton.setStyleSheet("background-color:rgba(135,206,250,0)")
        self.QuitButton.setIconSize(QSize(20, 20))
        self.QuitButton.setGeometry(570,10,20,20)
        self.QuitButton.setToolTip("退出")
        self.QuitButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.QuitButton.clicked.connect(self.close)

        #   最小化按钮
        self.MinimizeButton = QPushButton(qtawesome.icon('fa.minus', color='white'),"",self)
        self.MinimizeButton.setStyleSheet("background-color:rgba(135,206,250,0)")
        self.MinimizeButton.setIconSize(QSize(20, 20))
        self.MinimizeButton.setGeometry(540,10,20,20)
        self.MinimizeButton.setToolTip("最小化")
        self.MinimizeButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.MinimizeButton.clicked.connect(self.showMinimized)

        #   账号输入栏
        self.AccountInput = QTextEdit(self)
        self.AccountInput.setGeometry(40,65,300,30)
        self.AccountInput.setFont(QFont("黑体",10))
        self.AccountInput.setFixedHeight(30)
        self.AccountInput.setPlaceholderText("请输入账户名")
        self.AccountInput.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.AccountInput.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.AccountInput.setStyleSheet("QTextEdit {""background: transparent;border-width:0px; border-style:outset;color:#F8F8FF;border-bottom:2px dashed #F8F8FF;""}"
                                     "QTextEdit:focus {""border-bottom:2px dashed #4169E1;""}")

        #   密码输入栏
        self.PasswordInput = QTextEdit(self)
        self.PasswordInput.setGeometry(40,115,300,30)
        self.PasswordInput.setFont(QFont("黑体",10))
        self.PasswordInput.setPlaceholderText("请输入密码")
        self.PasswordInput.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.PasswordInput.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.PasswordInput.setStyleSheet("QTextEdit {""background: transparent;border-width:0px; border-style:outset;color:#F8F8FF;border-bottom:2px dashed #F8F8FF;""}"
                                         "QTextEdit:focus {""border-bottom:2px dashed #4169E1;""}")
        
        #   登录按钮
        self.LoginButton = QPushButton(qtawesome.icon('fa.chevron-right', color='white'),"",self)
        self.LoginButton.setStyleSheet("background-color:rgba(135,206,250,0)")
        self.LoginButton.setIconSize(QSize(40,40))
        self.LoginButton.setGeometry(30,170,40,40)
        self.LoginButton.setToolTip("登录")
        self.LoginButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.LoginButton.clicked.connect(self.SignIn)


        #   装饰图像
        self.Graduation = QPushButton(qtawesome.icon('fa.graduation-cap', color='white'),"",self)
        self.Graduation.setIconSize(QSize(170,170))
        self.Graduation.setStyleSheet("background-color:rgba(135,206,250,0)")
        self.Graduation.setGeometry(400,50,170,170)

        #   装饰文字
        self.TitleText = QLabel(self)
        self.TitleText.setText("学生成绩分析系统")
        self.TitleText.setFont(QFont("黑体",10))
        self.TitleText.setStyleSheet("background-color:rgba(135,206,250,0);color:white")
        self.TitleText.setGeometry(20,15,150,20)

        #   鼠标事件初始化
        self._tracking = False
        self._startPos = None
        self._endPos = None

    #   读取登录文件
    def LoadLoginData(self):
        file = open('./conf/LoginData.json')
        self.LoginData = json.load(file)
        file.close()

    """
    #   保存文件
    def SaveLoginData(self,Account,Password):
        file = open('./conf/LoginData.json')
        data = json.load(file)
        User = {
            "Account":Account,
            "Password":Password
            }
        UserData = json.dumps(User) 
    """

    #   输入合法验证
    def InputCheck(self):
        User = self.AccountInput.toPlainText()
        Password = self.PasswordInput.toPlainText()
        if User == "":
            self.ErrorMessageBox("请输入用户名")
            return 1
        if Password == "":
            self.ErrorMessageBox("请输入密码")
            return 1
        return 0

    #   登录验证
    def SignIn(self):
        #   合法性检测
        if (self.InputCheck()):
            return None
        i = 0
        #   加载登录数据
        self.LoadLoginData()
        try:
            while 1:
                if(self.LoginData["User"][i]["Account"] == self.AccountInput.toPlainText()):
                    if(self.LoginData["User"][i]["Password"] == self.PasswordInput.toPlainText()):
                        #   为初始化界面传入权限
                        self.LoginPermission = self.LoginData["User"][i]["Permission"]
                        #   为初始化界面传入数据ID
                        self.InitMain(permission=self.LoginPermission,DataId=i)
                        return 1
                    if(self.LoginData["User"][i]["Password"] != self.PasswordInput.toPlainText()):
                        self.ErrorMessageBox("登录失败，请检查用户名和密码")
                        return 0
                else:
                    i+=1
        except Exception:
            print_exc()
            self.ErrorMessageBox("登录失败，请检查用户名和密码")
            return 0

    #   初始化主界面
    def InitMain(self,permission,DataId):
        if(permission == "admin"):
            self.MainWindow = AdminMainWindow.AdminMainWindow(DataId=DataId)
        if(permission == "teacher"):
            self.MainWindow = TeacherMainWindow.TeacherMainWindow(DataId=DataId)
        if(permission == "student"):
            self.MainWindow = StudentMainWindow.StudentMainWindow(DataId=DataId)
        self.close()
        self.showMain()
    
    #   显示主界面
    def showMain(self):
        self.MainWindow.show()

    #   错误消息盒子
    def ErrorMessageBox(self,ErrorString):

        MessageBox = QMessageBox()
        MessageBox.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.WindowMaximizeButtonHint | Qt.MSWindowsFixedSizeDialogHint)
        MessageBox.setWindowTitle("错误")
        MessageBox.setText(ErrorString)
        MessageBox.addButton(QPushButton("知道了"),QMessageBox.YesRole)
        MessageBox.exec_()

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
            if (self._tracking == True):
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
            #   鼠标事件完成，所有的参数复位
            self._tracking = False
            self._startPos = None
            self._endPos = None


if __name__ == '__main__':

    app = QApplication(sys.argv)
    window = LoginWindow()
    #   显示主窗口
    window.show()
    sys.exit(app.exec_())