# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form_show_voucher.ui'
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

class Ui_FormShowVoucher(object):
    def setupUi(self, FormShowVoucher):
        if not FormShowVoucher.objectName():
            FormShowVoucher.setObjectName(u"FormShowVoucher")
        FormShowVoucher.resize(820, 751)
        self.layoutWidget = QWidget(FormShowVoucher)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(10, 10, 802, 734))
        self.verticalLayout = QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.labelInfoTextLeft = QLabel(self.layoutWidget)
        self.labelInfoTextLeft.setObjectName(u"labelInfoTextLeft")

        self.horizontalLayout.addWidget(self.labelInfoTextLeft)

        self.labelInfoTextRight = QLabel(self.layoutWidget)
        self.labelInfoTextRight.setObjectName(u"labelInfoTextRight")

        self.horizontalLayout.addWidget(self.labelInfoTextRight)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.tableView_voucher = QTableView(self.layoutWidget)
        self.tableView_voucher.setObjectName(u"tableView_voucher")
        self.tableView_voucher.setMinimumSize(QSize(800, 600))
        self.tableView_voucher.setSizeIncrement(QSize(2, 0))

        self.verticalLayout.addWidget(self.tableView_voucher)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.pushButtonAddGuarantorSignature = QPushButton(self.layoutWidget)
        self.pushButtonAddGuarantorSignature.setObjectName(u"pushButtonAddGuarantorSignature")

        self.horizontalLayout_3.addWidget(self.pushButtonAddGuarantorSignature)

        self.pushButtonSignAsCreator = QPushButton(self.layoutWidget)
        self.pushButtonSignAsCreator.setObjectName(u"pushButtonSignAsCreator")

        self.horizontalLayout_3.addWidget(self.pushButtonSignAsCreator)

        self.pushButtonSignAsGuarantor = QPushButton(self.layoutWidget)
        self.pushButtonSignAsGuarantor.setObjectName(u"pushButtonSignAsGuarantor")

        self.horizontalLayout_3.addWidget(self.pushButtonSignAsGuarantor)

        self.pushButtonSendToGuarantor = QPushButton(self.layoutWidget)
        self.pushButtonSendToGuarantor.setObjectName(u"pushButtonSendToGuarantor")

        self.horizontalLayout_3.addWidget(self.pushButtonSendToGuarantor)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.pushButtonRawData = QPushButton(self.layoutWidget)
        self.pushButtonRawData.setObjectName(u"pushButtonRawData")

        self.horizontalLayout_2.addWidget(self.pushButtonRawData)

        self.pushButtonClose = QPushButton(self.layoutWidget)
        self.pushButtonClose.setObjectName(u"pushButtonClose")

        self.horizontalLayout_2.addWidget(self.pushButtonClose)

        self.pushButtonRecover = QPushButton(self.layoutWidget)
        self.pushButtonRecover.setObjectName(u"pushButtonRecover")

        self.horizontalLayout_2.addWidget(self.pushButtonRecover)

        self.pushButtonTrash = QPushButton(self.layoutWidget)
        self.pushButtonTrash.setObjectName(u"pushButtonTrash")

        self.horizontalLayout_2.addWidget(self.pushButtonTrash)


        self.verticalLayout.addLayout(self.horizontalLayout_2)


        self.retranslateUi(FormShowVoucher)

        QMetaObject.connectSlotsByName(FormShowVoucher)
    # setupUi

    def retranslateUi(self, FormShowVoucher):
        FormShowVoucher.setWindowTitle(QCoreApplication.translate("FormShowVoucher", u"Voucher Details", None))
        self.labelInfoTextLeft.setText("")
        self.labelInfoTextRight.setText("")
        self.pushButtonAddGuarantorSignature.setText(QCoreApplication.translate("FormShowVoucher", u"Add Received Guarantor Signature", None))
        self.pushButtonSignAsCreator.setText(QCoreApplication.translate("FormShowVoucher", u"Sign as Creator", None))
        self.pushButtonSignAsGuarantor.setText(QCoreApplication.translate("FormShowVoucher", u"Sign as Guarantor", None))
        self.pushButtonSendToGuarantor.setText(QCoreApplication.translate("FormShowVoucher", u"Send to Guarantor", None))
        self.pushButtonRawData.setText(QCoreApplication.translate("FormShowVoucher", u"Raw Data", None))
        self.pushButtonClose.setText(QCoreApplication.translate("FormShowVoucher", u"Close", None))
        self.pushButtonRecover.setText(QCoreApplication.translate("FormShowVoucher", u"Restore", None))
        self.pushButtonTrash.setText(QCoreApplication.translate("FormShowVoucher", u"To Trash", None))
    # retranslateUi

