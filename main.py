import sys
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QPainter, QPen, QColor
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QGridLayout


class Background(QWidget):

    def __init__(self):
        super().__init__()
        self.pos = []
        self.drawing = False
        self.color = "black"

    def mousePressEvent(self, event):
        self.drawing = True
        self.pos.append((event.position().toPoint(), self.color))
        self.update()

    def mouseReleaseEvent(self, event):
        self.drawing = False
        self.pos.append((None, None))

    def mouseMoveEvent(self, event):
        if  self.drawing == True:
            self.pos.append((event.position().toPoint(), self.color))
            self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), Qt.GlobalColor.white)


        for i in range(1, len(self.pos)):
            p1, c1 = self.pos[i-1]
            p2, c2 = self.pos[i]

            if p1 is None or p2 is None:
                continue


            if c1 == c2:
                pen = QPen(QColor(c2), 6)
                pen.setCapStyle(Qt.PenCapStyle.RoundCap)
                pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
                painter.setPen(pen)
                painter.drawLine(p1, p2)

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Painter 1.1")

        self.bg = Background()
        self.bg.setFixedSize(1000, 700)

        mainWidget = QWidget()
        mainWidget.setStyleSheet("background-color: #636363")

        colors = [
            "black", "white", "gray", "darkGray", "lightGray",
            "red", "green", "blue", "yellow", "cyan", "magenta", "lime", "teal", "seagreen",
            "navy", "indigo", "azure", "violet", "purple",
            "orange", "pink", "coral", "salmon", "crimson", "maroon",
            "brown", "beige", "tan", "khaki", "chocolate", "sienna", "wheat",
            "plum", "turquoise", "aquamarine", "lavender", "olive", "snow",
            "gold", "silver"
        ]

        self.colorButtons = [QPushButton(color) for color in colors]

        buttonsLayout = QGridLayout()
        buttonsLayout.setSpacing(6)

        for i, color in enumerate(self.colorButtons):
            color.setFixedSize(25, 25)
            name = color.text()

            color.setStyleSheet(
                f"background-color: {name}; color: {name};"
            )

            row = i // 8
            col = i % 8
            buttonsLayout.addWidget(color, row, col, Qt.AlignmentFlag.AlignCenter)

            color.clicked.connect(lambda checked, n=name: self.colorChanged(n))

        buttonsWidget = QWidget()
        buttonsWidget.setFixedSize(210, 130)
        buttonsWidget.setLayout(buttonsLayout)

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(buttonsWidget)
        mainLayout.addWidget(self.bg, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)

        mainWidget.setLayout(mainLayout)
        mainWidget.setMinimumSize(1050, 800)

        self.setCentralWidget(mainWidget)

    def colorChanged(self, colorname):
        self.bg.color = colorname

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
