import os
import numpy as np
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QSpinBox, QLabel, QCheckBox, QLineEdit, QComboBox
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from utils.path_generation import generate_path
from utils.plot_utils import plot_path, plot_bezier_path
from utils.file_utils import save_favourite_image
from scipy.interpolate import make_interp_spline

plt.rcParams['font.family'] = 'Microsoft YaHei'

class PathGeneratorApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Path Generator")
        self.setGeometry(100, 100, 1000, 800)
        
        self.start_point = None
        self.random_start = False
        self.consider_45_degrees = False

        self.layout = QVBoxLayout()
        self.input_layout = QHBoxLayout()
        
        self.label_size_x = QLabel("Size X:")
        self.input_layout.addWidget(self.label_size_x)
        self.spin_size_x = QSpinBox()
        self.spin_size_x.setRange(3, 30)
        self.spin_size_x.setValue(15)
        self.spin_size_x.valueChanged.connect(self.update_path_length_range)
        self.input_layout.addWidget(self.spin_size_x)

        self.label_size_y = QLabel("Size Y:")
        self.input_layout.addWidget(self.label_size_y)
        self.spin_size_y = QSpinBox()
        self.spin_size_y.setRange(3, 30)
        self.spin_size_y.setValue(6)
        self.spin_size_y.valueChanged.connect(self.update_path_length_range)
        self.input_layout.addWidget(self.spin_size_y)

        self.label_length = QLabel("经过的点数:")
        self.input_layout.addWidget(self.label_length)
        self.spin_length = QSpinBox()
        self.spin_length.setValue(43)  # 初始化为34
        self.input_layout.addWidget(self.spin_length)

        self.layout.addLayout(self.input_layout)

        self.mode_layout = QHBoxLayout()
        
        self.label_mode = QLabel("模式:")
        self.mode_layout.addWidget(self.label_mode)
        self.combo_mode = QComboBox()
        self.combo_mode.addItems(["不考虑45度", "考虑45度"])
        self.combo_mode.currentIndexChanged.connect(self.update_mode)
        self.mode_layout.addWidget(self.combo_mode)

        self.layout.addLayout(self.mode_layout)

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

        self.random_start_checkbox = QCheckBox("随机起点")
        self.random_start_checkbox.stateChanged.connect(self.toggle_random_start)
        self.start_point_input_layout.addWidget(self.random_start_checkbox)

        self.start_point_layout.addLayout(self.start_point_input_layout)
        self.init_point_grid()
        self.start_point_layout.addWidget(self.point_grid_canvas)

        self.layout.addLayout(self.start_point_layout)

        self.generate_button = QPushButton("生成路径")
        self.generate_button.clicked.connect(self.generate_path)
        self.generate_button.setEnabled(False)
        self.layout.addWidget(self.generate_button)

        self.canvas = FigureCanvas(plt.figure())
        self.layout.addWidget(self.canvas)

        self.favourite_layout = QHBoxLayout()
        self.favourite_input = QLineEdit()
        self.favourite_input.setPlaceholderText("输入收藏名称")
        self.favourite_input.setText("DN")  # 初始化为DN
        self.favourite_input.textChanged.connect(self.update_favourite_button_state)
        self.favourite_layout.addWidget(self.favourite_input)

        self.favourite_button = QPushButton("收藏")
        self.favourite_button.setEnabled(False)
        self.favourite_button.clicked.connect(self.save_favourite)
        self.favourite_layout.addWidget(self.favourite_button)

        self.layout.addLayout(self.favourite_layout)

        self.setLayout(self.layout)

        self.update_path_length_range()

    def update_path_length_range(self):
        size_x = self.spin_size_x.value()
        size_y = self.spin_size_y.value()
        max_points = size_x * size_y
        self.spin_length.setRange(1, max_points)
        self.spin_length.setValue(min(self.spin_length.value(), max_points))
        self.init_point_grid()
        self.update_start_point()

    def update_mode(self):
        self.consider_45_degrees = self.combo_mode.currentText() == "考虑45度"
        self.update_generate_button_state()

    def toggle_random_start(self, state):
        if state == 2:
            self.input_start_x.clear()
            self.input_start_y.clear()
            self.input_start_x.setEnabled(False)
            self.input_start_y.setEnabled(False)
            self.random_start = True
        else:
            self.input_start_x.setEnabled(True)
            self.input_start_y.setEnabled(True)
            self.random_start = False
        self.update_generate_button_state()

    def init_point_grid(self):
        for i in reversed(range(self.start_point_layout.count())):
            widget = self.start_point_layout.itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)

        size_x = self.spin_size_x.value() + 1
        size_y = self.spin_size_y.value() + 1
        self.point_grid_fig = plt.figure()
        self.point_grid_ax = self.point_grid_fig.add_subplot(111)
        self.point_grid_ax.set_title("选择起点")
        self.point_grid_ax.set_xlim(0, size_x)
        self.point_grid_ax.set_ylim(0, size_y)
        self.point_grid_ax.set_xlabel('X')
        self.point_grid_ax.set_ylabel('Y')

        self.points = np.array([[x, y] for x in range(1, size_x) for y in range(1, size_y)])
        self.scatter = self.point_grid_ax.scatter(self.points[:, 0], self.points[:, 1], color='gray')

        self.point_grid_canvas = FigureCanvas(self.point_grid_fig)
        self.start_point_layout.addWidget(self.point_grid_canvas)

    def update_start_point(self):
        try:
            x = int(self.input_start_x.text())
            y = int(self.input_start_y.text())
            if 1 <= x <= self.spin_size_x.value() and 1 <= y <= self.spin_size_y.value():
                self.start_point = (x, y)
                colors = ['red' if (px, py) == self.start_point else 'gray' for px, py in self.points]
                self.scatter.set_color(colors)
                self.point_grid_canvas.draw()
            else:
                self.start_point = None
        except ValueError:
            self.start_point = None
        self.update_generate_button_state()

    def update_generate_button_state(self):
        self.generate_button.setEnabled(self.random_start or (self.start_point is not None))

    def update_favourite_button_state(self):
        self.favourite_button.setEnabled(bool(self.favourite_input.text()) and self.path is not None)

    def show_error(self):
        self.canvas.figure.clear()
        ax = self.canvas.figure.add_subplot(111)
        ax.text(0.5, 0.5, 'ERROR', color='red', fontsize=50, ha='center', va='center')
        ax.set_axis_off()
        self.canvas.draw()

    def generate_path(self):
        size_x = self.spin_size_x.value()
        size_y = self.spin_size_y.value()
        min_length = self.spin_length.value()

        self.update_start_point()

        self.path, self.directions, attempts, success = generate_path(size_x, size_y, min_length, self.start_point, self.random_start, self.consider_45_degrees)

        print(f"尝试次数: {attempts}")
        if success:
            print("生成成功")
        else:
            print("生成失败")

        if not self.path:
            self.show_error()
            return

        fig1 = plot_path(self.path, dimensions=(size_x, size_y))
        fig2 = plot_bezier_path(self.path, dimensions=(size_x, size_y))

        self.canvas.figure.clear()
        ax1 = self.canvas.figure.add_subplot(121)
        ax2 = self.canvas.figure.add_subplot(122)

        points = np.array(self.path)
        all_points = np.array([[x, y] for x in range(1, size_x + 1) for y in range(1, size_y + 1)])
        path_points = set(map(tuple, points))

        # 绘制所有点，非路径点为灰色
        for point in all_points:
            if tuple(point) not in path_points:
                ax1.scatter(point[0], point[1], s=100, marker='o', color='white', alpha=0.5)

        # 绘制路径点
        ax1.scatter(points[:, 0], points[:, 1], s=100, marker='o', color='pink', alpha=0.8)
        for i in range(len(self.path) - 1):
            x1, y1 = self.path[i]
            x2, y2 = self.path[i + 1]
            ax1.plot([x1, x2], [y1, y2], color='brown', linewidth=4)
        ax1.set_aspect('equal')
        ax1.set_axis_off()
        ax1.set_title("2D 路径")

        x = points[:, 0]
        y = points[:, 1]
        t = np.linspace(0, 1, len(points))
        spl_x = make_interp_spline(t, x, k=3)
        spl_y = make_interp_spline(t, y, k=3)
        t_new = np.linspace(0, 1, 300)
        x_smooth = spl_x(t_new)
        y_smooth = spl_y(t_new)
        ax2.plot(x_smooth, y_smooth, linewidth=5, color='blue')

        ax2.scatter(points[:, 0], points[:, 1], s=100, marker='o', color='white')
        ax2.set_aspect('equal')
        ax2.set_axis_off()
        ax2.set_title("贝塞尔曲线")

        self.canvas.draw()
        self.update_favourite_button_state()

    def save_favourite(self):
        favourite_name = self.favourite_input.text()
        min_length = self.spin_length.value()
        save_favourite_image(self.path, self.spin_size_x.value(), self.spin_size_y.value(), favourite_name, min_length)