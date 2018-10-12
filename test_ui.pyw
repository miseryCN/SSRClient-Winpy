# -*- coding: utf-8 -*-

import privoxy_mode
from PyQt5 import QtCore, QtGui, QtWidgets
import config
from shadowsocks import local

class Ui_Main(object):
    def setupUi(self, Main):
        Main.setObjectName("Main")
        Main.resize(800, 599)
        self.centralwidget = QtWidgets.QWidget(Main)
        self.centralwidget.setObjectName("centralwidget")
        self.title_label = QtWidgets.QLabel(self.centralwidget)
        self.title_label.setGeometry(QtCore.QRect(120, 20, 541, 51))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(18)
        font.setBold(False)
        font.setWeight(50)
        self.title_label.setFont(font)
        self.title_label.setAlignment(QtCore.Qt.AlignCenter)
        self.title_label.setObjectName("title_label")
        self.pac_button = QtWidgets.QPushButton(self.centralwidget)
        self.pac_button.setGeometry(QtCore.QRect(80, 250, 151, 71))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.pac_button.setFont(font)
        self.pac_button.setObjectName("pac_button")
        self.all_button = QtWidgets.QPushButton(self.centralwidget)
        self.all_button.setGeometry(QtCore.QRect(310, 250, 151, 71))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.all_button.setFont(font)
        self.all_button.setObjectName("all_button")
        self.direct_button = QtWidgets.QPushButton(self.centralwidget)
        self.direct_button.setGeometry(QtCore.QRect(540, 250, 151, 71))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.direct_button.setFont(font)
        self.direct_button.setObjectName("direct_button")
        self.exit_button = QtWidgets.QPushButton(self.centralwidget)
        self.exit_button.setGeometry(QtCore.QRect(660, 520, 101, 41))
        self.exit_button.setObjectName("exit_button")
        self.now = QtWidgets.QLabel(self.centralwidget)
        self.now.setGeometry(QtCore.QRect(220, 120, 131, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.now.setFont(font)
        self.now.setObjectName("now")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(330, 120, 191, 41))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        Main.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(Main)
        self.statusbar.setObjectName("statusbar")
        Main.setStatusBar(self.statusbar)

        self.retranslateUi(Main)
        self.pac_button.clicked.connect(self.pac)
        self.all_button.clicked.connect(self.all)
        self.direct_button.clicked.connect(self.direct)
        self.exit_button.clicked.connect(self.close)
        QtCore.QMetaObject.connectSlotsByName(Main)

    def retranslateUi(self, Main):
        _translate = QtCore.QCoreApplication.translate
        Main.setWindowTitle(_translate("Main", "小伟博客网络加速器客户端"))
        self.title_label.setText(_translate("Main", "小伟博客网络加速器客户端 技术预览版"))
        self.pac_button.setText(_translate("Main", "PAC模式"))
        self.all_button.setText(_translate("Main", "全局模式"))
        self.direct_button.setText(_translate("Main", "直连模式"))
        self.exit_button.setText(_translate("Main", "退出软件"))
        self.now.setText(_translate("Main", "当前模式:"))
        self.label_2.setText(_translate("Main","<html><head/><body><p><span style=\" font-weight:600; color:#ff0000;\">未切换模式</span></p></body></html>"))

    def pac(self):
        self.label_2.setText(
            "<html><head/><body><p><span style=\" font-weight:600; color:#ff0000;\">PAC模式</span></p></body></html>")
        privoxy_mode.pac_mode()
    def all(self):
        self.label_2.setText(
            "<html><head/><body><p><span style=\" font-weight:600; color:#ff0000;\">全局模式</span></p></body></html>")
        privoxy_mode.all_mode()
    def direct(self):
        self.label_2.setText(
            "<html><head/><body><p><span style=\" font-weight:600; color:#ff0000;\">直连模式</span></p></body></html>")
        privoxy_mode.direct_mode()
    def close(self,Main):
        privoxy_mode.direct_mode()
        self.exit_button.clicked.connect(Main.close)
if __name__ == '__main__':
    import sys
    from threading import Thread
    def sslocal():
        ss_config = config.get_config()
        local.main(ss_config)

    def MainUI():
        app = QtWidgets.QApplication(sys.argv)
        fromObj = QtWidgets.QMainWindow()
        ui = Ui_Main()
        ui.setupUi(fromObj)
        fromObj.show()
        sys.exit(app.exec_())

    UI = Thread(target=MainUI)
    ss_local = Thread(target=sslocal)
    ss_local.setDaemon(True)
    ss_local.start()
    UI.start()


