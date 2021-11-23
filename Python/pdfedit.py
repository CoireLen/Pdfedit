from os import system
import sys
from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from typing import Optional
import fitz
import numpy as np
import cv2
import tempfile
import os
main = {}
#


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
        toolBar.actionTriggered[QAction].connect(self.OnClickToolbarButton)
        self.listWidget = ListWidget()
        self.setWindowTitle('LPDF 4.8')
        # self.listWidget.setWrapping(True)

        # 添加条目

        # Add textfield to window
        layout.addWidget(self.listWidget)

    def OnClickToolbarButton(self, o):
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
        print("Click"+o.text())
        if o.text() =="导出":
            self.OnOutPut()
        if o.text() =="压缩":
            self.OnOutZip()
    def OnOutPut(self):
        if self.doc != None:
            savefile = QFileDialog.getExistingDirectory()
            gd=QInputDialog.getDouble(self, "缩放倍率",":", 1.3, 0, 5, 3)
            if gd[1]!=True:
                zoom=gd[0]
                select = self.listWidget.selectedItems()
                mase=100
                list = []
                for itm in select:
                        list.append(int(itm.text())-1)
                for pagenum in list:
                    page= self.doc[pagenum]
                    mat = fitz.Matrix(zoom, zoom).preRotate(0)
                    pix = page.getPixmap(matrix=mat, alpha=False)
                    imgdata=pix.getImageData(output="png")
                    image_array = np.frombuffer(imgdata, dtype=np.uint8)
                    img_cv = cv2.imdecode(image_array, cv2.IMREAD_ANYCOLOR)
                    cv2.imwrite(savefile+'\\'+str(pagenum)+".jpg", img_cv,[cv2.IMWRITE_JPEG_QUALITY,mase])
    def OnOutZip(self):
        if self.doc != None:
            gf=QFileDialog(self, "选择PDF文件", "",
                                   "PDF 文件(*.pdf)").getSaveFileName()
            savefile = gf[0]
            zoom=1.0
            gi=QInputDialog.getInt(self, "保存质量",":", 80, 0, 100, 10)
            mase=gi[0]
            select = self.listWidget.selectedItems()
            list = []
            tmpfilelist=[]
            if (gi[1] and gf[1]) !=False:
                for itm in select:
                        list.append(int(itm.text())-1)
                for pagenum in list:
                    page=self.doc[pagenum]
                    mat = fitz.Matrix(zoom, zoom).preRotate(0)
                    pix = page.getPixmap(matrix=mat, alpha=False)
                    imgdata=pix.getImageData(output="png")
                    image_array = np.frombuffer(imgdata, dtype=np.uint8)
                    img_cv = cv2.imdecode(image_array, cv2.IMREAD_ANYCOLOR)
                    tmpfilename=str(pagenum)+'.jpg'#tempfile.gettempdir()
                    tmpfilelist.append(tmpfilename)
                    cv2.imwrite(tmpfilename, img_cv,[cv2.IMWRITE_JPEG_QUALITY,mase])
                zippdf=fitz.open()
                for filepath in tmpfilelist:
                    img = fitz.open(filepath)
                    pdfbyte = img.convert_to_pdf()
                    img.close()
                    doc2 = fitz.open("pdf", pdfbyte)
                    zippdf.insert_pdf(doc2)
                    doc2.close()
                if savefile[-4:] == ".pdf":
                    zippdf.ez_save(savefile)
                else:
                    zippdf.ez_save(savefile+".pdf")
                for filepath in tmpfilelist:
                    os.remove(filepath)

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
        for page in self.doc:
            pix = page.get_pixmap(matrix=fitz.Matrix(1, 1))
            self.lwitem[page.number] = QListWidgetItem(str(page.number+1))
            fmt = QImage.Format_RGBA8888 if pix.alpha else QImage.Format_RGB888
            qtimg = QImage(pix.samples, pix.width, pix.height, pix.stride, fmt)
            self.lwitem[page.number].setIcon(QIcon(QPixmap.fromImage(qtimg)))
            self.listWidget.addItem(self.lwitem[page.number])


app = QApplication(sys.argv)
screen = Window()
screen.show()
sys.exit(app.exec_())
