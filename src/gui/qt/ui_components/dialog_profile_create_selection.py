# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dialog_profile_create_selection.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QPushButton, QSizePolicy,
    QWidget)

class Ui_Dialog_Profile_Create_Selection(object):
    def setupUi(self, Dialog_Profile_Create_Selection):
        if not Dialog_Profile_Create_Selection.objectName():
            Dialog_Profile_Create_Selection.setObjectName(u"Dialog_Profile_Create_Selection")
        Dialog_Profile_Create_Selection.resize(259, 90)
        self.pushButton_create_new_profile = QPushButton(Dialog_Profile_Create_Selection)
        self.pushButton_create_new_profile.setObjectName(u"pushButton_create_new_profile")
        self.pushButton_create_new_profile.setGeometry(QRect(10, 10, 231, 21))
        self.pushButton_restore_exisitin_profile = QPushButton(Dialog_Profile_Create_Selection)
        self.pushButton_restore_exisitin_profile.setObjectName(u"pushButton_restore_exisitin_profile")
        self.pushButton_restore_exisitin_profile.setGeometry(QRect(10, 50, 231, 23))

        self.retranslateUi(Dialog_Profile_Create_Selection)

        QMetaObject.connectSlotsByName(Dialog_Profile_Create_Selection)
    # setupUi

    def retranslateUi(self, Dialog_Profile_Create_Selection):
        Dialog_Profile_Create_Selection.setWindowTitle(QCoreApplication.translate("Dialog_Profile_Create_Selection", u"Dialogue", None))
        self.pushButton_create_new_profile.setText(QCoreApplication.translate("Dialog_Profile_Create_Selection", u"Create New Profile", None))
        self.pushButton_restore_exisitin_profile.setText(QCoreApplication.translate("Dialog_Profile_Create_Selection", u"Restore Old Profile", None))
    # retranslateUi

