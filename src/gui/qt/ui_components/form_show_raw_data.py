# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form_show_raw_data.ui'
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
from PySide6.QtWidgets import (QApplication, QLabel, QPushButton, QSizePolicy,
    QTextEdit, QVBoxLayout, QWidget)

class Ui_FormShowRawData(object):
    def setupUi(self, FormShowRawData):
        if not FormShowRawData.objectName():
            FormShowRawData.setObjectName(u"FormShowRawData")
        FormShowRawData.resize(830, 678)
        self.layoutWidget = QWidget(FormShowRawData)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(20, 10, 802, 661))
        self.verticalLayout = QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.labelRawData = QLabel(self.layoutWidget)
        self.labelRawData.setObjectName(u"labelRawData")
        font = QFont()
        font.setPointSize(12)
        self.labelRawData.setFont(font)

        self.verticalLayout.addWidget(self.labelRawData)

        self.textEdit_text_data = QTextEdit(self.layoutWidget)
        self.textEdit_text_data.setObjectName(u"textEdit_text_data")
        self.textEdit_text_data.setMinimumSize(QSize(800, 600))

        self.verticalLayout.addWidget(self.textEdit_text_data)

        self.pushButton_Close = QPushButton(self.layoutWidget)
        self.pushButton_Close.setObjectName(u"pushButton_Close")

        self.verticalLayout.addWidget(self.pushButton_Close)


        self.retranslateUi(FormShowRawData)

        QMetaObject.connectSlotsByName(FormShowRawData)
    # setupUi

    def retranslateUi(self, FormShowRawData):
        FormShowRawData.setWindowTitle(QCoreApplication.translate("FormShowRawData", u"Raw Data", None))
        self.labelRawData.setText(QCoreApplication.translate("FormShowRawData", u"Raw Data", None))
        self.pushButton_Close.setText(QCoreApplication.translate("FormShowRawData", u"Close", None))
    # retranslateUi

