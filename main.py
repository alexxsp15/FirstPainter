import sys
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter, QPen
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget


class Background(QWidget):
    def __init__(self):
        super().__init__()
        self.pos = []
        self.drawing = False

    def mousePressEvent(self, event):
        self.drawing = True
        self.pos.append(event.position().toPoint())
        self.update()

    def mouseReleaseEvent(self, event):
        self.drawing = False

    def mouseMoveEvent(self, event):
        if  self.drawing == True:
            self.pos.append(event.position().toPoint())
            self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), Qt.GlobalColor.white)

        pen = QPen(Qt.GlobalColor.darkGreen, 6)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
        painter.setPen(pen)
        for p in self.pos:
            painter.drawPoint(p)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Painter 1.1")

        widget = Background()
        widget.setFixedSize(1000, 700)
        self.setCentralWidget(widget)


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
