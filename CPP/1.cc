#include "fitz.hpp"
#include "MQIcon.h"
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
	std::vector<Doc> doc;
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
	doc.clear();
	doc.push_back(Doc(openfilepath));
	//QImage image(samples, width, height, pix->stride, QImage::Format_RGB888);
	this->LoadPages();
}

void Window::LoadPages() {
	if (listwidgetitems.empty()==false)
		for (auto i = listwidgetitems.rbegin(); i != listwidgetitems.rend(); i++) {
			listWidget.removeItemWidget(*i);
			delete* i;
		}
	listwidgetitems.clear();
	for (int i = 0; i < doc[0].pagecount(); i++) {
		fz_pixmap*pix= doc[0].GetPageToPixmap(i);
		listwidgetitems.push_back(new QListWidgetItem());
		listwidgetitems[i]->setText(QString::number(i + 1));
		QImage img((unsigned char*)pix->samples, pix->w, pix->h, pix->stride, QImage::Format_RGB888);
		listwidgetitems [i]->setIcon(QIcon(QPixmap::fromImage(img)));
		listWidget.addItem(listwidgetitems[i]);
	}
	//内存泄漏
}
void Window::OnSaveFile() {
	doc[0].save();
}
void Window::ReSaveFile() {
	QString resavefilepath = QFileDialog(this, "选择PDF文件", "", "PDF 文件(*.pdf)").getOpenFileName();
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
		doc[0].del_page(*i);
		listWidget.removeItemWidget(listwidgetitems[*i]);
		listwidgetitems[*i]->~QListWidgetItem();
		delete listwidgetitems[*i];
		listwidgetitems.erase(listwidgetitems.begin()+*i);
		//内存泄漏
		
	}
	//更新页面页码
	int x = 1;
	for (auto i : listwidgetitems) {
		i->setText(QString::number(x++));
	}
	//LoadPages();//待优化
}
void Window::OnRotatePage() {
	QList<QListWidgetItem*> llis = listWidget.selectedItems();
	std::vector<int> needDelPageNum;
	for (auto i : llis) {
		int pagenum = i->text().toInt() - 1;
		doc[0].set_rotation(90, pagenum);
		fz_pixmap* pix = doc[0].GetPageToPixmap(pagenum);
		QImage img((unsigned char*)pix->samples, pix->w, pix->h, pix->stride, QImage::Format_RGB888);
		//内存泄漏
		listwidgetitems[pagenum]->setIcon(QIcon(QPixmap::fromImage(img)));
		img.~QImage();
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