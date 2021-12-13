import sys
from PyQt5.QtWidgets import *
from LoginWindow import LoginWindow
from traceback import print_exc

class MainSolution():
    #   主程序
    def main(self):
        try:
            App = QApplication(sys.argv)
            self.Login = LoginWindow()
            self.Login.show()
            App.exit(App.exec_())
        except Exception:
            print_exc()

if __name__ == '__main__':
    _Main = MainSolution()
    _Main.main()