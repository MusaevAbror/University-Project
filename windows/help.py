from PyQt5.QtWidgets import *
from PyQt5.QtCore import * 
from PyQt5.QtGui import * 
import smtplib

class helpSender(QWidget):
    def __init__(self):
        super().__init__()
        self.initUi()
        appstyle = "background-color:darkgray"
        self.setStyleSheet(appstyle)
        self.qmessage = QMessageBox()

    def initUi(self):
        self.setGeometry(500, 300, 500, 600)
        self.resize(500, 400)
        self.qt = QTextEdit(self)
        self.qt.move(70, 80)
        self.qt.setStyleSheet("background-color:white")
        

        self.ql = QLabel(self)
        self.ql.move(30,35)
        self.ql.setText('<html><head/><body><p><span style=" font-size:12pt; font-style:italic;">Dasturdagi hatoliklarni Dasturchiga yuborish</span></p></body></html>')
        self.ql.setStyleSheet("background-color:white")


        self.btn = QPushButton("send", self)
        self.btn.move(340, 100)
        self.btn.setStyleSheet("background-color:white")
        self.btn.clicked.connect(self.onSend)

        self.btn_c = QPushButton("clear", self)
        self.btn_c.move(340, 150)
        self.btn_c.setStyleSheet("background-color:white")
        self.btn_c.clicked.connect(self.onClear)

    def onClear(self):
        self.qt.clear()
    
    def onSend(self):
        try:
            sender = "musaevabror.7636@gmail.com"
            reciver = "aaa11111.sx@gmail.com"
            pasword = "wyvmetnimpnlwdbl"
            smtpserver = smtplib.SMTP("smtp.gmail.com", 587)
            smtpserver.ehlo()
            smtpserver.starttls()
            smtpserver.ehlo()
            smtpserver.login(sender, pasword)
            msg = str(self.qt.toPlainText())
            smtpserver.sendmail(sender, reciver, msg)
            smtpserver.close()
            self.qmessage.setIcon(QMessageBox.Information)
            self.qmessage.setWindowTitle("Bajarildi")
            self.qmessage.setText("Xabar yuborildi")
            self.qmessage.show()
        except Exception as exp :
            self.qmessage.setIcon(QMessageBox.Critical)
            self.qmessage.setWindowTitle("Xatolik")
            self.qmessage.setText(str(exp))
            self.qmessage.show()
  


        
       