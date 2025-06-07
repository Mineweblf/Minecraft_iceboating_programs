import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import TextBox, CheckButtons

class StartPointSelector:
    def __init__(self, size):
        self.size = size
        self.start_point = None
        self.random_start = False

        self.fig, self.ax = plt.subplots(subplot_kw={'projection': '3d'})
        self.ax.set_title("Select Start Point")
        self.ax.set_xlim(0, size)
        self.ax.set_ylim(0, size)
        self.ax.set_zlim(0, size)
        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.ax.set_zlabel('Z')
        self.ax.view_init(elev=30, azim=30)

        self.points = np.array([[x, y, z] for x in range(size) for y in range(size) for z in range(size)])
        self.scatter = self.ax.scatter(self.points[:, 0], self.points[:, 1], self.points[:, 2], color='gray')

        self.text_box_x = TextBox(plt.axes([0.1, 0.9, 0.1, 0.05]), 'X=')
        self.text_box_y = TextBox(plt.axes([0.1, 0.8, 0.1, 0.05]), 'Y=')
        self.text_box_z = TextBox(plt.axes([0.1, 0.7, 0.1, 0.05]), 'Z=')
        self.text_box_x.on_submit(self.update_start_point)
        self.text_box_y.on_submit(self.update_start_point)
        self.text_box_z.on_submit(self.update_start_point)

        self.check_buttons = CheckButtons(plt.axes([0.1, 0.6, 0.1, 0.1]), ['Random Start'], [self.random_start])
        self.check_buttons.on_clicked(self.toggle_random_start)

    def update_start_point(self, _=None):
        try:
            x = int(self.text_box_x.text)
            y = int(self.text_box_y.text)
            z = int(self.text_box_z.text)
            print(f"Input coordinates: x={x}, y={y}, z={z}")  # 调试语句
            if 0 <= x < self.size and 0 <= y < self.size and 0 <= z < self.size:
                self.start_point = (x, y, z)
                print(f"Valid start point: {self.start_point}")  # 调试语句
                colors = ['red' if (px, py, pz) == self.start_point else 'gray' for px, py, pz in self.points]
                self.scatter._facecolor3d = self.scatter._edgecolor3d = np.array(colors)
                self.scatter.set_color(colors)  # 确保颜色更新
                self.fig.canvas.draw_idle()
            else:
                self.start_point = None
                print("Invalid start point, out of range")  # 调试语句
        except ValueError:
            self.start_point = None
            print("Invalid input, not an integer")  # 调试语句
        self.update_generate_button_state()

    def toggle_random_start(self, label):
        self.random_start = not self.random_start

    def update_generate_button_state(self):
        if self.start_point or self.random_start:
            self.generate_button.setEnabled(True)
        else:
            self.generate_button.setEnabled(False)

    def get_start_point(self):
        plt.show()
        return self.start_point, self.random_start