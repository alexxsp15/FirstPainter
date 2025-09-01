import sys
from PyQt6.QtCore import Qt, QSize, QRect
from PyQt6.QtGui import QPainter, QPen, QColor, QImage, QCursor, QPixmap, QBrush
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QGridLayout, QScrollArea


class Background(QWidget):

    def __init__(self, wigth = 1000, height = 700):
        super().__init__()
        self.pos = []
        self.drawing = False
        self.fill = False
        self.color = "black"
        self.tool = "pen"

        self.start_pos = None
        self.end_pos = None

        self.image = QImage(wigth, height, QImage.Format.Format_ARGB32)
        self.image.fill(QColor("white"))

        self.setFixedSize(QSize(wigth, height))

        #Cursor
        pix = QPixmap(32, 32)
        pix.fill(Qt.GlobalColor.transparent)

        p = QPainter(pix)
        b = QBrush(QColor(self.color), Qt.BrushStyle.SolidPattern)
        p.setBrush(b)
        p.drawEllipse(12, 12, 6, 6)
        p.end()
        self.setCursor(QCursor(pix))

    def fill_feild(self, x, y):
        stack = [(x, y)]
        start_color = self.image.pixelColor(x, y).rgb()
        to_fill_color = QColor(self.color).rgb()

        if start_color == to_fill_color:
            return

        while stack:
            cx, cy = stack.pop()

            if cx < 0 or cy < 0 or cx >= self.image.width() or cy >= self.image.height():
                continue

            if self.image.pixelColor(cx, cy).rgb() != start_color:
                continue

            self.image.setPixelColor(cx, cy, QColor(self.color))

            stack.append((cx + 1, cy))
            stack.append((cx - 1, cy))
            stack.append((cx, cy + 1))
            stack.append((cx, cy - 1))

    def change_cursor(self, color):
        pix = QPixmap(32, 32)
        pix.fill(Qt.GlobalColor.transparent)
        color = self.color

        p = QPainter(pix)
        b = QBrush(QColor(color), Qt.BrushStyle.SolidPattern)
        p.setBrush(b)
        p.drawEllipse(12, 12, 6, 6)
        p.end()
        self.setCursor(QCursor(pix))

    def mousePressEvent(self, event):
        self.x = int(event.position().x())
        self.y = int(event.position().y())

        if self.fill:
            self.fill_feild(self.x, self.y)
        elif self.tool == "pen":
            self.drawing = True
            self.pos.append((event.position().toPoint(), self.color))
        elif self.tool == "rect":
            self.start_pos = event.position().toPoint()
            self.end_pos = self.start_pos
        elif self.tool == "elipse":
            self.start_pos = event.position().toPoint()
            self.end_pos = self.start_pos
        self.update()

    def mouseMoveEvent(self, event):
        if  self.drawing and self.tool == "pen":
            self.pos.append((event.position().toPoint(), self.color))

            painter = QPainter(self.image)
            for i in range(1, len(self.pos)):
                p1, c1 = self.pos[i - 1]
                p2, c2 = self.pos[i]

                if p1 is None or p2 is None:
                    continue

                if c1 == c2:
                    pen = QPen(QColor(c2), 6)
                    pen.setCapStyle(Qt.PenCapStyle.RoundCap)
                    painter.setRenderHint(QPainter.RenderHint.Antialiasing, False)
                    pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
                    painter.setPen(pen)
                    painter.drawLine(p1, p2)
            painter.end()
            self.update()

        elif self.tool == "rect" and self.start_pos:
            self.end_pos = event.position().toPoint()
            self.update()
        elif self.tool == "elipse" and self.start_pos:
            self.end_pos = event.position().toPoint()
            self.update()

    def mouseReleaseEvent(self, event):
        if self.drawing:
            self.drawing = False
            self.pos.append((None, None))
        elif self.tool == "rect" and self.start_pos:
            rect = QRect(self.start_pos, event.position().toPoint())

            painter = QPainter(self.image)
            pen = QPen(QColor(self.color), 3)
            painter.setPen(pen)
            painter.drawRect(rect)

            self.start_pos = None
            self.end_pos = None
        elif self.tool == "elipse" and self.start_pos:
            elipse = QRect(self.start_pos, event.position().toPoint())

            painter = QPainter(self.image)
            pen = QPen(QColor(self.color), 3)
            painter.setPen(pen)
            painter.drawEllipse(elipse)

        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawImage(0, 0, self.image)

        if self.tool == "rect" and self.start_pos and self.end_pos:
            pen = QPen(QColor(self.color), 3)
            painter.setPen(pen)
            rect = QRect(self.start_pos, self.end_pos)
            painter.drawRect(rect)

        if self.tool == "elipse" and self.start_pos and self.end_pos:
            pen = QPen(QColor(self.color), 3)
            painter.setPen(pen)
            elipse = QRect(self.start_pos, self.end_pos)
            painter.drawEllipse(elipse)

        painter.end()


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

        figuresList = []

        self.penButton = QPushButton("pen")
        figuresList.append(self.penButton)
        self.lineButton = QPushButton("line")
        figuresList.append(self.lineButton)
        self.curveButton = QPushButton("Curve")
        figuresList.append(self.curveButton)
        self.ovalButton = QPushButton("Oval")
        figuresList.append(self.ovalButton)
        self.roundedRect = QPushButton("RoundedRect")
        figuresList.append(self.roundedRect)
        self.rightArrowButton = QPushButton("RArrow")
        figuresList.append(self.rightArrowButton)
        self.leftArrowButton = QPushButton("LRArrow")
        figuresList.append(self.leftArrowButton)
        self.upArrowButton = QPushButton("UArrow")
        figuresList.append(self.upArrowButton)
        self.downArrowButton = QPushButton("DArrow")
        figuresList.append(self.downArrowButton)
        self.triangleButton = QPushButton("Triangle")
        figuresList.append(self.triangleButton)
        self.diamond = QPushButton("Diamond")
        figuresList.append(self.diamond)
        self.rectButton = QPushButton("rect")
        figuresList.append(self.rectButton)
        self.ellipseButton = QPushButton("elipse")
        figuresList.append(self.ellipseButton)
        self.cloud = QPushButton("Cloud")
        figuresList.append(self.cloud)
        self.thoughtBubble = QPushButton("Thought button")
        figuresList.append(self.thoughtBubble)
        self.star = QPushButton("Star")
        figuresList.append(self.star)
        self.heart = QPushButton("Heart")
        figuresList.append(self.heart)
        self.lightning = QPushButton("Lightning")
        figuresList.append(self.lightning)
        self.elipseButton = QPushButton("Ellipse")
        figuresList.append(self.elipseButton)

        self.figuresScroll = QScrollArea()
        figuresWidget = QWidget()
        figuresLayout = QGridLayout()

        for i, button  in enumerate(figuresList):
            button.setFixedSize(25, 25)

            raw = i // 4
            col = i % 4

            figuresLayout.addWidget(button, raw, col, Qt.AlignmentFlag.AlignCenter)

        figuresWidget.setLayout(figuresLayout)
        self.figuresScroll.setWidget(figuresWidget)

        self.penButton.clicked.connect(lambda: self.set_tool("pen"))
        self.rectButton.clicked.connect(lambda: self.set_tool("rect"))
        self.elipseButton.clicked.connect(lambda: self.set_tool("elipse"))

        buttonsWidget.setFixedSize(210, 130)
        buttonsWidget.setLayout(buttonsLayout)
        topLayout.addWidget(buttonsWidget)
        topLayout.addWidget(self.figuresScroll)

        topWidget.setLayout(topLayout)
        topLayout.addWidget(self.fillButton)
        topLayout.addWidget(self.penButton)


        mainLayout = QVBoxLayout()
        mainLayout.addWidget(topWidget)
        mainLayout.addWidget(self.bg, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)

        mainWidget.setLayout(mainLayout)
        mainWidget.setMinimumSize(1050, 800)

        self.setCentralWidget(mainWidget)

    def colorChanged(self, colorname):
        self.bg.color = colorname
        self.bg.change_cursor(self.bg.color)

    def change_weapon(self):
        if self.fillButton.isChecked():
            self.bg.fill = True
            print(self.bg.fill)
        else:
            self.bg.fill = False
            print(self.bg.fill)

    def set_tool(self, tool):
        self.bg.tool = tool

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
