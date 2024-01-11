# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dialog_generate_profile.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QFrame, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QSizePolicy,
    QWidget)

class Ui_DialogGenerateProfile(object):
    def setupUi(self, DialogGenerateProfile):
        if not DialogGenerateProfile.objectName():
            DialogGenerateProfile.setObjectName(u"DialogGenerateProfile")
        DialogGenerateProfile.resize(712, 474)
        self.btn_new_seed_words = QPushButton(DialogGenerateProfile)
        self.btn_new_seed_words.setObjectName(u"btn_new_seed_words")
        self.btn_new_seed_words.setGeometry(QRect(260, 260, 171, 23))
        self.label = QLabel(DialogGenerateProfile)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(10, 200, 321, 16))
        self.label_2 = QLabel(DialogGenerateProfile)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(10, 290, 331, 16))
        font = QFont()
        font.setPointSize(11)
        self.label_2.setFont(font)
        self.btn_create_profile = QPushButton(DialogGenerateProfile)
        self.btn_create_profile.setObjectName(u"btn_create_profile")
        self.btn_create_profile.setGeometry(QRect(270, 440, 161, 23))
        self.lineEdit_profile_name = QLineEdit(DialogGenerateProfile)
        self.lineEdit_profile_name.setObjectName(u"lineEdit_profile_name")
        self.lineEdit_profile_name.setGeometry(QRect(10, 30, 331, 26))
        self.label_3 = QLabel(DialogGenerateProfile)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(10, 10, 331, 16))
        self.label_3.setFont(font)
        self.label_info = QLabel(DialogGenerateProfile)
        self.label_info.setObjectName(u"label_info")
        self.label_info.setGeometry(QRect(10, 360, 691, 71))
        self.label_info.setFont(font)
        self.label_info.setAutoFillBackground(False)
        self.label_info.setFrameShape(QFrame.Box)
        self.label_info.setFrameShadow(QFrame.Sunken)
        self.label_info.setLineWidth(2)
        self.label_info.setWordWrap(True)
        self.layoutWidget = QWidget(DialogGenerateProfile)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(10, 80, 691, 30))
        self.horizontalLayout = QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.lineEdit_organization = QLineEdit(self.layoutWidget)
        self.lineEdit_organization.setObjectName(u"lineEdit_organization")

        self.horizontalLayout.addWidget(self.lineEdit_organization)

        self.lineEdit_first_name = QLineEdit(self.layoutWidget)
        self.lineEdit_first_name.setObjectName(u"lineEdit_first_name")

        self.horizontalLayout.addWidget(self.lineEdit_first_name)

        self.lineEdit_last_name = QLineEdit(self.layoutWidget)
        self.lineEdit_last_name.setObjectName(u"lineEdit_last_name")

        self.horizontalLayout.addWidget(self.lineEdit_last_name)

        self.layoutWidget1 = QWidget(DialogGenerateProfile)
        self.layoutWidget1.setObjectName(u"layoutWidget1")
        self.layoutWidget1.setGeometry(QRect(10, 60, 691, 20))
        self.horizontalLayout_2 = QHBoxLayout(self.layoutWidget1)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.label_6 = QLabel(self.layoutWidget1)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setFont(font)

        self.horizontalLayout_2.addWidget(self.label_6)

        self.label_4 = QLabel(self.layoutWidget1)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setFont(font)

        self.horizontalLayout_2.addWidget(self.label_4)

        self.label_5 = QLabel(self.layoutWidget1)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setFont(font)

        self.horizontalLayout_2.addWidget(self.label_5)

        self.layoutWidget2 = QWidget(DialogGenerateProfile)
        self.layoutWidget2.setObjectName(u"layoutWidget2")
        self.layoutWidget2.setGeometry(QRect(10, 140, 461, 30))
        self.horizontalLayout_3 = QHBoxLayout(self.layoutWidget2)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.lineEdit_password = QLineEdit(self.layoutWidget2)
        self.lineEdit_password.setObjectName(u"lineEdit_password")
        self.lineEdit_password.setEchoMode(QLineEdit.Password)
        self.lineEdit_password.setClearButtonEnabled(False)

        self.horizontalLayout_3.addWidget(self.lineEdit_password)

        self.lineEdit_password_confirmed = QLineEdit(self.layoutWidget2)
        self.lineEdit_password_confirmed.setObjectName(u"lineEdit_password_confirmed")
        self.lineEdit_password_confirmed.setAutoFillBackground(False)
        self.lineEdit_password_confirmed.setEchoMode(QLineEdit.Password)

        self.horizontalLayout_3.addWidget(self.lineEdit_password_confirmed)

        self.layoutWidget3 = QWidget(DialogGenerateProfile)
        self.layoutWidget3.setObjectName(u"layoutWidget3")
        self.layoutWidget3.setGeometry(QRect(10, 120, 461, 19))
        self.horizontalLayout_4 = QHBoxLayout(self.layoutWidget3)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.label_7 = QLabel(self.layoutWidget3)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setFont(font)

        self.horizontalLayout_4.addWidget(self.label_7)

        self.label_8 = QLabel(self.layoutWidget3)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setFont(font)

        self.horizontalLayout_4.addWidget(self.label_8)

        self.lineEdit_new_seed = QLineEdit(DialogGenerateProfile)
        self.lineEdit_new_seed.setObjectName(u"lineEdit_new_seed")
        self.lineEdit_new_seed.setGeometry(QRect(10, 220, 691, 32))
        self.lineEdit_new_seed.setFont(font)
        self.lineEdit_new_seed.setReadOnly(True)
        self.lineEdit_new_seed_confirmed = QLineEdit(DialogGenerateProfile)
        self.lineEdit_new_seed_confirmed.setObjectName(u"lineEdit_new_seed_confirmed")
        self.lineEdit_new_seed_confirmed.setGeometry(QRect(10, 310, 691, 32))
        self.lineEdit_new_seed_confirmed.setFont(font)
        self.lineEdit_new_seed_confirmed.setReadOnly(False)

        self.retranslateUi(DialogGenerateProfile)

        QMetaObject.connectSlotsByName(DialogGenerateProfile)
    # setupUi

    def retranslateUi(self, DialogGenerateProfile):
        DialogGenerateProfile.setWindowTitle(QCoreApplication.translate("DialogGenerateProfile", u"Profil generieren", None))
        self.btn_new_seed_words.setText(QCoreApplication.translate("DialogGenerateProfile", u"Neue W\u00f6rter generieren", None))
        self.label.setText(QCoreApplication.translate("DialogGenerateProfile", u"Schl\u00fcsselw\u00f6rter", None))
        self.label_2.setText(QCoreApplication.translate("DialogGenerateProfile", u"Schl\u00fcsselw\u00f6rter zur Best\u00e4tigung nochmal eingeben", None))
        self.btn_create_profile.setText(QCoreApplication.translate("DialogGenerateProfile", u"Profil erstellen", None))
        self.label_3.setText(QCoreApplication.translate("DialogGenerateProfile", u"Profilname (beliebig w\u00e4hlbar)", None))
        self.label_info.setText(QCoreApplication.translate("DialogGenerateProfile", u"Diese W\u00f6rter erzeugen eine digitale Identit\u00e4t. Aufschreiben und geheim halten. Die Worte dienen auch zur Profil- und Passwortwiederherstellung.", None))
        self.lineEdit_organization.setText("")
        self.label_6.setText(QCoreApplication.translate("DialogGenerateProfile", u"Organisation / Firma:", None))
        self.label_4.setText(QCoreApplication.translate("DialogGenerateProfile", u"Rufname", None))
        self.label_5.setText(QCoreApplication.translate("DialogGenerateProfile", u"Familienname", None))
        self.lineEdit_password.setText("")
        self.lineEdit_password_confirmed.setText("")
        self.label_7.setText(QCoreApplication.translate("DialogGenerateProfile", u"Passwort", None))
        self.label_8.setText(QCoreApplication.translate("DialogGenerateProfile", u"Passwort wiederholen", None))
    # retranslateUi

