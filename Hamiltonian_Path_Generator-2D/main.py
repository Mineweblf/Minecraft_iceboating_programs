import sys
from PyQt5.QtWidgets import QApplication
from utils.gui import PathGeneratorApp

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PathGeneratorApp()
    window.show()
    sys.exit(app.exec_())