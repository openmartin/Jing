如何使用pyside+Html5开发桌面应用
====================================

`pyside <http://pyside.org>`_
是
`Qt <http://www.qt.io/>`_
的Python绑定，使用没有任何限制，而且配合python丰富的类库和简洁的语法，开发起来非常方便

pip
-----------------

如果Python版本是2.7.9或者是3.4 以上，pip默认包含于Python的安装包中

怎么安装pip，参考这里 https://pip.pypa.io/en/latest/installing.html

安装pyside
------------------

在Ubuntu 和　DeepinLinux　下安装非常方便

    sudo apt-get install python-pyside

或者使用pip安装

    sudo pip install pyside


创建窗口
-------------------

学习所有的GUI程序，第一步都是创建一个窗口，下面的程序创建了一个无边框的窗口。

    class MainWindow(QtGui.QWidget):
        def __init__(self):
            QtGui.QWidget.__init__(self)

            #初始化position
            self.m_DragPosition=self.pos()

            ＃设置窗口大小
            self.resize(1024,600)
            ＃窗口特征:没有边框
            self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowSystemMenuHint)
            self.setMouseTracking(True)
            #self.setStyleSheet("background-color:#f8f8f8;")

            ＃窗口居中
            desktop =QtGui.QApplication.desktop()
            width = desktop.width()
            height = desktop.height()
            self.move((width - self.width())/2, (height - self.height())/2)

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

    if __name__=="__main__":

        mapp=QtGui.QApplication(sys.argv)
        mw=MainWindow()
        mw.show()
        sys.exit(mapp.exec_())


设计UI
--------------------
pyside有三种设计UI的方式

* 手工编码,编码layout+widget
* xml定义(使用Qt Designer)
* QtQuick/QML定义(使用Qt Creator)，在QT5下更好用,QT4还不完善


查找帮助
--------------------

网上pyside的资料不多，我们该怎么查找资料呢？
QT Creator是QT的官方IDE，里面有官方的帮助文档，C++，不过pyside的函数名是一模一样的，功能也保持一致。

pyside的API文档也是很好的参考资料　http://pyside.github.io/docs/pyside/


webkit
---------------------

WebKit是一个排版引擎，主要设计是用来让网页浏览器绘制网页。WebKit目前作为Apple Safari及Google Chrome（直到版本27）等浏览器的主要引擎。

http://qt-project.org/wiki/QtWebKit

Qt WebKit is the port of WebKit on top of Qt. QtWebKit relies on the public APIs of Qt and can theoretically be used on any platform supported by Qt (theoretically because WebKit also requires a recent/good compiler).


Qt Webkit Bridge
---------------------

在Web环境中，web和后端的交互是通过http协议,但是在qtwebkit中怎么样才能和webkit中的网页交互。
Qt　提供了一个机制　Qt Webkit Bridge来实现这个功能。

有两个特别的函数,实现这个功能

让javascript调用python方法　QtWebKit.QWebView().page().mainFrame().addToJavaScriptWindowObject("pyObj", pyObj)

python中调用javascript函数　QtWebKit.QWebView().page().mainFrame().evaluateJavaScript("alert('Hello World!');")


