from PyQt5.QtGui import QImage

def pil_to_qimage(pil_image):
    """将PIL图像转换为QImage"""
    width, height = pil_image.size
    data = pil_image.tobytes("raw", "RGBA")
    qimage = QImage(data, width, height, QImage.Format_RGBA8888)
    return qimage
