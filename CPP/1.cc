#include "fitz.hpp"
//#include "QIcon.h"
#include <QtWidgets/qlistwidget.h>
#include <QtGui/qbitmap.h>
#include <QtWidgets/QApplication>
#include <QtWidgets/QMainWindow>
#include <QtWidgets/QLabel>
#include <QtCore/qtextcodec.h>
#include <QtWidgets/qlayout.h>
#include <QtWidgets/qwidget.h>
#include <QtWidgets/qtoolbar.h>
#include <QtWidgets/qaction.h>
#include <QtWidgets/qfiledialog.h>
#include <QtGui/qevent.h>
#include <QtWidgets/qmessagebox.h>
#include <iostream>
#include <algorithm>
QTextCodec* coder = QTextCodec::codecForName("GBK");


class MListWidget:public QListWidget
{
public:
	MListWidget();
	~MListWidget();
	void keyReleaseEvent(QKeyEvent*);
	void keyPressEvent(QKeyEvent*);
	void wheelEvent(QWheelEvent*);
	void Zoom();
private:
	double zoomsize = 1.5;
	bool ctrlPressed = false;
};

MListWidget::MListWidget()
{
	this->setViewMode(QListWidget::IconMode);
	this->setAcceptDrops(true);
	this->setDragEnabled(true);
	this->setDragDropMode(QAbstractItemView::InternalMove);           //设置拖放
	this->setSelectionMode(QAbstractItemView::ExtendedSelection); //设置选择多个
	this->setDefaultDropAction(Qt::MoveAction);
	this->setFlow(QListView::LeftToRight);
	Zoom();
}
void MListWidget::keyReleaseEvent(QKeyEvent* event) {
	if (event->key() == 0x1000021) {
		ctrlPressed = false;
	}
	printf("0x%X ",event->key());
}
void MListWidget::Zoom() {
	this->setIconSize(QSize(int(400 * this->zoomsize), int(500 * this->zoomsize)));
}
void MListWidget::wheelEvent(QWheelEvent*event) {
	if (this->ctrlPressed)
	{
		QPoint delta=event->angleDelta();
		int oriention=delta.y() / 8;
		if (oriention > 0) {
			zoomsize += 0.1;
		}
		else {
			zoomsize -= 0.1;
		}
		Zoom();
	}
	QListWidget::wheelEvent(event);
}
void MListWidget::keyPressEvent(QKeyEvent*event) {
	if (event->key() == 0x1000021) {
		ctrlPressed = true;
	}
	
}
MListWidget ::~MListWidget()
{
}

class Window:public QWidget
	
{
	
public:
	Window(QWidget* parent=0);
	~Window();
	void OnOpenFile();//打开
	void OnSaveFile();//保存
	void ReSaveFile();//另存为
	void OnDelPage();//删除页面
	void OnRotatePage();//旋转页面
	void OnInstPage();//插入页面
	void OnSortMode();//排序模式
	void OnReadMode();//阅读模式
	void OnCloseDoc();//关闭文档
	void LoadPages();
	void ClearListWidget();
	//void* doc=fz_open_document
private:
	std::vector<Doc*> doc;
	QGridLayout layout;
	QToolBar toolBar;
	MListWidget listWidget;
	bool ctrlPressed=false;
	double zoomsize = 1.5;
	std::vector<QListWidgetItem*> listwidgetitems;
	QString openfilepath;
};

Window::Window(QWidget* parent):QWidget(parent)
{	
	this->setGeometry(0, 0, 800, 600);
	this->setLayout(&layout);
	this->setWindowTitle(coder->toUnicode("LPDF 5.0"));
	/// <--  工具栏菜单
	//打开文件
	static QAction toolButton1(coder->toUnicode("打开"));
	toolBar.addAction(&toolButton1);
	connect(&toolButton1 ,&QAction::triggered, this, &Window::OnOpenFile);
	//保存文件
	static QAction toolButton2(coder->toUnicode("保存"));
	toolBar.addAction(&toolButton2);
	connect(&toolButton2, &QAction::triggered, this, &Window::OnSaveFile);
	//另存文件
	static QAction toolButton3(coder->toUnicode("另存"));
	toolBar.addAction(&toolButton3);
	connect(&toolButton3, &QAction::triggered, this, &Window::ReSaveFile);
	//删除页面
	static QAction toolButton4(coder->toUnicode("删除"));
	toolBar.addAction(&toolButton4);
	connect(&toolButton4, &QAction::triggered, this, &Window::OnDelPage);
	//旋转页面
	static QAction toolButton5(coder->toUnicode("旋转"));
	toolBar.addAction(&toolButton5);
	connect(&toolButton5, &QAction::triggered, this, &Window::OnRotatePage);
	//插入页面
	static QAction toolButton6(coder->toUnicode("插入"));
	toolBar.addAction(&toolButton6);
	connect(&toolButton6, &QAction::triggered, this, &Window::OnInstPage);
	//排序
	static QAction toolButton7(coder->toUnicode("排序"));
	toolBar.addAction(&toolButton7);
	connect(&toolButton7, &QAction::triggered, this, &Window::OnSortMode);
	//阅读
	static QAction toolButton8(coder->toUnicode("阅读"));
	toolBar.addAction(&toolButton8);
	connect(&toolButton8, &QAction::triggered, this, &Window::OnReadMode);
	//关闭文件
	static QAction toolButton9(coder->toUnicode("关闭"));
	toolBar.addAction(&toolButton9);
	connect(&toolButton9, &QAction::triggered, this, &Window::OnCloseDoc);
	/// -->
	layout.addWidget(&toolBar);
	layout.addWidget(&listWidget);
	this->show();
}
//按键的实现
void Window::OnOpenFile() {
	openfilepath = QFileDialog(this, "选择PDF文件", "", "PDF 文件(*.pdf)").getOpenFileName();
	if (!doc.empty()) {
		delete doc[0];
		doc.clear();
	}
	QByteArray qba = coder->fromUnicode(openfilepath);
	doc.push_back(new Doc(qba));
	//QImage image(samples, width, height, pix->stride, QImage::Format_RGB888);
	this->LoadPages();
}

void Window::LoadPages() {
	if (listwidgetitems.empty()==false)
		for (auto i = listwidgetitems.rbegin(); i != listwidgetitems.rend(); i++) {
			listWidget.removeItemWidget(*i);
			//(*i)->icon().~QIcon();
			delete* i;
		}
	listwidgetitems.clear();
	for (int i = 0; i < doc[0]->pagecount(); i++) {
		fz_pixmap*pix= doc[0]->GetPageToPixmap(i);
		listwidgetitems.push_back(new QListWidgetItem());
		listwidgetitems[i]->setText(QString::number(i + 1));
		QImage img((unsigned char*)pix->samples, pix->w, pix->h, pix->stride, QImage::Format_RGB888);
		listwidgetitems [i]->setIcon(QIcon(QPixmap::fromImage(img)));
		listWidget.addItem(listwidgetitems[i]);
		doc[0]->DorpPixmap(pix);
		//fz_pixmap* pix = doc[0].GetPageToPixmap(i);
		//QImage img((unsigned char*)pix->samples, pix->w, pix->h, pix->stride, QImage::Format_RGB888);
		//listitems.push_back(std::pair<QListWidgetItem*, QPixmap*>(new QListWidgetItem(), &QPixmap::fromImage(img)));
	}
	//内存泄漏
}
void Window::OnSaveFile() {
	if (!doc.empty())
		doc[0]->save();
	else {
		QMessageBox msgbox;
		msgbox.setText(coder->toUnicode("没有打开的文件,或内容为(空)"));
		msgbox.exec();
	}
}
void Window::ReSaveFile() {
	QString resavefilepath = QFileDialog(this, "选择文件", "*.pdf", "PDF 文件(*.pdf)").getOpenFileName();
}
void Window::OnDelPage() //删除页面
{

	QList<QListWidgetItem*> llis = listWidget.selectedItems();
	std::vector<int> needDelPageNum;
	for (auto i:llis){
		needDelPageNum.push_back(i->text().toInt()-1);
	}
	std::sort(needDelPageNum.begin(), needDelPageNum.end());
	for (auto i = needDelPageNum.rbegin(); i != needDelPageNum.rend(); i++) {
		doc[0]->del_page(*i);
		listWidget.removeItemWidget(listwidgetitems[*i]);
		listwidgetitems[*i]->~QListWidgetItem();
		listwidgetitems.erase(listwidgetitems.begin()+*i);

		//内存泄漏
	}
	//更新页面页码
	int x = 1;
	for (auto i : listwidgetitems) {
		i->setText(QString::number(x++));
	}
	if (listwidgetitems.empty()) {
		delete doc[0];
		doc.clear();
	}
	//LoadPages();//待优化
}
void Window::OnRotatePage() {
	QList<QListWidgetItem*> llis = listWidget.selectedItems();
	std::vector<int> needDelPageNum;
	for (auto i : llis) {
		int pagenum = i->text().toInt() - 1;
		doc[0]->set_rotation(90, pagenum);
		fz_pixmap* pix = doc[0]->GetPageToPixmap(pagenum);
		QImage img((unsigned char*)pix->samples, pix->w, pix->h, pix->stride, QImage::Format_RGB888);
		
		listwidgetitems[pagenum]->setIcon(QIcon(QPixmap::fromImage(img)));

		doc[0]->DorpPixmap(pix);
	}

}//旋转页面
void Window::OnInstPage(){}//插入页面
void Window::OnSortMode(){}//排序模式
void Window::OnReadMode(){}//阅读模式
void Window::OnCloseDoc(){}//关闭文档
Window::~Window()
{
	if (listwidgetitems.empty() == false)
		for (auto i = listwidgetitems.rbegin(); i != listwidgetitems.rend(); i++) {
			listWidget.removeItemWidget(*i);
			delete* i;
		}
	
}


int main(int argc,char **argv)
{
    QApplication app(argc, argv);
	Window screen;
    return app.exec();
}

/*
				   GNU LESSER GENERAL PUBLIC LICENSE
					   Version 3, 29 June 2007

 Copyright (C) 2007 Free Software Foundation, Inc. <https://fsf.org/>
 Everyone is permitted to copy and distribute verbatim copies
 of this license document, but changing it is not allowed.


  This version of the GNU Lesser General Public License incorporates
the terms and conditions of version 3 of the GNU General Public
License, supplemented by the additional permissions listed below.

  0. Additional Definitions.

  As used herein, "this License" refers to version 3 of the GNU Lesser
General Public License, and the "GNU GPL" refers to version 3 of the GNU
General Public License.

  "The Library" refers to a covered work governed by this License,
other than an Application or a Combined Work as defined below.

  An "Application" is any work that makes use of an interface provided
by the Library, but which is not otherwise based on the Library.
Defining a subclass of a class defined by the Library is deemed a mode
of using an interface provided by the Library.

  A "Combined Work" is a work produced by combining or linking an
Application with the Library.  The particular version of the Library
with which the Combined Work was made is also called the "Linked
Version".

  The "Minimal Corresponding Source" for a Combined Work means the
Corresponding Source for the Combined Work, excluding any source code
for portions of the Combined Work that, considered in isolation, are
based on the Application, and not on the Linked Version.

  The "Corresponding Application Code" for a Combined Work means the
object code and/or source code for the Application, including any data
and utility programs needed for reproducing the Combined Work from the
Application, but excluding the System Libraries of the Combined Work.

  1. Exception to Section 3 of the GNU GPL.

  You may convey a covered work under sections 3 and 4 of this License
without being bound by section 3 of the GNU GPL.

  2. Conveying Modified Versions.

  If you modify a copy of the Library, and, in your modifications, a
facility refers to a function or data to be supplied by an Application
that uses the facility (other than as an argument passed when the
facility is invoked), then you may convey a copy of the modified
version:

   a) under this License, provided that you make a good faith effort to
   ensure that, in the event an Application does not supply the
   function or data, the facility still operates, and performs
   whatever part of its purpose remains meaningful, or

   b) under the GNU GPL, with none of the additional permissions of
   this License applicable to that copy.

  3. Object Code Incorporating Material from Library Header Files.

  The object code form of an Application may incorporate material from
a header file that is part of the Library.  You may convey such object
code under terms of your choice, provided that, if the incorporated
material is not limited to numerical parameters, data structure
layouts and accessors, or small macros, inline functions and templates
(ten or fewer lines in length), you do both of the following:

   a) Give prominent notice with each copy of the object code that the
   Library is used in it and that the Library and its use are
   covered by this License.

   b) Accompany the object code with a copy of the GNU GPL and this license
   document.

  4. Combined Works.

  You may convey a Combined Work under terms of your choice that,
taken together, effectively do not restrict modification of the
portions of the Library contained in the Combined Work and reverse
engineering for debugging such modifications, if you also do each of
the following:

   a) Give prominent notice with each copy of the Combined Work that
   the Library is used in it and that the Library and its use are
   covered by this License.

   b) Accompany the Combined Work with a copy of the GNU GPL and this license
   document.

   c) For a Combined Work that displays copyright notices during
   execution, include the copyright notice for the Library among
   these notices, as well as a reference directing the user to the
   copies of the GNU GPL and this license document.

   d) Do one of the following:

	   0) Convey the Minimal Corresponding Source under the terms of this
	   License, and the Corresponding Application Code in a form
	   suitable for, and under terms that permit, the user to
	   recombine or relink the Application with a modified version of
	   the Linked Version to produce a modified Combined Work, in the
	   manner specified by section 6 of the GNU GPL for conveying
	   Corresponding Source.

	   1) Use a suitable shared library mechanism for linking with the
	   Library.  A suitable mechanism is one that (a) uses at run time
	   a copy of the Library already present on the user's computer
	   system, and (b) will operate properly with a modified version
	   of the Library that is interface-compatible with the Linked
	   Version.

   e) Provide Installation Information, but only if you would otherwise
   be required to provide such information under section 6 of the
   GNU GPL, and only to the extent that such information is
   necessary to install and execute a modified version of the
   Combined Work produced by recombining or relinking the
   Application with a modified version of the Linked Version. (If
   you use option 4d0, the Installation Information must accompany
   the Minimal Corresponding Source and Corresponding Application
   Code. If you use option 4d1, you must provide the Installation
   Information in the manner specified by section 6 of the GNU GPL
   for conveying Corresponding Source.)

  5. Combined Libraries.

  You may place library facilities that are a work based on the
Library side by side in a single library together with other library
facilities that are not Applications and are not covered by this
License, and convey such a combined library under terms of your
choice, if you do both of the following:

   a) Accompany the combined library with a copy of the same work based
   on the Library, uncombined with any other library facilities,
   conveyed under the terms of this License.

   b) Give prominent notice with the combined library that part of it
   is a work based on the Library, and explaining where to find the
   accompanying uncombined form of the same work.

  6. Revised Versions of the GNU Lesser General Public License.

  The Free Software Foundation may publish revised and/or new versions
of the GNU Lesser General Public License from time to time. Such new
versions will be similar in spirit to the present version, but may
differ in detail to address new problems or concerns.

  Each version is given a distinguishing version number. If the
Library as you received it specifies that a certain numbered version
of the GNU Lesser General Public License "or any later version"
applies to it, you have the option of following the terms and
conditions either of that published version or of any later version
published by the Free Software Foundation. If the Library as you
received it does not specify a version number of the GNU Lesser
General Public License, you may choose any version of the GNU Lesser
General Public License ever published by the Free Software Foundation.

  If the Library as you received it specifies that a proxy can decide
whether future versions of the GNU Lesser General Public License shall
apply, that proxy's public statement of acceptance of any version is
permanent authorization for you to choose that version for the
Library.
*/