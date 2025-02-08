# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
##
## Created by: Qt User Interface Compiler version 6.8.1
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
from PySide6.QtWidgets import (QApplication, QComboBox, QGroupBox, QHBoxLayout,
    QLabel, QLineEdit, QMainWindow, QPushButton,
    QSizePolicy, QSpacerItem, QTextEdit, QVBoxLayout,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(600, 400)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)

        self.cb_port = QComboBox(self.centralwidget)
        self.cb_port.setObjectName(u"cb_port")

        self.horizontalLayout.addWidget(self.cb_port)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_2.addWidget(self.label_2)

        self.cb_baudrate = QComboBox(self.centralwidget)
        self.cb_baudrate.setObjectName(u"cb_baudrate")

        self.horizontalLayout_2.addWidget(self.cb_baudrate)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer)

        self.btn_connect = QPushButton(self.centralwidget)
        self.btn_connect.setObjectName(u"btn_connect")

        self.horizontalLayout_3.addWidget(self.btn_connect)

        self.btn_refresh = QPushButton(self.centralwidget)
        self.btn_refresh.setObjectName(u"btn_refresh")

        self.horizontalLayout_3.addWidget(self.btn_refresh)

        self.indicator = QLabel(self.centralwidget)
        self.indicator.setObjectName(u"indicator")
        self.indicator.setMinimumSize(QSize(20, 20))
        self.indicator.setMaximumSize(QSize(20, 20))
        self.indicator.setStyleSheet(u"background-color: red; border-radius: 10px;")

        self.horizontalLayout_3.addWidget(self.indicator)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.gb_send = QGroupBox(self.centralwidget)
        self.gb_send.setObjectName(u"gb_send")
        self.verticalLayout_2 = QVBoxLayout(self.gb_send)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.txt_send = QLineEdit(self.gb_send)
        self.txt_send.setObjectName(u"txt_send")

        self.verticalLayout_2.addWidget(self.txt_send)

        self.btn_send = QPushButton(self.gb_send)
        self.btn_send.setObjectName(u"btn_send")

        self.verticalLayout_2.addWidget(self.btn_send)


        self.verticalLayout.addWidget(self.gb_send)

        self.gb_receive = QGroupBox(self.centralwidget)
        self.gb_receive.setObjectName(u"gb_receive")
        self.verticalLayout_3 = QVBoxLayout(self.gb_receive)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.txt_receive = QTextEdit(self.gb_receive)
        self.txt_receive.setObjectName(u"txt_receive")
        self.txt_receive.setReadOnly(True)

        self.verticalLayout_3.addWidget(self.txt_receive)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.btn_clear = QPushButton(self.gb_receive)
        self.btn_clear.setObjectName(u"btn_clear")

        self.horizontalLayout_4.addWidget(self.btn_clear)

        self.btn_save_csv = QPushButton(self.gb_receive)
        self.btn_save_csv.setObjectName(u"btn_save_csv")

        self.horizontalLayout_4.addWidget(self.btn_save_csv)


        self.verticalLayout_3.addLayout(self.horizontalLayout_4)


        self.verticalLayout.addWidget(self.gb_receive)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Serial Communication", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Port:", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Baudrate:", None))
        self.btn_connect.setText(QCoreApplication.translate("MainWindow", u"Connect", None))
        self.btn_refresh.setText(QCoreApplication.translate("MainWindow", u"Refresh", None))
        self.gb_send.setTitle(QCoreApplication.translate("MainWindow", u"Send Data", None))
        self.btn_send.setText(QCoreApplication.translate("MainWindow", u"Send", None))
        self.gb_receive.setTitle(QCoreApplication.translate("MainWindow", u"Received Data", None))
        self.btn_clear.setText(QCoreApplication.translate("MainWindow", u"Clear", None))
        self.btn_save_csv.setText(QCoreApplication.translate("MainWindow", u"Save CSV", None))
    # retranslateUi

