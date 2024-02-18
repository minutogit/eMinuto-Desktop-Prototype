# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form_send_minuto.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

class Ui_FormSendMinuto(object):
    def setupUi(self, FormSendMinuto):
        if not FormSendMinuto.objectName():
            FormSendMinuto.setObjectName(u"FormSendMinuto")
        FormSendMinuto.resize(687, 325)
        self.label_recipient_id_check = QLabel(FormSendMinuto)
        self.label_recipient_id_check.setObjectName(u"label_recipient_id_check")
        self.label_recipient_id_check.setGeometry(QRect(328, 50, 30, 30))
        self.label_recipient_id_check.setMinimumSize(QSize(30, 30))
        self.label_recipient_id_check.setMaximumSize(QSize(30, 16777215))
        font = QFont()
        font.setPointSize(12)
        self.label_recipient_id_check.setFont(font)
        self.widget = QWidget(FormSendMinuto)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(10, 20, 661, 281))
        self.verticalLayout_3 = QVBoxLayout(self.widget)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(self.widget)
        self.label.setObjectName(u"label")
        self.label.setMaximumSize(QSize(16777215, 30))
        font1 = QFont()
        font1.setPointSize(13)
        font1.setBold(True)
        self.label.setFont(font1)

        self.verticalLayout_3.addWidget(self.label)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label_recipient_id = QLabel(self.widget)
        self.label_recipient_id.setObjectName(u"label_recipient_id")
        font2 = QFont()
        font2.setPointSize(11)
        self.label_recipient_id.setFont(font2)

        self.verticalLayout.addWidget(self.label_recipient_id)

        self.label_purpose = QLabel(self.widget)
        self.label_purpose.setObjectName(u"label_purpose")
        self.label_purpose.setFont(font2)

        self.verticalLayout.addWidget(self.label_purpose)

        self.label_transfer_amount_text = QLabel(self.widget)
        self.label_transfer_amount_text.setObjectName(u"label_transfer_amount_text")
        self.label_transfer_amount_text.setFont(font2)

        self.verticalLayout.addWidget(self.label_transfer_amount_text)


        self.horizontalLayout_2.addLayout(self.verticalLayout)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.lineEdit_recipient_id = QLineEdit(self.widget)
        self.lineEdit_recipient_id.setObjectName(u"lineEdit_recipient_id")
        self.lineEdit_recipient_id.setMaximumSize(QSize(16777215, 30))
        font3 = QFont()
        font3.setPointSize(10)
        self.lineEdit_recipient_id.setFont(font3)

        self.verticalLayout_2.addWidget(self.lineEdit_recipient_id)

        self.lineEdit_purpose = QLineEdit(self.widget)
        self.lineEdit_purpose.setObjectName(u"lineEdit_purpose")

        self.verticalLayout_2.addWidget(self.lineEdit_purpose)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.lineEdit_transfer_amount = QLineEdit(self.widget)
        self.lineEdit_transfer_amount.setObjectName(u"lineEdit_transfer_amount")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_transfer_amount.sizePolicy().hasHeightForWidth())
        self.lineEdit_transfer_amount.setSizePolicy(sizePolicy)
        self.lineEdit_transfer_amount.setMinimumSize(QSize(50, 0))
        self.lineEdit_transfer_amount.setMaximumSize(QSize(100, 40))
        self.lineEdit_transfer_amount.setFont(font2)
        self.lineEdit_transfer_amount.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout.addWidget(self.lineEdit_transfer_amount)

        self.label_amount_currency_text = QLabel(self.widget)
        self.label_amount_currency_text.setObjectName(u"label_amount_currency_text")
        self.label_amount_currency_text.setFont(font2)

        self.horizontalLayout.addWidget(self.label_amount_currency_text)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)


        self.verticalLayout_2.addLayout(self.horizontalLayout)


        self.horizontalLayout_2.addLayout(self.verticalLayout_2)


        self.verticalLayout_3.addLayout(self.horizontalLayout_2)

        self.pushButton_Send_Minuto = QPushButton(self.widget)
        self.pushButton_Send_Minuto.setObjectName(u"pushButton_Send_Minuto")
        self.pushButton_Send_Minuto.setFont(font2)

        self.verticalLayout_3.addWidget(self.pushButton_Send_Minuto)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_note_text = QLabel(self.widget)
        self.label_note_text.setObjectName(u"label_note_text")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.label_note_text.sizePolicy().hasHeightForWidth())
        self.label_note_text.setSizePolicy(sizePolicy1)
        self.label_note_text.setMinimumSize(QSize(0, 100))
        font4 = QFont()
        font4.setPointSize(11)
        font4.setBold(True)
        self.label_note_text.setFont(font4)
        self.label_note_text.setWordWrap(False)

        self.horizontalLayout_3.addWidget(self.label_note_text)

        self.label_note = QLabel(self.widget)
        self.label_note.setObjectName(u"label_note")
        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.label_note.sizePolicy().hasHeightForWidth())
        self.label_note.setSizePolicy(sizePolicy2)
        self.label_note.setFont(font2)
        self.label_note.setWordWrap(True)

        self.horizontalLayout_3.addWidget(self.label_note)


        self.verticalLayout_3.addLayout(self.horizontalLayout_3)


        self.retranslateUi(FormSendMinuto)

        QMetaObject.connectSlotsByName(FormSendMinuto)
    # setupUi

    def retranslateUi(self, FormSendMinuto):
        FormSendMinuto.setWindowTitle(QCoreApplication.translate("FormSendMinuto", u"Minuto versenden", None))
#if QT_CONFIG(tooltip)
        self.label_recipient_id_check.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.label_recipient_id_check.setText("")
        self.label.setText(QCoreApplication.translate("FormSendMinuto", u"Minuto versenden", None))
        self.label_recipient_id.setText(QCoreApplication.translate("FormSendMinuto", u"Empf\u00e4nger ID (Adresse):", None))
        self.label_purpose.setText(QCoreApplication.translate("FormSendMinuto", u"Zweck:", None))
        self.label_transfer_amount_text.setText(QCoreApplication.translate("FormSendMinuto", u"Betrag:", None))
        self.lineEdit_transfer_amount.setInputMask("")
        self.label_amount_currency_text.setText(QCoreApplication.translate("FormSendMinuto", u"Minuto", None))
        self.pushButton_Send_Minuto.setText(QCoreApplication.translate("FormSendMinuto", u"Minuto jetzt versenden", None))
        self.label_note_text.setText(QCoreApplication.translate("FormSendMinuto", u"Hinweis:", None))
        self.label_note.setText(QCoreApplication.translate("FormSendMinuto", u"Es wird eine Datei erstellt die dann dem Empf\u00e4nger gesendet werden muss. (per E-Mail, Messenger, Datentr\u00e4ger, ..)", None))
    # retranslateUi

