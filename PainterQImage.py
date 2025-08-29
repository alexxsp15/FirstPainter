import sys
from PyQt6.QtCore import Qt, QSize, QRect
from PyQt6.QtGui import QPainter, QPen, QColor, QImage
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QGridLayout


class Background(QWidget):

    def __init__(self, wigth = 1000, height = 700):
        super().__init__()
        self.pos = []
        self.drawing = False
        self.fill = False
        self.figure = False
        self.color = "black"
        self.tool = "pen"

        self.start_posX = 0
        self.end_posX = 0
        self.start_posY = 0
        self.end_posY = 0

        self.image = QImage(wigth, height, QImage.Format.Format_ARGB32)
        self.image.fill(QColor("white"))

        self.setFixedSize(QSize(wigth, height))

    def fill_feild(self, x, y):
        stack = [(x, y)]
        start_color = self.image.pixelColor(x, y)
        to_fill_color = QColor(self.color)
        stack.append((x, y))

        if start_color == to_fill_color:
            return

        while stack:
            cx, cy = stack.pop()

            if cx < 0 or cy < 0 or cx >= self.image.width() or cy >= self.image.height():
                continue

            if self.image.pixelColor(cx, cy) != start_color:
                continue

            self.image.setPixelColor(cx, cy, to_fill_color)

            stack.append((cx + 1, cy))
            stack.append((cx - 1, cy))
            stack.append((cx, cy + 1))
            stack.append((cx, cy - 1))

    def draw_fig(self, start, end, tool):
        pass


    def mousePressEvent(self, event):
        self.x = int(event.position().x())
        self.y = int(event.position().y())

        if self.fill:
            self.fill_feild(self.x, self.y)
        elif self.tool == "pen":
            self.drawing = True
            self.pos.append((event.position().toPoint(), self.color))
        else:
            self.start_posX = event.position().x()
            self.start_posY = event.position().y()
        self.update()

    def mouseReleaseEvent(self, event):
        self.drawing = False
        self.pos.append((None, None))

    def mouseMoveEvent(self, event):
        if  self.drawing == True:
            self.pos.append((event.position().toPoint(), self.color))
            self.update()
        else:
            self.end_posX = event.position().x()
            self.end_posY = event.position().y()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawImage(0, 0, self.image)


        for i in range(1, len(self.pos)):
            painter = QPainter(self.image)
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
            painter.end()

        if self.figure:
            painter.drawRect(self.calculateRect(self.start_posX, self.start_posY, self.end_posX, self.end_posY))

    def calculateRect(self, sx, sy, ex, ey):
        x = sx
        y = sy
        w = abs(sx - ex)
        h = abs(sy - ey)

        return QRect(x, y, w ,h)

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Painter 1.1")

        self.bg = Background()
        #self.bg.setFixedSize(1000, 700)

        mainWidget = QWidget()
        mainWidget.setStyleSheet("background-color: #808080")

        topWidget = QWidget()
        topLayout = QHBoxLayout()

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
                f"background-color: {name}; color: {name}; "
            )

            row = i // 8
            col = i % 8
            buttonsLayout.addWidget(color, row, col, Qt.AlignmentFlag.AlignCenter)

            color.clicked.connect(lambda checked, n=name: self.colorChanged(n))

        buttonsWidget = QWidget()
        buttonsWidget.setStyleSheet("""
        QWidget {
        background-color: #696969;
        }""")

        self.fillButton = QPushButton("Заливка")
        self.fillButton.setCheckable(True)
        self.fillButton.toggled.connect(self.change_weapon)

        self.penButton = QPushButton("pen")
        self.rectButton = QPushButton("rect")

        self.penButton.clicked.connect(lambda: self.set_tool("pen"))
        self.rectButton.clicked.connect(lambda: self.set_tool("rect"))

        buttonsWidget.setFixedSize(210, 130)
        buttonsWidget.setLayout(buttonsLayout)
        topLayout.addWidget(buttonsWidget)

        topWidget.setLayout(topLayout)
        topLayout.addWidget(self.fillButton)
        topLayout.addWidget(self.penButton)
        topLayout.addWidget(self.rectButton)

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(topWidget)
        mainLayout.addWidget(self.bg, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)

        mainWidget.setLayout(mainLayout)
        mainWidget.setMinimumSize(1050, 800)

        self.setCentralWidget(mainWidget)

    def colorChanged(self, colorname):
        self.bg.color = colorname

    def change_weapon(self):
        if self.fillButton.isChecked():
            self.bg.fill = True
            print(self.bg.fill)
        else:
            self.bg.fill = False
            print(self.bg.fill)

    def set_tool(self, tool):
        self.bg.tool = tool
        if tool == "pen":
            self.bg.figure = False
        else:
            self.bg.figure = True

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
