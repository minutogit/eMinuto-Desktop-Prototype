# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dialog_profile.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QTextEdit, QVBoxLayout,
    QWidget)

class Ui_Form_Profile(object):
    def setupUi(self, Form_Profile):
        if not Form_Profile.objectName():
            Form_Profile.setObjectName(u"Form_Profile")
        Form_Profile.resize(581, 569)
        self.layoutWidget = QWidget(Form_Profile)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(20, 60, 521, 32))
        self.layoutWidget.setMinimumSize(QSize(120, 25))
        font = QFont()
        font.setPointSize(11)
        self.layoutWidget.setFont(font)
        self.hboxLayout = QHBoxLayout(self.layoutWidget)
        self.hboxLayout.setObjectName(u"hboxLayout")
        self.hboxLayout.setContentsMargins(0, 0, 0, 0)
        self.label_first_name = QLabel(self.layoutWidget)
        self.label_first_name.setObjectName(u"label_first_name")
        self.label_first_name.setMinimumSize(QSize(120, 22))
        self.label_first_name.setFont(font)

        self.hboxLayout.addWidget(self.label_first_name)

        self.lineEdit_first_name = QLineEdit(self.layoutWidget)
        self.lineEdit_first_name.setObjectName(u"lineEdit_first_name")
        self.lineEdit_first_name.setMinimumSize(QSize(0, 25))

        self.hboxLayout.addWidget(self.lineEdit_first_name)

        self.layoutWidget1 = QWidget(Form_Profile)
        self.layoutWidget1.setObjectName(u"layoutWidget1")
        self.layoutWidget1.setGeometry(QRect(20, 100, 521, 32))
        self.layoutWidget1.setMinimumSize(QSize(120, 25))
        self.layoutWidget1.setFont(font)
        self.hboxLayout1 = QHBoxLayout(self.layoutWidget1)
        self.hboxLayout1.setObjectName(u"hboxLayout1")
        self.hboxLayout1.setContentsMargins(0, 0, 0, 0)
        self.label_last_name = QLabel(self.layoutWidget1)
        self.label_last_name.setObjectName(u"label_last_name")
        self.label_last_name.setMinimumSize(QSize(120, 22))
        self.label_last_name.setFont(font)

        self.hboxLayout1.addWidget(self.label_last_name)

        self.lineEdit_last_name = QLineEdit(self.layoutWidget1)
        self.lineEdit_last_name.setObjectName(u"lineEdit_last_name")
        self.lineEdit_last_name.setMinimumSize(QSize(0, 25))

        self.hboxLayout1.addWidget(self.lineEdit_last_name)

        self.layoutWidget2 = QWidget(Form_Profile)
        self.layoutWidget2.setObjectName(u"layoutWidget2")
        self.layoutWidget2.setGeometry(QRect(20, 140, 521, 32))
        self.layoutWidget2.setMinimumSize(QSize(120, 25))
        self.layoutWidget2.setFont(font)
        self.hboxLayout2 = QHBoxLayout(self.layoutWidget2)
        self.hboxLayout2.setObjectName(u"hboxLayout2")
        self.hboxLayout2.setContentsMargins(0, 0, 0, 0)
        self.label_organization = QLabel(self.layoutWidget2)
        self.label_organization.setObjectName(u"label_organization")
        self.label_organization.setMinimumSize(QSize(120, 22))
        self.label_organization.setFont(font)

        self.hboxLayout2.addWidget(self.label_organization)

        self.lineEdit_organization = QLineEdit(self.layoutWidget2)
        self.lineEdit_organization.setObjectName(u"lineEdit_organization")
        self.lineEdit_organization.setMinimumSize(QSize(0, 25))

        self.hboxLayout2.addWidget(self.lineEdit_organization)

        self.layoutWidget3 = QWidget(Form_Profile)
        self.layoutWidget3.setObjectName(u"layoutWidget3")
        self.layoutWidget3.setGeometry(QRect(20, 180, 521, 32))
        self.layoutWidget3.setMinimumSize(QSize(120, 25))
        self.layoutWidget3.setFont(font)
        self.hboxLayout3 = QHBoxLayout(self.layoutWidget3)
        self.hboxLayout3.setObjectName(u"hboxLayout3")
        self.hboxLayout3.setContentsMargins(0, 0, 0, 0)
        self.label_address = QLabel(self.layoutWidget3)
        self.label_address.setObjectName(u"label_address")
        self.label_address.setMinimumSize(QSize(120, 22))
        self.label_address.setFont(font)

        self.hboxLayout3.addWidget(self.label_address)

        self.lineEdit_address = QLineEdit(self.layoutWidget3)
        self.lineEdit_address.setObjectName(u"lineEdit_address")
        self.lineEdit_address.setMinimumSize(QSize(0, 25))

        self.hboxLayout3.addWidget(self.lineEdit_address)

        self.layoutWidget4 = QWidget(Form_Profile)
        self.layoutWidget4.setObjectName(u"layoutWidget4")
        self.layoutWidget4.setGeometry(QRect(20, 220, 521, 32))
        self.layoutWidget4.setMinimumSize(QSize(120, 25))
        self.layoutWidget4.setFont(font)
        self.hboxLayout4 = QHBoxLayout(self.layoutWidget4)
        self.hboxLayout4.setObjectName(u"hboxLayout4")
        self.hboxLayout4.setContentsMargins(0, 0, 0, 0)
        self.label_email = QLabel(self.layoutWidget4)
        self.label_email.setObjectName(u"label_email")
        self.label_email.setMinimumSize(QSize(120, 22))
        self.label_email.setFont(font)

        self.hboxLayout4.addWidget(self.label_email)

        self.lineEdit_email = QLineEdit(self.layoutWidget4)
        self.lineEdit_email.setObjectName(u"lineEdit_email")
        self.lineEdit_email.setMinimumSize(QSize(0, 25))

        self.hboxLayout4.addWidget(self.lineEdit_email)

        self.layoutWidget5 = QWidget(Form_Profile)
        self.layoutWidget5.setObjectName(u"layoutWidget5")
        self.layoutWidget5.setGeometry(QRect(20, 261, 521, 31))
        self.layoutWidget5.setMinimumSize(QSize(120, 25))
        self.layoutWidget5.setFont(font)
        self.hboxLayout5 = QHBoxLayout(self.layoutWidget5)
        self.hboxLayout5.setObjectName(u"hboxLayout5")
        self.hboxLayout5.setContentsMargins(0, 0, 0, 0)
        self.label_phone = QLabel(self.layoutWidget5)
        self.label_phone.setObjectName(u"label_phone")
        self.label_phone.setMinimumSize(QSize(120, 22))
        self.label_phone.setFont(font)

        self.hboxLayout5.addWidget(self.label_phone)

        self.lineEdit_phone = QLineEdit(self.layoutWidget5)
        self.lineEdit_phone.setObjectName(u"lineEdit_phone")
        self.lineEdit_phone.setMinimumSize(QSize(0, 25))

        self.hboxLayout5.addWidget(self.lineEdit_phone)

        self.layoutWidget6 = QWidget(Form_Profile)
        self.layoutWidget6.setObjectName(u"layoutWidget6")
        self.layoutWidget6.setGeometry(QRect(20, 300, 521, 32))
        self.layoutWidget6.setMinimumSize(QSize(120, 25))
        self.layoutWidget6.setFont(font)
        self.hboxLayout6 = QHBoxLayout(self.layoutWidget6)
        self.hboxLayout6.setObjectName(u"hboxLayout6")
        self.hboxLayout6.setContentsMargins(0, 0, 0, 0)
        self.label_coordinates = QLabel(self.layoutWidget6)
        self.label_coordinates.setObjectName(u"label_coordinates")
        self.label_coordinates.setMinimumSize(QSize(120, 22))
        self.label_coordinates.setFont(font)

        self.hboxLayout6.addWidget(self.label_coordinates)

        self.lineEdit_coordinates = QLineEdit(self.layoutWidget6)
        self.lineEdit_coordinates.setObjectName(u"lineEdit_coordinates")
        self.lineEdit_coordinates.setMinimumSize(QSize(0, 25))

        self.hboxLayout6.addWidget(self.lineEdit_coordinates)

        self.layoutWidget_2 = QWidget(Form_Profile)
        self.layoutWidget_2.setObjectName(u"layoutWidget_2")
        self.layoutWidget_2.setGeometry(QRect(20, 10, 521, 32))
        self.layoutWidget_2.setMinimumSize(QSize(120, 25))
        self.layoutWidget_2.setFont(font)
        self._2 = QHBoxLayout(self.layoutWidget_2)
        self._2.setObjectName(u"_2")
        self._2.setContentsMargins(0, 0, 0, 0)
        self.label_profile_name = QLabel(self.layoutWidget_2)
        self.label_profile_name.setObjectName(u"label_profile_name")
        self.label_profile_name.setMinimumSize(QSize(120, 22))
        self.label_profile_name.setFont(font)

        self._2.addWidget(self.label_profile_name)

        self.lineEdit_profile_name = QLineEdit(self.layoutWidget_2)
        self.lineEdit_profile_name.setObjectName(u"lineEdit_profile_name")
        self.lineEdit_profile_name.setMinimumSize(QSize(0, 25))

        self._2.addWidget(self.lineEdit_profile_name)

        self.widget = QWidget(Form_Profile)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(20, 340, 521, 141))
        self.verticalLayout = QVBoxLayout(self.widget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.label_service_offer = QLabel(self.widget)
        self.label_service_offer.setObjectName(u"label_service_offer")
        self.label_service_offer.setMinimumSize(QSize(100, 0))
        self.label_service_offer.setFont(font)

        self.verticalLayout.addWidget(self.label_service_offer)

        self.textEdit_service_offer = QTextEdit(self.widget)
        self.textEdit_service_offer.setObjectName(u"textEdit_service_offer")
        self.textEdit_service_offer.setFont(font)

        self.verticalLayout.addWidget(self.textEdit_service_offer)

        self.widget1 = QWidget(Form_Profile)
        self.widget1.setObjectName(u"widget1")
        self.widget1.setGeometry(QRect(20, 510, 521, 28))
        self.horizontalLayout = QHBoxLayout(self.widget1)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.pushButton_save = QPushButton(self.widget1)
        self.pushButton_save.setObjectName(u"pushButton_save")
        self.pushButton_save.setFont(font)
        icon = QIcon(QIcon.fromTheme(u"media-floppy"))
        self.pushButton_save.setIcon(icon)
        self.pushButton_save.setIconSize(QSize(20, 20))

        self.horizontalLayout.addWidget(self.pushButton_save)

        self.pushButton_close = QPushButton(self.widget1)
        self.pushButton_close.setObjectName(u"pushButton_close")
        self.pushButton_close.setFont(font)
        icon1 = QIcon(QIcon.fromTheme(u"window-close"))
        self.pushButton_close.setIcon(icon1)
        self.pushButton_close.setIconSize(QSize(20, 20))

        self.horizontalLayout.addWidget(self.pushButton_close)


        self.retranslateUi(Form_Profile)

        QMetaObject.connectSlotsByName(Form_Profile)
    # setupUi

    def retranslateUi(self, Form_Profile):
        Form_Profile.setWindowTitle(QCoreApplication.translate("Form_Profile", u"Profil", None))
        self.label_first_name.setText(QCoreApplication.translate("Form_Profile", u"Vorname", None))
        self.label_last_name.setText(QCoreApplication.translate("Form_Profile", u"Nachname", None))
        self.label_organization.setText(QCoreApplication.translate("Form_Profile", u"Organisation", None))
        self.label_address.setText(QCoreApplication.translate("Form_Profile", u"Adresse", None))
        self.label_email.setText(QCoreApplication.translate("Form_Profile", u"E-Mail", None))
        self.label_phone.setText(QCoreApplication.translate("Form_Profile", u"Telefon", None))
        self.label_coordinates.setText(QCoreApplication.translate("Form_Profile", u"Koordinaten", None))
        self.lineEdit_coordinates.setText("")
        self.label_profile_name.setText(QCoreApplication.translate("Form_Profile", u"Profilname", None))
        self.label_service_offer.setText(QCoreApplication.translate("Form_Profile", u"Dienstleistungsangebot", None))
        self.textEdit_service_offer.setHtml(QCoreApplication.translate("Form_Profile", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Ubuntu'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None))
        self.pushButton_save.setText(QCoreApplication.translate("Form_Profile", u"Speichern", None))
        self.pushButton_close.setText(QCoreApplication.translate("Form_Profile", u"Schlie\u00dfen", None))
    # retranslateUi

