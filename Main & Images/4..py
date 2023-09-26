'''
Writer:UNDERDOG
Time:..
'''
from PyQt6.QtWidgets import *
from untitled import Ui_Dialog

if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    main = QDialog()               #获取窗口类型实例
    untitled_dialog = Ui_Dialog()  #取得Ui的class实例
    untitled_dialog.setupUi(main)  #将ui实例绘制到窗口实例上
    main.show()                    #展示窗口
    sys.exit(app.exec_())