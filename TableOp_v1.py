# -*- coding: utf-8 -*-

'''
Author: Lianghao ZOU
Date: 2019-03-06
Description:数据表处理
Version: 1.0
'''

from mpl_toolkits.mplot3d import Axes3D

import pandas as pd
import numpy as np
from PyQt5 import QtWidgets,QtGui, QtCore
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import qtawesome as qta
import SubWindow
import K_means
import linear_Regression
import sys

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.initUI()
        self.pfilename = ''
        self.filetype =''


    def initUI(self):

        # region定义整体布局
        self.setObjectName("self")
        self.setMinimumSize(1000,800)  # 设置窗口最小尺寸
        self.main_widget = QtWidgets.QWidget()
        self.main_layout = QtWidgets.QGridLayout()
        self.main_widget.setObjectName("main_widget")
        self.main_widget.setLayout(self.main_layout)  # 设置主控件为网格布局

        self.left_widget = QtWidgets.QWidget()
        self.left_layout = QtWidgets.QGridLayout()
        self.left_widget.setObjectName("left_widget")
        self.left_widget.setLayout(self.left_layout)

        self.right_widget = QtWidgets.QWidget()
        self.right_layout = QtWidgets.QGridLayout()
        self.right_widget.setObjectName("right_widget")
        self.right_widget.setLayout(self.right_layout)

        self.main_layout.addWidget(self.left_widget,0,0,10,3) # 从第0行0列开始，跨越五行三列，采用默认的对齐方式
        self.main_layout.addWidget(self.right_widget,0,3,10,12)
        self.setCentralWidget(self.main_widget)
        #endregion

        # region 左侧控件
        self.left_mini = QtWidgets.QPushButton("")
        self.left_max = QtWidgets.QPushButton("")
        self.left_close = QtWidgets.QPushButton("")

        self.left_tableio = QtWidgets.QPushButton(qta.icon("fa.table",color="white"),"数据读写")
        self.left_tableio.setObjectName("left_menu_btn")
        self.left_tableio.setContextMenuPolicy(Qt.CustomContextMenu)
        self.left_tableio.customContextMenuRequested.connect(self.showContextMenu)
        self.contextMenu_tableio = QtWidgets.QMenu(self.left_tableio)
        self.contextMenu_tableio.setObjectName("left_menu")
        self.act_left_import = self.contextMenu_tableio.addAction(qta.icon('fa.file-archive-o',color="white"),"数据导入")
        self.act_left_save = self.contextMenu_tableio.addAction(qta.icon("fa.save",color="white"),"数据保存")
        self.act_left_saveas = self.contextMenu_tableio.addAction(qta.icon("fa.copy",color = "white"),"数据另存为")


        self.left_stat = QtWidgets.QPushButton(qta.icon("fa.edit",color="white"),"数据分析")
        self.left_stat.setObjectName("left_menu_btn")
        self.left_stat.setContextMenuPolicy(Qt.CustomContextMenu)
        self.left_stat.customContextMenuRequested.connect(self.showContextMenu_1)
        self.contextMenu_stat = QtWidgets.QMenu(self.left_stat)
        self.contextMenu_stat.setObjectName("left_menu")
        self.act_left_basic = self.contextMenu_stat.addAction(qta.icon('fa.sort-amount-desc',color="white"),"数据统计")
        self.act_left_adv = self.contextMenu_stat.addAction(qta.icon('fa.signal',color ="white"),"相关性分析")


        self.left_dataop = QtWidgets.QPushButton(qta.icon("fa.wrench",color="white"),"数据处理")
        self.left_dataop.setObjectName("left_menu_btn")
        self.left_dataop.setContextMenuPolicy(Qt.CustomContextMenu)
        self.left_dataop.customContextMenuRequested.connect(self.showContextMenu_2)
        self.contextMenu_dataop = QtWidgets.QMenu(self.left_dataop)
        self.contextMenu_dataop.setObjectName("left_menu")
        self.act_left_rowcol = self.contextMenu_dataop.addAction(qta.icon("fa.delicious",color="white"),"数据检查")# 增删行列
        self.act_left_dataop = self.contextMenu_dataop.addAction(qta.icon("fa.exchange", color="white"), "数据变换")# 标准化，缺失值填充，数据归一化，排序
        self.act_left_search = self.contextMenu_dataop.addAction(qta.icon("fa.search",color="white"),"数据查找")#快速查找，模糊查找

        self.left_model = QtWidgets.QPushButton(qta.icon("fa.magic",color="white"),"模型分析")
        self.left_model.setObjectName("left_menu_btn")
        self.left_model.setContextMenuPolicy(Qt.CustomContextMenu)
        self.left_model.customContextMenuRequested.connect(self.showContextMenu_3)
        self.contextMenu_model = QtWidgets.QMenu(self.left_model)
        self.contextMenu_model.setObjectName("left_menu")
        self.act_left_cluster = self.contextMenu_model.addAction(qta.icon("fa.cube",color="white"),"聚类模型")
        self.act_left_mutli_regression = self.contextMenu_model.addAction(qta.icon("fa.compass",color="white"),
                                                                          "多元回归")
        self.act_left_randomforest = self.contextMenu_model.addAction(qta.icon("fa.tree",color="white"),"随机森林")
        self.act_left_neural = self.contextMenu_model.addAction(qta.icon("fa.venus",color="white"),"神经网络")
        self.act_left_svm = self.contextMenu_model.addAction(qta.icon("fa.rocket",color="white"),"支持向量机")
        self.act_left_series = self.contextMenu_model.addAction(qta.icon("fa.circle-o-notch",color="white"),"序列分解")

        self.left_visual = QtWidgets.QPushButton(qta.icon("fa.bar-chart",color="white"),"数据可视化")
        self.left_visual.setObjectName("left_menu_btn")

        '''
        self.left_logo = QtWidgets.QLabel("")
        self.left_logo.setMaximumSize(150,100)
        img = QtGui.QPixmap('CountryGarden.jpg')
        self.left_logo.setPixmap(img)
        self.left_logo.setScaledContents(True)
        '''
        self.left_layout.addWidget(self.left_mini,0,0,1,1,QtCore.Qt.AlignJustify)
        self.left_layout.addWidget(self.left_max,0,1,1,1,QtCore.Qt.AlignJustify)
        self.left_layout.addWidget(self.left_close,0,2,1,1,QtCore.Qt.AlignJustify)
        self.left_layout.addWidget(self.left_tableio,1,0,1,3)
        self.left_layout.addWidget(self.left_stat,2,0,1,3)
        self.left_layout.addWidget(self.left_dataop,3,0,1,3)
        self.left_layout.addWidget(self.left_model,4,0,1,3)
        self.left_layout.addWidget(self.left_visual,5,0,1,3)
        #self.left_layout.addWidget(self.left_logo,6,0,1,3)
        # endregion

        # region  右侧部件
        self.right_label = QtWidgets.QLabel("")
        self.right_label.setFont(QtGui.QFont("SimHei",10,QtGui.QFont.Bold))
        self.right_tableview = QtWidgets.QTableWidget()
        self.right_tableview.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Interactive)
        self.right_tableview.setMinimumSize(500,400)

        self.right_tableview.setContextMenuPolicy(Qt.CustomContextMenu)
        self.right_tableview.customContextMenuRequested.connect(self.TableShowContextMenu)
        self.right_context_menu = QtWidgets.QMenu(self.right_tableview)
        self.right_context_menu.setObjectName("right_menu")
        #self.right_context_menu.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.act_right_addcol = self.right_context_menu.addAction(qta.icon('fa.book',color ="white"),"增加一列")
        self.act_right_addrow = self.right_context_menu.addAction(qta.icon('fa.bell',color='white'),"增加一行")
        self.act_right_delrow = self.right_context_menu.addAction(qta.icon('fa.adjust',color='white'),"删除一行")
        self.act_right_delcol = self.right_context_menu.addAction(qta.icon('fa.bug',color='white'),"删除一列")
        self.act_right_notsel = self.right_context_menu.addAction(qta.icon('fa.bomb',color='white'),"取消选择")


        self.right_status = QtWidgets.QStatusBar()
        self.right_status.setMaximumHeight(20)
        self.right_status.setMinimumWidth(800)
        self.right_status.showMessage('value = ')

        self.right_layout.addWidget(self.right_label,0,0,1,5,Qt.AlignBottom)
        self.right_layout.setSpacing(0)
        self.right_layout.addWidget(self.right_tableview,1,0,10.5,12)
        self.right_layout.setSpacing(0)
        self.right_layout.addWidget(self.right_status,11,0,1,12,QtCore.Qt.AlignLeft)
        self.right_layout.setSpacing(0)
        # endregion

        # region美化界面
        self.left_close.setFixedSize(15,15)
        self.left_max.setFixedSize(15,15)
        self.left_mini.setFixedSize(15,15)
        self.left_close.setStyleSheet('''QPushButton{background:#F76677;border-radius:5px;}QPushButton:hover{background:red;}''')
        self.left_max.setStyleSheet('''QPushButton{background:#EEEE11;border-radius:5px;}QPushButton:hover{background:yellow;}''')
        self.left_mini.setStyleSheet('''QPushButton{background:#445CBB;border-radius:5px;}QPushButton:hover{background:blue;}''')
        self.left_widget.setStyleSheet('''
        QPushButton{border:none;color:white;}
        QPushButton#left_menu_btn{
            border:none;
            border-bottom:1px solid white;
            font-size:18px;
            font-weight:700;
            font-family:Helvetica Neue, Helvetica, Arial, sans-serif;
        }
        QMenu#left_menu{
            background:#B3B3B3;
            border:1px solid white;
            font-size:15px;
            border-bottom-left-radius:10px;
            border-top-left-radius:10px;
            border-bottom-right-radius:10px;
            border-top-right-radius:10px;
        }
        QPushButton#left_menu_btn:hover{
            border-left:3px solid white;
            font-weight:700;
        }
        QWidget#left_widget{
            background:grey;
            border-top:1px solid white;
            border-bottom:1px solid white;
            border-left:1px solid white;
            border-top-left-radius:10px;
            border-bottom-left-radius:10px;
        }
        ''')
        self.right_widget.setStyleSheet('''
        QWidget#right_widget{
            background:white;
            border-top:1px solid darkGray;
            border-bottom:1px solid darkGray;
            border-right:1px solid darkGray;
            border-top-right-radius:10px;
            border-bottom-right-radius:10px;
        }
        QMenu#right_menu{
            background:#B3B3B3;
            border:1px solid white;
            font-size:15px;
            border-bottom-left-radius:10px;
            border-top-left-radius:10px;
            border-bottom-right-radius:10px;
            border-top-right-radius:10px;
        }
        ''')
        #self.setWindowOpacity(0.9)# 设置窗口透明度
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)# 设置窗口背景透明
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.main_layout.setSpacing(0)
        # endregion

        # region 信号与槽函数相连
        #======================窗体按钮============== #
        self.left_close.clicked.connect(self.exitSystem)
        self.left_mini.clicked.connect(self.miniSystem)
        self.left_max.clicked.connect(self.maxSystem)
        # ========================================== #

        self.right_tableview.itemClicked.connect(lambda:self.on_status(self.right_tableview.selectedItems()))

        #=====================文件导入导出============ #
        self.act_left_import.triggered.connect(self.FileSelect)
        self.act_left_save.triggered.connect(self.FileSave)
        self.act_left_saveas.triggered.connect(self.FileSaveAs)
        # ========================================== #

        # ====================数据分析=============== #
        self.act_left_basic.triggered.connect(self.baiscStat)
        # ========================================== #

        # =====================数据处理=============== #
        self.act_left_rowcol.triggered.connect(self.CheckData)
        self.act_left_dataop.triggered.connect(self.NanFill)
        self.act_left_search.triggered.connect(self.SearchData)
        # =========================================== #

        # =====================增加行列=============== #
        self.act_right_addcol.triggered.connect(self.AddCol)
        self.act_right_addrow.triggered.connect(self.AddRow)
        self.act_right_delcol.triggered.connect(self.DelCol)
        self.act_right_delrow.triggered.connect(self.DelRow)
        self.act_right_notsel.triggered.connect(self.NotSel)
        # =========================================== #

        # =====================可视化=============== #
        self.left_visual.clicked.connect(self.Visualize)
        # =========================================== #

        # =====================模型分析================ #
        self.act_left_cluster.triggered.connect(self.Cluster)
        self.act_left_svm.triggered.connect(self.SVM)
        self.act_left_mutli_regression.triggered.connect(self.Regression)
        self.act_left_neural.triggered.connect(self.Neural)
        self.act_left_randomforest.triggered.connect(self.RandomForest)
        self.act_left_series.triggered.connect(self.Trend_Decompose)
        # ============================================ #
        # endregion

    # 更新状态栏的值
    def on_status(self,selected_items):
        if len(selected_items)!= 0:
            status_item = selected_items[-1].text()
            self.right_status.showMessage('value = '+status_item)

    # tablewidget（表单部件）更新时，同步更新后台的dataframe
    def item_Changed_Event(self):
        self.data_save = self.TabletoDf()
        # 以下的函数在运行时会弹出警告
        self.data_save = self.data_save.convert_objects(convert_numeric=True)

    # region 打开文档
    def FileSelect(self):
        try:
            pfilename,filetype = QtWidgets.QFileDialog.getOpenFileName(self,"选择文件","","2007 excel files(*.xlsx);;"
                                                                                      "2003 excel files(*.xls);;"
                                                                                      "csv files(*.csv)")
        except Exception:
            return
        self.pfilename, self.filetype = pfilename, filetype
        self.showTable()
        self.right_tableview.itemChanged.connect(self.item_Changed_Event)

    # 展示table，并后台转化为dataframe 方便计算
    def showTable(self):
        try:
            if self.pfilename == '':
                return
            if self.filetype in ["2007 excel files(*.xlsx)","2003 excel files(*.xls)"]:
                input_table = pd.read_excel(self.pfilename)
            elif self.filetype == "csv files(*.csv)":
                input_table = pd.read_csv(self.pfilename,encoding='GB2312',error_bad_lines=False,float_precision="high")
            self.right_label.setText(self.pfilename)
            input_table_rows = input_table.shape[0] # 行
            input_table_cols = input_table.shape[1] # 列
            input_table_header = input_table.columns.values.tolist() # 表头

            self.right_tableview.setColumnCount(input_table_cols)
            self.right_tableview.setRowCount(input_table_rows)
            self.right_tableview.setHorizontalHeaderLabels(input_table_header)

            for i in range(input_table_rows):
                input_row_values = input_table.iloc[[i]]
                input_row_values_array = np.array(input_row_values)
                input_row_values_list = input_row_values_array[0].tolist()
                for j in range(input_table_cols):
                    value_item = str(input_row_values_list[j])
                    input_item = QtWidgets.QTableWidgetItem(value_item)
                    input_item.setTextAlignment(Qt.AlignHCenter|Qt.AlignVCenter)
                    self.right_tableview.setItem(i,j,input_item)
            self.data_save = self.TabletoDf()
            #以下的函数在运行时会弹出警告
            self.data_save = self.data_save.convert_objects(convert_numeric=True)
        except Exception:
            QtWidgets.QMessageBox.critical(self, "错误", "无法读取所选文件")
            #self.close()

    # endregion

    # region 保存文档
    def FileSave(self):
        self.right_status.showMessage("正在保存...")
        if self.pfilename == "":
            return
        self.data_save = self.TabletoDf()
        try:
            if self.filetype in ["2007 excel files(*.xlsx)","2003 excel files(*.xls)"]:
                self.data_save.to_excel(self.pfilename,index=False)
            elif self.filetype == "csv files(*.csv)":
                self.data_save.to_csv(self.pfilename,index=False)
        except Exception:
            QtWidgets.QMessageBox.information(self, "错误", "保存失败，文件已打开")
        self.right_status.showMessage("保存成功！",2000)

    def FileSaveAs(self):
        if self.pfilename == "":
            return
        path,ftype = QtWidgets.QFileDialog.getSaveFileName(self,"选择文件","","excel files(*.xlsx);;"
                                                                                  "csv files(*.csv)")
        if ftype=="excel files(*.xlsx)":
            self.data_save.to_excel(path,index=False)
        elif ftype == "csv files(*.csv)":
            self.data_save.to_csv(path,index=False)

    # 将数据表转化到dataframe
    def TabletoDf(self):
        num_row = self.right_tableview.rowCount()
        num_col = self.right_tableview.columnCount()
        header = []
        list_temp = [[] for i in range(num_col)]
        for i in range(num_col):
            if self.right_tableview.horizontalHeaderItem(i):
                header.append(self.right_tableview.horizontalHeaderItem(i).text())
            else:
                header.append("New_Column")
            for j in range(num_row):
                if self.right_tableview.item(j,i) is not None:
                    list_temp[i].append(self.right_tableview.item(j,i).text())
                else:
                    list_temp[i].append("nan")


        dic = {k:v for k,v in zip(header,list_temp)}
        col = list(dic.keys())
        df_temp = pd.DataFrame(data=dic,columns=col)
        print(df_temp)
        return df_temp


    # endregion

    # region 统计
    '''
    对数据进行基本的统计计算，对于可能存在的字符型数据将只进行众数统计,
    统计结果保存3位或4位小数
    '''
    def baiscStat(self):
        res_item = self.right_tableview.selectedItems()
        res_str = list(map(lambda item:item.text(),res_item))
        res = []
        try:
            res_num = list(map(float,res_str))
            df = pd.DataFrame(data=res_num)
        except Exception :
            df_1 = pd.DataFrame(data= res_str)
            str_mod_1 = list(map(str,df_1[0].mode()))
            str_mod = ", ".join(str_mod_1)
            res = ["","",str_mod,"","","","",""]
            self.stat_window = SubWindow.StatWindow(res)
            self.stat_window.show()
            return

        if not df.empty:
            item_count = int(df.count())
            self.right_status.showMessage("选中了 " + str(item_count) + "要素", 5000)
            item_avg = round(float(df.mean()),3)#计算平均值
            res.append(item_avg)
            item_mid = round(float(df.median()),3)# 计算中位数
            res.append(item_mid)
            item_mod_1 = list(map(str, list(df[0].mode())))# 计算众数
            item_mod = ', '.join(item_mod_1)
            res.append(item_mod)
            item_max = float(df.max())# 计算极大值
            res.append(item_max)
            item_min = round(float(df.min()),3)# 计算极小值
            res.append(item_min)
            item_var = round(float(df.var()),3)# 计算极小值
            res.append(item_var)
            item_skew = round(float(df.skew()),3)# 计算偏度
            res.append(item_skew)
            item_kurt = float(round(df.kurt(), 4))# 计算峰度
            res.append(item_kurt)
            self.stat_window = SubWindow.StatWindow(res)
            self.stat_window.show()

    # endregion

    # region 检查数据
    '''
    检查数据的合法性，可以检查空值，也可以输入最小值和最大值，找到不在此范围内的值
    '''
    def CheckData(self):
        try:
            # 断开连接，避免重复对某一个元素操作时触发函数，造成时间上的浪费
            self.right_tableview.itemChanged.disconnect(self.item_Changed_Event)
        except:
            pass
        self.checkwindow = SubWindow.DataCheck()
        self.checkwindow.Dc_signal[float,float].connect(self.MyCheck)
        self.checkwindow.Dc_signal[str,str].connect(self.MyCheck)
        self.checkwindow.cancel_btn.clicked.connect(self.Init)
        self.checkwindow.show()
        try:
            self.right_tableview.itemChanged.connect(self.item_Changed_Event)
        except Exception:
            pass

    def Init(self):
        pass


    def MyCheck(self,pMin,pMax):
        if len(self.right_tableview.selectedIndexes()) == 0:
            self.right_tableview.selectAll()

        top_left_col = self.right_tableview.selectedIndexes()[0].column()
        top_left_row = self.right_tableview.selectedIndexes()[0].row()
        bot_right_col = self.right_tableview.selectedIndexes()[-1].column()
        bot_right_row = self.right_tableview.selectedIndexes()[-1].row()
        df_selected = self.data_save.iloc[top_left_row:bot_right_row+1,top_left_col:bot_right_col+1]

        header = df_selected.columns.values.tolist()

        # 选出空值
        if pMin=='/' and pMax=='/':
            # 在全局搜索填充为空值的位置，将其颜色设为红色，并且将鼠标滚轮移动到第一个的位置
            self.Init()
            items_sel = self.right_tableview.findItems('nan',QtCore.Qt.MatchExactly)
            if items_sel:
                row = items_sel[0].row()
                self.right_tableview.clearSelection()
                for item in items_sel:
                    item.setSelected(True)
                self.right_tableview.verticalScrollBar().setSliderPosition(row)
                self.checkwindow.content_label.setText("找到空值元素"+ str(len(items_sel)) + '个')
            else:
                self.checkwindow.content_label.setText("未找到空值元素")
        else:
            if self.right_tableview.selectedRanges()[0].columnCount() > 1:
                self.checkwindow.content_label.setText("请保持所选字段数量为1")
            else:
                try:
                    myMin, myMax = float(pMin),float(pMax)
                    pList = df_selected.loc[(df_selected[header[0]]<myMin)|(df_selected[header[0]]>myMax)].index.tolist()
                    self.right_tableview.clearSelection()
                    for i in pList:
                        self.right_tableview.item(top_left_row+i,top_left_col).setSelected(True)
                        #self.right_tableview.item(top_left_row+i,top_left_col).setForeground(Qt.red)
                    self.checkwindow.content_label.setText("找到不合法要素"+str(len(pList))+"个")
                except Exception:
                    QtWidgets.QMessageBox.critical(self,"错误","所选字段数据类型不是数值类型”")



    # endregion

    # region填充空值
    '''
    填充空值，提供五种方法填充，对于字符型数据只提供”“"重复值填充"这一方法，填充为选中的区域的第一个数据
    其他针对数值型的填充方式包括填充为0、填充为选中区域的平均值、线性插值填充、二次插值填充
    所有填充只能针对单字段操作
    '''
    def NanFill(self):
        self.nanfill = SubWindow.NanFillWindow()
        self.nanfill.NanFill_Signal.connect(self.myfill)
        self.nanfill.show()

    def myfill(self,method):
        try:
            self.right_tableview.itemChanged.disconnect(self.item_Changed_Event)# 断开连接，不然会很费时间
        except:
            pass

        if len(self.right_tableview.selectedIndexes())==0:
            self.right_tableview.selectAll()
        if self.right_tableview.selectedIndexes():
            top_left_col = self.right_tableview.selectedIndexes()[0].column()
            top_left_row = self.right_tableview.selectedIndexes()[0].row()
            bot_right_col = self.right_tableview.selectedIndexes()[-1].column()
            bot_right_row = self.right_tableview.selectedIndexes()[-1].row()
            df_selected = self.data_save.iloc[top_left_row:bot_right_row+1,top_left_col:bot_right_col+1]

            header = df_selected.columns.values.tolist()
            if len(header) > 1:
                QtWidgets.QMessageBox.critical(self, "错误“", "选中超过一个字段")
                return
            if method == "填充为零":
                # 利用转化好的dataframe 填充为0，再在表格中更新
                df_selected.fillna(0,inplace=True)
                #df_selected.replace('nan','0',inplace=True)
                for i in range(top_left_col,bot_right_col+1):
                    for j in range(top_left_row,bot_right_row+1):
                        Input_item = QtWidgets.QTableWidgetItem(str(df_selected.iloc[j-top_left_row,i-top_left_col]))
                        Input_item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                        self.right_tableview.setItem(j,i,Input_item)

            elif method == "填充为平均值":
                if df_selected[header[0]].dtypes == "object":
                    QtWidgets.QMessageBox.critical(self,"错误“","选中字段无法进行平均值计算", QtWidgets.QMessageBox.Yes
                                                           |QtWidgets.QMessageBox.Cancel)
                    return
                df_selected.fillna(round(df_selected.mean(),3),inplace=True)

                for i in range(top_left_row,bot_right_row+1):
                    Input_item = QtWidgets.QTableWidgetItem(str(df_selected.iloc[i-top_left_row,0]))
                    Input_item.setTextAlignment(Qt.AlignHCenter|Qt.AlignVCenter)
                    self.right_tableview.setItem(i,top_left_col,Input_item)
            elif method == "填充为复制值":
                if df_selected[header[0]].dtypes == "float64":
                    df_selected.fillna(self.right_tableview.selectedItems()[0].text(),inplace=True)
                elif df_selected[header[0]].dtypes == "object":
                    df_selected.replace('nan',self.right_tableview.selectedItems()[0].text(),inplace=True)
                for i in range(top_left_row, bot_right_row + 1):
                    Input_item = QtWidgets.QTableWidgetItem(str(df_selected.iloc[i - top_left_row, 0]))
                    Input_item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                    self.right_tableview.setItem(i, top_left_col, Input_item)
            elif method == "线性插值":
                if df_selected[header[0]].dtypes not in ["float64","int64"]:
                    QtWidgets.QMessageBox.critical(self, "错误“", "选中字段无法进行线性插值", QtWidgets.QMessageBox.Yes
                                                   | QtWidgets.QMessageBox.Cancel)
                    return
                df_selected.interpolate(method="linear",inplace=True)
                for i in range(top_left_row, bot_right_row+1):
                    Input_item = QtWidgets.QTableWidgetItem(str(round(df_selected.iloc[i-top_left_row, 0],3)))
                    Input_item.setTextAlignment(Qt.AlignHCenter| Qt.AlignVCenter)
                    self.right_tableview.setItem(i,top_left_col,Input_item)
            elif method == "二次插值":
                if df_selected[header[0]].dtypes not in ["float64","int64"]:
                    QtWidgets.QMessageBox.critical(self, "错误“", "选中字段无法进行二次插值", QtWidgets.QMessageBox.Yes
                                                   | QtWidgets.QMessageBox.Cancel)
                    return
                df_selected.interpolate(method="polynomial",order = 2,inplace=True)
                for i in range(top_left_row, bot_right_row+1):
                    Input_item = QtWidgets.QTableWidgetItem(str(round(df_selected.iloc[i-top_left_row, 0],3)))
                    Input_item.setTextAlignment(Qt.AlignHCenter| Qt.AlignVCenter)
                    self.right_tableview.setItem(i,top_left_col,Input_item)
            self.item_Changed_Event()
            try:
                self.right_tableview.itemChanged.connect(self.item_Changed_Event)
            except Exception:
                pass

    # endregion

    # region 数据查询
    '''
    数据查询，在全表上查询所输入的文本，包括精确查找和模糊查找
    '''
    def SearchData(self):
        self.SearchWindow = SubWindow.SearchWindow()
        self.SearchWindow.SearchSignal.connect(self.mysearch)
        self.SearchWindow.show()
    def mysearch(self,se_item,se_pattern):
        for i in self.right_tableview.selectedItems():
            i.setSelected(False)
        if se_pattern == "精确匹配":
            search_patten = Qt.MatchExactly
        elif se_pattern == "模糊匹配":
            search_patten = Qt.MatchContains
        search_items = self.right_tableview.findItems(se_item,search_patten)
        if search_items:
            row_1 = search_items[0].row()
            for item in search_items:
                item.setSelected(True)
            self.right_tableview.verticalScrollBar().setSliderPosition(row_1)
        self.SearchWindow.content_label.setText("共找到包含查找的元素" + str(len(search_items))+"个")





    # endregion

    # region 增加行列
    def AddRow(self):
        if self.right_tableview.selectedIndexes():
            row_index = self.right_tableview.selectedIndexes()[0].row()
            self.right_tableview.insertRow(row_index)

            self.data_save = self.TabletoDf()
            #以下的函数在运行时会弹出警告
            self.data_save = self.data_save.convert_objects(convert_numeric=True)

    def AddCol(self):
        if self.right_tableview.selectedIndexes():
            col_index = self.right_tableview.selectedIndexes()[0].column()
            self.right_tableview.insertColumn(col_index)
            self.data_save = self.TabletoDf()
            #以下的函数在运行时会弹出警告
            self.data_save = self.data_save.convert_objects(convert_numeric=True)

    def DelCol(self):
        if self.right_tableview.selectedIndexes():
            col_del_indexes = self.right_tableview.selectedIndexes()[0].column()
            self.right_tableview.removeColumn(col_del_indexes)
            self.data_save = self.TabletoDf()
            # 以下的函数在运行时会弹出警告
            self.data_save = self.data_save.convert_objects(convert_numeric=True)

    def DelRow(self):
        if self.right_tableview.selectedIndexes():
            row_del_indexes = self.right_tableview.selectedIndexes()[0].row()
            self.right_tableview.removeRow(row_del_indexes)
            self.data_save = self.TabletoDf()
            # 以下的函数在运行时会弹出警告
            self.data_save = self.data_save.convert_objects(convert_numeric=True)

    def NotSel(self):
        if not self.right_tableview.selectedItems():
            return
        for item in self.right_tableview.selectedItems():
            item.setSelected(False)
    # endregion

    # region 数据可视化
    '''
    对选中的数据进行数据可视化，提供饼状图，柱状图，散点图，折线图4种图形
    对于选取向量高于三维的情况，饼状图将只取第一列画图，散点图将选取前三列作为x,y,z画三维图形
    '''

    def Visualize(self,):

        self.VisualWindow = SubWindow.Visualization()
        self.VisualWindow.Visual_Siganl.connect(self.myVisual)
        self.VisualWindow.show()

    def myVisual(self,plot_type):
        if not self.right_tableview.selectedIndexes():
            return

        self.SelectedToDf()
        self.VisualWindow.plot_widget.clear()
        try:
            if plot_type == "     ":
                pass
            elif plot_type == "柱状图":
                ani_plot = self.VisualWindow.plot_widget.add_subplot(111, facecolor="#FFFFFF")
                self.selectedDf.T.plot(kind='bar',ax=ani_plot)
                self.VisualWindow.plot_canvas.draw()
            elif plot_type == "饼状图":
                ani_plot = self.VisualWindow.plot_widget.add_subplot(111, facecolor="#FFFFFF")
                self.selectedDf.T.iloc[:,0].plot(kind='pie',ax=ani_plot)
                self.VisualWindow.plot_canvas.draw()
            elif plot_type == "折线图":
                ani_plot = self.VisualWindow.plot_widget.add_subplot(111, facecolor="#FFFFFF")
                self.selectedDf.T.plot(kind="line",ax=ani_plot)
                self.VisualWindow.plot_canvas.draw()
            elif plot_type == "散点图":
                header_list = self.selectedDf.T.columns.values.tolist()
                if self.selectedDf.shape[0] ==1:
                    ani_plot = self.VisualWindow.plot_widget.add_subplot(111, facecolor="#FFFFFF")
                    ani_plot.scatter(self.selectedDf.T.index,self.selectedDf.T.iloc[:,0],color='r')
                    ani_plot.set_xlabel("index")
                    ani_plot.set_ylabel(header_list[-1])
                elif self.selectedDf.shape[0]==2:
                    ani_plot = self.VisualWindow.plot_widget.add_subplot(111, facecolor="#FFFFFF")
                    ani_plot.scatter(self.selectedDf.T.iloc[:,0],y = self.selectedDf.T.iloc[:,1],color="r")
                    ani_plot.set_xlabel(header_list[0])
                    ani_plot.set_ylabel(header_list[1])
                else:
                    ani_plot = Axes3D(self.VisualWindow.plot_widget)
                    ani_plot.scatter(self.selectedDf.T.iloc[:,0],self.selectedDf.T.iloc[:,1]
                                                       ,self.selectedDf.T.iloc[:,2],color='r')
                    ani_plot.set_xlabel(header_list[0])
                    ani_plot.set_ylabel(header_list[1])
                    ani_plot.set_zlabel(header_list[2])
                self.VisualWindow.plot_canvas.draw()

                #self.selectedDf.T.plot(x=self.selectedDf.T.iloc[:,0],y = self.selectedDf.T.iloc[:,1],
                 #                      kind="scatter",ax = self.VisualWindow.ani_plot)
                #self.VisualWindow.plot_canvas.draw()
        except Exception:
            pass

    #endregion

    # 将选中的元素转化为DataFrame,截取两端
    def SelectedToDf(self):
        self.selectedDf = None
        if self.right_tableview.selectedIndexes():
            top_row = self.right_tableview.selectedRanges()[0].topRow()
            bot_row = self.right_tableview.selectedRanges()[0].bottomRow()


            col_list = []
            col_list_2 = []

            for item_index in self.right_tableview.selectedIndexes():
                col_list.append(item_index.column())
            for i in col_list:
                if i not in col_list_2:
                    col_list_2.append(i)
            series_list = []
            print(self.data_save)
            print(col_list_2)
            for col_index in col_list_2:
                series_list.append(self.data_save.iloc[top_row:bot_row+1,col_index])
            self.selectedDf = pd.DataFrame(data=series_list)

            return self.selectedDf

    # region 无边框窗体的拖动
    def mouseMoveEvent(self, e: QMouseEvent):
        if self._isTracking == True:
            self._endPos = e.pos() - self._startPos
            self.move(self.pos() + self._endPos)

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

    # endregion

    # region 窗体关闭，最小化，最大化事件
    def closeEvent(self, event):
        reply = QtWidgets.QMessageBox.question(self, '退出', '是否退出系统？', QtWidgets.QMessageBox.Yes |
                                               QtWidgets.QMessageBox.Cancel)
        if reply ==  QtWidgets.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

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
    # endregion

    # region 二级菜单
    def showContextMenu(self):
        self.contextMenu_tableio.exec_(QCursor.pos())
    def showContextMenu_1(self):
        self.contextMenu_stat.exec_(QCursor.pos())
    def showContextMenu_2(self):
        self.contextMenu_dataop.exec_(QCursor.pos())
    def showContextMenu_3(self):
        self.contextMenu_model.exec_(QCursor.pos())

    def TableShowContextMenu(self):
        self.right_context_menu.exec_(QCursor.pos())
    # endregion

    # region 模型分析
    # k 均值聚类
    def Cluster(self):
        self.ClusterWindow = SubWindow.Cluster()
        self.ClusterWindow.ClusterSignal.connect(self.myCluster)
        self.ClusterWindow.show()

    def myCluster(self,str_clu, str_iter, str_thres):
        try:
            self.right_tableview.itemChanged.disconnect(self.item_Changed_Event)  # 断开连接，不然会很费时间
        except Exception:
            pass

        try:
            if str_clu != '':
                num_clu = int(str_clu)
            else:
                num_clu = 2
            if  str_iter!='':
                num_iter = int(str_iter)
            else:
                num_iter = 500
            if  str_thres!='':
                num_thres = float(str_thres)
            else:
                num_thres = 0.0001
        except Exception:
            QtWidgets.QMessageBox.critical(self,"错误","输入错误")
            return

        kmeans = K_means.Kmeans(num_clu,num_iter,num_thres)

        self.SelectedToDf()
        if  self.selectedDf is  None:
            return
        if not self.selectedDf.empty:
            if self.selectedDf.T.shape[1]< 2:
                QtWidgets.QMessageBox.critical(self,"错误","输入向量小于2维，无法聚类")
                return
            try:
                print(self.selectedDf)
                col = self.selectedDf.T.shape[1]
                data_X = self.selectedDf.T.iloc[:,:col].values
                predict_y = kmeans.predict(data_X)
                self.right_tableview.insertColumn(self.right_tableview.columnCount())
                for i in range(len(predict_y)):
                    Input_item = QtWidgets.QTableWidgetItem(str(predict_y[i]))
                    Input_item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                    self.right_tableview.setItem(i, self.right_tableview.columnCount()-1, Input_item)
                temp_x = pd.DataFrame(data=data_X)
                temp_y = pd.Series(data=predict_y)
                temp_x["Predict"] = temp_y

                if self.selectedDf.T.shape[1] == 2:
                    ax = self.ClusterWindow.plot_widget.add_subplot(111)
                    for i in range(num_clu):
                        ax.scatter(x= temp_x[temp_x.Predict==i].iloc[:,0],y=temp_x[temp_x.Predict==i].iloc[:,1])

                elif self.selectedDf.T.shape[1]>=3:
                    ax = Axes3D(self.ClusterWindow.plot_widget)
                    for i in range(num_clu):
                        ax.scatter( temp_x[temp_x.Predict==i].iloc[:,0],temp_x[temp_x.Predict==i].iloc[:,1],
                                     temp_x[temp_x.Predict==i].iloc[:,2])
            except Exception:
                QtWidgets.QMessageBox.critical(self, "错误", "聚类失败，请检查输入数据的合法性")
                return
            try:
                self.item_Changed_Event()
                self.right_tableview.itemChanged.connect(self.item_Changed_Event)  # 断开连接，不然会很费时间
            except Exception:
                pass
            self.ClusterWindow.plot_canvas.draw()

    # 支持向量机
    def SVM(self):
        QtWidgets.QMessageBox.information(self, "你好", "未完待续")

    # 随机森林
    def RandomForest(self):
        QtWidgets.QMessageBox.information(self, "你好", "未完待续")

    # 神经网络
    def Neural(self):
        QtWidgets.QMessageBox.information(self, "你好", "未完待续")

    # 多元回归
    def Regression(self):
        self.RegressionWindow = SubWindow.Regression()
        self.RegressionWindow.RegressionSignal.connect(self.myRegression)
        self.RegressionWindow.show()

    def myRegression(self,str_rate,str_iter):
        try:
            self.right_tableview.itemChanged.disconnect(self.item_Changed_Event)  # 断开连接，不然会很费时间
        except Exception:
            pass

        try:
            if str_rate != '':
                num_rate = float(str_rate)
            else:
                num_rate = 0.001
            if  str_iter!='':
                num_iter = int(str_iter)
            else:
                num_iter = 5000
        except Exception:
            QtWidgets.QMessageBox.critical(self,"错误","输入错误")
            return

        self.SelectedToDf()
        if  self.selectedDf is  None:
            return
        if not self.selectedDf.empty:
            if self.selectedDf.T.shape[1]< 2:
                QtWidgets.QMessageBox.critical(self,"错误","输入向量小于2维，无法进行线性回归")
                return
            try:
                col = self.selectedDf.T.shape[1]
                data_X = self.selectedDf.T.iloc[:,:col-1].values
                temp_data_Y = self.selectedDf.T.iloc[:,col-1].T.values
                data_Y = temp_data_Y.reshape(len(temp_data_Y),1)
                lr = linear_Regression.linear_Regression(data_X,data_Y, learningRate= num_rate, Loopnum=num_iter)
                res = lr.linear_Regression()
                self.RegressionWindow.result_label.setText("w=" + str(res[0])+'\n' + "b=" + str(res[1]))
                if self.selectedDf.T.shape[1] == 2:
                    temp_X = data_X.reshape(1,len(data_X))
                    min_X = min(temp_X[0])
                    max_X = max(temp_X[0])
                    ax = self.RegressionWindow.plot_widget.add_subplot(111)
                    ax.scatter(x=data_X,y = data_Y)
                    x= np.linspace(min_X,max_X,50)
                    ax.plot(x, res[0][0]*x+res[1][0],'r-')

                if self.selectedDf.T.shape[1] == 3:
                    ax = Axes3D(self.RegressionWindow.plot_widget)
                    X_3D = data_X.reshape(2, len(data_X))
                    ax.scatter(X_3D[0],X_3D[1],data_Y)
                    x1 = np.linspace(min(X_3D[0]), max(X_3D[0]), 50)
                    x2 = np.linspace(min(X_3D[1]), max(X_3D[1]),50)
                    x1, x2 = np.meshgrid(x1,x2)

                    ax.plot_surface(x1,x2,res[0][0][0]*x1+res[0][0][1]*x2+res[1][0],color ='r')
            except Exception:
                QtWidgets.QMessageBox.critical(self, "错误", "运行出错，请检查输入数据的合法性")


        self.RegressionWindow.plot_canvas.draw()

    # STL 序列分解
    def Trend_Decompose(self):
        QtWidgets.QMessageBox.information(self, "你好", "未完待续")

    # endregion



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    gui = MainWindow()
    gui.show()
    sys.exit(app.exec_())