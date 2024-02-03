# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dialog_voucher_list.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QDialog, QHBoxLayout,
    QHeaderView, QLabel, QLineEdit, QPushButton,
    QSizePolicy, QTableView, QVBoxLayout, QWidget)

class Ui_DialogVoucherList(object):
    def setupUi(self, DialogVoucherList):
        if not DialogVoucherList.objectName():
            DialogVoucherList.setObjectName(u"DialogVoucherList")
        DialogVoucherList.resize(839, 748)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(DialogVoucherList.sizePolicy().hasHeightForWidth())
        DialogVoucherList.setSizePolicy(sizePolicy)
        DialogVoucherList.setMaximumSize(QSize(16777215, 16777215))
        self.label_voucher_list = QLabel(DialogVoucherList)
        self.label_voucher_list.setObjectName(u"label_voucher_list")
        self.label_voucher_list.setGeometry(QRect(10, 10, 103, 19))
        font = QFont()
        font.setPointSize(12)
        self.label_voucher_list.setFont(font)
        self.layoutWidget = QWidget(DialogVoucherList)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(10, 35, 802, 700))
        self.verticalLayout = QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(3)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.statusComboBox = QComboBox(self.layoutWidget)
        self.statusComboBox.setObjectName(u"statusComboBox")
        self.statusComboBox.setMinimumSize(QSize(200, 0))
        font1 = QFont()
        font1.setPointSize(11)
        self.statusComboBox.setFont(font1)

        self.horizontalLayout.addWidget(self.statusComboBox)

        self.labelFilter = QLabel(self.layoutWidget)
        self.labelFilter.setObjectName(u"labelFilter")
        self.labelFilter.setFont(font1)

        self.horizontalLayout.addWidget(self.labelFilter)

        self.lineEditFilter = QLineEdit(self.layoutWidget)
        self.lineEditFilter.setObjectName(u"lineEditFilter")
        self.lineEditFilter.setFont(font1)

        self.horizontalLayout.addWidget(self.lineEditFilter)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.tableView_vouchers = QTableView(self.layoutWidget)
        self.tableView_vouchers.setObjectName(u"tableView_vouchers")
        sizePolicy.setHeightForWidth(self.tableView_vouchers.sizePolicy().hasHeightForWidth())
        self.tableView_vouchers.setSizePolicy(sizePolicy)
        self.tableView_vouchers.setMinimumSize(QSize(800, 600))

        self.verticalLayout.addWidget(self.tableView_vouchers)

        self.pushButton_open_voucher_or_signature = QPushButton(self.layoutWidget)
        self.pushButton_open_voucher_or_signature.setObjectName(u"pushButton_open_voucher_or_signature")

        self.verticalLayout.addWidget(self.pushButton_open_voucher_or_signature)


        self.retranslateUi(DialogVoucherList)

        QMetaObject.connectSlotsByName(DialogVoucherList)
    # setupUi

    def retranslateUi(self, DialogVoucherList):
        DialogVoucherList.setWindowTitle(QCoreApplication.translate("DialogVoucherList", u"Gutscheinliste", None))
        self.label_voucher_list.setText(QCoreApplication.translate("DialogVoucherList", u"Gutscheinliste", None))
        self.labelFilter.setText(QCoreApplication.translate("DialogVoucherList", u"  Filter:", None))
        self.pushButton_open_voucher_or_signature.setText(QCoreApplication.translate("DialogVoucherList", u"Gutschein oder B\u00fcrgenunterschrift aus Datei \u00f6ffen", None))
    # retranslateUi

