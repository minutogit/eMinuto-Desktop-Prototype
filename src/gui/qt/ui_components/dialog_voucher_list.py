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
from PySide6.QtWidgets import (QApplication, QDialog, QHeaderView, QLabel,
    QSizePolicy, QTableView, QWidget)

class Ui_DialogVoucherList(object):
    def setupUi(self, DialogVoucherList):
        if not DialogVoucherList.objectName():
            DialogVoucherList.setObjectName(u"DialogVoucherList")
        DialogVoucherList.resize(820, 648)
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
        self.tableView_vouchers = QTableView(DialogVoucherList)
        self.tableView_vouchers.setObjectName(u"tableView_vouchers")
        self.tableView_vouchers.setGeometry(QRect(10, 35, 800, 600))
        sizePolicy.setHeightForWidth(self.tableView_vouchers.sizePolicy().hasHeightForWidth())
        self.tableView_vouchers.setSizePolicy(sizePolicy)
        self.tableView_vouchers.setMinimumSize(QSize(800, 600))

        self.retranslateUi(DialogVoucherList)

        QMetaObject.connectSlotsByName(DialogVoucherList)
    # setupUi

    def retranslateUi(self, DialogVoucherList):
        DialogVoucherList.setWindowTitle(QCoreApplication.translate("DialogVoucherList", u"Gutscheinliste", None))
        self.label_voucher_list.setText(QCoreApplication.translate("DialogVoucherList", u"Gutscheinliste", None))
    # retranslateUi

