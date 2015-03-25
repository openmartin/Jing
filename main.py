#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
Jing Astrology Program
Author: pengzili
"""

import sys
import json
import urllib
from PySide import QtCore
from PySide import QtGui
from PySide import QtWebKit
from PySide.QtCore import Qt
from djing.settings import WEBKIT_RESOURCE_PATH
import views


class BridgeClass(QtCore.QObject):
    """The QtWebKit Bridge Class"""

    def __init__(self, window):
        """accept a QtCore.QWidget"""
        QtCore.QObject.__init__(self)
        self.window = window
    
    @QtCore.Slot(str)
    def passPara(self, msg):
        print msg
        #QtGui.QMessageBox.information(self.window, "Info", msg)
        order = json.loads(msg)
        action = order["action"]
        print action
        action_data = order["data"]
        print action_data
        #print sys.getdefaultencoding()
        
        if action == "add_action":
            self.add_action(action_data)
        if action == "natal":
            self.natal(action_data)
        if action == "edit":
            self.edit(action_data)
        if action == "edit_action":
            self.edit_action(action_data)
        if action == "delete":
            self.delete(action_data)
        if action == "page":
            self.list(action_data)

    def add_action(self, data):
        views.add_action(data)
        self.window.list()

    def natal(self, data):
        self.window.natal(data)

    def edit(self, data):
        self.window.edit(data)

    def edit_action(self, data):
        views.edit_action(data)
        self.window.list()

    def delete(self, data):
        views.delete(data)
        self.window.list()

    def list(self, data):
        self.window.list(page=int(data))




class MainWindow(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)

        #初始化position
        self.m_DragPosition=self.pos()

        self.resize(1024,600)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowSystemMenuHint)
        self.setMouseTracking(True)
        #self.setStyleSheet("background-color:#f8f8f8;")

        desktop =QtGui.QApplication.desktop()
        width = desktop.width()
        height = desktop.height()
        self.move((width - self.width())/2, (height - self.height())/2)
        
        #QVBoxLayout {QHBoxLayout{QPushButton}, QWebView}
        mainLayout = QtGui.QVBoxLayout()
        topLayout = QtGui.QHBoxLayout()

        #设置widget间没有空间 扁平化
        mainLayout.setContentsMargins(0, 0, 0, 0)
        topLayout.setContentsMargins(0, 0, 0, 0)
        mainLayout.setSpacing(0)
        topLayout.setSpacing(0)


        #按钮一
        qbtn_one=QtGui.QPushButton(u"本命盘",self)
        #qbtn_one.setGeometry(0,0,120,80)
        qbtn_one.setStyleSheet("QPushButton{background-color:#f8f8f8;border:none;color:#555;font-size:20px;padding:15px;margin:0;}"
                               "QPushButton:hover{background-color:#e7e7e7;}"
                               "QPushButton:disabled{background-color:#e7e7e7;}"
                               "QPushButton:focus {outline: none;}")

        qbtn_one.setEnabled(False)

        qbtn_two=QtGui.QPushButton(u"新增个人",self)
        qbtn_two.setStyleSheet("QPushButton{background-color:#f8f8f8;border:none;color:#555;font-size:20px;padding:15px;margin:0;}"
                               "QPushButton:hover{background-color:#e7e7e7;}"
                               "QPushButton:disabled{background-color:#e7e7e7;}"
                               "QPushButton:focus {outline: none;}")

        qbtn_three=QtGui.QPushButton(u"我的资料",self)
        qbtn_three.setStyleSheet("QPushButton{background-color:#f8f8f8;border:none;color:#555;font-size:20px;padding:15px;}"
                               "QPushButton:hover{background-color:#e7e7e7;}"
                               "QPushButton:disabled{background-color:#e7e7e7;}"
                               "QPushButton:focus {outline: none;}")

        qbtn_four=QtGui.QPushButton(u"点击测试",self)
        qbtn_four.setStyleSheet("QPushButton{background-color:#f8f8f8;border:none;color:#555;font-size:20px;padding:15px;}"
                               "QPushButton:hover{background-color:#e7e7e7;}"
                               "QPushButton:disabled{background-color:#e7e7e7;}"
                               "QPushButton:focus {outline: none;}")

        qbtn_close=QtGui.QPushButton(u"关闭此窗口",self)
        qbtn_close.setStyleSheet("QPushButton{background-color:#f8f8f8;border:none;color:#555;font-size:20px;padding:15px;}"
                               "QPushButton:hover{background-color:#e7e7e7;}"
                               "QPushButton:disabled{background-color:#e7e7e7;}"
                               "QPushButton:focus {outline: none;}")

        qbtn_max=QtGui.QPushButton(u"最大化",self)
        qbtn_max.setStyleSheet("QPushButton{background-color:#f8f8f8;border:none;color:#555;font-size:20px;padding:15px;}"
                               "QPushButton:hover{background-color:#e7e7e7;}"
                               "QPushButton:disabled{background-color:#e7e7e7;}"
                               "QPushButton:focus {outline: none;}")

        self.qbtn_one = qbtn_one
        self.qbtn_two = qbtn_two
        self.qbtn_three = qbtn_three
        self.qbtn_four = qbtn_four
        self.qbtn_close = qbtn_close
        self.qbtn_max = qbtn_max

        topLayout.addWidget(qbtn_one)
        topLayout.addWidget(qbtn_two)
        topLayout.addWidget(qbtn_three)
        topLayout.addWidget(qbtn_four)
        topLayout.addWidget(qbtn_close)
        topLayout.addWidget(qbtn_max)
        topLayout.addStretch()



        #add to javascript
        #myObj = BridgeClass(self)
        #self.myObj = myObj

        #QWebView
        html_render = QtWebKit.QWebView(self)
        html_render.settings().setAttribute(
            QtWebKit.QWebSettings.WebAttribute.DeveloperExtrasEnabled, True)
        #html_render.page().mainFrame().addToJavaScriptWindowObject("pyObj", self.myObj)

        url = QtCore.QUrl("https://html5test.com/")
        html_render.load(url)
        self.html_render = html_render

        mainLayout.addLayout(topLayout)
        mainLayout.addWidget(html_render)

        self.setLayout(mainLayout)

        #注册事件
        qbtn_two.clicked.connect(self.add)
        qbtn_three.clicked.connect(self.list)
        qbtn_four.clicked.connect(self.showone)

        #use new syntax
        qbtn_close.clicked.connect(QtGui.qApp.quit)
        qbtn_max.clicked.connect(self.maxSize)

        #If you intend to add QObjects to a QWebFrame using addToJavaScriptWindowObject(), 
        #you should add them in a slot connected to this signal. This ensures that your objects remain accessible when loading new URLs.
        self.html_render.page().mainFrame().javaScriptWindowObjectCleared.connect(self.addJSObject)


    #支持窗口拖动,重写两个方法
    def mousePressEvent(self, event):
        if event.button()==Qt.LeftButton:
            self.m_drag=True
            self.m_DragPosition=event.globalPos()-self.pos()
            event.accept()


    def mouseMoveEvent(self, QMouseEvent):
        if QMouseEvent.buttons() and Qt.LeftButton:
            self.move(QMouseEvent.globalPos()-self.m_DragPosition)
            QMouseEvent.accept()


    def mouseReleaseEvent(self, QMouseEvent):
        self.m_drag=False

    def addJSObject(self):
        self.html_render.page().mainFrame().addToJavaScriptWindowObject("pyObj", self.bridgeObj)

    def setBridge(self, bridge):
        self.bridgeObj = bridge
    
    def natal(self, data):
        tmp_html = views.natal(data)
        self.html_render.load(tmp_html, baseurl=WEBKIT_RESOURCE_PATH)

    def add(self):
        tmp_html = views.add()
        self.html_render.load(tmp_html, baseurl=WEBKIT_RESOURCE_PATH)

    def edit(self, data):
        tmp_html = views.edit(data)
        self.html_render.load(tmp_html, baseurl=WEBKIT_RESOURCE_PATH)

    def list(self, page=1):
        tmp_html = views.list(page)
        self.html_render.load(tmp_html, baseurl=WEBKIT_RESOURCE_PATH)

    def showone(self):
        tmp_html = views.testshow()
        self.html_render.load(tmp_html, baseurl=WEBKIT_RESOURCE_PATH)

    def maxSize(self):
        self.showMaximized()
    


if __name__=="__main__":

    mapp=QtGui.QApplication(sys.argv)
    mw=MainWindow()
    bridgeObj = BridgeClass(mw)
    mw.setBridge(bridgeObj)
    mw.show()
    sys.exit(mapp.exec_())