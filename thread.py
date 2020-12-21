import cv2
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtGui import QImage


class Thread(QThread):
    changePixmap = pyqtSignal(QImage)

    def __init__(self):
        super(Thread, self).__init__()
        self.cap = cv2.VideoCapture(0)
        self.video = ""
        self.photo = ""

    def run(self):
        while True:
            ret, self.video = self.cap.read()
            ret, self.photo = self.cap.read()

            if ret:
                rgb_image = cv2.cvtColor(self.video, cv2.COLOR_BGR2RGB)
                h, w, ch = rgb_image.shape
                bytes_per_line = ch * w
                convert_to_qtformat = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
                p = convert_to_qtformat.scaled(320, 240, Qt.KeepAspectRatio)
                self.changePixmap.emit(p)

    def take_photo(self):
        return self.photo
