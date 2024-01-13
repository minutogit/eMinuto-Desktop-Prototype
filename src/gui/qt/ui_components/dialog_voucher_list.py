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
    QLayout, QSizePolicy, QTableView, QVBoxLayout,
    QWidget)

class Ui_DialogVoucherList(object):
    def setupUi(self, DialogVoucherList):
        if not DialogVoucherList.objectName():
            DialogVoucherList.setObjectName(u"DialogVoucherList")
        DialogVoucherList.resize(739, 481)
        self.widget = QWidget(DialogVoucherList)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(20, 20, 701, 421))
        self.verticalLayout = QVBoxLayout(self.widget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setSizeConstraint(QLayout.SetMaximumSize)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.label_voucher_list = QLabel(self.widget)
        self.label_voucher_list.setObjectName(u"label_voucher_list")
        font = QFont()
        font.setPointSize(12)
        self.label_voucher_list.setFont(font)

        self.verticalLayout.addWidget(self.label_voucher_list)

        self.tableView_vouchers = QTableView(self.widget)
        self.tableView_vouchers.setObjectName(u"tableView_vouchers")

        self.verticalLayout.addWidget(self.tableView_vouchers)


        self.retranslateUi(DialogVoucherList)

        QMetaObject.connectSlotsByName(DialogVoucherList)
    # setupUi

    def retranslateUi(self, DialogVoucherList):
        DialogVoucherList.setWindowTitle(QCoreApplication.translate("DialogVoucherList", u"Dialog", None))
        self.label_voucher_list.setText(QCoreApplication.translate("DialogVoucherList", u"Gutscheinliste", None))
    # retranslateUi

