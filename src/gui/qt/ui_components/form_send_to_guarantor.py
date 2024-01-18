# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form_send_to_guarantor.ui'
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

class Ui_FormSendToGuarantor(object):
    def setupUi(self, FormSendToGuarantor):
        if not FormSendToGuarantor.objectName():
            FormSendToGuarantor.setObjectName(u"FormSendToGuarantor")
        FormSendToGuarantor.resize(688, 245)
        self.layoutWidget = QWidget(FormSendToGuarantor)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(20, 9, 661, 221))
        self.verticalLayout = QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.label_user_id = QLabel(self.layoutWidget)
        self.label_user_id.setObjectName(u"label_user_id")
        font = QFont()
        font.setPointSize(11)
        self.label_user_id.setFont(font)
        self.label_user_id.setAlignment(Qt.AlignBottom|Qt.AlignLeading|Qt.AlignLeft)

        self.verticalLayout.addWidget(self.label_user_id)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.lineEdit_user_ID = QLineEdit(self.layoutWidget)
        self.lineEdit_user_ID.setObjectName(u"lineEdit_user_ID")
        self.lineEdit_user_ID.setReadOnly(True)

        self.horizontalLayout_3.addWidget(self.lineEdit_user_ID)

        self.pushButton_copy_user_ID = QPushButton(self.layoutWidget)
        self.pushButton_copy_user_ID.setObjectName(u"pushButton_copy_user_ID")
        icon = QIcon()
        iconThemeName = u"edit-copy"
        if QIcon.hasThemeIcon(iconThemeName):
            icon = QIcon.fromTheme(iconThemeName)
        else:
            icon.addFile(u".", QSize(), QIcon.Normal, QIcon.Off)

        self.pushButton_copy_user_ID.setIcon(icon)
        self.pushButton_copy_user_ID.setIconSize(QSize(18, 18))

        self.horizontalLayout_3.addWidget(self.pushButton_copy_user_ID)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.label_guarantor_ID = QLabel(self.layoutWidget)
        self.label_guarantor_ID.setObjectName(u"label_guarantor_ID")
        self.label_guarantor_ID.setFont(font)
        self.label_guarantor_ID.setAlignment(Qt.AlignBottom|Qt.AlignLeading|Qt.AlignLeft)

        self.verticalLayout.addWidget(self.label_guarantor_ID)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.lineEdit_guarantor_ID = QLineEdit(self.layoutWidget)
        self.lineEdit_guarantor_ID.setObjectName(u"lineEdit_guarantor_ID")

        self.horizontalLayout_2.addWidget(self.lineEdit_guarantor_ID)

        self.label_guarantor_id_check = QLabel(self.layoutWidget)
        self.label_guarantor_id_check.setObjectName(u"label_guarantor_id_check")
        self.label_guarantor_id_check.setMinimumSize(QSize(30, 30))
        self.label_guarantor_id_check.setMaximumSize(QSize(30, 16777215))
        font1 = QFont()
        font1.setPointSize(12)
        self.label_guarantor_id_check.setFont(font1)

        self.horizontalLayout_2.addWidget(self.label_guarantor_id_check)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label = QLabel(self.layoutWidget)
        self.label.setObjectName(u"label")
        self.label.setEnabled(False)
        self.label.setFont(font)

        self.horizontalLayout_4.addWidget(self.label)

        self.lineEdit_guarantor_email_address = QLineEdit(self.layoutWidget)
        self.lineEdit_guarantor_email_address.setObjectName(u"lineEdit_guarantor_email_address")
        self.lineEdit_guarantor_email_address.setEnabled(False)

        self.horizontalLayout_4.addWidget(self.lineEdit_guarantor_email_address)

        self.label_guarantor_id_check_2 = QLabel(self.layoutWidget)
        self.label_guarantor_id_check_2.setObjectName(u"label_guarantor_id_check_2")
        self.label_guarantor_id_check_2.setMinimumSize(QSize(30, 30))
        self.label_guarantor_id_check_2.setMaximumSize(QSize(30, 16777215))
        self.label_guarantor_id_check_2.setFont(font1)

        self.horizontalLayout_4.addWidget(self.label_guarantor_id_check_2)


        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.checkBox_encrypt_voucher = QCheckBox(self.layoutWidget)
        self.checkBox_encrypt_voucher.setObjectName(u"checkBox_encrypt_voucher")
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.checkBox_encrypt_voucher.sizePolicy().hasHeightForWidth())
        self.checkBox_encrypt_voucher.setSizePolicy(sizePolicy)
        self.checkBox_encrypt_voucher.setFont(font)
        self.checkBox_encrypt_voucher.setChecked(True)

        self.horizontalLayout.addWidget(self.checkBox_encrypt_voucher)

        self.pushButton_save_as_file = QPushButton(self.layoutWidget)
        self.pushButton_save_as_file.setObjectName(u"pushButton_save_as_file")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.pushButton_save_as_file.sizePolicy().hasHeightForWidth())
        self.pushButton_save_as_file.setSizePolicy(sizePolicy1)

        self.horizontalLayout.addWidget(self.pushButton_save_as_file)

        self.pushButton_send_as_email = QPushButton(self.layoutWidget)
        self.pushButton_send_as_email.setObjectName(u"pushButton_send_as_email")
        self.pushButton_send_as_email.setEnabled(False)
        sizePolicy1.setHeightForWidth(self.pushButton_send_as_email.sizePolicy().hasHeightForWidth())
        self.pushButton_send_as_email.setSizePolicy(sizePolicy1)

        self.horizontalLayout.addWidget(self.pushButton_send_as_email)

        self.label_ = QLabel(self.layoutWidget)
        self.label_.setObjectName(u"label_")
        self.label_.setMinimumSize(QSize(30, 30))
        self.label_.setMaximumSize(QSize(30, 16777215))

        self.horizontalLayout.addWidget(self.label_)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.retranslateUi(FormSendToGuarantor)

        QMetaObject.connectSlotsByName(FormSendToGuarantor)
    # setupUi

    def retranslateUi(self, FormSendToGuarantor):
        FormSendToGuarantor.setWindowTitle(QCoreApplication.translate("FormSendToGuarantor", u"Von anderen B\u00fcrgen unterschreiben lassen", None))
        self.label_user_id.setText(QCoreApplication.translate("FormSendToGuarantor", u"Eigene Nutzer ID (Adresse zum Empfangen))", None))
        self.lineEdit_user_ID.setPlaceholderText("")
#if QT_CONFIG(tooltip)
        self.pushButton_copy_user_ID.setToolTip(QCoreApplication.translate("FormSendToGuarantor", u"Kopieren", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_copy_user_ID.setText("")
        self.label_guarantor_ID.setText(QCoreApplication.translate("FormSendToGuarantor", u"B\u00fcrgen ID (Adresse des B\u00fcrgen der unterzeichnen soll)", None))
#if QT_CONFIG(tooltip)
        self.lineEdit_guarantor_ID.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.lineEdit_guarantor_ID.setPlaceholderText("")
#if QT_CONFIG(tooltip)
        self.label_guarantor_id_check.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.label_guarantor_id_check.setText("")
        self.label.setText(QCoreApplication.translate("FormSendToGuarantor", u"EMail Adresse des B\u00fcrgen:", None))
#if QT_CONFIG(tooltip)
        self.lineEdit_guarantor_email_address.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.lineEdit_guarantor_email_address.setPlaceholderText(QCoreApplication.translate("FormSendToGuarantor", u"EMail Versand noch nicht m\u00f6glich", None))
        self.label_guarantor_id_check_2.setText("")
        self.checkBox_encrypt_voucher.setText(QCoreApplication.translate("FormSendToGuarantor", u"Daten verschl\u00fcsseln", None))
#if QT_CONFIG(tooltip)
        self.pushButton_save_as_file.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.pushButton_save_as_file.setText(QCoreApplication.translate("FormSendToGuarantor", u"Als Datei Speichern", None))
#if QT_CONFIG(tooltip)
        self.pushButton_send_as_email.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.pushButton_send_as_email.setText(QCoreApplication.translate("FormSendToGuarantor", u"Als E-Mail versenden", None))
        self.label_.setText("")
    # retranslateUi

