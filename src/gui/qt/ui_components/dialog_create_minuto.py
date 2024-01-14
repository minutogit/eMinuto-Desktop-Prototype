# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dialog_create_minuto.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QDialog,
    QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QSizePolicy, QSpinBox, QTextEdit, QVBoxLayout,
    QWidget)

class Ui_DialogCreateMinuto(object):
    def setupUi(self, DialogCreateMinuto):
        if not DialogCreateMinuto.objectName():
            DialogCreateMinuto.setObjectName(u"DialogCreateMinuto")
        DialogCreateMinuto.resize(506, 747)
        sizePolicy = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(DialogCreateMinuto.sizePolicy().hasHeightForWidth())
        DialogCreateMinuto.setSizePolicy(sizePolicy)
        self.widget_creator_first_name = QWidget(DialogCreateMinuto)
        self.widget_creator_first_name.setObjectName(u"widget_creator_first_name")
        self.widget_creator_first_name.setGeometry(QRect(20, 280, 461, 30))
        self.horizontalLayout_first_name = QHBoxLayout(self.widget_creator_first_name)
        self.horizontalLayout_first_name.setObjectName(u"horizontalLayout_first_name")
        self.horizontalLayout_first_name.setContentsMargins(0, 0, 0, 0)
        self.label_creator_first_name = QLabel(self.widget_creator_first_name)
        self.label_creator_first_name.setObjectName(u"label_creator_first_name")
        self.label_creator_first_name.setMinimumSize(QSize(150, 0))
        font = QFont()
        font.setPointSize(11)
        self.label_creator_first_name.setFont(font)

        self.horizontalLayout_first_name.addWidget(self.label_creator_first_name)

        self.lineEdit_creator_first_name = QLineEdit(self.widget_creator_first_name)
        self.lineEdit_creator_first_name.setObjectName(u"lineEdit_creator_first_name")

        self.horizontalLayout_first_name.addWidget(self.lineEdit_creator_first_name)

        self.widget_creator_last_name = QWidget(DialogCreateMinuto)
        self.widget_creator_last_name.setObjectName(u"widget_creator_last_name")
        self.widget_creator_last_name.setGeometry(QRect(20, 320, 461, 31))
        self.horizontalLayout_last_name = QHBoxLayout(self.widget_creator_last_name)
        self.horizontalLayout_last_name.setObjectName(u"horizontalLayout_last_name")
        self.horizontalLayout_last_name.setContentsMargins(0, 0, 0, 0)
        self.label_creator_last_name = QLabel(self.widget_creator_last_name)
        self.label_creator_last_name.setObjectName(u"label_creator_last_name")
        self.label_creator_last_name.setMinimumSize(QSize(150, 0))
        self.label_creator_last_name.setFont(font)

        self.horizontalLayout_last_name.addWidget(self.label_creator_last_name)

        self.lineEdit_creator_last_name = QLineEdit(self.widget_creator_last_name)
        self.lineEdit_creator_last_name.setObjectName(u"lineEdit_creator_last_name")
        self.lineEdit_creator_last_name.setFont(font)

        self.horizontalLayout_last_name.addWidget(self.lineEdit_creator_last_name)

        self.widget_creator_organization = QWidget(DialogCreateMinuto)
        self.widget_creator_organization.setObjectName(u"widget_creator_organization")
        self.widget_creator_organization.setGeometry(QRect(20, 240, 461, 31))
        self.horizontalLayout_organization = QHBoxLayout(self.widget_creator_organization)
        self.horizontalLayout_organization.setObjectName(u"horizontalLayout_organization")
        self.horizontalLayout_organization.setContentsMargins(0, 0, 0, 0)
        self.label_creator_organization = QLabel(self.widget_creator_organization)
        self.label_creator_organization.setObjectName(u"label_creator_organization")
        self.label_creator_organization.setMinimumSize(QSize(150, 0))
        self.label_creator_organization.setFont(font)

        self.horizontalLayout_organization.addWidget(self.label_creator_organization)

        self.lineEdit_creator_organization = QLineEdit(self.widget_creator_organization)
        self.lineEdit_creator_organization.setObjectName(u"lineEdit_creator_organization")
        self.lineEdit_creator_organization.setFont(font)

        self.horizontalLayout_organization.addWidget(self.lineEdit_creator_organization)

        self.widget_creator_address = QWidget(DialogCreateMinuto)
        self.widget_creator_address.setObjectName(u"widget_creator_address")
        self.widget_creator_address.setGeometry(QRect(20, 400, 461, 31))
        self.horizontalLayout_address = QHBoxLayout(self.widget_creator_address)
        self.horizontalLayout_address.setObjectName(u"horizontalLayout_address")
        self.horizontalLayout_address.setContentsMargins(0, 0, 0, 0)
        self.label_creator_address = QLabel(self.widget_creator_address)
        self.label_creator_address.setObjectName(u"label_creator_address")
        self.label_creator_address.setMinimumSize(QSize(150, 0))
        self.label_creator_address.setFont(font)

        self.horizontalLayout_address.addWidget(self.label_creator_address)

        self.lineEdit_creator_address = QLineEdit(self.widget_creator_address)
        self.lineEdit_creator_address.setObjectName(u"lineEdit_creator_address")
        self.lineEdit_creator_address.setFont(font)

        self.horizontalLayout_address.addWidget(self.lineEdit_creator_address)

        self.widget_creator_gender = QWidget(DialogCreateMinuto)
        self.widget_creator_gender.setObjectName(u"widget_creator_gender")
        self.widget_creator_gender.setGeometry(QRect(20, 360, 461, 30))
        self.horizontalLayout_gender = QHBoxLayout(self.widget_creator_gender)
        self.horizontalLayout_gender.setObjectName(u"horizontalLayout_gender")
        self.horizontalLayout_gender.setContentsMargins(0, 0, 0, 0)
        self.label_creator_gender = QLabel(self.widget_creator_gender)
        self.label_creator_gender.setObjectName(u"label_creator_gender")
        self.label_creator_gender.setMinimumSize(QSize(150, 0))
        self.label_creator_gender.setMaximumSize(QSize(150, 16777215))
        self.label_creator_gender.setFont(font)

        self.horizontalLayout_gender.addWidget(self.label_creator_gender)

        self.comboBox_creator_gender = QComboBox(self.widget_creator_gender)
        self.comboBox_creator_gender.addItem("")
        self.comboBox_creator_gender.addItem("")
        self.comboBox_creator_gender.addItem("")
        self.comboBox_creator_gender.setObjectName(u"comboBox_creator_gender")
        self.comboBox_creator_gender.setFont(font)
        self.comboBox_creator_gender.setEditable(True)

        self.horizontalLayout_gender.addWidget(self.comboBox_creator_gender)

        self.widget_creator_first_name_2 = QWidget(DialogCreateMinuto)
        self.widget_creator_first_name_2.setObjectName(u"widget_creator_first_name_2")
        self.widget_creator_first_name_2.setGeometry(QRect(20, 50, 141, 101))
        self.verticalLayout_2 = QVBoxLayout(self.widget_creator_first_name_2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.label_amount = QLabel(self.widget_creator_first_name_2)
        self.label_amount.setObjectName(u"label_amount")
        self.label_amount.setMinimumSize(QSize(120, 0))
        self.label_amount.setFont(font)
        self.label_amount.setWordWrap(True)

        self.verticalLayout_2.addWidget(self.label_amount)

        self.lineEdit_amount = QLineEdit(self.widget_creator_first_name_2)
        self.lineEdit_amount.setObjectName(u"lineEdit_amount")
        self.lineEdit_amount.setFont(font)
        self.lineEdit_amount.setAlignment(Qt.AlignCenter)

        self.verticalLayout_2.addWidget(self.lineEdit_amount)

        self.widget_creator_organization_3 = QWidget(DialogCreateMinuto)
        self.widget_creator_organization_3.setObjectName(u"widget_creator_organization_3")
        self.widget_creator_organization_3.setGeometry(QRect(20, 670, 461, 31))
        self.horizontalLayout_test_voucher = QHBoxLayout(self.widget_creator_organization_3)
        self.horizontalLayout_test_voucher.setObjectName(u"horizontalLayout_test_voucher")
        self.horizontalLayout_test_voucher.setContentsMargins(0, 0, 0, 0)
        self.label_region_2 = QLabel(self.widget_creator_organization_3)
        self.label_region_2.setObjectName(u"label_region_2")
        self.label_region_2.setMinimumSize(QSize(150, 0))
        self.label_region_2.setFont(font)

        self.horizontalLayout_test_voucher.addWidget(self.label_region_2)

        self.checkBox_is_test_voucher = QCheckBox(self.widget_creator_organization_3)
        self.checkBox_is_test_voucher.setObjectName(u"checkBox_is_test_voucher")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.checkBox_is_test_voucher.sizePolicy().hasHeightForWidth())
        self.checkBox_is_test_voucher.setSizePolicy(sizePolicy1)
        self.checkBox_is_test_voucher.setFont(font)

        self.horizontalLayout_test_voucher.addWidget(self.checkBox_is_test_voucher)

        self.widget_creator_last_name_3 = QWidget(DialogCreateMinuto)
        self.widget_creator_last_name_3.setObjectName(u"widget_creator_last_name_3")
        self.widget_creator_last_name_3.setGeometry(QRect(20, 480, 461, 31))
        self.horizontalLayout_last_name_3 = QHBoxLayout(self.widget_creator_last_name_3)
        self.horizontalLayout_last_name_3.setObjectName(u"horizontalLayout_last_name_3")
        self.horizontalLayout_last_name_3.setContentsMargins(0, 0, 0, 0)
        self.label_phone = QLabel(self.widget_creator_last_name_3)
        self.label_phone.setObjectName(u"label_phone")
        self.label_phone.setMinimumSize(QSize(150, 0))
        self.label_phone.setFont(font)

        self.horizontalLayout_last_name_3.addWidget(self.label_phone)

        self.lineEdit_phone = QLineEdit(self.widget_creator_last_name_3)
        self.lineEdit_phone.setObjectName(u"lineEdit_phone")
        self.lineEdit_phone.setFont(font)

        self.horizontalLayout_last_name_3.addWidget(self.lineEdit_phone)

        self.widget_creator_first_name_3 = QWidget(DialogCreateMinuto)
        self.widget_creator_first_name_3.setObjectName(u"widget_creator_first_name_3")
        self.widget_creator_first_name_3.setGeometry(QRect(20, 440, 461, 31))
        self.horizontalLayout_first_name_3 = QHBoxLayout(self.widget_creator_first_name_3)
        self.horizontalLayout_first_name_3.setObjectName(u"horizontalLayout_first_name_3")
        self.horizontalLayout_first_name_3.setContentsMargins(0, 0, 0, 0)
        self.label_email = QLabel(self.widget_creator_first_name_3)
        self.label_email.setObjectName(u"label_email")
        self.label_email.setMinimumSize(QSize(150, 0))
        self.label_email.setFont(font)

        self.horizontalLayout_first_name_3.addWidget(self.label_email)

        self.lineEdit_email = QLineEdit(self.widget_creator_first_name_3)
        self.lineEdit_email.setObjectName(u"lineEdit_email")
        self.lineEdit_email.setFont(font)

        self.horizontalLayout_first_name_3.addWidget(self.lineEdit_email)

        self.label_own_data = QLabel(DialogCreateMinuto)
        self.label_own_data.setObjectName(u"label_own_data")
        self.label_own_data.setGeometry(QRect(20, 200, 181, 31))
        font1 = QFont()
        font1.setPointSize(15)
        font1.setBold(True)
        self.label_own_data.setFont(font1)
        self.label_voucher_data = QLabel(DialogCreateMinuto)
        self.label_voucher_data.setObjectName(u"label_voucher_data")
        self.label_voucher_data.setGeometry(QRect(20, 20, 181, 21))
        self.label_voucher_data.setFont(font1)
        self.label_players_only = QLabel(DialogCreateMinuto)
        self.label_players_only.setObjectName(u"label_players_only")
        self.label_players_only.setGeometry(QRect(20, 630, 461, 20))
        self.label_players_only.setFont(font)
        self.label_players_only.setAlignment(Qt.AlignCenter)
        self.label_voucher_description = QLabel(DialogCreateMinuto)
        self.label_voucher_description.setObjectName(u"label_voucher_description")
        self.label_voucher_description.setGeometry(QRect(20, 160, 461, 41))
        self.label_voucher_description.setFont(font)
        self.label_voucher_description.setAlignment(Qt.AlignCenter)
        self.label_voucher_description.setWordWrap(True)
        self.pushButton_CreateVoucher = QPushButton(DialogCreateMinuto)
        self.pushButton_CreateVoucher.setObjectName(u"pushButton_CreateVoucher")
        self.pushButton_CreateVoucher.setGeometry(QRect(150, 710, 161, 28))
        self.pushButton_CreateVoucher.setFont(font)
        self.layoutWidget = QWidget(DialogCreateMinuto)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(20, 520, 461, 101))
        self.verticalLayout = QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.label_service_offer = QLabel(self.layoutWidget)
        self.label_service_offer.setObjectName(u"label_service_offer")
        self.label_service_offer.setMinimumSize(QSize(120, 0))
        self.label_service_offer.setFont(font)

        self.verticalLayout.addWidget(self.label_service_offer)

        self.textEdit_service_offer = QTextEdit(self.layoutWidget)
        self.textEdit_service_offer.setObjectName(u"textEdit_service_offer")
        self.textEdit_service_offer.setFont(font)

        self.verticalLayout.addWidget(self.textEdit_service_offer)

        self.layoutWidget1 = QWidget(DialogCreateMinuto)
        self.layoutWidget1.setObjectName(u"layoutWidget1")
        self.layoutWidget1.setGeometry(QRect(180, 120, 301, 30))
        self.horizontalLayout = QHBoxLayout(self.layoutWidget1)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.label_validit_until = QLabel(self.layoutWidget1)
        self.label_validit_until.setObjectName(u"label_validit_until")
        sizePolicy2 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.label_validit_until.sizePolicy().hasHeightForWidth())
        self.label_validit_until.setSizePolicy(sizePolicy2)
        self.label_validit_until.setMinimumSize(QSize(0, 0))
        self.label_validit_until.setFont(font)

        self.horizontalLayout.addWidget(self.label_validit_until)

        self.spinBox_years_valid = QSpinBox(self.layoutWidget1)
        self.spinBox_years_valid.setObjectName(u"spinBox_years_valid")
        self.spinBox_years_valid.setMaximumSize(QSize(49, 16777215))
        self.spinBox_years_valid.setFont(font)
        self.spinBox_years_valid.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.spinBox_years_valid.setMinimum(5)
        self.spinBox_years_valid.setMaximum(10)

        self.horizontalLayout.addWidget(self.spinBox_years_valid)

        self.label_years = QLabel(self.layoutWidget1)
        self.label_years.setObjectName(u"label_years")
        sizePolicy3 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.label_years.sizePolicy().hasHeightForWidth())
        self.label_years.setSizePolicy(sizePolicy3)
        self.label_years.setFont(font)

        self.horizontalLayout.addWidget(self.label_years)

        self.layoutWidget2 = QWidget(DialogCreateMinuto)
        self.layoutWidget2.setObjectName(u"layoutWidget2")
        self.layoutWidget2.setGeometry(QRect(180, 60, 301, 56))
        self.horizontalLayout_2 = QHBoxLayout(self.layoutWidget2)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label_region = QLabel(self.layoutWidget2)
        self.label_region.setObjectName(u"label_region")
        self.label_region.setMinimumSize(QSize(120, 0))
        self.label_region.setFont(font)

        self.verticalLayout_3.addWidget(self.label_region)

        self.lineEdit_region = QLineEdit(self.layoutWidget2)
        self.lineEdit_region.setObjectName(u"lineEdit_region")
        self.lineEdit_region.setMinimumSize(QSize(150, 0))
        self.lineEdit_region.setFont(font)
        self.lineEdit_region.setAlignment(Qt.AlignCenter)

        self.verticalLayout_3.addWidget(self.lineEdit_region)


        self.horizontalLayout_2.addLayout(self.verticalLayout_3)

        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.label_coordinates = QLabel(self.layoutWidget2)
        self.label_coordinates.setObjectName(u"label_coordinates")
        self.label_coordinates.setMinimumSize(QSize(120, 0))
        self.label_coordinates.setFont(font)

        self.verticalLayout_4.addWidget(self.label_coordinates)

        self.lineEdit_coordinates = QLineEdit(self.layoutWidget2)
        self.lineEdit_coordinates.setObjectName(u"lineEdit_coordinates")
        self.lineEdit_coordinates.setFont(font)
        self.lineEdit_coordinates.setAlignment(Qt.AlignCenter)

        self.verticalLayout_4.addWidget(self.lineEdit_coordinates)


        self.horizontalLayout_2.addLayout(self.verticalLayout_4)


        self.retranslateUi(DialogCreateMinuto)

        QMetaObject.connectSlotsByName(DialogCreateMinuto)
    # setupUi

    def retranslateUi(self, DialogCreateMinuto):
        DialogCreateMinuto.setWindowTitle(QCoreApplication.translate("DialogCreateMinuto", u"Minuto sch\u00f6pfen", None))
        self.label_creator_first_name.setText(QCoreApplication.translate("DialogCreateMinuto", u"Rufname", None))
        self.label_creator_last_name.setText(QCoreApplication.translate("DialogCreateMinuto", u"Familienname", None))
        self.label_creator_organization.setText(QCoreApplication.translate("DialogCreateMinuto", u"Organisation / Firma", None))
        self.label_creator_address.setText(QCoreApplication.translate("DialogCreateMinuto", u"Adresse", None))
        self.label_creator_gender.setText(QCoreApplication.translate("DialogCreateMinuto", u"Geschlecht", None))
        self.comboBox_creator_gender.setItemText(0, QCoreApplication.translate("DialogCreateMinuto", u"unbekannt", None))
        self.comboBox_creator_gender.setItemText(1, QCoreApplication.translate("DialogCreateMinuto", u"m\u00e4nnlich", None))
        self.comboBox_creator_gender.setItemText(2, QCoreApplication.translate("DialogCreateMinuto", u"weiblich", None))

        self.label_amount.setText(QCoreApplication.translate("DialogCreateMinuto", u"Wie viel Minuto sollen gesch\u00f6pft werden?", None))
        self.lineEdit_amount.setInputMask(QCoreApplication.translate("DialogCreateMinuto", u"99999", None))
        self.lineEdit_amount.setText("")
        self.lineEdit_amount.setPlaceholderText(QCoreApplication.translate("DialogCreateMinuto", u"1000", None))
        self.label_region_2.setText(QCoreApplication.translate("DialogCreateMinuto", u"Testgutschein?", None))
        self.checkBox_is_test_voucher.setText(QCoreApplication.translate("DialogCreateMinuto", u"Als Testgutschein markieren", None))
        self.label_phone.setText(QCoreApplication.translate("DialogCreateMinuto", u"Telefon", None))
        self.label_email.setText(QCoreApplication.translate("DialogCreateMinuto", u"eMail Adresse", None))
        self.label_own_data.setText(QCoreApplication.translate("DialogCreateMinuto", u"Eigene Daten", None))
        self.label_voucher_data.setText(QCoreApplication.translate("DialogCreateMinuto", u"Gutschein Daten", None))
        self.label_players_only.setText(QCoreApplication.translate("DialogCreateMinuto", u"Gutschein-Nutzung nur f\u00fcr Mitspieler/innen.", None))
        self.label_voucher_description.setText("")
        self.pushButton_CreateVoucher.setText(QCoreApplication.translate("DialogCreateMinuto", u"Erstellen", None))
        self.label_service_offer.setText(QCoreApplication.translate("DialogCreateMinuto", u"Angebote / F\u00e4higkeiten", None))
        self.label_validit_until.setText(QCoreApplication.translate("DialogCreateMinuto", u"G\u00fcltigkeit", None))
        self.label_years.setText(QCoreApplication.translate("DialogCreateMinuto", u"Jahre", None))
        self.label_region.setText(QCoreApplication.translate("DialogCreateMinuto", u"Minuto Region", None))
        self.lineEdit_region.setPlaceholderText(QCoreApplication.translate("DialogCreateMinuto", u"10115", None))
        self.label_coordinates.setText(QCoreApplication.translate("DialogCreateMinuto", u"Koordinaten", None))
        self.lineEdit_coordinates.setText("")
        self.lineEdit_coordinates.setPlaceholderText(QCoreApplication.translate("DialogCreateMinuto", u"52.5, 13.40", None))
    # retranslateUi

