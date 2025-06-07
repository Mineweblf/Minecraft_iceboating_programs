from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton, QLineEdit, QLabel, QGraphicsScene, QGraphicsView, QColorDialog, QFileDialog, QGraphicsPixmapItem
from PyQt5.QtGui import QPixmap, QColor, QPainter
from PyQt5.QtCore import Qt
from PIL import Image
import os
from image_processing import ImageProcessor
from utils import pil_to_qimage

class ImageEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("图像处理工具")
        self.setGeometry(100, 100, 1000, 600)

        self.img = None
        self.processed_img = None
        self.colors_to_select = []
        self.selected_color = None
        self.image_path = None

        # UI元素
        self.init_ui()
        self.image_processor = ImageProcessor()  # 引入图像处理类

    def init_ui(self):
        main_widget = QWidget(self)
        main_layout = QVBoxLayout()

        # 创建颜色选择按钮
        self.color_button = QPushButton("选择颜色", self)
        self.color_button.clicked.connect(self.select_colors)
        main_layout.addWidget(self.color_button)

        # 创建圈数输入框
        self.input_label = QLabel("描边圈数: ", self)
        self.input_field = QLineEdit(self)
        self.input_field.setText("3")
        main_layout.addWidget(self.input_label)
        main_layout.addWidget(self.input_field)

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
        self.view.setRenderHint(QPainter.Antialiasing)
        self.view.setRenderHint(QPainter.SmoothPixmapTransform)
        self.view.setResizeAnchor(QGraphicsView.AnchorUnderMouse)
        self.view.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.view.setDragMode(QGraphicsView.ScrollHandDrag)
        self.view.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
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

    def resizeEvent(self, event):
        """在窗口大小调整时更新视图"""
        self.view.fitInView(self.scene.sceneRect(), Qt.KeepAspectRatio)
        super().resizeEvent(event)

    def select_colors(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.selected_color = color
            self.colors_to_select.append(color)
            print(f"Selected color: {color.name()}")

    def preview(self):
        """预览原图和处理后的图像"""
        if not self.img:
            return

        # 获取用户输入的圈数
        border_width = int(self.input_field.text())

        # 先处理图像
        img_with_border = self.image_processor.add_border(self.img, self.colors_to_select, border_width)

        # 缩小图像并应用抗锯齿
        img_with_border = self.image_processor.resize_and_smooth(img_with_border)

        # 更新处理后的图像
        self.processed_img = img_with_border

        # 显示原图和处理后的图像
        self.display_image(self.img, "原图")
        self.display_image(img_with_border, "处理后的图像")

    def display_image(self, img, label):
        """显示图像到PyQt窗口，并确保两张图并排显示"""
        img_qt = pil_to_qimage(img)
        pixmap = QPixmap.fromImage(img_qt)
        item = QGraphicsPixmapItem(pixmap)

        # 设置标签数据
        item.setData(0, label)

        if label == "原图":
            item.setPos(0, 0)
        elif label == "处理后的图像":
            original_item = self.scene.items()[0]  # 假设原图是第一个item
            original_width = original_item.pixmap().width()
            item.setPos(original_width + 10, 0)

        self.scene.addItem(item)
        self.view.fitInView(self.scene.sceneRect(), Qt.KeepAspectRatio)

    def load_image(self, image_path):
        """加载图像并显示"""
        self.img = Image.open(image_path)
        self.img = self.img.convert("RGBA")  # 转为RGBA格式
        self.image_path = image_path
        self.preview()

    def save_image(self):
        """保存图像"""
        if not self.processed_img:
            return

        # 创建output文件夹
        current_dir = os.path.dirname(__file__)
        output_dir = os.path.join(current_dir, 'output')
        os.makedirs(output_dir, exist_ok=True)

        # 获取文件原名
        base_name = os.path.basename(self.image_path)
        name, ext = os.path.splitext(base_name)

        # 获取颜色和描边数量
        color_name = self.selected_color.name().replace('#', '')
        border_width = int(self.input_field.text())

        # 生成文件名
        index = 1
        while True:
            file_name = f"{name}_{color_name}_{border_width}_{index}.png"
            file_path = os.path.join(output_dir, file_name)
            if not os.path.exists(file_path):
                break
            index += 1

        # 保存图像
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