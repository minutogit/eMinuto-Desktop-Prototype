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
from PySide6.QtWidgets import (QApplication, QComboBox, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QSizePolicy, QTextEdit,
    QVBoxLayout, QWidget)

class Ui_Form_Profile(object):
    def setupUi(self, Form_Profile):
        if not Form_Profile.objectName():
            Form_Profile.setObjectName(u"Form_Profile")
        Form_Profile.resize(590, 688)
        self.layoutWidget = QWidget(Form_Profile)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(20, 100, 521, 32))
        self.layoutWidget.setMinimumSize(QSize(120, 25))
        font = QFont()
        font.setPointSize(11)
        self.layoutWidget.setFont(font)
        self.hboxLayout = QHBoxLayout(self.layoutWidget)
        self.hboxLayout.setObjectName(u"hboxLayout")
        self.hboxLayout.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(self.layoutWidget)
        self.label.setObjectName(u"label")

        self.hboxLayout.addWidget(self.label)

        self.lineEdit_first_name = QLineEdit(self.layoutWidget)
        self.lineEdit_first_name.setObjectName(u"lineEdit_first_name")
        self.lineEdit_first_name.setMinimumSize(QSize(0, 25))

        self.hboxLayout.addWidget(self.lineEdit_first_name)

        self.lineEdit_last_name = QLineEdit(self.layoutWidget)
        self.lineEdit_last_name.setObjectName(u"lineEdit_last_name")
        self.lineEdit_last_name.setMinimumSize(QSize(0, 25))

        self.hboxLayout.addWidget(self.lineEdit_last_name)

        self.layoutWidget1 = QWidget(Form_Profile)
        self.layoutWidget1.setObjectName(u"layoutWidget1")
        self.layoutWidget1.setGeometry(QRect(20, 60, 521, 32))
        self.layoutWidget1.setMinimumSize(QSize(120, 25))
        self.layoutWidget1.setFont(font)
        self.hboxLayout1 = QHBoxLayout(self.layoutWidget1)
        self.hboxLayout1.setObjectName(u"hboxLayout1")
        self.hboxLayout1.setContentsMargins(0, 0, 0, 0)
        self.label_organization = QLabel(self.layoutWidget1)
        self.label_organization.setObjectName(u"label_organization")
        self.label_organization.setMinimumSize(QSize(120, 22))
        self.label_organization.setFont(font)

        self.hboxLayout1.addWidget(self.label_organization)

        self.lineEdit_organization = QLineEdit(self.layoutWidget1)
        self.lineEdit_organization.setObjectName(u"lineEdit_organization")
        self.lineEdit_organization.setMinimumSize(QSize(0, 25))

        self.hboxLayout1.addWidget(self.lineEdit_organization)

        self.layoutWidget2 = QWidget(Form_Profile)
        self.layoutWidget2.setObjectName(u"layoutWidget2")
        self.layoutWidget2.setGeometry(QRect(20, 180, 521, 32))
        self.layoutWidget2.setMinimumSize(QSize(120, 25))
        self.layoutWidget2.setFont(font)
        self.hboxLayout2 = QHBoxLayout(self.layoutWidget2)
        self.hboxLayout2.setObjectName(u"hboxLayout2")
        self.hboxLayout2.setContentsMargins(0, 0, 0, 0)
        self.label_street = QLabel(self.layoutWidget2)
        self.label_street.setObjectName(u"label_street")
        self.label_street.setMinimumSize(QSize(120, 22))
        self.label_street.setFont(font)

        self.hboxLayout2.addWidget(self.label_street)

        self.lineEdit_street = QLineEdit(self.layoutWidget2)
        self.lineEdit_street.setObjectName(u"lineEdit_street")
        self.lineEdit_street.setMinimumSize(QSize(0, 25))

        self.hboxLayout2.addWidget(self.lineEdit_street)

        self.layoutWidget3 = QWidget(Form_Profile)
        self.layoutWidget3.setObjectName(u"layoutWidget3")
        self.layoutWidget3.setGeometry(QRect(20, 339, 521, 32))
        self.layoutWidget3.setMinimumSize(QSize(120, 25))
        self.layoutWidget3.setFont(font)
        self.hboxLayout3 = QHBoxLayout(self.layoutWidget3)
        self.hboxLayout3.setObjectName(u"hboxLayout3")
        self.hboxLayout3.setContentsMargins(0, 0, 0, 0)
        self.label_email = QLabel(self.layoutWidget3)
        self.label_email.setObjectName(u"label_email")
        self.label_email.setMinimumSize(QSize(120, 22))
        self.label_email.setFont(font)

        self.hboxLayout3.addWidget(self.label_email)

        self.lineEdit_email = QLineEdit(self.layoutWidget3)
        self.lineEdit_email.setObjectName(u"lineEdit_email")
        self.lineEdit_email.setMinimumSize(QSize(0, 25))

        self.hboxLayout3.addWidget(self.lineEdit_email)

        self.layoutWidget4 = QWidget(Form_Profile)
        self.layoutWidget4.setObjectName(u"layoutWidget4")
        self.layoutWidget4.setGeometry(QRect(20, 380, 521, 31))
        self.layoutWidget4.setMinimumSize(QSize(120, 25))
        self.layoutWidget4.setFont(font)
        self.hboxLayout4 = QHBoxLayout(self.layoutWidget4)
        self.hboxLayout4.setObjectName(u"hboxLayout4")
        self.hboxLayout4.setContentsMargins(0, 0, 0, 0)
        self.label_phone = QLabel(self.layoutWidget4)
        self.label_phone.setObjectName(u"label_phone")
        self.label_phone.setMinimumSize(QSize(120, 22))
        self.label_phone.setFont(font)

        self.hboxLayout4.addWidget(self.label_phone)

        self.lineEdit_phone = QLineEdit(self.layoutWidget4)
        self.lineEdit_phone.setObjectName(u"lineEdit_phone")
        self.lineEdit_phone.setMinimumSize(QSize(0, 25))

        self.hboxLayout4.addWidget(self.lineEdit_phone)

        self.layoutWidget5 = QWidget(Form_Profile)
        self.layoutWidget5.setObjectName(u"layoutWidget5")
        self.layoutWidget5.setGeometry(QRect(20, 419, 521, 32))
        self.layoutWidget5.setMinimumSize(QSize(120, 25))
        self.layoutWidget5.setFont(font)
        self.hboxLayout5 = QHBoxLayout(self.layoutWidget5)
        self.hboxLayout5.setObjectName(u"hboxLayout5")
        self.hboxLayout5.setContentsMargins(0, 0, 0, 0)
        self.label_coordinates = QLabel(self.layoutWidget5)
        self.label_coordinates.setObjectName(u"label_coordinates")
        self.label_coordinates.setMinimumSize(QSize(120, 22))
        self.label_coordinates.setFont(font)

        self.hboxLayout5.addWidget(self.label_coordinates)

        self.lineEdit_coordinates = QLineEdit(self.layoutWidget5)
        self.lineEdit_coordinates.setObjectName(u"lineEdit_coordinates")
        self.lineEdit_coordinates.setMinimumSize(QSize(0, 25))

        self.hboxLayout5.addWidget(self.lineEdit_coordinates)

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

        self.layoutWidget6 = QWidget(Form_Profile)
        self.layoutWidget6.setObjectName(u"layoutWidget6")
        self.layoutWidget6.setGeometry(QRect(20, 459, 521, 141))
        self.verticalLayout = QVBoxLayout(self.layoutWidget6)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.label_service_offer = QLabel(self.layoutWidget6)
        self.label_service_offer.setObjectName(u"label_service_offer")
        self.label_service_offer.setMinimumSize(QSize(100, 0))
        self.label_service_offer.setFont(font)

        self.verticalLayout.addWidget(self.label_service_offer)

        self.textEdit_service_offer = QTextEdit(self.layoutWidget6)
        self.textEdit_service_offer.setObjectName(u"textEdit_service_offer")
        self.textEdit_service_offer.setFont(font)

        self.verticalLayout.addWidget(self.textEdit_service_offer)

        self.layoutWidget7 = QWidget(Form_Profile)
        self.layoutWidget7.setObjectName(u"layoutWidget7")
        self.layoutWidget7.setGeometry(QRect(20, 629, 521, 34))
        self.horizontalLayout = QHBoxLayout(self.layoutWidget7)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.pushButton_save = QPushButton(self.layoutWidget7)
        self.pushButton_save.setObjectName(u"pushButton_save")
        self.pushButton_save.setFont(font)
        icon = QIcon()
        iconThemeName = u"media-floppy"
        if QIcon.hasThemeIcon(iconThemeName):
            icon = QIcon.fromTheme(iconThemeName)
        else:
            icon.addFile(u".", QSize(), QIcon.Normal, QIcon.Off)

        self.pushButton_save.setIcon(icon)
        self.pushButton_save.setIconSize(QSize(20, 20))

        self.horizontalLayout.addWidget(self.pushButton_save)

        self.pushButton_close = QPushButton(self.layoutWidget7)
        self.pushButton_close.setObjectName(u"pushButton_close")
        self.pushButton_close.setFont(font)
        icon1 = QIcon()
        iconThemeName = u"window-close"
        if QIcon.hasThemeIcon(iconThemeName):
            icon1 = QIcon.fromTheme(iconThemeName)
        else:
            icon1.addFile(u".", QSize(), QIcon.Normal, QIcon.Off)

        self.pushButton_close.setIcon(icon1)
        self.pushButton_close.setIconSize(QSize(20, 20))

        self.horizontalLayout.addWidget(self.pushButton_close)

        self.layoutWidget_3 = QWidget(Form_Profile)
        self.layoutWidget_3.setObjectName(u"layoutWidget_3")
        self.layoutWidget_3.setGeometry(QRect(20, 220, 521, 32))
        self.layoutWidget_3.setMinimumSize(QSize(120, 25))
        self.layoutWidget_3.setFont(font)
        self._3 = QHBoxLayout(self.layoutWidget_3)
        self._3.setObjectName(u"_3")
        self._3.setContentsMargins(0, 0, 0, 0)
        self.label_zip_code_city = QLabel(self.layoutWidget_3)
        self.label_zip_code_city.setObjectName(u"label_zip_code_city")
        self.label_zip_code_city.setMinimumSize(QSize(120, 22))
        self.label_zip_code_city.setFont(font)

        self._3.addWidget(self.label_zip_code_city)

        self.lineEdit_zip_code = QLineEdit(self.layoutWidget_3)
        self.lineEdit_zip_code.setObjectName(u"lineEdit_zip_code")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_zip_code.sizePolicy().hasHeightForWidth())
        self.lineEdit_zip_code.setSizePolicy(sizePolicy)
        self.lineEdit_zip_code.setMinimumSize(QSize(0, 25))

        self._3.addWidget(self.lineEdit_zip_code)

        self.lineEdit_city = QLineEdit(self.layoutWidget_3)
        self.lineEdit_city.setObjectName(u"lineEdit_city")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(2)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.lineEdit_city.sizePolicy().hasHeightForWidth())
        self.lineEdit_city.setSizePolicy(sizePolicy1)
        self.lineEdit_city.setMinimumSize(QSize(0, 25))

        self._3.addWidget(self.lineEdit_city)

        self.layoutWidget_5 = QWidget(Form_Profile)
        self.layoutWidget_5.setObjectName(u"layoutWidget_5")
        self.layoutWidget_5.setGeometry(QRect(20, 300, 521, 32))
        self.layoutWidget_5.setMinimumSize(QSize(120, 25))
        self.layoutWidget_5.setFont(font)
        self._5 = QHBoxLayout(self.layoutWidget_5)
        self._5.setObjectName(u"_5")
        self._5.setContentsMargins(0, 0, 0, 0)
        self.label_country = QLabel(self.layoutWidget_5)
        self.label_country.setObjectName(u"label_country")
        self.label_country.setMinimumSize(QSize(120, 22))
        self.label_country.setFont(font)

        self._5.addWidget(self.label_country)

        self.lineEdit_country = QLineEdit(self.layoutWidget_5)
        self.lineEdit_country.setObjectName(u"lineEdit_country")
        self.lineEdit_country.setMinimumSize(QSize(0, 25))

        self._5.addWidget(self.lineEdit_country)

        self.layoutWidget_6 = QWidget(Form_Profile)
        self.layoutWidget_6.setObjectName(u"layoutWidget_6")
        self.layoutWidget_6.setGeometry(QRect(20, 260, 521, 32))
        self.layoutWidget_6.setMinimumSize(QSize(120, 25))
        self.layoutWidget_6.setFont(font)
        self._6 = QHBoxLayout(self.layoutWidget_6)
        self._6.setObjectName(u"_6")
        self._6.setContentsMargins(0, 0, 0, 0)
        self.label_state_or_region = QLabel(self.layoutWidget_6)
        self.label_state_or_region.setObjectName(u"label_state_or_region")
        self.label_state_or_region.setMinimumSize(QSize(120, 22))
        self.label_state_or_region.setFont(font)

        self._6.addWidget(self.label_state_or_region)

        self.lineEdit_state_or_region = QLineEdit(self.layoutWidget_6)
        self.lineEdit_state_or_region.setObjectName(u"lineEdit_state_or_region")
        self.lineEdit_state_or_region.setMinimumSize(QSize(0, 25))

        self._6.addWidget(self.lineEdit_state_or_region)

        self.layoutWidget_4 = QWidget(Form_Profile)
        self.layoutWidget_4.setObjectName(u"layoutWidget_4")
        self.layoutWidget_4.setGeometry(QRect(20, 140, 511, 27))
        self.layoutWidget_4.setMinimumSize(QSize(120, 25))
        self.layoutWidget_4.setFont(font)
        self._4 = QHBoxLayout(self.layoutWidget_4)
        self._4.setObjectName(u"_4")
        self._4.setContentsMargins(0, 0, 0, 0)
        self.label_street_2 = QLabel(self.layoutWidget_4)
        self.label_street_2.setObjectName(u"label_street_2")
        self.label_street_2.setMinimumSize(QSize(120, 22))
        self.label_street_2.setFont(font)

        self._4.addWidget(self.label_street_2)

        self.comboBox_gender = QComboBox(self.layoutWidget_4)
        self.comboBox_gender.addItem("")
        self.comboBox_gender.addItem("")
        self.comboBox_gender.addItem("")
        self.comboBox_gender.setObjectName(u"comboBox_gender")

        self._4.addWidget(self.comboBox_gender)

        QWidget.setTabOrder(self.lineEdit_profile_name, self.lineEdit_organization)
        QWidget.setTabOrder(self.lineEdit_organization, self.lineEdit_first_name)
        QWidget.setTabOrder(self.lineEdit_first_name, self.lineEdit_last_name)
        QWidget.setTabOrder(self.lineEdit_last_name, self.comboBox_gender)
        QWidget.setTabOrder(self.comboBox_gender, self.lineEdit_street)
        QWidget.setTabOrder(self.lineEdit_street, self.lineEdit_zip_code)
        QWidget.setTabOrder(self.lineEdit_zip_code, self.lineEdit_city)
        QWidget.setTabOrder(self.lineEdit_city, self.lineEdit_state_or_region)
        QWidget.setTabOrder(self.lineEdit_state_or_region, self.lineEdit_country)
        QWidget.setTabOrder(self.lineEdit_country, self.lineEdit_email)
        QWidget.setTabOrder(self.lineEdit_email, self.lineEdit_phone)
        QWidget.setTabOrder(self.lineEdit_phone, self.lineEdit_coordinates)
        QWidget.setTabOrder(self.lineEdit_coordinates, self.textEdit_service_offer)
        QWidget.setTabOrder(self.textEdit_service_offer, self.pushButton_save)
        QWidget.setTabOrder(self.pushButton_save, self.pushButton_close)

        self.retranslateUi(Form_Profile)

        QMetaObject.connectSlotsByName(Form_Profile)
    # setupUi

    def retranslateUi(self, Form_Profile):
        Form_Profile.setWindowTitle(QCoreApplication.translate("Form_Profile", u"Profile", None))
        self.label.setText(QCoreApplication.translate("Form_Profile", u"Name Surname", None))
        self.lineEdit_first_name.setPlaceholderText(QCoreApplication.translate("Form_Profile", u"First Name", None))
        self.lineEdit_last_name.setPlaceholderText(QCoreApplication.translate("Form_Profile", u"Last Name", None))
        self.label_organization.setText(QCoreApplication.translate("Form_Profile", u"Organization / Company", None))
        self.label_street.setText(QCoreApplication.translate("Form_Profile", u"Street", None))
        self.label_email.setText(QCoreApplication.translate("Form_Profile", u"Email", None))
        self.label_phone.setText(QCoreApplication.translate("Form_Profile", u"Phone", None))
        self.label_coordinates.setText(QCoreApplication.translate("Form_Profile", u"Coordinates", None))
        self.lineEdit_coordinates.setText("")
        self.label_profile_name.setText(QCoreApplication.translate("Form_Profile", u"Profile Name", None))
        self.label_service_offer.setText(QCoreApplication.translate("Form_Profile", u"Service Offering", None))
        self.textEdit_service_offer.setHtml(QCoreApplication.translate("Form_Profile", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'Ubuntu'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None))
        self.pushButton_save.setText(QCoreApplication.translate("Form_Profile", u"Save", None))
        self.pushButton_close.setText(QCoreApplication.translate("Form_Profile", u"Close", None))
        self.label_zip_code_city.setText(QCoreApplication.translate("Form_Profile", u"Postal Code City", None))
        self.lineEdit_zip_code.setPlaceholderText(QCoreApplication.translate("Form_Profile", u"Postal Code", None))
        self.lineEdit_city.setPlaceholderText(QCoreApplication.translate("Form_Profile", u"City", None))
        self.label_country.setText(QCoreApplication.translate("Form_Profile", u"Country", None))
        self.label_state_or_region.setText(QCoreApplication.translate("Form_Profile", u"State", None))
        self.label_street_2.setText(QCoreApplication.translate("Form_Profile", u"Gender", None))
        self.comboBox_gender.setItemText(0, QCoreApplication.translate("Form_Profile", u"Unknown", None))
        self.comboBox_gender.setItemText(1, QCoreApplication.translate("Form_Profile", u"Male", None))
        self.comboBox_gender.setItemText(2, QCoreApplication.translate("Form_Profile", u"Female", None))

    # retranslateUi

