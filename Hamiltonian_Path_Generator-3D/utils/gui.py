import numpy as np
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QSpinBox, QLabel, QCheckBox, QLineEdit, QComboBox
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from utils.path_generation import generate_path
from utils.plot_utils import plot_path
from utils.file_utils import save_plane_images
from utils.csv_utils import save_path_to_csv
import csv

# 设置 Matplotlib 自动加载系统字体
plt.rcParams['font.family'] = 'Microsoft YaHei'

class PathGeneratorApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Path Generator")
        self.setGeometry(100, 100, 1000, 800)
        
        # 初始化起点
        self.start_point = None
        self.random_start = False

        # 设置布局
        self.layout = QVBoxLayout()

        # 输入部分
        self.input_layout = QHBoxLayout()
        
        self.label_size = QLabel("Size:")
        self.input_layout.addWidget(self.label_size)
        self.spin_size = QSpinBox()
        self.spin_size.setRange(3, 11)
        self.spin_size.setValue(5)
        self.spin_size.valueChanged.connect(self.update_path_length_range)
        self.input_layout.addWidget(self.spin_size)

        self.label_length = QLabel("Minimum Path Length:")
        self.input_layout.addWidget(self.label_length)
        self.spin_length = QSpinBox()
        self.input_layout.addWidget(self.spin_length)

        self.layout.addLayout(self.input_layout)

        # 模式选择部分
        self.mode_layout = QHBoxLayout()
        
        self.label_mode = QLabel("Mode:")
        self.mode_layout.addWidget(self.label_mode)
        self.combo_mode = QComboBox()
        self.combo_mode.addItems(["开放路径", "闭合路径"])
        self.combo_mode.currentIndexChanged.connect(self.update_mode)
        self.mode_layout.addWidget(self.combo_mode)

        self.layout.addLayout(self.mode_layout)

        # 起点选择部分
        self.start_point_layout = QHBoxLayout()
        
        self.start_point_input_layout = QVBoxLayout()
        
        self.label_start_x = QLabel("X=")
        self.start_point_input_layout.addWidget(self.label_start_x)
        self.input_start_x = QLineEdit()
        self.input_start_x.textChanged.connect(self.update_start_point)
        self.start_point_input_layout.addWidget(self.input_start_x)

        self.label_start_y = QLabel("Y=")
        self.start_point_input_layout.addWidget(self.label_start_y)
        self.input_start_y = QLineEdit()
        self.input_start_y.textChanged.connect(self.update_start_point)
        self.start_point_input_layout.addWidget(self.input_start_y)

        self.label_start_z = QLabel("Z=")
        self.start_point_input_layout.addWidget(self.label_start_z)
        self.input_start_z = QLineEdit()
        self.input_start_z.textChanged.connect(self.update_start_point)
        self.start_point_input_layout.addWidget(self.input_start_z)

        self.random_start_checkbox = QCheckBox("随机起点")
        self.random_start_checkbox.stateChanged.connect(self.toggle_random_start)
        self.start_point_input_layout.addWidget(self.random_start_checkbox)

        self.start_point_layout.addLayout(self.start_point_input_layout)

        # 初始化点阵图
        self.init_point_grid()
        self.start_point_layout.addWidget(self.point_grid_canvas)

        self.layout.addLayout(self.start_point_layout)

        # 生成路径按钮
        self.generate_button = QPushButton("生成路径")
        self.generate_button.clicked.connect(self.generate_path)
        self.generate_button.setEnabled(False)
        self.layout.addWidget(self.generate_button)

        # 添加matplotlib的图形显示
        self.canvas = FigureCanvas(plt.figure())
        self.layout.addWidget(self.canvas)

        self.setLayout(self.layout)

        # 生成截图按钮
        self.save_button = QPushButton("生成截图")
        self.save_button.setEnabled(False)
        self.save_button.clicked.connect(self.save_screenshots)
        self.layout.addWidget(self.save_button)

        # 初始化路径长度范围
        self.update_path_length_range()

    def update_path_length_range(self):
        size = self.spin_size.value()
        max_points = size * size * size
        self.spin_length.setRange(1, max_points)
        self.spin_length.setValue(min(self.spin_length.value(), max_points))
        self.init_point_grid()  # 重新初始化点阵图
        self.update_start_point()

    def update_mode(self):
        self.update_generate_button_state()

    def toggle_random_start(self, state):
        if state == 2:  # Checked
            self.input_start_x.clear()
            self.input_start_y.clear()
            self.input_start_z.clear()
            self.input_start_x.setEnabled(False)
            self.input_start_y.setEnabled(False)
            self.input_start_z.setEnabled(False)
            self.random_start = True
        else:
            self.input_start_x.setEnabled(True)
            self.input_start_y.setEnabled(True)
            self.input_start_z.setEnabled(True)
            self.random_start = False
        self.update_generate_button_state()

    def init_point_grid(self):
        # 清除旧的图形
        for i in reversed(range(self.start_point_layout.count())):
            widget = self.start_point_layout.itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)

        self.point_grid_fig = plt.figure()
        self.point_grid_ax = self.point_grid_fig.add_subplot(111, projection='3d')
        self.point_grid_ax.set_title("选择起点")
        self.point_grid_ax.set_xlim(0, self.spin_size.value())
        self.point_grid_ax.set_ylim(0, self.spin_size.value())
        self.point_grid_ax.set_zlim(0, self.spin_size.value())
        self.point_grid_ax.set_xlabel('X')
        self.point_grid_ax.set_ylabel('Y')
        self.point_grid_ax.set_zlabel('Z')
        self.point_grid_ax.view_init(elev=30, azim=30)

        self.points = np.array([[x, y, z] for x in range(1, self.spin_size.value() + 1) for y in range(1, self.spin_size.value() + 1) for z in range(1, self.spin_size.value() + 1)])
        self.scatter = self.point_grid_ax.scatter(self.points[:, 0], self.points[:, 1], self.points[:, 2], color='gray')

        self.point_grid_canvas = FigureCanvas(self.point_grid_fig)
        self.start_point_layout.addWidget(self.point_grid_canvas)

    def update_start_point(self):
        try:
            x = int(self.input_start_x.text())
            y = int(self.input_start_y.text())
            z = int(self.input_start_z.text())
            print(f"输入坐标: x={x}, y={y}, z={z}")  # 调试语句
            if 1 <= x <= self.spin_size.value() and 1 <= y <= self.spin_size.value() and 1 <= z <= self.spin_size.value():
                self.start_point = (x, y, z)
                print(f"有效起点: {self.start_point}")  # 调试语句
                colors = ['red' if (px, py, pz) == self.start_point else 'gray' for px, py, pz in self.points]
                self.scatter._facecolor3d = self.scatter._edgecolor3d = np.array(colors)
                self.point_grid_canvas.draw()
            else:
                self.start_point = None
                print("无效起点，超出范围")  # 调试语句
        except ValueError:
            self.start_point = None
            print("无效输入，不是整数")  # 调试语句
        self.update_generate_button_state()

    def update_generate_button_state(self):
        if self.random_start or (self.start_point is not None):
            self.generate_button.setEnabled(True)
        else:
            self.generate_button.setEnabled(False)

    def show_error(self):
        # 清除画布上的内容
        self.canvas.figure.clear()
        ax = self.canvas.figure.add_subplot(111)
        ax.text(0.5, 0.5, 'ERROR', color='red', fontsize=50, ha='center', va='center')
        ax.set_axis_off()
        self.canvas.draw()

    def generate_path(self):
        # 获取用户输入
        size = self.spin_size.value()
        min_length = self.spin_length.value()
        mode = self.combo_mode.currentText()

        # 更新起点
        self.update_start_point()

        # 生成路径
        self.path, self.directions = generate_path(size, min_length, self.start_point, self.random_start, mode)

        # 确保路径生成成功
        if not self.path:
            print("路径生成失败")
            self.show_error()
            return

        print(f"生成成功！")

        # 绘制路径
        fig = plot_path(self.path, dimensions=(size, size, size))

        # 更新画布
        self.canvas.figure.clear()
        ax = self.canvas.figure.add_subplot(111, projection='3d')

        # 绘制路径
        points = np.array(self.path)
        ax.scatter(points[:, 0], points[:, 1], points[:, 2], s=100, marker='o', color='pink', alpha=0.8)

        for i in range(len(self.path) - 1):
            x1, y1, z1 = self.path[i]
            x2, y2, z2 = self.path[i + 1]
            ax.plot([x1, x2], [y1, y2], [z1, z2], color='brown', linewidth=4)

        ax.set_axis_off()
        ax.set_title("3D 路径")
        ax.view_init(elev=30, azim=30)

        # 刷新画布
        self.canvas.draw()

        # 启用生成截图按钮
        self.save_button.setEnabled(True)

        # 保存路径信息到 CSV 文件
        save_path_to_csv(self.path, self.directions, 'data')

    def save_screenshots(self):
        size = self.spin_size.value()
        output_folder = "screenshots"
        save_plane_images(size, size, size, self.path, output_folder)