
import sys
import qtawesome
import json
from traceback import print_exc
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import AdminScoreAddBox

#   本类为教师提供查看以及管理科目分数的功能
class TeacherTable(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        #   窗口标题
        self.setWindowTitle('月考成绩一览')

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

        #   下拉选择栏
        self.ComboBox = QComboBox()
        for num in range(len(self.ScoreData)):
            self.ComboBox.addItem(list(self.ScoreData.keys())[num])
        
        #   构建9行表格模型
        self.ConstrustModel(self.ComboBox.currentText())
        self.ShowTableView()

        #   当选择栏变化时重新构建表格
        self.ComboBox.activated[str].connect(self.UpdateModel)

        self.Label = QLabel()
        self.Label.setText("次月考（双击可进行图表修改）")

        #   保存按钮
        self.SaveButton = QPushButton(qtawesome.icon('fa.floppy-o', color='white'),"保存",self)
        self.SaveButton.setStyleSheet("background-color:rgba(144,238,144,0.9);border:0px;border-radius:5px")
        self.SaveButton.setIconSize(QSize(20, 20))
        self.SaveButton.setToolTip("保存")
        self.SaveButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.SaveButton.clicked.connect(self.SaveScoreData)

        #   添加按钮
        self.AddButton = QPushButton(qtawesome.icon('fa.plus', color='white'),"添加",self)
        self.AddButton.setStyleSheet("background-color:rgba(255,165,0,0.9);border:0px;border-radius:5px")
        self.AddButton.setIconSize(QSize(20, 20))
        self.AddButton.setToolTip("添加")
        self.AddButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.AddButton.clicked.connect(self.AddEvent)

        #   底部退出按钮
        self.QuitButtonB = QPushButton(qtawesome.icon('fa.times-circle', color='white'),"退出",self)
        self.QuitButtonB.setStyleSheet("background-color:rgba(255,182,193,0.9);border:0px;border-radius:5px")
        self.QuitButtonB.setIconSize(QSize(20, 20))
        self.QuitButtonB.setToolTip("退出")
        self.QuitButtonB.setCursor(QCursor(Qt.PointingHandCursor))
        self.QuitButtonB.clicked.connect(self.close)

        #   设置布局
        self.Vlayout = QVBoxLayout()
        self.Hlayout1 = QHBoxLayout()
        self.Hlayout2 = QHBoxLayout()
        self.Hlayout3 = QHBoxLayout()

        self.Hlayout1.addWidget(self.ComboBox)
        self.Hlayout1.addWidget(self.Label)

        self.Hlayout2.addWidget(self.tableView)

        self.Hlayout3.addWidget(self.SaveButton)
        self.Hlayout3.addWidget(self.AddButton)
        self.Hlayout3.addWidget(self.QuitButtonB)

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
    def ConstrustModel(self,month):

        #   读取成绩数据
        self.LoadScoreData()

        #   设置数据层次结构，（学生数量）行6列
        self.model = QStandardItemModel(len(self.ScoreData[month]),6)

        #   更新模型数据
        self.UpdateModel(month)

    #   更新模型数据
    def UpdateModel(self,month):

        #   清空模型
        self.model.clear()

        #   设置水平方向四个头标签文本内容
        self.model.setHorizontalHeaderLabels(['语文','数学','英语','物理','化学','生物'])

        #   读取成绩数据
        self.LoadScoreData()

        #   设置每个位置的文本值
        for row in range(len(self.ScoreData[month])):
            for column in range(6):
                if(column == 0):
                    item = QStandardItem('%.1f' % (self.ScoreData[month][row]["语文"]))  
                    self.model.setItem(row,column,item)
                if(column == 1):
                    item = QStandardItem('%.1f' % (self.ScoreData[month][row]["数学"]))  
                    self.model.setItem(row,column,item)
                if(column == 2):
                    item = QStandardItem('%.1f' % (self.ScoreData[month][row]["英语"]))  
                    self.model.setItem(row,column,item)             
                if(column == 3):
                    item = QStandardItem('%.1f' % (self.ScoreData[month][row]["物理"]))  
                    self.model.setItem(row,column,item)
                if(column == 4):
                    item = QStandardItem('%.1f' % (self.ScoreData[month][row]["化学"]))  
                    self.model.setItem(row,column,item)
                if(column == 5):        
                    item = QStandardItem('%.1f' % (self.ScoreData[month][row]["生物"]))  
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

    #   保存修改后的成绩文件
    def SaveScoreData(self):
        month = self.ComboBox.currentText()
        try:
            #   重新打开一份新的成绩文件副本用于编辑
            file = open('./conf/MonthScore.json')
            Data = json.load(file)
            file.close()
            #   获取每个位置的文本值
            for row in range(len(self.ScoreData[month])):
                for column in range(6):
                    if(column == 0):
                        Data[month][row]["语文"] = float(self.model.item(row,column).text())
                    if(column == 1):
                        Data[month][row]["数学"] = float(self.model.item(row,column).text())
                    if(column == 2):
                        Data[month][row]["英语"] = float(self.model.item(row,column).text())    
                    if(column == 3):
                        Data[month][row]["物理"] = float(self.model.item(row,column).text())
                    if(column == 4):
                        Data[month][row]["化学"] = float(self.model.item(row,column).text())
                    if(column == 5):        
                        Data[month][row]["生物"] = float(self.model.item(row,column).text())
            #   进行文件保存
            file = open('./conf/MonthScore.json','w')
            json.dump(Data,file,ensure_ascii=False)
            self.MessageBox("保存成功！")
            file.close()
        except Exception:
            print_exc()
            self.MessageBox("保存失败！请检查填入的数据！")

    def AddEvent(self):
        self.AddBox=AdminScoreAddBox.ScoreAddBox()
        self.close()
        self.AddBox.show()

    #   消息盒子
    def MessageBox(self,MessageString):
        MessageBox = QMessageBox()
        MessageBox.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.WindowMaximizeButtonHint | Qt.MSWindowsFixedSizeDialogHint)
        MessageBox.setWindowTitle("新消息")
        MessageBox.setText(MessageString)
        MessageBox.addButton(QPushButton("知道了"),QMessageBox.YesRole)
        MessageBox.exec_()


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
  table = TeacherTable()
  table.show()
  sys.exit(app.exec_())    
