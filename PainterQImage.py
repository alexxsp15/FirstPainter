import sys
from PyQt6.QtCore import Qt, QSize, QRect, QRectF
from PyQt6.QtGui import QPainter, QPen, QColor, QImage, QCursor, QPixmap, QBrush, QIcon, QPainterPath
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QGridLayout, QScrollArea
from figure_buttons_function import paint_button


class Background(QWidget):

    def __init__(self, wigth = 1000, height = 700):
        super().__init__()
        self.pos = []
        self.drawing = False
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

        if self.tool == "fill":
            self.fill_feild(self.x, self.y)
        elif self.tool == "pen":
            self.drawing = True
            self.pos.append((event.position().toPoint(), self.color))
        elif self.tool == "rect":
            self.start_pos = event.position().toPoint()
            self.end_pos = self.start_pos
        elif self.tool == "ellipse":
            self.start_pos = event.position().toPoint()
            self.end_pos = self.start_pos
        elif self.tool == "line":
            self.start_pos = event.position().toPoint()
            self.end_pos = self.start_pos
        elif self.tool == "curve":
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
        elif self.tool == "ellipse" and self.start_pos:
            self.end_pos = event.position().toPoint()
            self.update()
        elif self.tool == "line":
            self.end_pos = event.position().toPoint()
            self.update()
        elif self.tool == "curve" and self.start_pos:
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
        elif self.tool == "ellipse" and self.start_pos:
            elipse = QRect(self.start_pos, event.position().toPoint())

            painter = QPainter(self.image)
            pen = QPen(QColor(self.color), 3)
            painter.setPen(pen)
            painter.drawEllipse(elipse)
        elif self.tool == "line" and self.start_pos:
            painter = QPainter(self.image)
            pen = QPen(QColor(self.color), 3)
            painter.setPen(pen)
            painter.drawLine(self.start_pos, self.end_pos)
        elif self.tool == "curve" and self.start_pos:
            rect = QRectF(self.start_pos, event.position().toPoint())
            path = QPainterPath()
            path.moveTo(self.start_pos)
            path.arcTo(rect, 0, 180)

            painter = QPainter(self.image)
            pen = QPen(QColor(self.color), 3)
            painter.setPen(pen)
            painter.drawPath(path)
            painter.end()

            self.start_pos = None
            self.end_pos = None

            self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawImage(0, 0, self.image)

        if self.tool == "rect" and self.start_pos and self.end_pos:
            pen = QPen(QColor(self.color), 3)
            painter.setPen(pen)
            rect = QRect(self.start_pos, self.end_pos)
            painter.drawRect(rect)

        if self.tool == "ellipse" and self.start_pos and self.end_pos:
            pen = QPen(QColor(self.color), 3)
            painter.setPen(pen)
            elipse = QRect(self.start_pos, self.end_pos)
            painter.drawEllipse(elipse)

        if self.tool == "line" and self.start_pos and self.end_pos:
            pen = QPen(QColor(self.color), 3)
            painter.setPen(pen)
            painter.drawLine(self.start_pos, self.end_pos)

        if self.tool == "curve" and self.start_pos and self.end_pos:
            pen = QPen(QColor(self.color), 3)
            painter.setPen(pen)
            rect = QRectF(self.start_pos, self.end_pos)
            path = QPainterPath()
            path.moveTo(self.start_pos)
            path.arcTo(rect, 0, 180)
            painter.drawPath(path)

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
            buttonsLayout.addWidget(color, row, col)

            color.clicked.connect(lambda checked, n=name: self.colorChanged(n))

        buttonsWidget = QWidget()
        buttonsWidget.setStyleSheet("""
        QWidget {
        background-color: #696969;
        }""")

        self.fillButton = QPushButton("Заливка")
        self.fillButton.setCheckable(True)
        self.fillButton.clicked.connect(lambda: self.set_tool("fill"))

        self.figuresList = []

        self.penButton = QPushButton("pen")

        self.lineButton = QPushButton()
        self.figuresList.append(self.lineButton)
        self.curveButton = QPushButton()
        self.figuresList.append(self.curveButton)
        self.circlelButton = QPushButton()
        self.figuresList.append(self.circlelButton)
        self.roundedRect = QPushButton()
        self.figuresList.append(self.roundedRect)
        self.rightArrowButton = QPushButton()
        self.figuresList.append(self.rightArrowButton)
        self.pentagonButton = QPushButton()
        self.figuresList.append(self.pentagonButton)
        self.leftArrowButton = QPushButton()
        self.figuresList.append(self.leftArrowButton)
        self.upArrowButton = QPushButton()
        self.figuresList.append(self.upArrowButton)
        self.downArrowButton = QPushButton()
        self.figuresList.append(self.downArrowButton)
        self.triangleButton = QPushButton()
        self.figuresList.append(self.triangleButton)
        self.diamond = QPushButton()
        self.figuresList.append(self.diamond)
        self.rectButton = QPushButton()
        self.figuresList.append(self.rectButton)
        self.ellipseButton = QPushButton()
        self.figuresList.append(self.ellipseButton)
        self.cloud = QPushButton()
        self.figuresList.append(self.cloud)
        self.thoughtBubble = QPushButton()
        self.figuresList.append(self.thoughtBubble)
        self.star = QPushButton()
        self.figuresList.append(self.star)
        self.heart = QPushButton()
        self.figuresList.append(self.heart)
        self.lightning = QPushButton()
        self.figuresList.append(self.lightning)
        self.elipseButton = QPushButton()
        self.figuresList.append(self.elipseButton)
        self.idkButton = QPushButton()
        self.figuresList.append(self.idkButton)

        self.figuresScroll = QScrollArea()
        self.figuresScroll.setWidgetResizable(True)
        self.figuresScroll.setFixedWidth(150)
        self.figuresScroll.setStyleSheet("""
                QScrollBar:vertical {
                width: 10px;
                background: transparent;
                }
                QScrollBar::handle:vertical {
                border-radius: 4px;
                background: #3B3B3B;
                min-height: 20px;
                }
                QScrollBar::add-line:vertical,
                QScrollBar::sub-line:vertical {
                height: 0;  
                }
                QScrollBar::add-page:vertical,
                QScrollBar::sub-page:vertical {
                background: transparent;
                }
                """)
        figuresWidget = QWidget()
        figuresWidget.setStyleSheet("Background-color: #696969")
        figuresLayout = QGridLayout()
        figuresLayout.setSpacing(2)

        for i, button  in enumerate(self.figuresList):
            button.setFixedSize(25, 25)
            button.setStyleSheet("""
            QPushButton {
            border: 0px;
            border-radius: 3px
            }

            QPushButton:checked {
            border: 1px solid #3B3B3B;
            background-color: #242424; 
            }

            QPushButton:hover {
            background-color: #525252;
            border: 1px solid #3B3B3B;
            }""")

            raw = i // 4
            col = i % 4

            figuresLayout.addWidget(button, raw, col, Qt.AlignmentFlag.AlignCenter)

        for btn in self.figuresList:
            btn.setCheckable(True)
            btn.clicked.connect(lambda checked, b=btn: self.on_button_clicked(b))

        figuresWidget.setLayout(figuresLayout)
        self.figuresScroll.setWidget(figuresWidget)

        self.lineButton.setIcon(paint_button("line"))
        self.curveButton.setIcon(paint_button("curve"))
        self.circlelButton.setIcon(paint_button("circle"))
        self.roundedRect.setIcon(paint_button("roundedrect"))
        self.rightArrowButton.setIcon(paint_button("rightarrow"))
        self.pentagonButton.setIcon(paint_button("pentagon"))
        self.leftArrowButton.setIcon(paint_button("leftarrow"))
        self.upArrowButton.setIcon(paint_button("uparrow"))
        self.downArrowButton.setIcon(paint_button("downarrow"))
        self.triangleButton.setIcon(paint_button("triangle"))
        self.diamond.setIcon(paint_button("diamond"))
        self.rectButton.setIcon(paint_button("rect"))
        self.ellipseButton.setIcon(paint_button("ellipse"))
        self.cloud.setIcon(paint_button("cloud"))
        self.thoughtBubble.setIcon(paint_button("drop"))
        self.star.setIcon(paint_button("star"))
        self.heart.setIcon(paint_button("heart"))
        self.lightning.setIcon(paint_button("lightning"))
        self.elipseButton.setIcon(paint_button("elipse"))
        self.idkButton.setIcon(paint_button("idk"))

        self.penButton.clicked.connect(lambda: self.set_tool("pen"))
        self.rectButton.clicked.connect(lambda: self.set_tool("rect"))
        self.elipseButton.clicked.connect(lambda: self.set_tool("elipse"))
        self.lineButton.clicked.connect(lambda: self.set_tool("line"))
        self.curveButton.clicked.connect(lambda: self.set_tool("curve"))
        self.circlelButton.clicked.connect(lambda: self.set_tool("circle"))
        self.roundedRect.clicked.connect(lambda: self.set_tool("roundedrect"))
        self.rightArrowButton.clicked.connect(lambda: self.set_tool("rightarrow"))
        self.pentagonButton.clicked.connect(lambda: self.set_tool("pentagon"))
        self.leftArrowButton.clicked.connect(lambda: self.set_tool("leftarrow"))
        self.upArrowButton.clicked.connect(lambda: self.set_tool("uparrow"))
        self.downArrowButton.clicked.connect(lambda: self.set_tool("downarrow"))
        self.triangleButton.clicked.connect(lambda: self.set_tool("triangle"))
        self.diamond.clicked.connect(lambda: self.set_tool("diamond"))
        self.rectButton.clicked.connect(lambda: self.set_tool("rect"))
        self.ellipseButton.clicked.connect(lambda: self.set_tool("ellipse"))
        self.cloud.clicked.connect(lambda: self.set_tool("cloud"))
        self.thoughtBubble.clicked.connect(lambda: self.set_tool("drop"))
        self.star.clicked.connect(lambda: self.set_tool("star"))
        self.heart.clicked.connect(lambda: self.set_tool("heart"))
        self.lightning.clicked.connect(lambda: self.set_tool("lightning"))
        self.idkButton.clicked.connect(lambda: self.set_tool("idk"))

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

    def set_tool(self, tool):
        if tool == "fill":
            for btn in self.figuresList:
                btn.setChecked(False)
            self.fillButton.setChecked(True)
            self.penButton.setChecked(False)
        elif tool == "pen":
            for btn in self.figuresList:
                btn.setChecked(False)
            self.fillButton.setChecked(False)
            self.penButton.setChecked(True)
        else:
            self.fillButton.setChecked(False)
            self.penButton.setChecked(False)
        self.bg.tool = tool
        print(self.bg.tool)

    def on_button_clicked(self, clicked_btn):
        for btn in self.figuresList:
             btn.setChecked(btn is clicked_btn)

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
