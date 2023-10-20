from PySide2 import QtWidgets
from PySide2.QtUiTools import QUiLoader
import sys

main_win = None

class LoginWin:

    def __init__(self):
        super().__init__()
        self.ui = QUiLoader().load('ui/login.ui')
        self.ui.btn_login.clicked.connect(self.onLogin)

    def onLogin(self):
        global main_win
        # 实例化另外一个窗口
        main_win = Window_Main()
        # 显示新窗口
        main_win.ui.show()
        # 关闭自己
        self.ui.close()



class Window_Main:
    def __init__(self):
        super().__init__()
        self.ui = QUiLoader().load('ui/main.ui')

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    wm = LoginWin()
    wm.ui.show()
    sys.exit(app.exec_())