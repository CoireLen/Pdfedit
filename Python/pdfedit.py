import sys
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from typing import Optional
from PyQt5.sip import delete
import fitz
from fitz.fitz import linkDest
import numpy as np
import cv2
from numpy.lib.function_base import append, select
from numpy.lib.npyio import load

main = {}
class singlesilder(QWidget):#单控制条的窗口
    def __init__(self,num,slider1start,slider1end,windowtitle):
        super(doublesilder, self).__init__()
        self.num=num
        self.slider1=QSlider()
        self.slider1.setRange(slider1start,slider1end);
        self.setWindowTitle(windowtitle);
        self.layout = QGridLayout()
        self.setLayout(self.layout)
        self.slider1.valueChanged.connect(self.slider1change)
        self.slider1.setOrientation(Qt.Horizontal)
        self.label1datanum=0
        self.label1data=""
        self.resize(300,60);

    def slider1change(self):
        main["ImgTodoListWindow"].SetCommand(self.num,True,"%s:%d,%d"%(self.windowTitle(),self.slider1.value(),self.slider2.value()))
        main["OptimizeWindow"].MakeImg()
        if self.label1datanum >1 :
            if len(self.label1data)>self.slider1.value():
                self.label1.setText(self.label1data[self.slider1.value()])
            else:
                self.label1.setText(self.label1data[0])

    def SetShowLabel(self,num,data):
        self.label1=QLabel()
        self.label1datanum=num
        self.label1data=data
        if num>0:
            self.layout.addWidget(self.label1)
        self.layout.addWidget(self.slider1)



class doublesilder(QWidget):#双控制条的窗口
    def __init__(self,num,slider1start,slider1end,slider2start,slider2end,windowtitle):
        super(doublesilder, self).__init__()
        self.num=num
        self.slider1=QSlider()
        self.slider2=QSlider()
        self.slider1.setRange(slider1start,slider1end);
        self.slider2.setRange(slider2start,slider2end);
        self.setWindowTitle(windowtitle);
        layout = QGridLayout()
        self.setLayout(layout)
        layout.addWidget(self.slider1)
        layout.addWidget(self.slider2)
        self.slider1.valueChanged.connect(self.slider1change)
        self.slider2.valueChanged.connect(self.slider2change)
        self.slider1.setOrientation(Qt.Horizontal)
        self.slider2.setOrientation(Qt.Horizontal)
        self.resize(300,60);

    def slider1change(self):
        main["ImgTodoListWindow"].SetCommand(self.num,True,"%s:%d,%d"%(self.windowTitle(),self.slider1.value(),self.slider2.value()))
        main["OptimizeWindow"].MakeImg()
    def slider2change(self):
        main["ImgTodoListWindow"].SetCommand(self.num,True,"%s:%d,%d"%(self.windowTitle(),self.slider1.value(),self.slider2.value()))
        main["OptimizeWindow"].MakeImg()
    
class threesilder(QWidget):#三控制条的窗口
    def __init__(self,num,slider1start,slider1end,slider2start,slider2end,slider3start,slider3end,windowtitle):
        super(threesilder, self).__init__()
        self.num=num
        self.slider1=QSlider()
        self.slider2=QSlider()
        self.slider3=QSlider()
        self.slider1.setRange(slider1start,slider1end);
        self.slider2.setRange(slider2start,slider2end);
        self.slider3.setRange(slider3start,slider3end);
        self.setWindowTitle(windowtitle);
        self.layout = QGridLayout()
        self.setLayout(self.layout)
        self.slider1.valueChanged.connect(self.slider1change)
        self.slider2.valueChanged.connect(self.slider2change)
        self.slider3.valueChanged.connect(self.slider3change)
        self.slider1.setOrientation(Qt.Horizontal)
        self.slider2.setOrientation(Qt.Horizontal)
        self.slider3.setOrientation(Qt.Horizontal)
        self.label1datanum=0
        self.label1data=[""]
        self.label2datanum=0
        self.label2data=[""]
        self.label3datanum=0
        self.label3data=[""]
        self.resize(300,90);

    def slider1change(self):
        main["ImgTodoListWindow"].SetCommand(self.num,True,"%s:%d,%d,%d"%(self.windowTitle(),self.slider1.value(),self.slider2.value(),self.slider3.value()))
        main["OptimizeWindow"].MakeImg()
        if self.label1datanum >1 :
            if len(self.label1data)>self.slider1.value():
                self.label1.setText(self.label1data[self.slider1.value()])
            else:
                self.label1.setText(self.label1data[0])
    def slider2change(self):
        main["ImgTodoListWindow"].SetCommand(self.num,True,"%s:%d,%d,%d"%(self.windowTitle(),self.slider1.value(),self.slider2.value(),self.slider3.value()))
        main["OptimizeWindow"].MakeImg()
        if self.label2datanum >1:
            if len(self.label2data)>self.slider2.value():
                self.label2.setText(self.label2data[self.slider2.value()])
            else:
                self.label2.setText(self.label2data[0])
    def slider3change(self):
        main["ImgTodoListWindow"].SetCommand(self.num,True,"%s:%d,%d,%d"%(self.windowTitle(),self.slider1.value(),self.slider2.value(),self.slider3.value()))
        main["OptimizeWindow"].MakeImg()
        if self.label3datanum >1:
            if len(self.label3data)>self.slider3.value():
                self.label3.setText(self.label3data[self.slider3.value()])
            else:
                self.label3.setText(self.label3data[0])
    def SetShowLabel(self,num1,data1,num2,data2,num3,data3):
        self.label1=QLabel()
        self.label1datanum=num1
        self.label1data=data1
        self.label2datanum=num2
        self.label2data=data2
        self.label3datanum=num3
        self.label3data=data3
        if num1>0:
            self.layout.addWidget(self.label1)
        self.layout.addWidget(self.slider1)
        if num2>0:
            self.layout.addWidget(self.label2)
        self.layout.addWidget(self.slider2)
        if num3>0:
            self.layout.addWidget(self.label3)
        self.layout.addWidget(self.slider3)


class TodoImgListWidget(QListWidget):
    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        # 拖拽设置
        self.setAcceptDrops(True)
        self.setDragEnabled(True)
        self.setDragDropMode(QAbstractItemView.InternalMove)            # 设置拖放
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)  # 设置选择多个
        self.setDefaultDropAction(Qt.MoveAction)
        self.setViewMode(self.ListMode)
class haveguiListWidgetIte(QListWidgetItem):
    def __init__(self,gui):
        super().__init__()
        self.gui=gui
    def showgui(self):
        self.gui.show()
class ImgTodoListWindow(QWidget):#图片处理序列命令窗口
    def __init__(self):
        super(ImgTodoListWindow, self).__init__()
        self.setWindowTitle("命令序列")
        mainlayout = QHBoxLayout()
        leftlayout =QGridLayout()
        rightlayour=QGridLayout()
        self.setLayout(mainlayout)
        mainlayout.addLayout(leftlayout)
        mainlayout.addLayout(rightlayour)
        #左边一个ListWeight
        self.commandlist=TodoImgListWidget()
        self.commandlist.doubleClicked.connect(self.commandlistdoubleClicked)
        self.commandlist.itemChanged.connect(self.commandlistitemchange)
        leftlayout.addWidget(self.commandlist)
        #右边一堆Button
        button3=QPushButton()
        rightlayour.addWidget(button3)
        button3.setText("方框滤波")
        button3.clicked.connect(self.button3clicked)

        button1=QPushButton()
        rightlayour.addWidget(button1)
        button1.setText("均值滤波")
        button1.clicked.connect(self.button1clicked)

        button2=QPushButton()
        rightlayour.addWidget(button2)
        button2.setText("高斯滤波")
        button2.clicked.connect(self.button2clicked)

        button4=QPushButton()
        rightlayour.addWidget(button4)
        button4.setText("中值滤波")
        button4.clicked.connect(self.button4clicked)

        button5=QPushButton()
        rightlayour.addWidget(button5)
        button5.setText("双边滤波")
        button5.clicked.connect(self.button5clicked)

        button6=QPushButton()
        rightlayour.addWidget(button6)
        button6.setText("显示图片")
        button6.clicked.connect(self.button6clicked)

        buttondel=QPushButton()
        rightlayour.addWidget(buttondel)
        buttondel.setText("删除选中")
        buttondel.clicked.connect(self.buttondelclicked)

        self.windict={}
        main["ImgTodoListWindow"]=self
        
    def button1clicked(self):
        num=self.commandlist.count()
        x=doublesilder(num,1,100,1,100,"均值滤波")
        x.show()
        self.AddCommand(True,"均值滤波:5,5",x)

    def button2clicked(self):
        num=self.commandlist.count()
        x=threesilder(num,1,100,1,100,0,200,"高斯滤波")
        x.SetShowLabel(0,[""],0,[""],0,[""])
        x.show()
        self.AddCommand(True,"高斯滤波:5,5,0",x)
    def button3clicked(self):
        num=self.commandlist.count()
        x=doublesilder(num,1,100,1,100,"方框滤波")
        x.show()
        self.AddCommand(True,"方框滤波:5,5",x)
    def button4clicked(self):
        num=self.commandlist.count()
        x=doublesilder(num,1,100,1,100,"中值滤波")
        x.show()
        self.AddCommand(True,"中值滤波:5,5",x)
    def button5clicked(self):
        num=self.commandlist.count()
        x=threesilder(num,0,255,0,255,0,255,"双边滤波")
        x.SetShowLabel(0,[""],0,[""],0,[""])
        x.show()
        self.AddCommand(True,"双边滤波:0,0,0",x)

    def button6clicked(self):
        self.AddCommand(True,"显示图片",None)
    def buttondelclicked(self):
        secd=self.commandlist.selectedItems()
        list1=[]
        for i in secd:
            list1.append(self.commandlist.row(i))
        for i in list1[::-1]:
            self.commandlist.takeItem(i)
        None
    def commandlistdoubleClicked(self):
        if (self.commandlist.currentItem()):
            self.commandlist.item(self.commandlist.currentRow()).showgui()
    def commandlistitemchange(self):
        main["OptimizeWindow"].MakeImg(self.num)
    def AddCommand(self,use,command,gui,fromtext1=0,totext1=0):
        if fromtext1==0 and totext1==0:
            fromtext1=self.commandlist.count()
            totext1=fromtext1+1
        qwidget1=QWidget()
        cllayout=QHBoxLayout()
        usecommand=QRadioButton()
        usecommand.setChecked(use)
        commandlabel=QLabel()
        commandlabel.setText(command)
        fromtext=QLineEdit()
        fromtext.setText(str(fromtext1))
        fromtext.setObjectName("from")
        totext=QLineEdit()
        totext.setText(str(totext1))
        main["OptimizeWindow"].defLoadimg=str(totext1)
        totext.setObjectName("to")
        cllayout.addWidget(usecommand)
        cllayout.addWidget(commandlabel)
        cllayout.addWidget(fromtext)
        cllayout.addWidget(totext)
        qwidget1.setLayout(cllayout)
        qlistwidgetitem1=haveguiListWidgetIte(gui)
        qlistwidgetitem1.setSizeHint(QSize(0,50));
        self.commandlist.addItem(qlistwidgetitem1)
        self.commandlist.setItemWidget(qlistwidgetitem1,qwidget1)
        main["OptimizeWindow"].MakeImg()
    def GetCommand(self,num):
        i=self.commandlist.itemWidget(self.commandlist.item(num))
        use=i.findChild(QRadioButton)
        command=i.findChild(QLabel)
        fromtext=i.findChild(QLineEdit,"from")
        totext=i.findChild(QLineEdit,"to")
        return [use.isChecked(),command.text(),fromtext.text(),totext.text()]
    def GetCommandListItem(self,qlistitem:QListWidgetItem):
        i=self.commandlist.itemWidget(qlistitem)
        use=i.findChild(QRadioButton)
        command=i.findChild(QLabel)
        fromtext=i.findChild(QLineEdit,"from")
        totext=i.findChild(QLineEdit,"to")
        return [use.isChecked(),command.text(),fromtext.text(),totext.text()]
    def SetCommand(self,num,checked,command,fromtext="0",totext="0"):
        i=self.commandlist.itemWidget(self.commandlist.item(num))
        usecommand=i.findChild(QRadioButton)
        usecommand.setChecked(checked)
        commandlabel=i.findChild(QLabel)
        commandlabel.setText(command)
        if fromtext!="0" and totext!="0":
            fromlinetext=i.findChild(QLineEdit,"from")
            fromlinetext.setText(fromtext)
            tolinetext=i.findChild(QLineEdit,"to")
            tolinetext.setText(totext)
    def SetCommandListItem(self,qlistitem:QListWidgetItem,checked,command,fromtext="0",totext="0"):
        i=self.commandlist.itemWidget(qlistitem)
        usecommand=i.findChild(QRadioButton)
        usecommand.setChecked(checked)
        commandlabel=i.findChild(QLabel)
        commandlabel.setText(command)
        if fromtext!="0" and totext!="0":
            fromlinetext=i.findChild(QLineEdit,"from")
            fromlinetext.setText(fromtext)
            tolinetext=i.findChild(QLineEdit,"to")
            tolinetext.setText(totext)
class OptimizeWindow(QWidget):#优化工具窗口
    def __init__(self):
        super(OptimizeWindow, self).__init__()
        layout = QGridLayout()
        toolBar = QToolBar()
        layout.addWidget(toolBar);
        toolBar.actionTriggered[QAction].connect(self.OnClickToolbarButton)

        toolButton1 = QAction(text="处理列表", parent=self)
        toolBar.addAction(toolButton1)
        #处理列表 得有开关选项 双击进入gui修改模式，修改后自动向下计算 多个gui可以同时控制图片
        self.imgcachelist={}#图片处理中间文件
        toolButton2 = QAction(text="载入预设", parent=self)
        toolBar.addAction(toolButton2)
        #预设从文件中读取查询文件夹举出所有文件
        toolButton3 = QAction(text="保存预设", parent=self)
        toolBar.addAction(toolButton3)
        #将现有处理列表参数转换成预设文件
        toolButton4 = QAction(text="应用到文件", parent=self)
        toolBar.addAction(toolButton4)
        self.setLayout(layout)
        self.slider1 = QSlider()
        self.slider1.setRange(0,0)
        self.slider1.setValue(0)
        self.slider1.setOrientation(Qt.Horizontal)
        self.slider1.valueChanged.connect(self.doChangePage)
        layout.addWidget(self.slider1)
        self.defLoadimg="0"
        self.picview = QGraphicsView()
        layout.addWidget(self.picview)
        self.setWindowTitle("优化工具")
        self.imgtodolistwindow=ImgTodoListWindow()
        self.resize(800,600)
        main["OptimizeWindow"]=self
        
        
    def OnClickToolbarButton(self,o):
        if o.text()=="处理列表":
            
            self.imgtodolistwindow.show()
    def LoadFromSelect(self):
        select=main["self"].listWidget.selectedItems()
        self.pagenumlist=[]
        for i in select:
            self.pagenumlist.append(main["self"].listWidget.row(i))
        self.slider1.setRange(0,len(self.pagenumlist)-1)
        self.LoadImg(self.pagenumlist[0])
    def DoBlur(self,vaule,from1,to1):
        self.imgcachelist[to1]=cv2.blur(self.imgcachelist[from1],(int(vaule[0]),int(vaule[1])))
        
    def DoGaussianBlur(self,vaule,from1,to1):
        (x,y)=(int(vaule[0]),int(vaule[1]))
        if x%2==0:
            x+=1
        if y%2==0:
            y+=1
        self.imgcachelist[to1]=cv2.GaussianBlur(self.imgcachelist[from1],(x,y),float(vaule[2])/10)
    def DoboxFilter(self,vaule,from1,to1):
        (x,y)=(int(vaule[0]),int(vaule[1]))
        self.imgcachelist[to1]=cv2.boxFilter(self.imgcachelist[from1],cv2.CV_8U,(x,y))
    def DoMedianBlur(self,vaule,from1,to1):
        (x,y)=(int(vaule[0]),int(vaule[1]))
        if x%2==0:
            x+=1
        if y%2==0:
            y+=1
        self.imgcachelist[to1]=cv2.medianBlur(self.imgcachelist[from1],(x,y))
    def DoBilateralFilter(self,vaule,from1,to1):
        (x,y,z)=(int(vaule[0]),int(vaule[1]),int(vaule[2]))
        self.imgcachelist[to1]=cv2.bilateralFilter(self.imgcachelist[from1],x,y,z)
    def DoShowImg(self,from1,to1):
        self.imgcachelist[to1]=self.imgcachelist[from1]
        self.defLoadimg=to1
    def DoDilate(self,vaule,from1,to1):
        (x,y)=(int(vaule[0]),int(vaule[1]))
        if x%2==0:
            x+=1
        if y%2==0:
            y+=1
        self.imgcachelist[to1]=cv2.dilate(self.imgcachelist[from1],(x,y))
    def DoErode(self,vaule,from1,to1):
        (x,y)=(int(vaule[0]),int(vaule[1]))
        if x%2==0:
            x+=1
        if y%2==0:
            y+=1
        self.imgcachelist[to1]=cv2.erode(self.imgcachelist[from1],(x,y))
    def DoFloodFill(self,vaule,from1,to1):
        (x,y)=(int(vaule[0]),int(vaule[1]))
        if x%2==0:
            x+=1
        if y%2==0:
            y+=1
        self.imgcachelist[to1]=cv2.floodFill(self.imgcachelist[from1],(x,y))
    def linkstart(self,command,num):
        #command约定
        cmd=command[1].split(":")
        if cmd[0]=="均值滤波":
            vaule=cmd[1].split(',')
            self.DoBlur(vaule,command[2],command[3])
        elif cmd[0]=="高斯滤波":
            vaule=cmd[1].split(',')
            self.DoGaussianBlur(vaule,command[2],command[3])
        elif cmd[0]=="方框滤波":
            vaule=cmd[1].split(',')
            self.DoboxFilter(vaule,command[2],command[3])
        elif cmd[0]=="中值滤波":
            vaule=cmd[1].split(',')
            self.DoMedianBlur(vaule,command[2],command[3])
        elif cmd[0]=="双边滤波":
            vaule=cmd[1].split(',')
            self.DoBilateralFilter(vaule,command[2],command[3])
        elif cmd[0]=="膨胀":
            vaule=cmd[1].split(',')
            self.DoDilate(vaule,command[2],command[3])
        elif cmd[0]=="腐蚀":
            vaule=cmd[1].split(',')
            self.DoErode(vaule,command[2],command[3])
        elif cmd[0]=="显示图片":
            self.DoShowImg(command[2],command[3])
        None
    def todoCommand(self):
        #获取序列数据
        commandlist=[]
        for i in range(main["ImgTodoListWindow"].commandlist.count()):
            commandlist.append(main["ImgTodoListWindow"].GetCommand(i))
        #匹配执行命令
        for i in range(0,len(commandlist)):
            if commandlist[i][0]==True:
                self.linkstart(commandlist[i],i)
    def LoadImg(self,num):
        img=QPixmap()
        imgdata=main["self"].GetPageToData(num)
        self.imgcachelist[self.defLoadimg]=imgdata
        #执行函数序列
        self.todoCommand()

        img.loadFromData(np.array(cv2.imencode('.jpg',self.imgcachelist[self.defLoadimg])[1]).tobytes())
        secen=QGraphicsScene()
        secen.addPixmap(img)
        self.picview.setScene(secen)
    def MakeImg(self):
        self.todoCommand()
        img=QPixmap()
        img.loadFromData(np.array(cv2.imencode('.jpg',self.imgcachelist[self.defLoadimg])[1]).tobytes())
        secen=QGraphicsScene()
        secen.addPixmap(img)
        self.picview.setScene(secen)
    def doChangePage(self):
        self.LoadImg(self.pagenumlist[self.slider1.value()])

class MergeListWidget(QListWidget):
    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        # 拖拽设置
        self.setAcceptDrops(True)
        self.setDragEnabled(True)
        self.setDragDropMode(QAbstractItemView.InternalMove)            # 设置拖放
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)  # 设置选择多个
        self.setDefaultDropAction(Qt.MoveAction)
        self.setViewMode(self.ListMode)
        
    def dragEnterEvent(self, e: QDragEnterEvent) -> None:
            if e.mimeData().hasText():
                if e.mimeData().text().startswith('file:///'):
                    filePathList = e.mimeData().text()
                    filePathS = filePathList.split('\n')
                    for filePath in filePathS:
                        if filePath.startswith('file:///'):
                            filePath = filePath.replace(
                                'file:///', '', 1)  # 去除文件地址前缀的特定字符
                            print(filePath)
                            if filePath[-4:] in (".pdf",".jpg",".png"):
                                self.addItem(QListWidgetItem(filePath))
            else:
                e.accept()
class MergeListWindow(QWidget):#合并工具 列表窗口
    def __init__(self):
        super(MergeListWindow, self).__init__()
        layout = QGridLayout()
        self.setLayout(layout)
        toolBar = QToolBar()
        layout.addWidget(toolBar)
        # Add buttons to toolbar
        toolButton1 = QAction(text="删除", parent=self)
        toolBar.addAction(toolButton1)

        toolButton2 = QAction(text="保存", parent=self)
        toolBar.addAction(toolButton2)

        toolBar.actionTriggered[QAction].connect(self.OnClickToolbarButton)
        self.list1=MergeListWidget()
        layout.addWidget(self.list1)
        self.setWindowTitle("合并工具")
        self.resize(800,600)
    def OnClickToolbarButton(self,o):
        if o.text() == "删除":
            self.OnDelLine()
        if o.text() == "保存":
            self.OnSave()
    def OnDelLine(self):
        select=self.list1.selectedItems()
        list=[]
        for i in select:
            list.append(self.list1.row(i))
        list.sort()
        for i in list[::-1]:
            item=self.list1.takeItem(i)
            del item
    def OnSave(self):
        table=[]
        for i in range(self.list1.count()):
            table.append(self.list1.item(i).text())
        if len(table)==0:
            return
        savepath=QFileDialog(self, "选择PDF文件", "",
                                   "PDF 文件(*.pdf)").getSaveFileName()
        if savepath[1] ==True:
            return
        if savepath[0][-4:]!=".pdf":
            savepath=savepath[0]+'.pdf'
        else:
            savepath=savepath[0]
        doc=fitz.open()
        procbar=ProgressWindow()
        procbar.SetRange(0,len(table)+1)
        RateOfProgress=0
        procbar.SetVaule(RateOfProgress)
        for insterfile in table:
            if insterfile[-4:] in {".png", ".jpg"}:
                img = fitz.open(insterfile)
                rect = img[0].rect
                pdfbyte = img.convert_to_pdf()
                img.close()
                doc2 = fitz.open("pdf", pdfbyte)
            else:
                doc2 = fitz.open(insterfile)
            RateOfProgress+=1
            procbar.SetVaule(RateOfProgress)
            doc.insert_pdf(doc2)
        doc.save(savepath)
        RateOfProgress+=1
        procbar.SetVaule(RateOfProgress)
        doc.close()
        self.close()

class ProgressWindow(QWidget): #进度条
    def __init__(self):
        super(ProgressWindow, self).__init__()
        layout = QGridLayout()
        self.setWindowTitle("进度")
        self.progress1=QProgressBar(self)
        self.progress1.resize(500,30)
        self.resize(500,30)
        layout.addWidget(self.progress1)
        self.show()
    def SetRange(self,startvalue,endvalue):
        self.progress1.setMinimum(startvalue)
        self.progress1.setMaximum(endvalue)
    def SetVaule(self,value):
        self.progress1.setValue(value)
        QApplication.processEvents()
class OutputOption(QWidget): #导出压缩使用的设置窗口
    def __init__(self):
        super(OutputOption, self).__init__()
        layout = QGridLayout()
        self.setLayout(layout)
        self.mode="未初始化"
        self.setWindowTitle(self.mode)
        self.resize(300,200)

        self.defZoom=13
        self.label1=QLabel()
        self.label1.setText("页面缩放倍率:"+str(self.defZoom/10))
        layout.addWidget(self.label1,0,0,1,2)

        self.slider1 = QSlider()
        self.slider1.setMaximum(50)
        self.slider1.setMinimum(1)
        self.slider1.setValue(self.defZoom)
        self.slider1.valueChanged.connect(self.slider1changed)
        self.slider1.setOrientation(Qt.Horizontal)
        layout.addWidget(self.slider1,1,0,1,2)

        self.defMase=80

        self.label2=QLabel()
        self.label2.setText("页面图像质量:"+str(self.defMase))
        layout.addWidget(self.label2,2,0,1,2)

        
        self.slider2 = QSlider()
        self.slider2.setMaximum(100)
        self.slider2.setMinimum(10)
        self.slider2.setValue(self.defMase)
        self.slider2.valueChanged.connect(self.slider2changed)
        self.slider2.setOrientation(Qt.Horizontal)
        layout.addWidget(self.slider2,3,0,1,2)

        self.label3=QLabel()
        self.palette=QPalette()
        self.label3.setAutoFillBackground(True);
        self.savepath=""
        self.label3.setText(self.savepath)
        button3=QPushButton()
        button3.setText("存储路径")
        button3.clicked.connect(self.selectFilepath)
        layout.addWidget(self.label3,4,0,1,1)
        layout.addWidget(button3,4,1,1,1)

        button1=QPushButton()
        button1.setText("取消")
        button1.clicked.connect(self.buttonCancel)
        layout.addWidget(button1,5,0,1,1)

        button2=QPushButton()
        button2.setText("确定")
        button2.clicked.connect(self.buttonAccept)
        layout.addWidget(button2,5,1,1,1)

        self.show()
    def slider1changed(self):
        self.label1.setText("页面缩放倍率:"+str(self.slider1.value()/10))
    def slider2changed(self):
        self.label2.setText("页面图像质量:"+str(self.slider2.value()))
    def buttonAccept(self):
        zoom=self.slider1.value()/10
        mase=self.slider2.value()
        savefile=self.savepath
        if savefile=="":
            self.palette.setColor(QPalette.Background, QColor(255, 100,100));
            self.label3.setPalette(self.palette);
            return
        if self.mode=="导出":
            main["self"].OnOutPut(zoom,mase,savefile)
        elif self.mode=="压缩":
            main["self"].OnOutZip(zoom,mase,savefile)
            None
        self.close()
    def buttonCancel(self):
        print(self.mode+"取消")
        self.close()
    def dateUpdate(self,zoom,mase,mode):
        self.mode=mode
        self.setWindowTitle(mode+"设置")
        self.slider1.setValue(zoom)
        self.slider2.setValue(mase)
        self.slider1changed()
        self.slider2changed()
    def selectFilepath(self):
        if self.mode=="压缩":
            filesavepath=QFileDialog(self, "选择PDF保存位置", "提示",
                                    "PDF 文件(*.pdf)").getSaveFileName()
            if filesavepath[1]!=True:
                self.savepath=filesavepath[0]
                if self.savepath[-4:] != ".pdf":
                    self.savepath+='.pdf'
            else:
                print("选择文件:取消操作")
        elif self.mode=="导出":
            self.savepath=QFileDialog.getExistingDirectory()
        self.label3.setText(self.savepath)
        if self.savepath!="":
            self.palette.setColor(QPalette.Background, QColor(100, 255, 100));
            self.label3.setPalette(self.palette);
class ListWidget(QListWidget):
    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        # 拖拽设置
        self.SetMode()
        self.setIconSize(
            QSize(int(400*main["self"].zoomsize), int(500*main["self"].zoomsize)))
        self.ctrlPressed = False

    def SetMode(self, mode=QListWidget.IconMode):
        self.setViewMode(mode)
        self.setAcceptDrops(True)
        self.setDragEnabled(True)
        self.setDragDropMode(QAbstractItemView.InternalMove)            # 设置拖放
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)  # 设置选择多个
        self.setDefaultDropAction(Qt.MoveAction)
        self.setFlow(QListView.LeftToRight)

    def click(self, item):
        # QMessageBox.information(self,'ListWidget','你选择了：'+item.text())
        print(item)

    def dragEnterEvent(self, e: QDragEnterEvent) -> None:
        """（从外部或内部控件）拖拽进入后触发的事件"""
        # print(e.mimeData().text())
        if e.mimeData().hasText():
            if e.mimeData().text().startswith('file:///'):
                filePathList = e.mimeData().text()
                filePathS = filePathList.split('\n')
                for filePath in filePathS:
                    if filePath.startswith('file:///'):
                        filePath = filePath.replace(
                            'file:///', '', 1)  # 去除文件地址前缀的特定字符
                        print(filePath)
                        if filePath[-4:] == ".pdf":
                            if main["self"] != None:
                                if main["self"].doc == None:
                                    main["self"].doc = fitz.open(filePath)
                                    main["self"].OnLoadPages()
                                else:
                                    main["self"].insterfile = filePath
                                    main["self"].DoInster()
                        elif filePath[-4:] in {".png", ".jpg"}:
                            if main["self"].doc == None:
                                main["self"].doc = fitz.open()
                            main["self"].insterfile = filePath
                            main["self"].DoInster()

        else:
            e.accept()

    def keyReleaseEvent(self, QKeyEvent):
        if QKeyEvent.key() == QtCore.Qt.Key_Control:
            self.ctrlPressed = False
        return super().keyReleaseEvent(QKeyEvent)

    def keyPressEvent(self, QKeyEvent):
        if QKeyEvent.key() == QtCore.Qt.Key_Control:
            self.ctrlPressed = True
            print("The ctrl key is holding down")
        return super().keyPressEvent(QKeyEvent)

    # 响应鼠标事件
    def wheelEvent(self, event):  # this is the rewrite of the function
        if self.ctrlPressed:  # if the ctrl key is pressed: then deal with the defined process
            delta = event.angleDelta()
            oriention = delta.y()/8
            if oriention > 0:
                main["self"].zoomsize = main["self"].zoomsize+0.1
            else:
                main["self"].zoomsize = main["self"].zoomsize-0.1
            self.setIconSize(
                QSize(int(400*main["self"].zoomsize), int(500*main["self"].zoomsize)))
            # self.zoomIn(self.zoomsize)
        else:  # if the ctrl key isn't pressed then submiting                   the event to it's super class
            return super().wheelEvent(event)


class Window(QWidget):

    def __init__(self):
        QWidget.__init__(self)
        layout = QGridLayout()
        self.setLayout(layout)
        self.resize(800, 600)
        self.ctrlPressed = False
        self.zoomsize = 1.5
        self.lwitem = {}
        self.doc = None
        main["self"] = self
        # Create pyqt toolbar
        toolBar = QToolBar()
        layout.addWidget(toolBar)
        # Add buttons to toolbar
        toolButton1 = QAction(text="打开", parent=self)
        toolBar.addAction(toolButton1)
        toolButton2 = QAction(text="保存", parent=self)
        toolBar.addAction(toolButton2)
        toolButton3 = QAction(text="另存", parent=self)
        toolBar.addAction(toolButton3)
        toolButton4 = QAction(text="删除", parent=self)
        toolBar.addAction(toolButton4)
        toolButton5 = QAction(text="旋转", parent=self)
        toolBar.addAction(toolButton5)
        toolButton6 = QAction(text="插入", parent=self)
        toolBar.addAction(toolButton6)
        toolButton7 = QAction(text="排序", parent=self)
        toolBar.addAction(toolButton7)
        toolButton9 = QAction(text="阅读", parent=self)
        toolBar.addAction(toolButton9)
        toolButton8 = QAction(text="关闭", parent=self)
        toolBar.addAction(toolButton8)
        toolButton9 = QAction(text="导出", parent=self)
        toolBar.addAction(toolButton9)
        toolButton10 = QAction(text="压缩", parent=self)
        toolBar.addAction(toolButton10)
        toolButton11 = QAction(text="合并", parent=self) #合并功能 不显示页面加快速度
        toolBar.addAction(toolButton11)
        toolButton12 = QAction(text="优化", parent=self) #优化页面 对页面进行一些处理
        toolBar.addAction(toolButton12)
        toolButton13 = QAction(text="叠加", parent=self) #将一张图片叠加到页面上
        toolBar.addAction(toolButton13)
        toolButton14 = QAction(text="盖章", parent=self) #齐缝章
        toolBar.addAction(toolButton14)
        toolBar.actionTriggered[QAction].connect(self.OnClickToolbarButton)
        self.listWidget = ListWidget()
        self.setWindowTitle('LPDF 4.8.3')
        # self.listWidget.setWrapping(True)

        # 添加条目

        # Add textfield to window
        layout.addWidget(self.listWidget)

    def OnClickToolbarButton(self, o):
        print("Click"+o.text())
        if o.text() == "打开":
            self.OnOpenFile()
        if o.text() == "保存":
            if self.doc != None:
                self.doc.saveIncr()
                QMessageBox.question(self, '提示', "已保存", QMessageBox.Yes)
        if o.text() == "另存":
            self.OnReSave()
        if o.text() == "删除":
            self.OnDelPage()
        if o.text() == "旋转":
            self.OnRotatePage()
        if o.text() == "插入":
            self.OnInsterPage()
        if o.text() == "关闭":
            self.lwitem.clear()
            self.listWidget.clear()
            if self.doc != None:
                self.doc.close()
                self.doc = None
            self.listWidget.update()
        if o.text() == "排序":
            self.listWidget.SetMode(self.listWidget.ListMode)
            # self.listWidget.setSelectionMode(QAbstractItemView.ExtendedSelection) #设置可多选
            # self.listWidget.setDragDropMode(QAbstractItemView.InternalMove) #设置可拖动排序
            self.listWidget.setIconSize(
                QSize(int(400*self.zoomsize), int(500*self.zoomsize)))
        if o.text() == "阅读":
            self.listWidget.SetMode()
        
        if o.text() =="导出":
            self.outputwindow=OutputOption()
            self.outputwindow.dateUpdate(13,100,"导出")
            #self.OnOutPut()
        if o.text() =="压缩":
            self.outputwindow=OutputOption()
            self.outputwindow.dateUpdate(10,80,"压缩")
            #self.OnOutZip()
        if o.text() =="合并":
            self.mergelistwindow=MergeListWindow()
            self.mergelistwindow.show()
            #?合并功能 新窗口 拥有调整文件合并顺序的功能
            #?在一个窗口中显示 文件列表 保存路径
        if o.text() =="优化":
            if len(self.listWidget.selectedItems())!=0:
                self.optimizewindow=OptimizeWindow()
                self.optimizewindow.show()
                self.optimizewindow.LoadFromSelect()
            else:
                QMessageBox.question(self, '提示', "未选择需要优化的页面", QMessageBox.Yes)

    def OnOutPut(self,zoom,mase,savefile):
        if self.doc != None:
            select = self.listWidget.selectedItems()
            list = []
            for itm in select:
                    list.append(int(itm.text())-1)
            procbar=ProgressWindow()
            procbar.SetRange(0,len(list))
            RateOfProgress=0
            procbar.SetVaule(RateOfProgress)
            for pagenum in list:
                page= self.doc[pagenum]
                mat = fitz.Matrix(zoom, zoom).preRotate(0)
                pix = page.getPixmap(matrix=mat, alpha=False)
                imgdata=pix.getImageData(output="png")
                image_array = np.frombuffer(imgdata, dtype=np.uint8)
                img_cv = cv2.imdecode(image_array, cv2.IMREAD_ANYCOLOR)
                tmp=savefile+'/%04d'%pagenum+".jpg"
                cv2.imwrite(tmp, img_cv,[cv2.IMWRITE_JPEG_QUALITY,mase])
                RateOfProgress+=1
                procbar.SetVaule(RateOfProgress)
            procbar.close()

    def OnOutZip(self,zoom,mase,savefile):
        #?加进度条 -完成
        #?加入0页面提示无法保存提示 -完成
        #?新建窗口 将输入信息合并
        if self.doc != None:
            select = self.listWidget.selectedItems()
            if len(select)==0:
                QMessageBox.question(self, '提示', "未选择需要压缩的页面", QMessageBox.Yes)
                return
            list = []
            tmpfilelist=[]
            #?压缩图片建立在内存不拷贝至硬盘
            for itm in select:
                    list.append(int(itm.text())-1)
            zippdf=fitz.open()
            procbar=ProgressWindow()
            procbar.SetRange(0,len(list))
            RateOfProgress=0
            procbar.SetVaule(RateOfProgress)
            for pagenum in list:
                page=self.doc[pagenum]
                mat = fitz.Matrix(zoom, zoom).preRotate(0)
                pix = page.getPixmap(matrix=mat, alpha=False)
                imgdata=pix.getImageData(output="png")
                image_array = np.frombuffer(imgdata, dtype=np.uint8)
                img_cv = cv2.imdecode(image_array, cv2.IMREAD_ANYCOLOR)
                #废弃代码
                #tmpfilename="v:"+str(pagenum)+'.jpg'#tempfile.gettempdir()
                #tmpfilelist.append(tmpfilename)
                #cv2.imwrite(tmpfilename, img_cv,[cv2.IMWRITE_JPEG_QUALITY,mase])
                #废弃代码
                jpgimg=cv2.imencode(".jpg",img_cv,[cv2.IMWRITE_JPEG_QUALITY,mase])
                img = fitz.open("jpg",np.array(jpgimg[1]).tobytes())
                pdfbyte = img.convert_to_pdf()
                img.close()
                doc2 = fitz.open("pdf", pdfbyte)
                zippdf.insert_pdf(doc2)
                doc2.close()
                RateOfProgress+=1
                procbar.SetVaule(RateOfProgress)
            zippdf.ez_save(savefile)

            #废弃代码
            #for filepath in tmpfilelist:
            #    img = fitz.open(filepath)
            #    pdfbyte = img.convert_to_pdf()
            #    img.close()
            #    doc2 = fitz.open("pdf", pdfbyte)
            #    zippdf.insert_pdf(doc2)
            #    doc2.close()
            #if savefile[-4:] == ".pdf":
            #    zippdf.ez_save(savefile)
            #else:
            #    zippdf.ez_save(savefile+".pdf")
            #for filepath in tmpfilelist:
            #    os.remove(filepath)
            #废弃代码
    def OnReSave(self):
        if self.doc != None:
            select = self.listWidget.selectedItems()
            savefile = QFileDialog(self, "选择PDF文件", "",
                                   "PDF 文件(*.pdf)").getSaveFileName()[0]
            savedoc = fitz.open()
            if len(select) == 0:
                for i in range(0, self.listWidget.count()):
                    itm = self.listWidget.item(i)
                    savedoc.insert_pdf(self.doc, int(
                        itm.text())-1, int(itm.text())-1, -1)
            else:
                list = []
                for itm in select:
                    list.append(int(itm.text())-1)
                    savedoc.insert_pdf(self.doc, int(
                        itm.text())-1, int(itm.text())-1, -1)
            if savefile[-4:] == ".pdf":
                savedoc.ez_save(savefile)
            else:
                savedoc.ez_save(savefile+".pdf")

    def OnInsterPage(self):
        if self.doc != None:
            self.insterfile = QFileDialog(
                self, "选择PDF文件", "", "PDF 文件(*.pdf)").getOpenFileName()[0]
            self.DoInster()

    def DoInster(self):
        if self.insterfile[-4:] in {".png", ".jpg"}:
            img = fitz.open(self.insterfile)
            rect = img[0].rect
            pdfbyte = img.convert_to_pdf()
            img.close()
            doc2 = fitz.open("pdf", pdfbyte)
        else:
            doc2 = fitz.open(self.insterfile)
        select = self.listWidget.selectedItems()
        list = []
        for itm in select:
            list.append(int(itm.text())-1)
        list.sort()
        if len(list) == 0:
            self.doc.insert_pdf(doc2)
        else:
            self.doc.insert_pdf(doc2, -1, -1, list[0])
        self.ReLoad()

    def OnRotatePage(self):
        if self.doc != None:
            select = self.listWidget.selectedItems()
            list = []
            for itm in select:
                page = self.doc.load_page(int(itm.text())-1)
                page.set_rotation((page.rotation+90) % 360)
                pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
                fmt = QImage.Format_RGBA8888 if pix.alpha else QImage.Format_RGB888
                qtimg = QImage(pix.samples, pix.width,
                               pix.height, pix.stride, fmt)
                self.lwitem[int(itm.text()) -
                            1].setIcon(QIcon(QPixmap.fromImage(qtimg)))

    def OnDelPage(self):
        if self.doc != None:
            select = self.listWidget.selectedItems()
            list = []
            for itm in select:
                list.append(int(itm.text())-1)
            list.sort()
            i = 0
            for i in range(0, len(list)):
                self.doc.delete_page(list[i]-i)
            self.ReLoad()

    def ReLoad(self):
        self.lwitem.clear()
        self.listWidget.clear()
        self.OnLoadPages()

    def OnOpenFile(self):
        self.openfile = QFileDialog(
            self, "选择PDF文件", "", "PDF 文件(*.pdf)").getOpenFileName()[0]
        if self.openfile != "":
            self.lwitem.clear()
            self.listWidget.clear()
            print(self.openfile)
            self.doc = fitz.open(self.openfile)
            self.OnLoadPages()

    def OnLoadPages(self):
        procbar=ProgressWindow()
        procbar.SetRange(0,self.doc.page_count)
        RateOfProgress=0
        procbar.SetVaule(RateOfProgress)
        for page in self.doc:
            pix = page.get_pixmap(matrix=fitz.Matrix(1, 1))
            self.lwitem[page.number] = QListWidgetItem(str(page.number+1))
            fmt = QImage.Format_RGBA8888 if pix.alpha else QImage.Format_RGB888
            qtimg = QImage(pix.samples, pix.width, pix.height, pix.stride, fmt)
            self.lwitem[page.number].setIcon(QIcon(QPixmap.fromImage(qtimg)))
            self.listWidget.addItem(self.lwitem[page.number])
            RateOfProgress+=1
            procbar.SetVaule(RateOfProgress)
        procbar.close()
    def GetPageToData(self,pagenum):
        page=self.doc[pagenum]
        zoom=1.3
        mat = fitz.Matrix(zoom, zoom).preRotate(0)
        pix = page.getPixmap(matrix=mat, alpha=False)
        imgdata=pix.getImageData(output="png")
        image_array = np.frombuffer(imgdata, dtype=np.uint8)
        img_cv = cv2.imdecode(image_array, cv2.IMREAD_ANYCOLOR)
        #jpgimg=cv2.imencode(".jpg",img_cv,[cv2.IMWRITE_JPEG_QUALITY,100])
        return img_cv

app = QApplication(sys.argv)
screen = Window()
screen.show()
sys.exit(app.exec_())
