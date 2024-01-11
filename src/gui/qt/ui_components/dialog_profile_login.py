# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dialog_profile_login.ui'
##
## Created by: Qt User Interface Compiler version 6.6.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QDialog, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QWidget)

class Ui_DialogProfileLogin(object):
    def setupUi(self, DialogProfileLogin):
        if not DialogProfileLogin.objectName():
            DialogProfileLogin.setObjectName(u"DialogProfileLogin")
        DialogProfileLogin.resize(269, 128)
        DialogProfileLogin.setLayoutDirection(Qt.RightToLeft)
        self.lineEdit_entered_password = QLineEdit(DialogProfileLogin)
        self.lineEdit_entered_password.setObjectName(u"lineEdit_entered_password")
        self.lineEdit_entered_password.setGeometry(QRect(30, 40, 211, 26))
        font = QFont()
        font.setPointSize(11)
        self.lineEdit_entered_password.setFont(font)
        self.lineEdit_entered_password.setLayoutDirection(Qt.LeftToRight)
        self.lineEdit_entered_password.setEchoMode(QLineEdit.Password)
        self.label_enter_password = QLabel(DialogProfileLogin)
        self.label_enter_password.setObjectName(u"label_enter_password")
        self.label_enter_password.setGeometry(QRect(10, 10, 251, 20))
        self.label_enter_password.setFont(font)
        self.label_enter_password.setLayoutDirection(Qt.LeftToRight)
        self.label_enter_password.setLineWidth(-1)
        self.label_enter_password.setAlignment(Qt.AlignCenter)
        self.pushButton_OK = QPushButton(DialogProfileLogin)
        self.pushButton_OK.setObjectName(u"pushButton_OK")
        self.pushButton_OK.setGeometry(QRect(90, 70, 91, 23))
        self.pushButton_OK.setFont(font)
        self.pushButton_OK.setLayoutDirection(Qt.LeftToRight)
        self.label_status = QLabel(DialogProfileLogin)
        self.label_status.setObjectName(u"label_status")
        self.label_status.setGeometry(QRect(7, 100, 251, 20))
        self.label_status.setFont(font)
        self.label_status.setAlignment(Qt.AlignCenter)

        self.retranslateUi(DialogProfileLogin)

        QMetaObject.connectSlotsByName(DialogProfileLogin)
    # setupUi

    def retranslateUi(self, DialogProfileLogin):
        DialogProfileLogin.setWindowTitle(QCoreApplication.translate("DialogProfileLogin", u"Einloggen", None))
        self.label_enter_password.setText(QCoreApplication.translate("DialogProfileLogin", u"Passwort eingeben:", None))
        self.pushButton_OK.setText(QCoreApplication.translate("DialogProfileLogin", u"OK", None))
        self.label_status.setText("")
    # retranslateUi

