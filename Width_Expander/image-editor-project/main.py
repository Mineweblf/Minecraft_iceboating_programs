import os
import sys
from PyQt5.QtWidgets import QApplication, QFileDialog
from PyQt5.QtCore import QStandardPaths
from editor import ImageEditor

def main():
    app = QApplication(sys.argv)
    window = ImageEditor()

    # 打开文件对话框选择输入图片
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    file_dialog = QFileDialog()
    file_dialog.setFileMode(QFileDialog.ExistingFile)
    file_dialog.setNameFilter("Images (*.png *.jpg *.jpeg)")

    # 设置默认目录为用户的桌面目录
    default_dir = QStandardPaths.writableLocation(QStandardPaths.DesktopLocation)
    file_dialog.setDirectory(default_dir)

    if file_dialog.exec_():
        input_path = file_dialog.selectedFiles()[0]
        window.load_image(input_path)
        window.show()
        sys.exit(app.exec_())
    else:
        sys.exit()

if __name__ == "__main__":
    main()