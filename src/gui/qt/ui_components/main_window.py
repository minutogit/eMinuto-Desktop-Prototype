# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window.ui'
##
## Created by: Qt User Interface Compiler version 6.6.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QLabel,
    QLineEdit, QMainWindow, QMenu, QMenuBar,
    QSizePolicy, QStatusBar, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        self.actionProfile = QAction(MainWindow)
        self.actionProfile.setObjectName(u"actionProfile")
        self.actionClose = QAction(MainWindow)
        self.actionClose.setObjectName(u"actionClose")
        self.actionEditProfile = QAction(MainWindow)
        self.actionEditProfile.setObjectName(u"actionEditProfile")
        self.actionProfileLogin = QAction(MainWindow)
        self.actionProfileLogin.setObjectName(u"actionProfileLogin")
        self.actionProfileLogout = QAction(MainWindow)
        self.actionProfileLogout.setObjectName(u"actionProfileLogout")
        self.actionCreateProfile = QAction(MainWindow)
        self.actionCreateProfile.setObjectName(u"actionCreateProfile")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.label_username = QLabel(self.centralwidget)
        self.label_username.setObjectName(u"label_username")
        self.label_username.setGeometry(QRect(10, 10, 781, 21))
        font = QFont()
        font.setPointSize(14)
        font.setBold(True)
        self.label_username.setFont(font)
        self.frame = QFrame(self.centralwidget)
        self.frame.setObjectName(u"frame")
        self.frame.setGeometry(QRect(10, 40, 781, 121))
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.label = QLabel(self.frame)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(10, 10, 121, 16))
        font1 = QFont()
        font1.setPointSize(14)
        font1.setBold(True)
        font1.setItalic(False)
        self.label.setFont(font1)
        self.layoutWidget = QWidget(self.frame)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(10, 40, 341, 70))
        self.verticalLayout = QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_2 = QLabel(self.layoutWidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(150, 0))
        font2 = QFont()
        font2.setPointSize(11)
        self.label_2.setFont(font2)

        self.horizontalLayout.addWidget(self.label_2)

        self.lineEdit_own_balance = QLineEdit(self.layoutWidget)
        self.lineEdit_own_balance.setObjectName(u"lineEdit_own_balance")
        self.lineEdit_own_balance.setFont(font2)
        self.lineEdit_own_balance.setReadOnly(True)

        self.horizontalLayout.addWidget(self.lineEdit_own_balance)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_3 = QLabel(self.layoutWidget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMinimumSize(QSize(150, 0))
        self.label_3.setFont(font2)

        self.horizontalLayout_2.addWidget(self.label_3)

        self.lineEdit_other_balance = QLineEdit(self.layoutWidget)
        self.lineEdit_other_balance.setObjectName(u"lineEdit_other_balance")
        self.lineEdit_other_balance.setFont(font2)
        self.lineEdit_other_balance.setReadOnly(True)

        self.horizontalLayout_2.addWidget(self.lineEdit_other_balance)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 22))
        self.menuStart = QMenu(self.menubar)
        self.menuStart.setObjectName(u"menuStart")
        self.menuProfile = QMenu(self.menubar)
        self.menuProfile.setObjectName(u"menuProfile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuStart.menuAction())
        self.menubar.addAction(self.menuProfile.menuAction())
        self.menuStart.addAction(self.actionClose)
        self.menuProfile.addAction(self.actionCreateProfile)
        self.menuProfile.addAction(self.actionEditProfile)
        self.menuProfile.addAction(self.actionProfileLogin)
        self.menuProfile.addAction(self.actionProfileLogout)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionProfile.setText(QCoreApplication.translate("MainWindow", u"Profil", None))
        self.actionClose.setText(QCoreApplication.translate("MainWindow", u"Beenden", None))
        self.actionEditProfile.setText(QCoreApplication.translate("MainWindow", u"Profil bearbeiten", None))
        self.actionProfileLogin.setText(QCoreApplication.translate("MainWindow", u"Einloggen", None))
        self.actionProfileLogout.setText(QCoreApplication.translate("MainWindow", u"Ausloggen", None))
        self.actionCreateProfile.setText(QCoreApplication.translate("MainWindow", u"Profil erstellen", None))
        self.label_username.setText("")
        self.label.setText(QCoreApplication.translate("MainWindow", u"Kontostand", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"eigene Minuto", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"andere Minuto", None))
        self.menuStart.setTitle(QCoreApplication.translate("MainWindow", u"Start", None))
        self.menuProfile.setTitle(QCoreApplication.translate("MainWindow", u"Profil", None))
    # retranslateUi

