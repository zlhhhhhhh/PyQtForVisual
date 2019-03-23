# -*- coding: utf-8 -*-

'''
Author: Lianghao ZOU
Date: 2019-03-06
Description:主窗口下的次级窗口
Version: 1.0
'''


from PyQt5 import QtWidgets,QtGui, QtCore
import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from pylab import mpl
import matplotlib
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


# 设置字体以及符号显示
matplotlib.use("Qt5Agg")
mpl.rcParams['font.sans-serif'] = ['SimHei']
mpl.rcParams['axes.unicode_minus'] = False


class SubWindow(QtWidgets.QWidget):
    def __init__(self):
        super(SubWindow, self).__init__()
        self.setObjectName("self")
        self.setMinimumSize(300,200)  # 设置窗口最小尺寸

        self.main_layout = QtWidgets.QGridLayout()
        self.main_layout.setSpacing(5)
        self.setLayout(self.main_layout)

        self.left_mini = QtWidgets.QPushButton("")
        self.left_max = QtWidgets.QPushButton("")
        self.left_close = QtWidgets.QPushButton("")

        #self.setCentralWidget(self.main_widget)
        #endregion

        self.main_layout.addWidget(self.left_mini,0,0,1,1,QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.main_layout.addWidget(self.left_max,0,1,1,1,QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.main_layout.addWidget(self.left_close,0,2,1,1,QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.left_close.setStyleSheet('''QPushButton{background:#F76677;border-radius:5px;}QPushButton:hover{background:red;}''')
        self.left_max.setStyleSheet('''QPushButton{background:#EEEE11;border-radius:5px;}QPushButton:hover{background:yellow;}''')
        self.left_mini.setStyleSheet('''QPushButton{background:#445CBB;border-radius:5px;}QPushButton:hover{background:blue;}''')

        #self.setAttribute(QtCore.Qt.WA_TranslucentBackground)# 设置窗口背景透明
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setStyleSheet('''QWidget#self{background:#D5D5D5;
                              border-radius:10px;}''')
        self.left_close.clicked.connect(self.exitSystem)
        self.left_mini.clicked.connect(self.miniSystem)
        self.left_max.clicked.connect(self.maxSystem)

    def exitSystem(self):
        self.close()

    def miniSystem(self):
        if not self.isMinimized():
            self.showMinimized()

    def maxSystem(self):
        if not self.isMaximized():
            self.showMaximized()
        else:
            self.showNormal()

    def mouseMoveEvent(self, e: QMouseEvent):
        try:
            self._endPos = e.pos() - self._startPos
            self.move(self.pos() + self._endPos)
        except:
            pass

    def mousePressEvent(self, e: QMouseEvent):
        if e.button() == Qt.LeftButton:
            self._isTracking = True
            self._startPos = QPoint(e.x(), e.y())
        else:
            self._isTracking = False

    def mouseReleaseEvent(self, e: QMouseEvent):
        if e.button() == Qt.LeftButton:
            self._isTracking = False
            self._startPos = None
            self._endPos = None

# 数据统计
class StatWindow(SubWindow):
    def __init__(self,result):
        super(StatWindow, self).__init__()
        self.result = result
        self.Stat_initUI()

    def Stat_initUI(self):
        self.setFixedSize(500,400)
        self.datalabel = QtWidgets.QLabel("统计结果")
        self.datalabel.setFont(QFont("SimHei",16,QFont.Bold))
        self.main_layout.addWidget(self.datalabel,2,0,1,10,Qt.AlignTop|Qt.AlignLeft)
        #self.content_label = QtWidgets.QLabel("")
        self.content_label = QtWidgets.QTextEdit()
        self.content_label.setFont(QFont("SimHei",12,QFont.Bold))
        self.content_label.setObjectName("content")
        #self.content_label.setScaledContents(True)
        self.content_label.setMinimumWidth(400)
        self.content_label.setStyleSheet("QTextEdit#content{letter-spacing::5px;line-height:1px}")
        #self.content_label.setWordWrap(True)
        self.content_label.setSizePolicy(QtWidgets.QSizePolicy.Expanding,QtWidgets.QSizePolicy.Expanding)
        self.main_layout.addWidget(self.content_label,3,0,10,10,Qt.AlignJustify|Qt.AlignLeft)
        try:
            res = "所选区域平均数为: "+str(self.result[0])+'\n' + "所选区域中位数为：" +str(self.result[1])+'\n'+\
              "所选区域众数为："+self.result[2]+'\n' + "所选区域极大值为："+str(self.result[3])+'\n'\
                + "所选区域极小值为："+str(self.result[4])+'\n'  + "所选区域方差为："+str(self.result[5])+'\n'\
                + "所选区域偏度为：" +str(self.result[6])+'\n'+ "所选区域峰度为："+str(self.result[7])+'\n'
        except Exception:
            pass
        self.content_label.setText(res)

# 数据检查
class DataCheck(SubWindow):
    Dc_signal = QtCore.pyqtSignal([float,float],[str,str])

    def __init__(self):
        super(DataCheck, self).__init__()
        self.input_min = 0
        self.input_max = 0
        self.nan_fill = ''
        self.DcInitUI()

    def DcInitUI(self):

        self.setFixedSize(300,200)
        self.setLayout(self.main_layout)
        min_label = QtWidgets.QLabel("Min: ")
        min_label.setFont(QFont("SimHei",12,QFont.Bold))
        self.min_edit = QtWidgets.QLineEdit(self)
        self.min_edit.setFont(QFont("SimHei",12,QFont.Bold))
        max_label = QtWidgets.QLabel("Max: ")
        max_label.setFont(QFont("SimHei", 12, QFont.Bold))
        self.max_edit = QtWidgets.QLineEdit(self)
        self.max_edit.setFont(QFont("SimHei",12,QFont.Bold))
        info_label = QtWidgets.QLabel("说明：如果检查空值，请都输入为/")
        info_label.setFont(QFont("SimHei", 8, QFont.Light))
        self.content_label = QtWidgets.QLabel("")
        self.content_label.setFont(QFont("SimHei", 12, QFont.Bold))
        self.content_label.setWordWrap(True)
        self.ok_btn = QtWidgets.QPushButton("确定")
        self.ok_btn.setFixedSize(30,20)
        self.ok_btn.setStyleSheet('''QPushButton{background:blue;border-radius:3px;color:white;}
                                QPushButton:hover{color:#0938F7;}''')
        self.cancel_btn = QtWidgets.QPushButton("取消")
        self.cancel_btn.setFixedSize(30, 20)
        self.cancel_btn.setStyleSheet('''QPushButton{background:red;border-radius:3px;color:white;}
                                    QPushButton:hover{color:#C43C57;}''')

        self.main_layout.addWidget(min_label,1,0,1,1, Qt.AlignLeft)
        self.main_layout.addWidget(max_label,2,0,1,1,Qt.AlignLeft)
        self.main_layout.addWidget(self.min_edit,1,1,1,4,Qt.AlignLeft)
        self.main_layout.addWidget(self.max_edit,2,1,1,4,Qt.AlignLeft)
        self.main_layout.addWidget(info_label,3,0,1,5,Qt.AlignLeft|Qt.AlignJustify)
        self.main_layout.addWidget(self.content_label,4,0,2,5,Qt.AlignLeft|Qt.AlignTop)
        self.main_layout.addWidget(self.ok_btn,6,1,1,1)
        self.main_layout.addWidget(self.cancel_btn,6,3,1,1)
        self.cancel_btn.clicked.connect(self.closeOK)
        self.ok_btn.clicked.connect(self.dc_emit)

    def closeOK(self):

        self.close()

    def dc_emit(self):
        if self.min_edit.text() =='/' and self.max_edit.text()=='/':
            self.Dc_signal[str,str].emit('/','/')
            return
        try:
            self.input_min = float(self.min_edit.text())
            self.input_max = float(self.max_edit.text())
            if self.input_max > self.input_min:
                self.Dc_signal[float,float].emit(self.input_min,self.input_max)
            else:
                QtWidgets.QMessageBox.critical(self,"错误","最小值应小于最大值")
        except Exception:
            QtWidgets.QMessageBox.critical(self,"错误","非法输入")

# 数据填充
class NanFillWindow(SubWindow):
    NanFill_Signal = QtCore.pyqtSignal(str)

    def __init__(self):
        super(NanFillWindow, self).__init__()
        self.NanFillInit()

    def NanFillInit(self):
        self.setFixedSize(250,200)
        self.setLayout(self.main_layout)
        title_label = QtWidgets.QLabel("请选择填充空值的方法")
        title_label.setFont(QFont("SimHei",12,QFont.Bold))
        self.main_layout.addWidget(title_label,2,0,1,10,Qt.AlignLeft|Qt.AlignJustify)
        self.combo = QtWidgets.QComboBox()
        self.combo.addItem("填充为零")
        self.combo.addItem("填充为平均值")
        self.combo.addItem("填充为复制值")
        self.combo.addItem("线性插值")
        self.combo.addItem("二次插值")
        self.combo.setStyleSheet('''QComboBox{font-family:SimHei;
                                    font-size:12px;
                                    outline:0px;
                                    min-height:20px;
                                    min-width:150px;}
                                    QComboBox::item{
                                    min-height:20px;
                                    min-width:100px;}''')
        self.combo.currentIndexChanged.connect(self.IndexChanged)
        self.main_layout.addWidget(self.combo,3,0,2,10,Qt.AlignTop|Qt.AlignLeft)
        self.info_label = QtWidgets.QLabel("说明：填充选中区域的空值为零")
        self.info_label.setFixedWidth(200)
        self.info_label.setFont(QFont("SimHei",10,QFont.Light))
        self.info_label.setWordWrap(True)
        self.main_layout.addWidget(self.info_label,5,0,2,10,Qt.AlignLeft|Qt.AlignTop)
        self.ok_btn = QtWidgets.QPushButton("确定")
        self.ok_btn.setFont(QFont("SimHei",10,QFont.Light))
        self.ok_btn.setFixedSize(30,20)
        self.ok_btn.setStyleSheet('''QPushButton{background:blue;border-radius:2px;color:white;}
                                QPushButton:hover{color:#0938F7;}''')
        self.cancel_btn = QtWidgets.QPushButton("取消")
        self.cancel_btn.setFixedSize(30,20)
        self.cancel_btn.setFont(QFont("SimHei",10,QFont.Light))
        self.cancel_btn.setStyleSheet('''QPushButton{background:red;border-radius:2px;color:white;}
                                    QPushButton:hover{color:#C43C57;}''')
        self.main_layout.addWidget(self.ok_btn,8,2,1,1)
        self.main_layout.addWidget(self.cancel_btn,8,5,1,1)
        self.ok_btn.clicked.connect(self.nan_emit)
        self.cancel_btn.clicked.connect(self.close_window)

    def IndexChanged(self):
        txt = self.combo.currentText()
        if txt == "填充为零":
            self.info_label.setText("说明：填充选中区域的空值为零,只填充数值类型")
        elif txt == "填充为平均值":
            self.info_label.setText("说明：填充选中区域的空值为有效值的平均值")
        elif txt == "填充为复制值":
            self.info_label.setText("说明：填充选中区域的空值为选中区域的第一个值")
        elif txt == "线性插值":
            self.info_label.setText("说明：利用选中区域的有效值进行线性插值")
        elif txt == "二次插值":
            self.info_label.setText("说明：利用选中区域的有效值进行二次插值")

    def close_window(self):
        self.close()

    def nan_emit(self):
        self.NanFill_Signal.emit(self.combo.currentText())

# 数据查找
class SearchWindow(SubWindow):
    SearchSignal = QtCore.pyqtSignal([str,str])

    def __init__(self):
        super(SearchWindow, self).__init__()
        self.SearchInit()

    def SearchInit(self):
        self.setFixedSize(250, 200)
        title_label = QtWidgets.QLabel("查找的元素值：")
        title_label.setFont(QFont("SimHei", 8, QFont.Light))
        search_label = QtWidgets.QLabel("选择查找模式")
        search_label.setFont(QFont("SimHei",8,QFont.Light))
        self.search_edit = QtWidgets.QLineEdit(self)
        self.search_edit.setFont(QFont("SimHei", 12, QFont.Bold))
        self.combo = QtWidgets.QComboBox()
        self.combo.addItem("精确匹配")
        self.combo.addItem("模糊匹配")
        self.combo.setStyleSheet('''QComboBox{font-family:SimHei;
                                    font-size:12px;
                                    outline:0px;
                                    min-height:20px;
                                    min-width:150px;}
                                    QComboBox::item{
                                    min-height:20px;
                                    min-width:100px;}''')
        self.content_label = QtWidgets.QLabel("")
        self.content_label.setFont(QFont("SimHei", 10, QFont.Light))
        self.ok_btn = QtWidgets.QPushButton("确定")
        self.ok_btn.setFont(QFont("SimHei",10,QFont.Light))
        self.ok_btn.setFixedSize(30,20)
        self.ok_btn.setStyleSheet('''QPushButton{background:blue;border-radius:2px;color:white;}
                                QPushButton:hover{color:#0938F7;}''')
        self.cancel_btn = QtWidgets.QPushButton("取消")
        self.cancel_btn.setFixedSize(30,20)
        self.cancel_btn.setFont(QFont("SimHei",10,QFont.Light))
        self.cancel_btn.setStyleSheet('''QPushButton{background:red;border-radius:2px;color:white;}
                                    QPushButton:hover{color:#C43C57;}''')
        self.main_layout.addWidget(title_label,2,0,1,2,Qt.AlignLeft|Qt.AlignJustify)
        self.main_layout.addWidget(self.search_edit,2,2,1,4,Qt.AlignLeft|Qt.AlignJustify)
        self.main_layout.addWidget(search_label,3,0,1,2,Qt.AlignVCenter|Qt.AlignHCenter)
        self.main_layout.addWidget(self.combo,3,2,1,4,Qt.AlignHCenter|Qt.AlignVCenter)
        self.main_layout.addWidget(self.content_label,4,0,2,5,Qt.AlignLeft|Qt.AlignJustify)
        self.main_layout.addWidget(self.ok_btn,6,1,1,1,Qt.AlignLeft|Qt.AlignJustify)
        self.main_layout.addWidget(self.cancel_btn,6,3,1,1,Qt.AlignLeft|Qt.AlignJustify)
        self.cancel_btn.clicked.connect(self.close_window)
        self.ok_btn.clicked.connect(self.search_emit)

    def close_window(self):
        self.close()

    def search_emit(self):
        self.SearchSignal[str,str].emit(self.search_edit.text(),self.combo.currentText())

# 添加一列
class AddColumnWindwow(SubWindow):
    AddColSignal = QtCore.pyqtSignal(str)
    def __init__(self):
        super(AddColumnWindwow, self).__init__()
        self.AddColInit()

    def AddColInit(self):
        self.setFixedSize(250, 150)
        title_label = QtWidgets.QLabel("请输入列名")
        title_label.setFont(QFont("SimHei", 10, QFont.Light))
        self.col_header_edit = QtWidgets.QLineEdit(self)
        self.col_header_edit.setFont(QFont("SimHei", 10, QFont.Bold))
        self.ok_btn = QtWidgets.QPushButton("确定")
        self.ok_btn.setFont(QFont("SimHei",10,QFont.Light))
        self.ok_btn.setFixedSize(30,20)
        self.ok_btn.setStyleSheet('''QPushButton{background:blue;border-radius:2px;color:white;}
                                QPushButton:hover{color:#0938F7;}''')
        self.cancel_btn = QtWidgets.QPushButton("取消")
        self.cancel_btn.setFixedSize(30,20)
        self.cancel_btn.setFont(QFont("SimHei",10,QFont.Light))
        self.cancel_btn.setStyleSheet('''QPushButton{background:red;border-radius:2px;color:white;}
                                    QPushButton:hover{color:#C43C57;}''')
        self.main_layout.addWidget(title_label,1,0,1,2,Qt.AlignTop|Qt.AlignLeft)
        self.main_layout.addWidget(self.col_header_edit,2,0,1,8,Qt.AlignTop|Qt.AlignLeft)
        self.main_layout.addWidget(self.ok_btn,3,1,1,1,Qt.AlignTop|Qt.AlignLeft)
        self.main_layout.addWidget(self.cancel_btn,3,3,1,1,Qt.AlignTop|Qt.AlignLeft)
        self.ok_btn.clicked.connect(self.AddCol_emit)
        self.cancel_btn.clicked.connect(self.close_window)


    def close_window(self):
        self.close()


    def AddCol_emit(self):
        self.AddColSignal.emit(self.col_header_edit.text())

# 可视化数据
class Visualization(SubWindow):
    Visual_Siganl = QtCore.pyqtSignal(str)
    def __init__(self):
        super(Visualization, self).__init__()
        self.VisInit()

    def VisInit(self):
        self.setFixedSize(800,600)
        title_label = QtWidgets.QLabel("请选择需要的图表:")
        title_label.setFont(QFont("SimHei", 12, QFont.Light))
        self.combo = QtWidgets.QComboBox()
        self.combo.addItem("     ")
        self.combo.addItem("柱状图")
        self.combo.addItem("散点图")
        self.combo.addItem("饼状图")
        self.combo.addItem("折线图")
        self.combo.setStyleSheet('''QComboBox{font-family:SimHei;
                                    font-size:12px;
                                    outline:0px;
                                    min-height:20px;
                                    min-width:150px;}
                                    QComboBox::item{
                                    min-height:20px;
                                    min-width:100px;}''')
        self.plot_widget = Figure(figsize=(200,200),dpi=100,facecolor="#D5D5D5")
        self.plot_canvas = FigureCanvas(self.plot_widget)
        self.plot_widget.subplots_adjust(left=0.065, right=0.935, bottom=0.15, top=0.95, hspace=0.1, wspace=0.1)
        self.main_layout.addWidget(title_label,3,0,1,2,Qt.AlignLeft|Qt.AlignBottom)
        #self.main_layout.setContentsMargins(10,10,10,10)
        self.main_layout.addWidget(self.combo,3,2,1,5,Qt.AlignLeft|Qt.AlignBottom)
        self.main_layout.addWidget(self.plot_canvas,6,0,5,10,Qt.AlignLeft|Qt.AlignBottom)
        self.combo.currentIndexChanged.connect(self.VisSignalEmit)

    def VisSignalEmit(self):
        self.Visual_Siganl.emit(self.combo.currentText())

# 聚类算法
class Cluster(SubWindow):

    ClusterSignal = QtCore.pyqtSignal([str,str,str])
    def __init__(self):
        super(Cluster, self).__init__()
        self.ClusterInit()

    def ClusterInit(self):
        self.setFixedSize(800,600)
        title_label = QtWidgets.QLabel("请选择分类的数量")
        title_label.setFont(QFont("SimHei", 10, QFont.Light))
        self.cluster_edit = QtWidgets.QLineEdit()
        self.cluster_edit.setPlaceholderText("默认为两类")
        title_label_2 = QtWidgets.QLabel("最大迭代次数")
        title_label_2.setFont(QFont("SimHei", 10, QFont.Light))
        self.iter_edit = QtWidgets.QLineEdit()
        self.iter_edit.setPlaceholderText("默认为500次")
        title_label_3 = QtWidgets.QLabel("判断是否收敛的阈值")
        title_label_3.setFont(QFont("SimHei",10, QFont.Light))
        self.thres_edit = QtWidgets.QLineEdit()
        self.thres_edit.setPlaceholderText("默认为0.0001")
        self.plot_widget = Figure(figsize=(200, 200), dpi=100, facecolor="#D5D5D5")
        self.plot_canvas = FigureCanvas(self.plot_widget)
        self.plot_widget.subplots_adjust(left=0.065, right=0.935, bottom=0.15, top=0.95, hspace=0.1, wspace=0.1)
        self.ok_btn = QtWidgets.QPushButton("确定")
        self.ok_btn.setFont(QFont("SimHei",10,QFont.Light))
        self.ok_btn.setFixedSize(30,20)
        self.ok_btn.setStyleSheet('''QPushButton{background:blue;border-radius:2px;color:white;}
                                QPushButton:hover{color:#0938F7;}''')

        self.cancel_btn = QtWidgets.QPushButton("取消")
        self.cancel_btn.setFont(QFont("SimHei",10,QFont.Light))
        self.cancel_btn.setFixedSize(30,20)
        self.cancel_btn.setStyleSheet('''QPushButton{background:red;border-radius:2px;color:white;}
                                QPushButton:hover{color:#0938F7;}''')
        self.main_layout.addWidget(title_label, 2, 0, 1, 2, Qt.AlignLeft | Qt.AlignBottom)
        self.main_layout.addWidget(self.cluster_edit, 2, 2, 1, 2, Qt.AlignLeft | Qt.AlignBottom)
        self.main_layout.addWidget(title_label_2, 2, 5, 1, 1, Qt.AlignLeft | Qt.AlignBottom)
        self.main_layout.addWidget(self.iter_edit, 2, 6, 1, 2, Qt.AlignLeft | Qt.AlignBottom)
        self.main_layout.addWidget(title_label_3, 3, 0, 1, 2, Qt.AlignLeft | Qt.AlignBottom)
        self.main_layout.addWidget(self.thres_edit, 3, 2, 1, 2, Qt.AlignLeft | Qt.AlignBottom)
        self.main_layout.addWidget(self.ok_btn,3,5,1,1,Qt.AlignLeft | Qt.AlignBottom)
        self.main_layout.addWidget(self.cancel_btn,3,6,1,1,Qt.AlignLeft | Qt.AlignBottom)
        self.main_layout.addWidget(self.plot_canvas, 4, 0, 5, 10, Qt.AlignLeft | Qt.AlignBottom)

        self.ok_btn.clicked.connect(self.ClusterSignalEmit)
        self.cancel_btn.clicked.connect(self.CloseEvent)

    def ClusterSignalEmit(self):
        self.ClusterSignal[str,str,str].emit(self.cluster_edit.text(),self.iter_edit.text(),self.thres_edit.text())

    def CloseEvent(self):
        self.close()

# 线性回归
class Regression(SubWindow):

    RegressionSignal = QtCore.pyqtSignal([str,str])
    def __init__(self):
        super(Regression, self).__init__()
        self.RegressionInit()

    def RegressionInit(self):
        self.setFixedSize(800,700)
        title_label = QtWidgets.QLabel("请设置学习率")
        title_label.setFont(QFont("SimHei", 10, QFont.Light))
        self.regre_edit = QtWidgets.QLineEdit()
        self.regre_edit.setPlaceholderText("默认为0.001")
        title_label_2 = QtWidgets.QLabel("最大迭代次数")
        title_label_2.setFont(QFont("SimHei", 10, QFont.Light))
        self.iter_edit = QtWidgets.QLineEdit()
        self.iter_edit.setPlaceholderText("默认为5000次")

        self.plot_widget = Figure(figsize=(200, 200), dpi=100, facecolor="#D5D5D5")
        self.plot_canvas = FigureCanvas(self.plot_widget)
        #ax = self.plot_widget.add_subplot(111)
        self.plot_widget.subplots_adjust(left=0.065, right=0.935, bottom=0.15, top=0.95, hspace=0.1, wspace=0.1)
        self.ok_btn = QtWidgets.QPushButton("确定")
        self.ok_btn.setFont(QFont("SimHei",10,QFont.Light))
        self.ok_btn.setFixedSize(30,20)
        self.ok_btn.setStyleSheet('''QPushButton{background:blue;border-radius:2px;color:white;}
                                QPushButton:hover{color:#0938F7;}''')
        self.result_label = QtWidgets.QTextEdit("w = \nb = ")
        self.result_label.setFont(QFont("SimHei",10,QFont.Light))
        #self.result_label.setWordWrap(True)
        self.result_label.setStyleSheet("QLabel{border-width:1 px;border-style:solid}")
        self.cancel_btn = QtWidgets.QPushButton("取消")
        self.cancel_btn.setFont(QFont("SimHei",10,QFont.Light))
        self.cancel_btn.setFixedSize(30,20)
        self.cancel_btn.setStyleSheet('''QPushButton{background:red;border-radius:2px;color:white;}
                                QPushButton:hover{color:#0938F7;}''')
        self.main_layout.addWidget(title_label, 2, 0, 1, 1, Qt.AlignLeft | Qt.AlignBottom)
        self.main_layout.addWidget(self.regre_edit, 2,1, 1, 2, Qt.AlignLeft | Qt.AlignBottom)
        self.main_layout.addWidget(title_label_2, 3, 0, 1, 1, Qt.AlignLeft | Qt.AlignBottom)
        self.main_layout.addWidget(self.iter_edit, 3, 1, 1, 2, Qt.AlignLeft | Qt.AlignBottom)
        self.main_layout.addWidget(self.result_label,2,3,2,5, Qt.AlignLeft | Qt.AlignTop)
        self.main_layout.addWidget(self.ok_btn,4,0,1,1,Qt.AlignLeft | Qt.AlignBottom)
        self.main_layout.addWidget(self.cancel_btn,4,1,1,1,Qt.AlignLeft | Qt.AlignBottom)
        self.main_layout.addWidget(self.plot_canvas, 5, 0, 5, 10, Qt.AlignLeft | Qt.AlignBottom)

        self.ok_btn.clicked.connect(self.RegressionSignalEmit)
        self.cancel_btn.clicked.connect(self.CloseEvent)

    def RegressionSignalEmit(self):
        self.RegressionSignal[str,str].emit(self.regre_edit.text(),self.iter_edit.text())

    def CloseEvent(self):
        self.close()



# Back up the reference to the exceptionhook
sys._excepthook = sys.excepthook

def my_exception_hook(exctype, value, traceback):
    # Print the error and traceback
    print(exctype, value, traceback)
    # Call the normal Exception hook after
    sys._excepthook(exctype, value, traceback)
    sys.exit(1)

# Set the exception hook to our wrapping function
sys.excepthook = my_exception_hook

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    gui =StatWindow()
    gui.show()
    try:
        sys.exit(app.exec_())
    except:
        print("exciting")


