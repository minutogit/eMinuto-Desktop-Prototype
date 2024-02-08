# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dialog_forgot_password.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QSizePolicy, QVBoxLayout,
    QWidget)

class Ui_DialogForgotPassword(object):
    def setupUi(self, DialogForgotPassword):
        if not DialogForgotPassword.objectName():
            DialogForgotPassword.setObjectName(u"DialogForgotPassword")
        DialogForgotPassword.resize(582, 264)
        DialogForgotPassword.setLayoutDirection(Qt.RightToLeft)
        self.widget = QWidget(DialogForgotPassword)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(10, 19, 551, 201))
        self.verticalLayout = QVBoxLayout(self.widget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.label_3 = QLabel(self.widget)
        self.label_3.setObjectName(u"label_3")
        font = QFont()
        font.setPointSize(11)
        self.label_3.setFont(font)

        self.verticalLayout.addWidget(self.label_3)

        self.lineEdit_seed_words = QLineEdit(self.widget)
        self.lineEdit_seed_words.setObjectName(u"lineEdit_seed_words")

        self.verticalLayout.addWidget(self.lineEdit_seed_words)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.lineEdit_new_password = QLineEdit(self.widget)
        self.lineEdit_new_password.setObjectName(u"lineEdit_new_password")
        self.lineEdit_new_password.setEchoMode(QLineEdit.Password)

        self.horizontalLayout.addWidget(self.lineEdit_new_password)

        self.label = QLabel(self.widget)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(180, 0))
        self.label.setFont(font)
        self.label.setLayoutDirection(Qt.RightToLeft)
        self.label.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout.addWidget(self.label)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.lineEdit_new_password_retyped = QLineEdit(self.widget)
        self.lineEdit_new_password_retyped.setObjectName(u"lineEdit_new_password_retyped")
        self.lineEdit_new_password_retyped.setEchoMode(QLineEdit.Password)

        self.horizontalLayout_2.addWidget(self.lineEdit_new_password_retyped)

        self.label_2 = QLabel(self.widget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(180, 0))
        self.label_2.setFont(font)
        self.label_2.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_2.addWidget(self.label_2)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.pushButton_save_new_password = QPushButton(self.widget)
        self.pushButton_save_new_password.setObjectName(u"pushButton_save_new_password")
        self.pushButton_save_new_password.setFont(font)

        self.verticalLayout.addWidget(self.pushButton_save_new_password)


        self.retranslateUi(DialogForgotPassword)

        QMetaObject.connectSlotsByName(DialogForgotPassword)
    # setupUi

    def retranslateUi(self, DialogForgotPassword):
        DialogForgotPassword.setWindowTitle(QCoreApplication.translate("DialogForgotPassword", u"Neues Passwort eingeben", None))
        self.label_3.setText(QCoreApplication.translate("DialogForgotPassword", u"Schl\u00fcsselw\u00f6rter", None))
        self.label.setText(QCoreApplication.translate("DialogForgotPassword", u"Neues Passwort:", None))
        self.label_2.setText(QCoreApplication.translate("DialogForgotPassword", u"Passwort wiederholen:", None))
        self.pushButton_save_new_password.setText(QCoreApplication.translate("DialogForgotPassword", u"Neues Passwort speichern", None))
    # retranslateUi

