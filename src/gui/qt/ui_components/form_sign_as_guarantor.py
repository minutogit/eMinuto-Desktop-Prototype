# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form_sign_as_guarantor.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QSizePolicy, QVBoxLayout,
    QWidget)

class Ui_FormSignVoucherAsGuarantor(object):
    def setupUi(self, FormSignVoucherAsGuarantor):
        if not FormSignVoucherAsGuarantor.objectName():
            FormSignVoucherAsGuarantor.setObjectName(u"FormSignVoucherAsGuarantor")
        FormSignVoucherAsGuarantor.resize(761, 331)
        self.widget = QWidget(FormSignVoucherAsGuarantor)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(20, 10, 721, 301))
        self.verticalLayout = QVBoxLayout(self.widget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.label_2 = QLabel(self.widget)
        self.label_2.setObjectName(u"label_2")
        font = QFont()
        font.setPointSize(13)
        font.setBold(True)
        self.label_2.setFont(font)

        self.verticalLayout.addWidget(self.label_2)

        self.label_guarantor_liability_notice = QLabel(self.widget)
        self.label_guarantor_liability_notice.setObjectName(u"label_guarantor_liability_notice")
        font1 = QFont()
        font1.setPointSize(11)
        self.label_guarantor_liability_notice.setFont(font1)
        self.label_guarantor_liability_notice.setWordWrap(True)

        self.verticalLayout.addWidget(self.label_guarantor_liability_notice)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.checkBox_liability_acceptance = QCheckBox(self.widget)
        self.checkBox_liability_acceptance.setObjectName(u"checkBox_liability_acceptance")
        self.checkBox_liability_acceptance.setFont(font1)

        self.horizontalLayout_2.addWidget(self.checkBox_liability_acceptance)

        self.pushButton_sign_as_guarantor = QPushButton(self.widget)
        self.pushButton_sign_as_guarantor.setObjectName(u"pushButton_sign_as_guarantor")

        self.horizontalLayout_2.addWidget(self.pushButton_sign_as_guarantor)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.labelSendToCreatorInfo = QLabel(self.widget)
        self.labelSendToCreatorInfo.setObjectName(u"labelSendToCreatorInfo")
        self.labelSendToCreatorInfo.setFont(font1)

        self.verticalLayout.addWidget(self.labelSendToCreatorInfo)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.labelCreatorEMail = QLabel(self.widget)
        self.labelCreatorEMail.setObjectName(u"labelCreatorEMail")
        self.labelCreatorEMail.setEnabled(False)
        self.labelCreatorEMail.setFont(font1)

        self.horizontalLayout_4.addWidget(self.labelCreatorEMail)

        self.lineEdit_creator_email_address = QLineEdit(self.widget)
        self.lineEdit_creator_email_address.setObjectName(u"lineEdit_creator_email_address")
        self.lineEdit_creator_email_address.setEnabled(False)

        self.horizontalLayout_4.addWidget(self.lineEdit_creator_email_address)


        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.pushButton_save_as_file = QPushButton(self.widget)
        self.pushButton_save_as_file.setObjectName(u"pushButton_save_as_file")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_save_as_file.sizePolicy().hasHeightForWidth())
        self.pushButton_save_as_file.setSizePolicy(sizePolicy)

        self.horizontalLayout.addWidget(self.pushButton_save_as_file)

        self.pushButton_send_as_email = QPushButton(self.widget)
        self.pushButton_send_as_email.setObjectName(u"pushButton_send_as_email")
        self.pushButton_send_as_email.setEnabled(False)
        sizePolicy.setHeightForWidth(self.pushButton_send_as_email.sizePolicy().hasHeightForWidth())
        self.pushButton_send_as_email.setSizePolicy(sizePolicy)

        self.horizontalLayout.addWidget(self.pushButton_send_as_email)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.retranslateUi(FormSignVoucherAsGuarantor)

        QMetaObject.connectSlotsByName(FormSignVoucherAsGuarantor)
    # setupUi

    def retranslateUi(self, FormSignVoucherAsGuarantor):
        FormSignVoucherAsGuarantor.setWindowTitle(QCoreApplication.translate("FormSignVoucherAsGuarantor", u"Sign as Guarantor", None))
        self.label_2.setText(QCoreApplication.translate("FormSignVoucherAsGuarantor", u"Signature of the voucher as Guarantor", None))
        self.label_guarantor_liability_notice.setText(QCoreApplication.translate("FormSignVoucherAsGuarantor", u"Note: By signing, you take responsibility to provide the promised service for the agreed duration in case of the voucher creator's death or incapacity.", None))
        self.checkBox_liability_acceptance.setText(QCoreApplication.translate("FormSignVoucherAsGuarantor", u"I understand the note", None))
        self.pushButton_sign_as_guarantor.setText(QCoreApplication.translate("FormSignVoucherAsGuarantor", u"Sign as Guarantor Now", None))
        self.labelSendToCreatorInfo.setText(QCoreApplication.translate("FormSignVoucherAsGuarantor", u"After signing, you must provide the file to the guarantor.", None))
        self.labelCreatorEMail.setText(QCoreApplication.translate("FormSignVoucherAsGuarantor", u"Email Address of the Creator:", None))
#if QT_CONFIG(tooltip)
        self.lineEdit_creator_email_address.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.lineEdit_creator_email_address.setPlaceholderText(QCoreApplication.translate("FormSignVoucherAsGuarantor", u"Email sending not available yet", None))
#if QT_CONFIG(tooltip)
        self.pushButton_save_as_file.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.pushButton_save_as_file.setText(QCoreApplication.translate("FormSignVoucherAsGuarantor", u"Save as file", None))
#if QT_CONFIG(tooltip)
        self.pushButton_send_as_email.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.pushButton_send_as_email.setText(QCoreApplication.translate("FormSignVoucherAsGuarantor", u"Send as email", None))
    # retranslateUi

