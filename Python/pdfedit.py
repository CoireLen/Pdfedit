import sys
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from typing import Optional
from PyQt5.sip import delete
import fitz
import numpy as np
import cv2
from numpy.lib.function_base import select

main = {}
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
        toolButton2 = QAction(text="载入预设", parent=self)
        toolBar.addAction(toolButton2)
        toolButton3 = QAction(text="保存预设", parent=self)
        toolBar.addAction(toolButton3)
        self.setLayout(layout)
        self.slider1 = QSlider()
        self.slider1.setRange(0,0)
        self.slider1.setValue(0)
        self.slider1.setOrientation(Qt.Horizontal)
        layout.addWidget(self.slider1)

        self.picview = QGraphicsView()
        layout.addWidget(self.picview)
        self.setWindowTitle("优化工具")
        
        self.resize(800,600)
    def OnClickToolbarButton(self,o):
        if o.text()=="":
            None

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
        for i in range(self.list1.count()-1):
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
                            else:
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
            self.optimizewindow=OptimizeWindow()
            self.optimizewindow.show()

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


app = QApplication(sys.argv)
screen = Window()
screen.show()
sys.exit(app.exec_())
