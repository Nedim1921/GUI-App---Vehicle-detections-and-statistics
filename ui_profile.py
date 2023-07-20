# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'interface_profile.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from Custom_Widgets.Widgets import QCustomStackedWidget

import profile_resources_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(466, 529)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QSize(0, 0))
        MainWindow.setMaximumSize(QSize(16777215, 16777215))
        MainWindow.setStyleSheet(u"*{\n"
"	border: none;\n"
"	background-color: transparent;\n"
"	background: transparent;\n"
"	padding: 0;\n"
"	margin: 0;\n"
"	color: #fff;\n"
"}\n"
"\n"
"#profileCentralwidget{\n"
"	background-color: #16191d;\n"
"}\n"
"\n"
"#widget{\n"
"	background-color: #343b47;\n"
"	border-radius: 20px;\n"
"}\n"
"\n"
"QLineEdit{\n"
"	background-color: #1f232a;\n"
"	padding: 5px 3px;\n"
"	border-radius: 5px;\n"
"}\n"
"\n"
"QPushButton{\n"
"	background-color:#1f232a;\n"
"	padding: 10px 5px;\n"
"	border-radius: 10px;\n"
"}\n"
"\n"
"#to_login, #to_register{\n"
"	background-color: transparent;\n"
"}\n"
"\n"
"")
        self.profileCentralwidget = QWidget(MainWindow)
        self.profileCentralwidget.setObjectName(u"profileCentralwidget")
        self.gridLayout = QGridLayout(self.profileCentralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.widget = QWidget(self.profileCentralwidget)
        self.widget.setObjectName(u"widget")
        self.widget.setMinimumSize(QSize(250, 450))
        self.widget.setMaximumSize(QSize(250, 450))
        self.verticalLayout = QVBoxLayout(self.widget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.closeBtn = QPushButton(self.widget)
        self.closeBtn.setObjectName(u"closeBtn")
        sizePolicy.setHeightForWidth(self.closeBtn.sizePolicy().hasHeightForWidth())
        self.closeBtn.setSizePolicy(sizePolicy)
        self.closeBtn.setMinimumSize(QSize(30, 30))
        self.closeBtn.setMaximumSize(QSize(30, 30))
        icon = QIcon()
        icon.addFile(u":/icons/icons/x-circle.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.closeBtn.setIcon(icon)
        self.closeBtn.setIconSize(QSize(24, 24))

        self.verticalLayout.addWidget(self.closeBtn, 0, Qt.AlignRight)

        self.stackedWidget = QCustomStackedWidget(self.widget)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.registerPage = QWidget()
        self.registerPage.setObjectName(u"registerPage")
        self.verticalLayout_3 = QVBoxLayout(self.registerPage)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(6, 0, 6, 6)
        self.label = QLabel(self.registerPage)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(50, 50))
        self.label.setMaximumSize(QSize(50, 50))
        self.label.setPixmap(QPixmap(u":/icons/icons/user-plus.svg"))
        self.label.setScaledContents(True)

        self.verticalLayout_3.addWidget(self.label, 0, Qt.AlignHCenter)

        self.label_2 = QLabel(self.registerPage)
        self.label_2.setObjectName(u"label_2")
        font = QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)

        self.verticalLayout_3.addWidget(self.label_2, 0, Qt.AlignHCenter|Qt.AlignTop)

        self.label_3 = QLabel(self.registerPage)
        self.label_3.setObjectName(u"label_3")

        self.verticalLayout_3.addWidget(self.label_3, 0, Qt.AlignHCenter|Qt.AlignTop)

        self.frame = QFrame(self.registerPage)
        self.frame.setObjectName(u"frame")
        self.frame.setMinimumSize(QSize(0, 150))
        self.frame.setMaximumSize(QSize(16777215, 150))
        self.frame.setStyleSheet(u"")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_4 = QVBoxLayout(self.frame)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(6, 6, 6, 6)
        self.username_1 = QLineEdit(self.frame)
        self.username_1.setObjectName(u"username_1")

        self.verticalLayout_4.addWidget(self.username_1)

        self.password_1 = QLineEdit(self.frame)
        self.password_1.setObjectName(u"password_1")
        self.password_1.setEchoMode(QLineEdit.Password)

        self.verticalLayout_4.addWidget(self.password_1)

        self.confirmpassword = QLineEdit(self.frame)
        self.confirmpassword.setObjectName(u"confirmpassword")
        self.confirmpassword.setEchoMode(QLineEdit.Password)

        self.verticalLayout_4.addWidget(self.confirmpassword)


        self.verticalLayout_3.addWidget(self.frame)

        self.registerBtn = QPushButton(self.registerPage)
        self.registerBtn.setObjectName(u"registerBtn")
        sizePolicy1 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.registerBtn.sizePolicy().hasHeightForWidth())
        self.registerBtn.setSizePolicy(sizePolicy1)
        self.registerBtn.setMinimumSize(QSize(0, 0))
        self.registerBtn.setMaximumSize(QSize(100, 100))
        font1 = QFont()
        font1.setPointSize(9)
        font1.setBold(True)
        font1.setWeight(75)
        self.registerBtn.setFont(font1)
        icon1 = QIcon()
        icon1.addFile(u":/icons/icons/log-in.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.registerBtn.setIcon(icon1)

        self.verticalLayout_3.addWidget(self.registerBtn, 0, Qt.AlignHCenter)

        self.to_login = QPushButton(self.registerPage)
        self.to_login.setObjectName(u"to_login")
        self.to_login.setMinimumSize(QSize(0, 0))
        self.to_login.setMaximumSize(QSize(16777215, 50))
        font2 = QFont()
        font2.setUnderline(True)
        self.to_login.setFont(font2)

        self.verticalLayout_3.addWidget(self.to_login, 0, Qt.AlignHCenter)

        self.label_4 = QLabel(self.registerPage)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setMinimumSize(QSize(0, 0))

        self.verticalLayout_3.addWidget(self.label_4, 0, Qt.AlignHCenter)

        self.stackedWidget.addWidget(self.registerPage)
        self.loginPage = QWidget()
        self.loginPage.setObjectName(u"loginPage")
        self.verticalLayout_6 = QVBoxLayout(self.loginPage)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(6, 0, 6, 6)
        self.label_5 = QLabel(self.loginPage)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setMinimumSize(QSize(50, 50))
        self.label_5.setMaximumSize(QSize(50, 50))
        self.label_5.setPixmap(QPixmap(u":/icons/icons/user-check.svg"))
        self.label_5.setScaledContents(True)

        self.verticalLayout_6.addWidget(self.label_5, 0, Qt.AlignHCenter)

        self.label_6 = QLabel(self.loginPage)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setFont(font)

        self.verticalLayout_6.addWidget(self.label_6, 0, Qt.AlignHCenter)

        self.label_7 = QLabel(self.loginPage)
        self.label_7.setObjectName(u"label_7")

        self.verticalLayout_6.addWidget(self.label_7, 0, Qt.AlignHCenter)

        self.frame_2 = QFrame(self.loginPage)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setMinimumSize(QSize(0, 150))
        self.frame_2.setMaximumSize(QSize(16777215, 150))
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.verticalLayout_5 = QVBoxLayout(self.frame_2)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.username_2 = QLineEdit(self.frame_2)
        self.username_2.setObjectName(u"username_2")

        self.verticalLayout_5.addWidget(self.username_2)

        self.password_2 = QLineEdit(self.frame_2)
        self.password_2.setObjectName(u"password_2")
        self.password_2.setEchoMode(QLineEdit.Password)

        self.verticalLayout_5.addWidget(self.password_2)


        self.verticalLayout_6.addWidget(self.frame_2)

        self.loginBtn = QPushButton(self.loginPage)
        self.loginBtn.setObjectName(u"loginBtn")
        self.loginBtn.setFont(font1)
        self.loginBtn.setIcon(icon1)

        self.verticalLayout_6.addWidget(self.loginBtn, 0, Qt.AlignHCenter)

        self.to_register = QPushButton(self.loginPage)
        self.to_register.setObjectName(u"to_register")
        self.to_register.setMinimumSize(QSize(0, 0))
        self.to_register.setMaximumSize(QSize(16777215, 50))
        self.to_register.setFont(font2)

        self.verticalLayout_6.addWidget(self.to_register, 0, Qt.AlignHCenter)

        self.label_8 = QLabel(self.loginPage)
        self.label_8.setObjectName(u"label_8")

        self.verticalLayout_6.addWidget(self.label_8, 0, Qt.AlignHCenter)

        self.stackedWidget.addWidget(self.loginPage)

        self.verticalLayout.addWidget(self.stackedWidget)


        self.gridLayout.addWidget(self.widget, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.profileCentralwidget)

        self.retranslateUi(MainWindow)

        self.stackedWidget.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.closeBtn.setText("")
        self.label.setText("")
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Sign Up", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Enter your information below", None))
        self.username_1.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Username", None))
        self.password_1.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Password", None))
        self.confirmpassword.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Confirm Password", None))
        self.registerBtn.setText(QCoreApplication.translate("MainWindow", u"Register", None))
        self.to_login.setText(QCoreApplication.translate("MainWindow", u"Already registered? Login", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Open CV", None))
        self.label_5.setText("")
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"Log In", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"Enter your information below", None))
        self.username_2.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Username", None))
        self.password_2.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Password", None))
        self.loginBtn.setText(QCoreApplication.translate("MainWindow", u"Login", None))
        self.to_register.setText(QCoreApplication.translate("MainWindow", u"Not registered? Register", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"Open CV", None))
    # retranslateUi

