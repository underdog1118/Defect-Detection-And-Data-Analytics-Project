'''
Writer:UNDERDOG
Time:..
'''
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

class FirstWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.windowUI()

    def windowUI(self):
        self.setWindowTitle("Login")
        self.textfield()
        self.center()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def textfield(self):
        QToolTip.setFont(QFont('SansSerif', 12))
        user = QLabel("User:")
        userEdit = QLineEdit()
        userEdit.setToolTip("请输入你的帐号")

        passWord = QLabel("PassWord:")
        passWordEdit = QLineEdit()
        passWordEdit.setToolTip("请输入你的密码")

        grid = QGridLayout()
        grid.setSpacing(0)

        grid.addWidget(user, 0, 0)
        grid.addWidget(userEdit, 1, 0)
        grid.addWidget(passWord, 2, 0)
        grid.addWidget(passWordEdit, 3, 0)
        empty = QLabel()
        grid.addWidget(empty, 4, 0)

        btn_logon = QPushButton("Log on")
        btn_quit = QPushButton("Quit")
        grid.addWidget(btn_logon, 5, 0, 1, 2)
        grid.addWidget(btn_quit, 6, 0, 1, 2)

        btn_logon.clicked.connect(self.onclick)
        btn_quit.clicked.connect(quit)

        self.setLayout(grid)

    def onclick(self):
        newWindow = SecondWindow()
        newWindow.show()
        newWindow.exec_()

class SecondWindow(QWidget):
    def __init__(self):
        super().__init__
        self.newWindowUI

    def newWindowUI(self):
        self.resize(300,300)
        self.move(200,200)

if __name__ == "__main__":
    App = QApplication(sys.argv)
    ex = FirstWindow()
    ex.show()
    sys.exit(App.exec_())