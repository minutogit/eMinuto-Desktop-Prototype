# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dialog_enter_password.ui'
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

class Ui_DialogEnterPassword(object):
    def setupUi(self, DialogEnterPassword):
        if not DialogEnterPassword.objectName():
            DialogEnterPassword.setObjectName(u"DialogEnterPassword")
        DialogEnterPassword.resize(269, 102)
        DialogEnterPassword.setLayoutDirection(Qt.RightToLeft)
        self.lineEdit_entered_password = QLineEdit(DialogEnterPassword)
        self.lineEdit_entered_password.setObjectName(u"lineEdit_entered_password")
        self.lineEdit_entered_password.setGeometry(QRect(50, 40, 171, 23))
        self.lineEdit_entered_password.setLayoutDirection(Qt.LeftToRight)
        self.lineEdit_entered_password.setEchoMode(QLineEdit.Password)
        self.label_enter_password = QLabel(DialogEnterPassword)
        self.label_enter_password.setObjectName(u"label_enter_password")
        self.label_enter_password.setGeometry(QRect(10, 10, 251, 20))
        self.label_enter_password.setLayoutDirection(Qt.LeftToRight)
        self.label_enter_password.setLineWidth(-1)
        self.label_enter_password.setAlignment(Qt.AlignCenter)
        self.pushButton_OK = QPushButton(DialogEnterPassword)
        self.pushButton_OK.setObjectName(u"pushButton_OK")
        self.pushButton_OK.setGeometry(QRect(100, 70, 81, 23))
        self.pushButton_OK.setLayoutDirection(Qt.LeftToRight)

        self.retranslateUi(DialogEnterPassword)

        QMetaObject.connectSlotsByName(DialogEnterPassword)
    # setupUi

    def retranslateUi(self, DialogEnterPassword):
        DialogEnterPassword.setWindowTitle(QCoreApplication.translate("DialogEnterPassword", u"Enter password", None))
        self.label_enter_password.setText(QCoreApplication.translate("DialogEnterPassword", u"Enter password:", None))
        self.pushButton_OK.setText(QCoreApplication.translate("DialogEnterPassword", u"OK", None))
    # retranslateUi

