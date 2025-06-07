# Minecraft Hamiltonian Path 赛道生成与宽度扩展工具集

## 项目简介

本工具集包含三个子项目，旨在辅助Minecraft冰船赛道的设计与制作：

- **Hamiltonian_Path_Generator-3D**：用于生成三维哈密顿路径（立体赛道结构示意图），适合设计立体冰船赛道。
- **Hamiltonian_Path_Generator-2D**：用于生成二维哈密顿路径（平面赛道结构），适合设计平面冰船赛道。
- **Width_Expander**：用于对生成的赛道图片进行宽度扩展处理，方便后续在Minecraft中设计宽赛道。

生成的赛道结构可通过Minecraft社区的 [SlopeCraft](https://github.com/Slimefun/Slimefun4/wiki/SlopeCraft) 工具转化为游戏内可用的投影文件，辅助实际建造。

---

## 依赖环境

- Python 3.7+
- PyQt5
- matplotlib
- numpy
- Pillow
- scipy

安装依赖（在每个子项目根目录下执行）：

```sh
pip install -r requirements.txt
```

---

## 使用步骤

### 1. 生成三维赛道结构（立体赛道）

1. 进入 `Hamiltonian_Path_Generator-3D` 文件夹。
2. 运行主程序：

   ```sh
   python main.py
   ```

3. 在弹出的界面中设置赛道尺寸、路径长度、起点（或随机起点）、模式（开放/闭合），点击“生成路径”。
4. 可视化赛道结构后，点击“生成截图”保存每一层的平面投影图（在 `screenshots/xoy_plane/` 文件夹下）。

### 2. 生成二维赛道结构（平面赛道）

1. 进入 `Hamiltonian_Path_Generator-2D` 文件夹。
2. 运行主程序：

   ```sh
   python main.py
   ```

3. 设置赛道尺寸、路径点数、起点（或随机起点）、是否考虑45度转角，点击“生成路径”。
4. 可视化赛道结构后，可点击“收藏”保存贝塞尔曲线图（在 `screenshots/favour/` 文件夹下）。

### 3. 赛道宽度扩展（可选）

1. 进入 `Width_Expander/image-editor-project` 文件夹。
2. 运行主程序：

   ```sh
   python main.py
   ```

3. 选择需要扩展宽度的赛道图片，选择颜色，设置描边圈数，点击“预览”查看效果，点击“保存”导出处理后的图片（在 `output/` 文件夹下）。

---

## 工作流程建议

1. **生成赛道结构**：使用3D或2D工具生成赛道结构图。
2. **宽度扩展（可选）**：如需更宽的赛道，使用宽度扩展工具处理生成的图片。
3. **投影转换**：将处理后的图片通过[SlopeCraft](https://github.com/Slimefun/Slimefun4/wiki/SlopeCraft)等工具转为Minecraft投影文件。
4. **游戏内建造**：在Minecraft中导入投影文件，辅助实际赛道搭建。

---

## 文件结构说明

### Hamiltonian_Path_Generator-3D

- `main.py`  
  启动三维路径生成器的主程序入口。
- `data/`  
  存放生成的路径数据（如 CSV 文件）。
- `screenshots/`  
  存放生成的赛道截图。
- `utils/`
  - `csv_utils.py`  
    路径及方向数据的 CSV 文件保存工具。
  - `file_utils.py`  
    平面截图的生成与保存工具。
  - `gui.py`  
    主界面与交互逻辑（PyQt5）。
  - `path_generation.py`  
    三维哈密顿路径的生成算法。
  - `plot_utils.py`  
    路径的三维可视化绘图工具。
  - `start_point_selector.py`  
    起点选择器（含可视化）。
  - 其它辅助工具文件。

### Hamiltonian_Path_Generator-2D

- `main.py`  
  启动二维路径生成器的主程序入口。
- `data/`  
  存放生成的路径数据。
- `saidao/`  
  可能用于存放赛道相关的中间数据。
- `screenshots/`  
  存放生成的赛道截图和收藏图。
- `utils/`
  - `file_utils.py`  
    收藏赛道图片的保存工具。
  - `gui.py`  
    主界面与交互逻辑（PyQt5）。
  - `path_generation.py`  
    二维哈密顿路径的生成算法。
  - `plot_utils.py`  
    路径及贝塞尔曲线的可视化工具。
  - `start_point_selector.py`  
    起点选择器（含可视化）。
  - 其它辅助工具文件。

### Width_Expander

- `1.md`  
  说明文档，介绍各文件功能和使用方法。
- `放大宽度.py`  
  独立的图像处理工具，支持颜色选择、描边、预览与保存。
- `image-editor-project/`
  - `main.py`  
    项目入口，负责加载图片并启动主界面。
  - `editor.py`  
    图像编辑器主界面与业务逻辑（PyQt5）。
  - `image_processing.py`  
    图像处理算法（如描边、缩放等）。
  - `ui.py`  
    预留的界面定义文件（当前为空）。
  - `utils.py`  
    PIL 图像与 QImage 互转等实用函数。
  - `output/`  
    处理后图片的输出目录。
  - `resources/`  
    资源文件目录。
  - `__pycache__/`  
    Python 缓存文件夹。

---

md文件通过colipt生成+作者小改
如有问题或建议，欢迎在GitHub仓库提交Issue或PR。
