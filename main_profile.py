import sys
import os
from ui_profile import *
from Custom_Widgets.Widgets import *
import mysql.connector
from PySide2.QtWidgets import QMessageBox
import bcrypt
from db_connection import get_db_connection

class ProfileMainWindow(QMainWindow):
    usernameChanged = Signal(str, int)
    closed = Signal()
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        loadJsonStyle(self, self.ui, jsonFiles = {
        "styleProfile.json",
        })
        
        self.ui.registerBtn.clicked.connect(self.register)
        self.ui.loginBtn.clicked.connect(self.login)
        self.setWindowFlag(Qt.FramelessWindowHint)
        

    def on_main_window_resized(self, size: QSize):
        main_width = size.width()
        main_height = size.height()
        
        profile_width = main_width * 0.5
        profile_height = main_height * 0.5

        profile_x = (main_width - profile_width) / 2
        profile_y = (main_height - profile_height) / 2
        self.setGeometry(profile_x, profile_y, profile_width, profile_height)

    def register(self):
        username = self.ui.username_1.text()
        password = self.ui.password_1.text()
        confirmpassword = self.ui.confirmpassword.text()

        if len(username) == 0 or len(password) == 0 or len(confirmpassword) == 0:
            QMessageBox.warning(self, "Warning", "<font color='white'>Please fill in all inputs.</font>", QMessageBox.Ok)
        elif password != confirmpassword:
            QMessageBox.warning(self, "Warning", "<font color='white'>Password do not match!</font>", QMessageBox.Ok)
        elif len(password) < 4:
            QMessageBox.warning(self, "Warning", "<font color='white'>Password must be at least 4 characters long.</font>", QMessageBox.Ok)
        else:
            connection = get_db_connection()
            mycursor = connection.cursor()
            sql = "SELECT * FROM users WHERE username = %s"
            values = (username,)
            mycursor.execute(sql, values)
            result = mycursor.fetchone()

            if result:
                QMessageBox.warning(self, "Warning", "<font color='white'>Username is already taken!</font>", QMessageBox.Ok)
            else:
                salt = bcrypt.gensalt()
                # Heširanje lozinke
                hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

                sql = "INSERT INTO users (username, password) VALUES (%s, %s)"
                values = (username, hashed_password)
                mycursor.execute(sql, values)
                connection.commit()
                QMessageBox.information(self, "Information", "<font color='white'>Successful registration</font>")

                self.ui.stackedWidget.setCurrentIndex(1)

    def login(self):
        username = self.ui.username_2.text()
        password = self.ui.password_2.text()
        
        if len(username) == 0 or len(password) == 0:
            QMessageBox.warning(self, "Warning", "<font color='white'>Please input all fields.</font>", QMessageBox.Ok)
        elif self.check_user(username, password):
            user_id = self.get_user_id(username)
            if user_id is not None:
                QMessageBox.information(self, "Information", "<font color='white'>Successful login.</font>", QMessageBox.Ok)
                self.usernameChanged.emit(username, user_id)  
                self.close()
            else:
                QMessageBox.warning(self, "Warning", "<font color='white'>User ID not found.</font>", QMessageBox.Ok)
        else:
            QMessageBox.warning(self, "Warning", "<font color='white'>Username or password incorrect.</font>", QMessageBox.Ok)
        

    def check_user(self, username, password):
        connection = get_db_connection()

        mycursor = connection.cursor()
        sql = "SELECT * FROM users WHERE username = %s"
        values = (username,)
        mycursor.execute(sql, values)
        result = mycursor.fetchone()

        if result:
            hashed_password = result[2].encode('utf-8')  # Kodiranje hashed_password u bajtovni oblik
            return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
        return False
    
    def get_user_id(self, username):
        connection = get_db_connection()
        mycursor = connection.cursor()

        sql = "SELECT id FROM users WHERE username = %s"
        mycursor.execute(sql, (username,))
        result = mycursor.fetchone()
        connection.commit()

        if result:
            return result[0]  # Vraćanje ID-a korisnika
        else:
            return None

