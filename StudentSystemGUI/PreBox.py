import sys
import qtawesome
import json
from traceback import print_exc
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import ScorePre
import DVTeacher


class PreBox(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        #   窗口标题
        self.setWindowTitle('月考成绩分析一览')

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

        #   装饰文字
        self.TitleText = QLabel(self)
        self.TitleText.setText("成绩分析")
        self.TitleText.setFont(QFont("黑体",10))
        self.TitleText.setStyleSheet("background-color:rgba(135,206,250,0);color:white")
        self.TitleText.adjustSize()
        self.TitleText.move(10,10)

        #   构建表格模型
        self.ConstrustModel()
        self.ShowTableView()

        #   设置布局
        self.Hlayout = QHBoxLayout()
        self.Vlayout1 = QVBoxLayout()
        self.Vlayout2 = QVBoxLayout()
        self.Hlayout1 = QHBoxLayout()
        self.Hlayout2 = QHBoxLayout()

        self.Hlayout1.addItem(QSpacerItem(20,20))
        self.Vlayout1.addItem(QSpacerItem(300,50))

        self.Hlayout2.addWidget(self.tableView)

        self.Vlayout2.addLayout(self.Hlayout1)
        self.Vlayout2.addLayout(self.Hlayout2)

        self.Hlayout.addLayout(self.Vlayout1)
        self.Hlayout.addLayout(self.Vlayout2)

        self.setLayout(self.Hlayout)

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

        #   各科平均分柱状图查看按钮
        self.AveScoreButton = QPushButton(qtawesome.icon('fa.bar-chart', color='white'),"总平均分",self)
        self.AveScoreButton.setStyleSheet("background-color:rgba(139,69,19,0.8);border:0px;color:white;border-radius:5px")
        self.AveScoreButton.setIconSize(QSize(40,40))
        self.AveScoreButton.setGeometry(20,50,130,260)
        self.AveScoreButton.setToolTip("各科平均分")
        self.AveScoreButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.AveScoreButton.clicked.connect(self.ConstrustASAS)

        #   六次月考平均分折线图查看按钮
        self.MonthAveScoreButton = QPushButton(qtawesome.icon('fa.line-chart', color='white'),"六次月考平均分",self)
        self.MonthAveScoreButton.setStyleSheet("background-color:rgba(34,139,34,0.8);border:0px;color:white;border-radius:5px")
        self.MonthAveScoreButton.setIconSize(QSize(40,40))
        self.MonthAveScoreButton.setGeometry(160,50,130,260)
        self.MonthAveScoreButton.setToolTip("六次月考平均分")
        self.MonthAveScoreButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.MonthAveScoreButton.clicked.connect(self.ConstrustAAS)

        #   总分散点图查看按钮
        self.TotalScatterButton = QPushButton(qtawesome.icon('fa.area-chart', color='white'),"总分散点图",self)
        self.TotalScatterButton.setStyleSheet("background-color:rgba(199,21,133,0.8);border:0px;color:white;border-radius:5px")
        self.TotalScatterButton.setIconSize(QSize(40,40))
        self.TotalScatterButton.setGeometry(20,320,130,260)
        self.TotalScatterButton.setToolTip("总分散点图")
        self.TotalScatterButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.TotalScatterButton.clicked.connect(self.ConstrustTS)

        #   六科成绩饼状图查看按钮
        self.ScoresPieChartButton = QPushButton(qtawesome.icon('fa.pie-chart', color='white'),"各科饼状图",self)
        self.ScoresPieChartButton.setStyleSheet("background-color:rgba(0,0,139,0.8);border:0px;color:white;border-radius:5px")
        self.ScoresPieChartButton.setIconSize(QSize(40,40))
        self.ScoresPieChartButton.setGeometry(160,320,130,260)
        self.ScoresPieChartButton.setToolTip("六科成绩饼状图")
        self.ScoresPieChartButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.ScoresPieChartButton.clicked.connect(self.ConstrustSPC)

        #   鼠标事件初始化
        self._tracking = False
        self._startPos = None
        self._endPos = None

    #   构建数据模型
    def ConstrustASAS(self):
        self.ASAS = DVTeacher.ASAS()
        self.ASAS.show()

    def ConstrustAAS(self):
        self.AAS = DVTeacher.AAS()
        self.AAS.show()

    def ConstrustTS(self):
        self.TS = DVTeacher.TS()
        self.TS.show()

    def ConstrustSPC(self):
        self.SPC = DVTeacher.SPC()
        self.SPC.show()

    #   构建表格模型
    def ConstrustModel(self):

        #   读取成绩数据
        self.LoadScoreData()

        #   设置数据层次结构，（学生数量）行6列
        self.model = QStandardItemModel(60,6)

        #   更新模型数据
        self.UpdateModel()

    #   更新模型数据
    def UpdateModel(self):

        #   清空模型
        self.model.clear()

        DictSubject = ['语文','数学','英语','物理','化学','生物']

        #   设置水平方向四个头标签文本内容
        self.model.setHorizontalHeaderLabels(['语文预测','数学预测','英语预测','物理预测','化学预测','生物预测'])

        #   设置每个位置的文本值
        for column in range(6):
            #   获取预测结果
            self.PerEvent = ScorePre.ScorePre(DictSubject[column])
            self.PerResult = self.PerEvent.dicts
            for row in range(60):
                if(column == 0):
                    item = QStandardItem('%.1f' % float(self.PerResult[row + 1]))  
                    self.model.setItem(row,column,item)
                if(column == 1):
                    item = QStandardItem('%.1f' % float(self.PerResult[row + 1]))  
                    self.model.setItem(row,column,item)
                if(column == 2):
                    item = QStandardItem('%.1f' % float(self.PerResult[row + 1]))  
                    self.model.setItem(row,column,item)
                if(column == 3):
                    item = QStandardItem('%.1f' % float(self.PerResult[row + 1]))  
                    self.model.setItem(row,column,item)
                if(column == 4):
                    item = QStandardItem('%.1f' % float(self.PerResult[row + 1]))  
                    self.model.setItem(row,column,item)
                if(column == 5):
                    item = QStandardItem('%.1f' % float(self.PerResult[row + 1]))  
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
    table = PreBox()
    table.show()
    sys.exit(app.exec_())    