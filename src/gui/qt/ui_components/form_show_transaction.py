# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form_show_transaction.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QHeaderView, QLabel,
    QPushButton, QSizePolicy, QTableView, QVBoxLayout,
    QWidget)

class Ui_FormShowTransaction(object):
    def setupUi(self, FormShowTransaction):
        if not FormShowTransaction.objectName():
            FormShowTransaction.setObjectName(u"FormShowTransaction")
        FormShowTransaction.resize(820, 751)
        self.widget = QWidget(FormShowTransaction)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(11, 11, 802, 731))
        self.verticalLayout = QVBoxLayout(self.widget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.labelInfoTextLeft = QLabel(self.widget)
        self.labelInfoTextLeft.setObjectName(u"labelInfoTextLeft")

        self.horizontalLayout.addWidget(self.labelInfoTextLeft)

        self.labelInfoTextRight = QLabel(self.widget)
        self.labelInfoTextRight.setObjectName(u"labelInfoTextRight")

        self.horizontalLayout.addWidget(self.labelInfoTextRight)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.tableView_transaction = QTableView(self.widget)
        self.tableView_transaction.setObjectName(u"tableView_transaction")
        self.tableView_transaction.setMinimumSize(QSize(800, 600))
        self.tableView_transaction.setSizeIncrement(QSize(2, 0))

        self.verticalLayout.addWidget(self.tableView_transaction)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.pushButtonRawData = QPushButton(self.widget)
        self.pushButtonRawData.setObjectName(u"pushButtonRawData")

        self.horizontalLayout_2.addWidget(self.pushButtonRawData)

        self.pushButtonSaveTransactionFile = QPushButton(self.widget)
        self.pushButtonSaveTransactionFile.setObjectName(u"pushButtonSaveTransactionFile")

        self.horizontalLayout_2.addWidget(self.pushButtonSaveTransactionFile)

        self.pushButtonClose = QPushButton(self.widget)
        self.pushButtonClose.setObjectName(u"pushButtonClose")

        self.horizontalLayout_2.addWidget(self.pushButtonClose)


        self.verticalLayout.addLayout(self.horizontalLayout_2)


        self.retranslateUi(FormShowTransaction)

        QMetaObject.connectSlotsByName(FormShowTransaction)
    # setupUi

    def retranslateUi(self, FormShowTransaction):
        FormShowTransaction.setWindowTitle(QCoreApplication.translate("FormShowTransaction", u"Voucher Details", None))
        self.labelInfoTextLeft.setText("")
        self.labelInfoTextRight.setText("")
        self.pushButtonRawData.setText(QCoreApplication.translate("FormShowTransaction", u"Raw Data", None))
        self.pushButtonSaveTransactionFile.setText(QCoreApplication.translate("FormShowTransaction", u"Save Transaction File", None))
        self.pushButtonClose.setText(QCoreApplication.translate("FormShowTransaction", u"Close", None))
    # retranslateUi

