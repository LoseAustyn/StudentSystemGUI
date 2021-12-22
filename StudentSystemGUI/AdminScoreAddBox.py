import sys
import qtawesome
import json
import AdminTableList
from traceback import print_exc
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

class ScoreAddBox(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    #   主界面UI
    def initUI(self):
        #   主窗口大小
        self.windowX = 600
        self.windowY = 250
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
        self.QuitButton.setGeometry(690,10,20,20)
        self.QuitButton.setToolTip("退出")
        self.QuitButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.QuitButton.clicked.connect(self.close)

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
        self.TitleText.setText("添加成绩")
        self.TitleText.setFont(QFont("黑体",10))
        self.TitleText.setStyleSheet("background-color:rgba(135,206,250,0);color:white")
        self.TitleText.setGeometry(20,15,100,20)

        #   装饰文字
        self.MonthLabel = QLabel(self)
        self.MonthLabel.setText("月考：")
        self.MonthLabel.setFont(QFont("黑体",12))
        self.MonthLabel.setStyleSheet("background-color:rgba(135,206,250,0);color:white")
        self.MonthLabel.setGeometry(100,70,100,20)

        #   装饰文字
        self.NumLabel = QLabel(self)
        self.NumLabel.setText("学生数量：")
        self.NumLabel.setFont(QFont("黑体",12))
        self.NumLabel.setStyleSheet("background-color:rgba(135,206,250,0);color:white")
        self.NumLabel.setGeometry(60,120,100,20)

        #   月考输入栏
        self.MonthInput = QTextEdit(self)
        self.MonthInput.setGeometry((self.windowX - 300) / 2,65,300,30)
        self.MonthInput.setFont(QFont("黑体",10))
        self.MonthInput.setFixedHeight(30)
        self.MonthInput.setPlaceholderText("第几次月考（请输入数字）")
        self.MonthInput.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.MonthInput.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.MonthInput.setStyleSheet("QTextEdit {""background: transparent;border-width:0px; border-style:outset;color:#F8F8FF;border-bottom:2px dashed #F8F8FF;""}"
                                     "QTextEdit:focus {""border-bottom:2px dashed #4169E1;""}")

        #   学生数量输入栏
        self.StudentNumInput = QTextEdit(self)
        self.StudentNumInput.setGeometry((self.windowX - 300) / 2,115,300,30)
        self.StudentNumInput.setFont(QFont("黑体",10))
        self.StudentNumInput.setPlaceholderText("添加多少个学生")
        self.StudentNumInput.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.StudentNumInput.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.StudentNumInput.setStyleSheet("QTextEdit {""background: transparent;border-width:0px; border-style:outset;color:#F8F8FF;border-bottom:2px dashed #F8F8FF;""}"
                                         "QTextEdit:focus {""border-bottom:2px dashed #4169E1;""}")

        #   添加按钮
        self.AddButton = QPushButton(qtawesome.icon('fa.plus', color='white'),"添加",self)
        self.AddButton.setStyleSheet("background-color:rgba(255,165,0,0.9);border:0px;border-radius:5px")
        self.AddButton.setIconSize(QSize(20, 20))
        self.AddButton.setGeometry((self.windowX - 300) / 2,165,140,25)
        self.AddButton.setToolTip("添加")
        self.AddButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.AddButton.clicked.connect(self.AddRow)

        #   取消按钮
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
        self.LoadScoreData()
        try:
            month = self.MonthInput.toPlainText()
            num = int(self.StudentNumInput.toPlainText())
            
            #   添加学生
            if month in self.ScoreData:
                length = len(self.ScoreData[month])
                for row in range(num):
                    length+=1
                    NewIn = {
                        "学号":length,
                        "语文": 0,
                        "数学": 0,
                        "英语": 0,
                        "物理": 0,
                        "化学": 0,
                        "生物": 0
                        }
                    self.ScoreData[month].append(NewIn)
            else:
                NewIn = {month:[]}
                self.ScoreData.update(NewIn)
                length = 0
                for row in range(num):
                    length+=1
                    NewIn = {
                        "学号":length,
                        "语文": 0,
                        "数学": 0,
                        "英语": 0,
                        "物理": 0,
                        "化学": 0,
                        "生物": 0
                        }
                    self.ScoreData[month].append(NewIn)

            file = open('./conf/MonthScore.json','w')
            json.dump(self.ScoreData,file,ensure_ascii=False)
            self.MessageBox("添加成功！请返回表格界面进行编辑！")
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

    #   读取成绩文件
    def LoadScoreData(self):
        file = open('./conf/MonthScore.json')
        self.ScoreData = json.load(file)
        file.close()

    def Back(self):
        self.close()
        self.table = AdminTableList.TeacherTable()
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
    window = ScoreAddBox()
    #   显示主窗口
    window.show()
    sys.exit(app.exec_())