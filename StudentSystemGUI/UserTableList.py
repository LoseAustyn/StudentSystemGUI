
import sys
import qtawesome
import json
import UserAddBox
from traceback import print_exc
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

#   本类用于构建用户表
class UserTable(QWidget):

    def __init__(self,UserType):

        super().__init__()
        self.initUI(UserType)

    def initUI(self,UserType):

        self.UserType = UserType

        #   窗口标题
        self.setWindowTitle('用户表')

        #   窗口大小
        self.windowX = 1000
        self.windowY = 600
        self.resize(self.windowX,self.windowY)

        #   设置窗口隐藏背景和边框、去除标题栏
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint)
        #   设置透明背景
        self.background = QLabel(self)
        #   85%透明度淡蓝色背景，10px大小平滑角
        self.background.setStyleSheet("background-color:rgba(135,206,250,0.85);border:1px;border-radius:10px")
        self.background.setGeometry(0,0,self.windowX,self.windowY)

        #   读取用户数据
        self.LoadLoginData()

        #   构建表格模型
        self.ConstrustModel()
        self.ShowTableView()

        #   保存按钮
        self.SaveButton = QPushButton(qtawesome.icon('fa.floppy-o', color='white'),"保存",self)
        self.SaveButton.setStyleSheet("background-color:rgba(144,238,144,0.9);border:0px;border-radius:5px")
        self.SaveButton.setIconSize(QSize(20, 20))
        self.SaveButton.setToolTip("保存")
        self.SaveButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.SaveButton.clicked.connect(self.SaveUserData)

        #   添加按钮
        self.AddButton = QPushButton(qtawesome.icon('fa.plus', color='white'),"添加",self)
        self.AddButton.setStyleSheet("background-color:rgba(255,165,0,0.9);border:0px;border-radius:5px")
        self.AddButton.setIconSize(QSize(20, 20))
        self.AddButton.setToolTip("添加")
        self.AddButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.AddButton.clicked.connect(self.AddBox)

        #   设置布局
        self.Vlayout = QVBoxLayout()
        self.Hlayout1 = QHBoxLayout()
        self.Hlayout2 = QHBoxLayout()
        self.Hlayout3 = QHBoxLayout()

        self.Hlayout1.addItem(QSpacerItem(20,20))

        self.Hlayout2.addWidget(self.tableView)

        self.Hlayout3.addWidget(self.SaveButton)
        self.Hlayout3.addWidget(self.AddButton)

        self.Vlayout.addLayout(self.Hlayout1)
        self.Vlayout.addLayout(self.Hlayout2)
        self.Vlayout.addLayout(self.Hlayout3)

        self.setLayout(self.Vlayout)

        #   顶部退出按钮
        self.QuitButton = QPushButton(qtawesome.icon('fa.times', color='white'),"",self)
        self.QuitButton.setStyleSheet("background-color:rgba(135,206,250,0)")
        self.QuitButton.setIconSize(QSize(20, 20))
        self.QuitButton.setGeometry(970,10,20,20)
        self.QuitButton.setToolTip("退出")
        self.QuitButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.QuitButton.clicked.connect(self.close)

        #   最小化按钮
        self.MinimizeButton = QPushButton(qtawesome.icon('fa.minus', color='white'),"",self)
        self.MinimizeButton.setStyleSheet("background-color:rgba(135,206,250,0)")
        self.MinimizeButton.setIconSize(QSize(20, 20))
        self.MinimizeButton.setGeometry(940,10,20,20)
        self.MinimizeButton.setToolTip("最小化")
        self.MinimizeButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.MinimizeButton.clicked.connect(self.showMinimized)

        #   鼠标事件初始化
        self._tracking = False
        self._startPos = None
        self._endPos = None


    #   构建表格模型
    def ConstrustModel(self):

        #   读取用户数据
        self.LoadLoginData()

        #   构建教师表格模型
        if(self.UserType == "teacher"):
            TeacherNum = 0
            for i in range(len(self.LoginData["User"])):
                if(self.LoginData["User"][i]["Permission"] == "teacher"):
                    TeacherNum+=1
            self.TeacherNum = TeacherNum
            #   设置数据层次结构
            self.model = QStandardItemModel(TeacherNum,8)
            #   更新模型数据
            self.UpdateModel()

        #   构建学生表格模型
        if(self.UserType == "student"):
            StudentNum = 0
            for i in range(len(self.LoginData["User"])):
                if(self.LoginData["User"][i]["Permission"] == "student"):
                    StudentNum+=1
            self.StudentNum = StudentNum
            #   设置数据层次结构
            self.model = QStandardItemModel(StudentNum,9)
            #   更新模型数据
            self.UpdateModel()

    #   更新模型数据
    def UpdateModel(self):

        #   清空模型
        self.model.clear()

        #   读取用户数据
        self.LoadLoginData()

        #   设置每个位置的文本值
        #   教师表填充
        if(self.UserType == "teacher"):
            #   设置水平方向四个头标签文本内容
            self.model.setHorizontalHeaderLabels(['账号','密码','权限组','工号','名字','性别','生日','民族'])
            i = 0
            for row in range(len(self.LoginData["User"])):
                if(self.LoginData["User"][row]["Permission"] == "teacher"):
                    for column in range(8):
                        if(column == 0):
                            item = QStandardItem(self.LoginData["User"][row]["Account"])
                            self.model.setItem(i,column,item)
                        if(column == 1):
                            item = QStandardItem(self.LoginData["User"][row]["Password"])
                            self.model.setItem(i,column,item)
                        if(column == 2):
                            item = QStandardItem(self.LoginData["User"][row]["Permission"])
                            self.model.setItem(i,column,item)
                        if(column == 3):
                            item = QStandardItem(str(self.LoginData["User"][row]["TeacherId"]))
                            self.model.setItem(i,column,item)
                        if(column == 4):
                            item = QStandardItem(self.LoginData["User"][row]["Name"])
                            self.model.setItem(i,column,item)
                        if(column == 5):
                            item = QStandardItem(self.LoginData["User"][row]["Sex"])
                            self.model.setItem(i,column,item)
                        if(column == 6):
                            item = QStandardItem(self.LoginData["User"][row]["Date"])
                            self.model.setItem(i,column,item)
                        if(column == 7):
                            item = QStandardItem(self.LoginData["User"][row]["Nation"])
                            self.model.setItem(i,column,item)
                    i+=1

        #   学生表填充
        if(self.UserType == "student"):
            #   设置水平方向四个头标签文本内容
            self.model.setHorizontalHeaderLabels(['账号','密码','权限组','学号','名字','性别','生日','民族','班级'])
            i = 0
            for row in range(len(self.LoginData["User"])):
                if(self.LoginData["User"][row]["Permission"] == "student"):
                    for column in range(9):
                        if(column == 0):
                            item = QStandardItem(self.LoginData["User"][row]["Account"]) 
                            self.model.setItem(i,column,item)
                        if(column == 1):
                            item = QStandardItem(self.LoginData["User"][row]["Password"])
                            self.model.setItem(i,column,item)
                        if(column == 2):
                            item = QStandardItem(self.LoginData["User"][row]["Permission"])
                            self.model.setItem(i,column,item)
                        if(column == 3):
                            item = QStandardItem(str(self.LoginData["User"][row]["StudentId"]))
                            self.model.setItem(i,column,item)
                        if(column == 4):
                            item = QStandardItem(self.LoginData["User"][row]["Name"])
                            self.model.setItem(i,column,item)
                        if(column == 5):
                            item = QStandardItem(self.LoginData["User"][row]["Sex"])
                            self.model.setItem(i,column,item)
                        if(column == 6):
                            item = QStandardItem(self.LoginData["User"][row]["Date"])
                            self.model.setItem(i,column,item)
                        if(column == 7):
                            item = QStandardItem(self.LoginData["User"][row]["Nation"])
                            self.model.setItem(i,column,item)
                        if(column == 8):
                            item = QStandardItem(self.LoginData["User"][row]["Class"])
                            self.model.setItem(i,column,item)
                    i+=1

    #   显示表格
    def ShowTableView(self):
        #   创建表格，设置模型为ConstrustModel方法中构建的模型
        self.tableView = QTableView()
        self.tableView.setModel(self.model)
        self.tableView.setStyleSheet("background-color:rgba(255,255,255,0.9)")
        #   水平方向标签拓展剩下的窗口部分，填满表格
        #self.tableView.horizontalHeader().setStretchLastSection(True)
        #   水平方向，表格大小拓展到适当的尺寸
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)     

    def LoadLoginData(self):
        file = open('./conf/LoginData.json')
        self.LoginData = json.load(file)
        file.close()

    def SaveUserData(self):
        try:
            file = open('./conf/LoginData.json')
            Data = json.load(file)
            file.close()
            if(self.UserType == "teacher"):
                i = 0
                #   获取每个位置的文本值
                for row in range(len(self.LoginData["User"])):
                    if(self.LoginData["User"][row]["Permission"] == "teacher"):
                        for column in range(8):
                            if(column == 0):
                                Data["User"][row]["Account"] = self.model.item(i,column).text()
                            if(column == 1):
                                Data["User"][row]["Password"] = self.model.item(i,column).text()
                            if(column == 2):
                                Data["User"][row]["Permission"] = self.model.item(i,column).text()
                            if(column == 3):
                                Data["User"][row]["TeacherId"] = int(self.model.item(i,column).text())
                            if(column == 4):
                                Data["User"][row]["Name"] = self.model.item(i,column).text()
                            if(column == 5):
                                Data["User"][row]["Sex"] = self.model.item(i,column).text()
                            if(column == 6):
                                Data["User"][row]["Date"] = self.model.item(i,column).text()
                            if(column == 7):
                                Data["User"][row]["Nation"] = self.model.item(i,column).text()
                        i+=1

            if(self.UserType == "student"):
                i = 0
                #   获取每个位置的文本值
                for row in range(len(self.LoginData["User"])):
                    if(self.LoginData["User"][row]["Permission"] == "student"):
                        for column in range(9):
                            if(column == 0):
                                Data["User"][row]["Account"] = self.model.item(i,column).text()
                            if(column == 1):
                                Data["User"][row]["Password"] = self.model.item(i,column).text()
                            if(column == 2):
                                Data["User"][row]["Permission"] = self.model.item(i,column).text()
                            if(column == 3):
                                Data["User"][row]["StudentId"] = int(self.model.item(i,column).text())
                            if(column == 4):
                                Data["User"][row]["Name"] = self.model.item(i,column).text()
                            if(column == 5):
                                Data["User"][row]["Sex"] = self.model.item(i,column).text()
                            if(column == 6):
                                Data["User"][row]["Date"] = self.model.item(i,column).text()
                            if(column == 7):
                                Data["User"][row]["Nation"] = self.model.item(i,column).text()
                            if(column == 8):
                                Data["User"][row]["Class"] = self.model.item(i,column).text()
                        i+=1
            #   进行文件保存
            file = open('./conf/LoginData.json','w')
            json.dump(Data,file,ensure_ascii=False)
            self.MessageBox("保存成功！")
            file.close()
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

    def AddBox(self):
        self.UserAdd = UserAddBox.UserAddBox(self.UserType)
        self.UserAdd.show()
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
  table = UserTable("teacher")
  table.show()
  sys.exit(app.exec_())    