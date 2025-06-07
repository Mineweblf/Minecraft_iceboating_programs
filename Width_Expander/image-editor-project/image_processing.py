from PIL import Image

class ImageProcessor:
    def __init__(self):
        self.selected_color = None

    def add_border(self, img, colors_to_select, border_width=5):
        pixels = img.load()
        width, height = img.size
        new_img = Image.new("RGBA", (width, height), (0, 0, 0, 0))  # 创建透明背景

        for y in range(height):
            for x in range(width):
                pixel = pixels[x, y]
                if self.is_selected_color(pixel, colors_to_select):
                    # 添加描边
                    self.add_borders_to_pixel(x, y, pixels, new_img, border_width)
                else:
                    # 设置透明
                    new_img.putpixel((x, y), (0, 0, 0, 0))

        # 将非透明区域变为绿色
        pixels = new_img.load()
        for y in range(height):
            for x in range(width):
                pixel = pixels[x, y]
                if pixel[3] > 0:  # 如果不是透明像素
                    new_img.putpixel((x, y), (0, 255, 0, 255))  # 设置为绿色

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

    def is_selected_color(self, pixel, colors_to_select):
        """检查像素是否为选择的颜色之一"""
        r, g, b, a = pixel
        for color in colors_to_select:
            # 允许一定的颜色容差
            if (abs(r - color.red()) < 50 and abs(g - color.green()) < 50 and abs(b - color.blue()) < 50):
                return True
        return False

# 这里可以拿来设置图片的大小
    def resize_and_smooth(self, img, max_size=(500, 500)):
        """缩放图像并应用抗锯齿"""
        img.thumbnail(max_size, Image.LANCZOS)
        return img