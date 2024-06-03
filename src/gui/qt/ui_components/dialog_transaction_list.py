# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dialog_transaction_list.ui'
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
    QHeaderView, QLabel, QLineEdit, QSizePolicy,
    QTableView, QVBoxLayout, QWidget)

class Ui_DialogTransactionList(object):
    def setupUi(self, DialogTransactionList):
        if not DialogTransactionList.objectName():
            DialogTransactionList.setObjectName(u"DialogTransactionList")
        DialogTransactionList.resize(830, 748)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(DialogTransactionList.sizePolicy().hasHeightForWidth())
        DialogTransactionList.setSizePolicy(sizePolicy)
        DialogTransactionList.setMaximumSize(QSize(16777215, 16777215))
        self.label_voucher_list = QLabel(DialogTransactionList)
        self.label_voucher_list.setObjectName(u"label_voucher_list")
        self.label_voucher_list.setGeometry(QRect(10, 10, 521, 19))
        font = QFont()
        font.setPointSize(12)
        self.label_voucher_list.setFont(font)
        self.layoutWidget = QWidget(DialogTransactionList)
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

        self.tableView_transactions = QTableView(self.layoutWidget)
        self.tableView_transactions.setObjectName(u"tableView_transactions")
        sizePolicy.setHeightForWidth(self.tableView_transactions.sizePolicy().hasHeightForWidth())
        self.tableView_transactions.setSizePolicy(sizePolicy)
        self.tableView_transactions.setMinimumSize(QSize(800, 600))

        self.verticalLayout.addWidget(self.tableView_transactions)


        self.retranslateUi(DialogTransactionList)

        QMetaObject.connectSlotsByName(DialogTransactionList)
    # setupUi

    def retranslateUi(self, DialogTransactionList):
        DialogTransactionList.setWindowTitle(QCoreApplication.translate("DialogTransactionList", u"Transaction List", None))
        self.label_voucher_list.setText(QCoreApplication.translate("DialogTransactionList", u"List of all transactions", None))
        self.labelFilter.setText(QCoreApplication.translate("DialogTransactionList", u"Filter:", None))
    # retranslateUi

