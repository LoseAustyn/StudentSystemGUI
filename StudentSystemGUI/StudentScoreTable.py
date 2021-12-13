import sys
import qtawesome
import json
from traceback import print_exc
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

#   本类为学生提供查看自己分数的功能
class StudentTable(QWidget):

    def __init__(self,Num):
        super().__init__()
        self.initUI(Num)

    def initUI(self,Num):

        #   窗口标题
        self.setWindowTitle('个人成绩一览')

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

        #   读取成绩
        self.LoadScoreData()

        #   构建表格
        self.ConstrustModel(Num)
        #   显示表格
        self.ShowTableView()

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

        #   设置布局
        self.Vlayout = QVBoxLayout()

        self.Vlayout.addItem(QSpacerItem(20,20))
        self.Vlayout.addWidget(self.tableView)

        self.setLayout(self.Vlayout)

    #   构建表格模型
    def ConstrustModel(self,Num):

        #   读取成绩数据
        self.LoadScoreData()

        #   设置数据层次结构，（月考次数）行6列
        self.model = QStandardItemModel(len(self.ScoreData),6)

        #   更新模型数据
        self.UpdateModel(Num)

    #   更新模型数据
    def UpdateModel(self,Num):

        #   清空模型
        self.model.clear()

        #   设置水平方向四个头标签文本内容
        self.model.setHorizontalHeaderLabels(['语文','数学','英语','物理','化学','生物'])

        #   设置垂直方向四个头标签文本内容
        MonthNum = []
        for i in range(len(self.ScoreData)):
            MonthNum.append(("第" + str(i + 1) + "次月考"))
        self.model.setVerticalHeaderLabels(MonthNum)

        #   读取成绩数据
        self.LoadScoreData()

        #   设置每个位置的文本值
        for row in range(len(self.ScoreData)):
            for column in range(6):
                if(column == 0):
                    item = QStandardItem('%.1f' % (self.ScoreData[str(row + 1)][Num-1]["语文"]))  
                    self.model.setItem(row,column,item)
                if(column == 1):
                    item = QStandardItem('%.1f' % (self.ScoreData[str(row + 1)][Num-1]["数学"]))  
                    self.model.setItem(row,column,item)
                if(column == 2):
                    item = QStandardItem('%.1f' % (self.ScoreData[str(row + 1)][Num-1]["英语"]))  
                    self.model.setItem(row,column,item)             
                if(column == 3):
                    item = QStandardItem('%.1f' % (self.ScoreData[str(row + 1)][Num-1]["物理"]))  
                    self.model.setItem(row,column,item)
                if(column == 4):
                    item = QStandardItem('%.1f' % (self.ScoreData[str(row + 1)][Num-1]["化学"]))  
                    self.model.setItem(row,column,item)
                if(column == 5):        
                    item = QStandardItem('%.1f' % (self.ScoreData[str(row + 1)][Num-1]["生物"]))  
                    self.model.setItem(row,column,item)

    #   显示表格视图
    def ShowTableView(self):
        #   创建表格，设置模型为ConstrustModel方法中构建的模型
        self.tableView = QTableView()
        self.tableView.setModel(self.model)
        self.tableView.setStyleSheet("background-color:rgba(255,255,255,0.9)")
        #   水平方向标签拓展剩下的窗口部分，填满表格
        #self.tableView.horizontalHeader().setStretchLastSection(True)
        #   水平方向，表格大小拓展到适当的尺寸
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)    

    #   读取成绩文件
    def LoadScoreData(self):
        file = open('./conf/MonthScore.json')
        self.ScoreData = json.load(file)
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
  table = StudentTable(Num=1)
  table.show()
  sys.exit(app.exec_())    