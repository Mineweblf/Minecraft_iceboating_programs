import os
from PyQt5.QtWidgets import QApplication, QFileDialog, QMainWindow, QWidget, QVBoxLayout, QPushButton, QSlider, QLabel, QColorDialog, QHBoxLayout, QGraphicsScene, QGraphicsView, QGraphicsPixmapItem
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QImage, QPixmap, QColor
from PIL import Image, ImageDraw, ImageFilter
import sys
import math


class ImageEditor(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("图像处理工具")
        self.setGeometry(100, 100, 1000, 600)

        self.img = None
        self.processed_img = None
        self.colors_to_select = []
        self.selected_color = None

        # UI elements
        self.init_ui()

    def init_ui(self):
        main_widget = QWidget(self)
        main_layout = QVBoxLayout()

        # 创建颜色选择按钮
        self.color_button = QPushButton("选择颜色", self)
        self.color_button.clicked.connect(self.select_colors)
        main_layout.addWidget(self.color_button)

        # 创建圈数滑块
        self.slider_label = QLabel("描边圈数: 1", self)
        self.slider = QSlider(Qt.Horizontal, self)
        self.slider.setMinimum(1)
        self.slider.setMaximum(10)
        self.slider.setValue(1)
        self.slider.valueChanged.connect(self.update_slider_label)
        main_layout.addWidget(self.slider_label)
        main_layout.addWidget(self.slider)

        # 创建预览按钮
        self.preview_button = QPushButton("预览", self)
        self.preview_button.clicked.connect(self.preview)
        main_layout.addWidget(self.preview_button)

        # 创建保存按钮
        self.save_button = QPushButton("保存", self)
        self.save_button.clicked.connect(self.save_image)
        main_layout.addWidget(self.save_button)

        # 创建显示图像的区域
        self.scene = QGraphicsScene(self)
        self.view = QGraphicsView(self.scene, self)
        main_layout.addWidget(self.view)

        # 创建颜色显示标签
        self.color_info_label = QLabel("颜色编号: None", self)
        main_layout.addWidget(self.color_info_label)

        # 设置主窗口布局
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

        # 设置鼠标事件
        self.view.setMouseTracking(True)
        self.view.mouseMoveEvent = self.on_mouse_move

    def select_colors(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.selected_color = color
            self.colors_to_select.append(color)
            print(f"Selected color: {color.name()}")

    def update_slider_label(self):
        self.slider_label.setText(f"描边圈数: {self.slider.value()}")

    def add_border(self, img, border_width=5):
        pixels = img.load()
        width, height = img.size
        new_img = Image.new("RGBA", (width, height), (0, 0, 0, 0))  # 创建一个透明的背景

        for y in range(height):
            for x in range(width):
                pixel = pixels[x, y]
                if self.is_selected_color(pixel):
                    # 在符合条件的像素周围添加描边
                    self.add_borders_to_pixel(x, y, pixels, new_img, border_width)
                else:
                    # 其余部分设置为透明
                    new_img.putpixel((x, y), (0, 0, 0, 0))

        # 将所有非透明区域变成绿色
        pixels = new_img.load()
        for y in range(height):
            for x in range(width):
                pixel = pixels[x, y]
                if pixel[3] > 0:  # 如果该像素不是透明的
                    new_img.putpixel((x, y), (0, 255, 0, 255))  # 将其设置为绿色

        return new_img

    def add_borders_to_pixel(self, x, y, pixels, new_img, border_width):
        """为符合颜色的像素添加描边"""
        width, height = new_img.size
        for i in range(-border_width, border_width + 1):
            for j in range(-border_width, border_width + 1):
                new_x = x + i
                new_y = y + j
                if 0 <= new_x < width and 0 <= new_y < height:
                    new_img.putpixel((new_x, new_y), pixels[x, y])

    def is_selected_color(self, pixel):
        """判断像素是否是用户选择的颜色之一"""
        r, g, b, a = pixel
        for color in self.colors_to_select:
            # 允许一定的颜色容差
            if (abs(r - color.red()) < 50 and abs(g - color.green()) < 50 and abs(b - color.blue()) < 50):
                return True
        return False

    def preview(self):
        """预览原图和处理后的图像"""
        if not self.img:
            return

        # 获取用户选择的圈数
        border_width = self.slider.value()

        # 先处理图像
        img_with_border = self.add_border(self.img, border_width)

        # 缩小图像并应用抗锯齿
        width, height = img_with_border.size
        target_width = 700
        new_height = int(target_width * height / width)
        img_with_border = img_with_border.resize((target_width, new_height), Image.LANCZOS)
        img_with_border = img_with_border.filter(ImageFilter.SMOOTH)

        # 更新处理后的图像
        self.processed_img = img_with_border

        # 显示原图和处理后的图像
        self.display_image(self.img, "原图")
        self.display_image(img_with_border, "处理后的图像")

    def display_image(self, img, label):
        """显示图像到PyQt窗口，并确保两张图并排显示"""
        img_qt = self.pil_to_qimage(img)
        pixmap = QPixmap.fromImage(img_qt)
        item = QGraphicsPixmapItem(pixmap)

        # 设置标签数据
        item.setData(0, label)

        # 如果是原图，将其显示在左侧
        if label == "原图":
            item.setPos(0, 0)  # 原图放在左侧
        # 如果是处理后的图，将其显示在右侧
        elif label == "处理后的图像":
            # 获取原图的宽度，确保它们并排显示
            original_item = self.scene.items()[0]  # 假设原图是第一个item
            original_width = original_item.pixmap().width()
            item.setPos(original_width + 10, 0)  # 处理图放在原图右侧，并加一点间隔

        self.scene.addItem(item)


    def pil_to_qimage(self, pil_img):
        """将PIL图像转换为QImage"""
        pil_img = pil_img.convert("RGBA")
        data = pil_img.tobytes("raw", "BGRA")
        qimage = QImage(data, pil_img.width, pil_img.height, QImage.Format_RGBA8888)
        return qimage

    def load_image(self, image_path):
        """加载图像并显示"""
        self.img = Image.open(image_path)
        self.img = self.img.convert("RGBA")  # 转为RGBA格式
        self.preview()

    def save_image(self):
        """保存图像"""
        if not self.processed_img:
            return

        # 选择保存路径
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(self, "保存图像", os.path.expanduser("~/Desktop/processed_image.png"), "PNG Files (*.png);;JPEG Files (*.jpg *.jpeg)", options=options)
        if file_path:
            self.processed_img.save(file_path)
            print(f"Image saved to {file_path}")

    def on_mouse_move(self, event):
        """监听鼠标移动事件并获取当前像素的颜色"""
        if self.img:
            pos = event.pos()
            scene_pos = self.view.mapToScene(pos)
            x, y = int(scene_pos.x()), int(scene_pos.y())

            # 确保鼠标在图像范围内
            if 0 <= x < self.img.width and 0 <= y < self.img.height:
                pixel = self.img.getpixel((x, y))
                self.update_color_info(pixel)

    def update_color_info(self, pixel):
        """更新颜色信息标签"""
        r, g, b, a = pixel
        color_code = f"颜色编号: ({r}, {g}, {b})"
        self.color_info_label.setText(color_code)
        self.selected_color = QColor(r, g, b)


def main():
    app = QApplication(sys.argv)
    window = ImageEditor()

    # 打开文件对话框选择输入图片
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    file_dialog = QFileDialog()
    file_dialog.setFileMode(QFileDialog.ExistingFile)
    file_dialog.setNameFilter("Images (*.png *.jpg *.jpeg)")
    file_dialog.setDirectory(os.path.expanduser("~/Desktop"))

    if file_dialog.exec_():
        input_path = file_dialog.selectedFiles()[0]
        window.load_image(input_path)

    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
