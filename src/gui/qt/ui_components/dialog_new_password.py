# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dialog_new_password.ui'
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

class Ui_DialogNewPassword(object):
    def setupUi(self, DialogNewPassword):
        if not DialogNewPassword.objectName():
            DialogNewPassword.setObjectName(u"DialogNewPassword")
        DialogNewPassword.resize(383, 133)
        DialogNewPassword.setLayoutDirection(Qt.RightToLeft)
        self.lineEdit_new_password = QLineEdit(DialogNewPassword)
        self.lineEdit_new_password.setObjectName(u"lineEdit_new_password")
        self.lineEdit_new_password.setGeometry(QRect(160, 20, 181, 23))
        self.lineEdit_new_password.setEchoMode(QLineEdit.Password)
        self.lineEdit_new_password_retyped = QLineEdit(DialogNewPassword)
        self.lineEdit_new_password_retyped.setObjectName(u"lineEdit_new_password_retyped")
        self.lineEdit_new_password_retyped.setGeometry(QRect(160, 60, 181, 23))
        self.lineEdit_new_password_retyped.setEchoMode(QLineEdit.Password)
        self.label = QLabel(DialogNewPassword)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(30, 20, 121, 20))
        self.label.setLayoutDirection(Qt.RightToLeft)
        self.label.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.label_2 = QLabel(DialogNewPassword)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(10, 60, 141, 20))
        self.label_2.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.pushButton_save_password = QPushButton(DialogNewPassword)
        self.pushButton_save_password.setObjectName(u"pushButton_save_password")
        self.pushButton_save_password.setGeometry(QRect(90, 100, 151, 23))

        self.retranslateUi(DialogNewPassword)

        QMetaObject.connectSlotsByName(DialogNewPassword)
    # setupUi

    def retranslateUi(self, DialogNewPassword):
        DialogNewPassword.setWindowTitle(QCoreApplication.translate("DialogNewPassword", u"Neues Passwort eingeben", None))
        self.label.setText(QCoreApplication.translate("DialogNewPassword", u"Neues Passwort:", None))
        self.label_2.setText(QCoreApplication.translate("DialogNewPassword", u"Passwort wiederholen:", None))
        self.pushButton_save_password.setText(QCoreApplication.translate("DialogNewPassword", u"Passwort speichern", None))
    # retranslateUi

