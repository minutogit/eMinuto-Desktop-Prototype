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
    QPushButton, QSizePolicy, QSpacerItem, QStatusBar,
    QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(624, 415)
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
        self.actionCreateMinuto = QAction(MainWindow)
        self.actionCreateMinuto.setObjectName(u"actionCreateMinuto")
        self.actionVoucherList = QAction(MainWindow)
        self.actionVoucherList.setObjectName(u"actionVoucherList")
        self.actionOpenFile = QAction(MainWindow)
        self.actionOpenFile.setObjectName(u"actionOpenFile")
        self.actionTransactions = QAction(MainWindow)
        self.actionTransactions.setObjectName(u"actionTransactions")
        self.actionEnglish = QAction(MainWindow)
        self.actionEnglish.setObjectName(u"actionEnglish")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.layoutWidget = QWidget(self.centralwidget)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(10, 10, 591, 351))
        self.verticalLayout_2 = QVBoxLayout(self.layoutWidget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_username = QLabel(self.layoutWidget)
        self.label_username.setObjectName(u"label_username")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_username.sizePolicy().hasHeightForWidth())
        self.label_username.setSizePolicy(sizePolicy)
        font = QFont()
        font.setPointSize(14)
        font.setBold(True)
        self.label_username.setFont(font)

        self.horizontalLayout_3.addWidget(self.label_username)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer)

        self.label_user_id_text = QLabel(self.layoutWidget)
        self.label_user_id_text.setObjectName(u"label_user_id_text")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.label_user_id_text.sizePolicy().hasHeightForWidth())
        self.label_user_id_text.setSizePolicy(sizePolicy1)
        self.label_user_id_text.setFont(font)

        self.horizontalLayout_3.addWidget(self.label_user_id_text)

        self.lineEdit_user_id = QLineEdit(self.layoutWidget)
        self.lineEdit_user_id.setObjectName(u"lineEdit_user_id")
        self.lineEdit_user_id.setMaximumSize(QSize(150, 16777215))
        self.lineEdit_user_id.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.lineEdit_user_id.setReadOnly(True)

        self.horizontalLayout_3.addWidget(self.lineEdit_user_id)

        self.pushButton_copy_user_ID = QPushButton(self.layoutWidget)
        self.pushButton_copy_user_ID.setObjectName(u"pushButton_copy_user_ID")
        icon = QIcon()
        icon.addFile(u".", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButton_copy_user_ID.setIcon(icon)
        self.pushButton_copy_user_ID.setIconSize(QSize(18, 18))

        self.horizontalLayout_3.addWidget(self.pushButton_copy_user_ID)


        self.verticalLayout_2.addLayout(self.horizontalLayout_3)

        self.frame = QFrame(self.layoutWidget)
        self.frame.setObjectName(u"frame")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy2)
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.layoutWidget1 = QWidget(self.frame)
        self.layoutWidget1.setObjectName(u"layoutWidget1")
        self.layoutWidget1.setGeometry(QRect(10, 10, 471, 285))
        self.verticalLayout = QVBoxLayout(self.layoutWidget1)
        self.verticalLayout.setSpacing(12)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(self.layoutWidget1)
        self.label.setObjectName(u"label")
        font1 = QFont()
        font1.setPointSize(14)
        font1.setBold(True)
        font1.setItalic(False)
        self.label.setFont(font1)

        self.verticalLayout.addWidget(self.label)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_2 = QLabel(self.layoutWidget1)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(150, 0))
        font2 = QFont()
        font2.setPointSize(11)
        self.label_2.setFont(font2)

        self.horizontalLayout.addWidget(self.label_2)

        self.lineEdit_own_balance = QLineEdit(self.layoutWidget1)
        self.lineEdit_own_balance.setObjectName(u"lineEdit_own_balance")
        self.lineEdit_own_balance.setFont(font2)
        self.lineEdit_own_balance.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.lineEdit_own_balance.setReadOnly(True)

        self.horizontalLayout.addWidget(self.lineEdit_own_balance)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_3 = QLabel(self.layoutWidget1)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMinimumSize(QSize(150, 0))
        self.label_3.setFont(font2)

        self.horizontalLayout_2.addWidget(self.label_3)

        self.lineEdit_other_balance = QLineEdit(self.layoutWidget1)
        self.lineEdit_other_balance.setObjectName(u"lineEdit_other_balance")
        self.lineEdit_other_balance.setFont(font2)
        self.lineEdit_other_balance.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.lineEdit_other_balance.setReadOnly(True)

        self.horizontalLayout_2.addWidget(self.lineEdit_other_balance)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.pushButton_send_minuto = QPushButton(self.layoutWidget1)
        self.pushButton_send_minuto.setObjectName(u"pushButton_send_minuto")

        self.verticalLayout.addWidget(self.pushButton_send_minuto)

        self.pushButton_receive_minuto = QPushButton(self.layoutWidget1)
        self.pushButton_receive_minuto.setObjectName(u"pushButton_receive_minuto")

        self.verticalLayout.addWidget(self.pushButton_receive_minuto)

        self.line = QFrame(self.layoutWidget1)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.line)

        self.pushButton_show_transactions = QPushButton(self.layoutWidget1)
        self.pushButton_show_transactions.setObjectName(u"pushButton_show_transactions")

        self.verticalLayout.addWidget(self.pushButton_show_transactions)

        self.pushButton_show_vouchers = QPushButton(self.layoutWidget1)
        self.pushButton_show_vouchers.setObjectName(u"pushButton_show_vouchers")

        self.verticalLayout.addWidget(self.pushButton_show_vouchers)


        self.verticalLayout_2.addWidget(self.frame)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 624, 22))
        self.menuStart = QMenu(self.menubar)
        self.menuStart.setObjectName(u"menuStart")
        self.menuLanguage = QMenu(self.menuStart)
        self.menuLanguage.setObjectName(u"menuLanguage")
        self.menuProfile = QMenu(self.menubar)
        self.menuProfile.setObjectName(u"menuProfile")
        self.menuMinuto = QMenu(self.menubar)
        self.menuMinuto.setObjectName(u"menuMinuto")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuStart.menuAction())
        self.menubar.addAction(self.menuMinuto.menuAction())
        self.menubar.addAction(self.menuProfile.menuAction())
        self.menuStart.addAction(self.actionOpenFile)
        self.menuStart.addAction(self.menuLanguage.menuAction())
        self.menuStart.addAction(self.actionClose)
        self.menuProfile.addAction(self.actionCreateProfile)
        self.menuProfile.addAction(self.actionEditProfile)
        self.menuProfile.addAction(self.actionProfileLogin)
        self.menuProfile.addAction(self.actionProfileLogout)
        self.menuMinuto.addAction(self.actionCreateMinuto)
        self.menuMinuto.addAction(self.actionVoucherList)
        self.menuMinuto.addAction(self.actionTransactions)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionProfile.setText(QCoreApplication.translate("MainWindow", u"Profile", None))
        self.actionClose.setText(QCoreApplication.translate("MainWindow", u"Exit", None))
        self.actionEditProfile.setText(QCoreApplication.translate("MainWindow", u"Edit Profile", None))
        self.actionProfileLogin.setText(QCoreApplication.translate("MainWindow", u"Log in", None))
        self.actionProfileLogout.setText(QCoreApplication.translate("MainWindow", u"Log out", None))
        self.actionCreateProfile.setText(QCoreApplication.translate("MainWindow", u"Create Profile", None))
        self.actionCreateMinuto.setText(QCoreApplication.translate("MainWindow", u"Create Minuto", None))
        self.actionVoucherList.setText(QCoreApplication.translate("MainWindow", u"Voucher List", None))
        self.actionOpenFile.setText(QCoreApplication.translate("MainWindow", u"Open File", None))
        self.actionTransactions.setText(QCoreApplication.translate("MainWindow", u"Transactions", None))
        self.actionEnglish.setText(QCoreApplication.translate("MainWindow", u"English", None))
        self.label_username.setText("")
        self.label_user_id_text.setText(QCoreApplication.translate("MainWindow", u"ID:", None))
#if QT_CONFIG(tooltip)
        self.pushButton_copy_user_ID.setToolTip(QCoreApplication.translate("MainWindow", u"Copy", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_copy_user_ID.setText(QCoreApplication.translate("MainWindow", u"Copy ID", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Account Balance", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Own Minuto", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Other Minuto", None))
        self.pushButton_send_minuto.setText(QCoreApplication.translate("MainWindow", u"Send Minuto", None))
        self.pushButton_receive_minuto.setText(QCoreApplication.translate("MainWindow", u"Receive Minuto", None))
        self.pushButton_show_transactions.setText(QCoreApplication.translate("MainWindow", u"View Transactions", None))
        self.pushButton_show_vouchers.setText(QCoreApplication.translate("MainWindow", u"View Vouchers", None))
        self.menuStart.setTitle(QCoreApplication.translate("MainWindow", u"Start", None))
        self.menuLanguage.setTitle(QCoreApplication.translate("MainWindow", u"Language", None))
        self.menuProfile.setTitle(QCoreApplication.translate("MainWindow", u"Profile", None))
        self.menuMinuto.setTitle(QCoreApplication.translate("MainWindow", u"Minuto", None))
    # retranslateUi

