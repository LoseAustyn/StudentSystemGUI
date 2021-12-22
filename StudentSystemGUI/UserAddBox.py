
import sys
import qtawesome
import json
import UserTableList
from traceback import print_exc
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

class UserAddBox(QWidget):
    def __init__(self,UserType):
        super().__init__()
        self.initUI(UserType)

    #   主界面UI
    def initUI(self,UserType):

        self.UserType = UserType

        #   主窗口大小
        self.windowX = 600
        self.windowY = 250
        self.resize(self.windowX, self.windowY)

        #   窗口标题
        self.setWindowTitle('添加用户')

        #   设置窗口隐藏背景和边框、去除标题栏
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint)

        #   设置透明背景
        self.background = QLabel(self)
        #   85%透明度白色背景，10px大小平滑角
        self.background.setStyleSheet("background-color:rgba(135,206,250,0.9);border:1px;border-radius:10px")
        self.background.setGeometry(0,0,self.windowX,self.windowY)

        #   装饰文字
        self.TitleText = QLabel(self)
        if(self.UserType == "teacher"):
            self.TitleText.setText("添加教师")
        if(self.UserType == "student"):
            self.TitleText.setText("添加学生")
        self.TitleText.setFont(QFont("黑体",10))
        self.TitleText.setStyleSheet("background-color:rgba(135,206,250,0);color:white")
        self.TitleText.setGeometry(20,15,100,20)

        #   装饰文字
        self.NumLabel = QLabel(self)
        self.NumLabel.setText("用户数量：")
        self.NumLabel.setFont(QFont("黑体",12))
        self.NumLabel.setStyleSheet("background-color:rgba(135,206,250,0);color:white")
        self.NumLabel.setGeometry(60,85,100,20)

        #   用户数量输入栏
        self.UserNumInput = QTextEdit(self)
        self.UserNumInput.setGeometry((self.windowX - 300) / 2,80,300,30)
        self.UserNumInput.setFont(QFont("黑体",10))
        self.UserNumInput.setPlaceholderText("添加多少个用户")
        self.UserNumInput.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.UserNumInput.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.UserNumInput.setStyleSheet("QTextEdit {""background: transparent;border-width:0px; border-style:outset;color:#F8F8FF;border-bottom:2px dashed #F8F8FF;""}"
                                         "QTextEdit:focus {""border-bottom:2px dashed #4169E1;""}")

        #   添加按钮
        self.AddButton = QPushButton(qtawesome.icon('fa.plus', color='white'),"添加",self)
        self.AddButton.setStyleSheet("background-color:rgba(255,165,0,0.9);border:0px;border-radius:5px")
        self.AddButton.setIconSize(QSize(20, 20))
        self.AddButton.setGeometry((self.windowX - 300) / 2,165,140,25)
        self.AddButton.setToolTip("添加")
        self.AddButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.AddButton.clicked.connect(self.AddRow)

        #   返回按钮
        self.QuitButtonB = QPushButton(qtawesome.icon('fa.times-circle', color='white'),"返回",self)
        self.QuitButtonB.setStyleSheet("background-color:rgba(255,182,193,0.9);border:0px;border-radius:5px")
        self.QuitButtonB.setIconSize(QSize(20, 20))
        self.QuitButtonB.setGeometry((self.windowX - 300) / 2 + 160,165,140,25)
        self.QuitButtonB.setToolTip("返回")
        self.QuitButtonB.setCursor(QCursor(Qt.PointingHandCursor))
        self.QuitButtonB.clicked.connect(self.Back)

        #   鼠标事件初始化
        self._tracking = False
        self._startPos = None
        self._endPos = None

    #   添加
    def AddRow(self):
        #   加载用户数据
        self.LoadUserData()
        try:
            num = int(self.UserNumInput.toPlainText())
            if(self.UserType == "teacher"):
                #   添加用户
                for row in range(num):
                    TeacherId = 1
                    for i in range(len(self.UserData["User"])):
                        if(self.UserData["User"][i]["Permission"] == "teacher"):
                            if(TeacherId == self.UserData["User"][i]["TeacherId"]):
                                TeacherId+=1
                    NewIn = {
                              "Account": "",
                              "Password": "",
                              "Permission": "teacher",
                              "TeacherId": TeacherId,
                              "Name": "",
                              "Sex": "",
                              "Date": "2021-12-1",
                              "Nation": ""
                             }
                    self.UserData["User"].append(NewIn)

            if(self.UserType == "student"):
                #   添加用户
                for row in range(num):
                    StudentId = 1
                    for i in range(len(self.UserData["User"])):
                        if(self.UserData["User"][i]["Permission"] == "student"):
                            if(TeacherId == self.UserData["User"][i]["StudentId"]):
                                StudentId+=1
                    NewIn = {
                              "Account": "",
                              "Password": "",
                              "Permission": "student",
                              "TeacherId": StudentId,
                              "Name": "",
                              "Sex": "",
                              "Date": "2021-12-1",
                              "Nation": "",
                              "Class":""
                             }
                    self.UserData["User"].append(NewIn)
            file = open('./conf/LoginData.json','w')
            json.dump(self.UserData,file,ensure_ascii=False)
            self.MessageBox("添加成功！请返回表格界面进行编辑！")
            print(self.UserData)
            file.close()
            self.Back()
        except Exception:
            print_exc()
            self.MessageBox("保存失败！请检查填入的数据！")

    #   消息盒子
    def MessageBox(self,MessageString):
        MessageBox = QMessageBox()
        MessageBox.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.WindowMaximizeButtonHint | Qt.MSWindowsFixedSizeDialogHint)
        MessageBox.setWindowTitle("新消息")
        MessageBox.setText(MessageString)
        MessageBox.addButton(QPushButton("知道了"),QMessageBox.YesRole)
        MessageBox.exec_()

    #   读取用户数据
    def LoadUserData(self):
        file = open('./conf/LoginData.json')
        self.UserData = json.load(file)
        file.close()

    def Back(self):
        self.close()
        self.table = UserTableList.UserTable(UserType=self.UserType)
        self.table.show()        

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
    window = UserAddBox("teacher")
    #   显示主窗口
    window.show()
    sys.exit(app.exec_())