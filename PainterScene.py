import sys, os
from PyQt6.QtCore import Qt, QSize, QRect, QRectF, QPointF
from PyQt6.QtGui import QPainter, QPen, QColor, QImage, QCursor, QPixmap, QBrush, QIcon, QPainterPath, QWheelEvent
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QGridLayout, \
    QScrollArea, QGraphicsView, QGraphicsScene, QGraphicsItem, QGraphicsProxyWidget, QSlider, QLabel, QButtonGroup
from figure_buttons_function import paint_button

class MovableProxy(QGraphicsProxyWidget):
    def __init__(self):
        super().__init__()
        self.dragging = False
        self.offset = None

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.RightButton:
            self.dragging = True
            self.offset = event.pos()
            self.setCursor(Qt.CursorShape.ClosedHandCursor)
        else:
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.dragging and (event.buttons() & Qt.MouseButton.RightButton):
            new_pos = self.mapToScene(event.pos() - self.offset)
            self.setPos(new_pos)
            self.scene().update()
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.RightButton:
            self.dragging = False
            self.setCursor(Qt.CursorShape.ArrowCursor)
        else:
            super().mouseReleaseEvent(event)

class GraphicsView(QGraphicsView):
    def __init__(self, scene):
        super().__init__(scene)
        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
        self.scale_factor = 1.15

    def wheelEvent(self, event: QWheelEvent):
        if event.angleDelta().y() > 0:
            zoom_in_factor = self.scale_factor
            self.scale(zoom_in_factor, zoom_in_factor)
        else:
            zoom_out_factor = 1 / self.scale_factor
            self.scale(zoom_out_factor, zoom_out_factor)

class Background(QWidget):

    def __init__(self, wigth = 1920, height = 1080):
        super().__init__()
        self.pos = []
        self.drawing = False
        self.color = QColor("black")
        self.tool = "pen"
        self.opt = 1
        self.penSize = 5

        self.start_pos = None
        self.end_pos = None

        self.image = QImage(wigth, height, QImage.Format.Format_ARGB32)
        self.image.fill(QColor("white"))

        self.setFixedSize(QSize(wigth, height))

        #Cursor
        pix = QPixmap(32, 32)
        pix.fill(Qt.GlobalColor.transparent)

        p = QPainter(pix)
        b = QBrush(self.color, Qt.BrushStyle.SolidPattern)
        p.setBrush(b)
        p.drawEllipse(12, 12, 6, 6)
        p.end()
        self.setCursor(QCursor(pix))

    def fill_feild(self, x, y):
        stack = [(x, y)]
        start_color = self.image.pixelColor(x, y).rgb()
        to_fill_color = self.color.rgb()

        if start_color == to_fill_color:
            return

        while stack:
            cx, cy = stack.pop()

            if cx < 0 or cy < 0 or cx >= self.image.width() or cy >= self.image.height():
                continue

            if self.image.pixelColor(cx, cy).rgb() != start_color:
                continue

            self.image.setPixelColor(cx, cy, self.color)

            stack.append((cx + 1, cy))
            stack.append((cx - 1, cy))
            stack.append((cx, cy + 1))
            stack.append((cx, cy - 1))

    def change_cursor(self, color):
        pix = QPixmap(32, 32)
        pix.fill(Qt.GlobalColor.transparent)
        color = self.color

        p = QPainter(pix)
        b = QBrush(self.color, Qt.BrushStyle.SolidPattern)
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
            point = event.position().toPoint()
            self.pos.append([point, self.color, self.penSize])

            point1 = event.position()
            painter = QPainter(self.image)
            painter.setPen(Qt.PenStyle.NoPen)  # без контуру
            painter.setBrush(self.color)
            painter.setBrush(self.color)  # заливка кольором
            radius = self.penSize / 2
            painter.drawEllipse(point1, radius, radius)

        elif self.tool == "rect":
            self.start_pos = event.position().toPoint()
            self.end_pos = self.start_pos
        elif self.tool == "ellipse":
            self.start_pos = event.position().toPoint()
            self.end_pos = self.start_pos
        elif self.tool == "line":
            self.start_pos = event.position().toPoint()
            self.end_pos = self.start_pos
        elif self.tool == "circle":
            self.start_pos = event.position().toPoint()
            self.end_pos = self.start_pos
        elif self.tool == "roundedrect":
            self.start_pos = event.position().toPoint()
            self.end_pos = self.start_pos
        elif self.tool == "rightarrow":
            self.start_pos = event.position().toPoint()
            self.end_pos = self.start_pos
        elif self.tool == "pentagon":
            self.start_pos = event.position().toPoint()
            self.end_pos = self.start_pos
        elif self.tool == "leftarrow":
            self.start_pos = event.position().toPoint()
            self.end_pos = self.start_pos
        elif self.tool == "uparrow":
            self.start_pos = event.position().toPoint()
            self.end_pos = self.start_pos
        elif self.tool == "downarrow":
            self.start_pos = event.position().toPoint()
            self.end_pos = self.start_pos
        elif self.tool == "triangle":
            self.start_pos = event.position().toPoint()
            self.end_pos = self.start_pos
        elif self.tool == "diamond":
            self.start_pos = event.position().toPoint()
            self.end_pos = self.start_pos
        elif self.tool == "star":
            self.start_pos = event.position().toPoint()
            self.end_pos = self.start_pos
        elif self.tool == "lightning":
            self.start_pos = event.position().toPoint()
            self.end_pos = self.start_pos
        elif self.tool == "heart":
            self.start_pos = event.position().toPoint()
            self.end_pos = self.start_pos

    def mouseMoveEvent(self, event):
        if self.drawing and self.tool == "pen":
            point = event.position().toPoint()
            self.pos.append((point, self.color, self.penSize))

            if len(self.pos) >= 2:
                p1, c1, a1 = self.pos[-2]
                p2, c2, a2 = self.pos[-1]

                painter = QPainter(self.image)
                pen = QPen(c2, a2)
                pen.setCapStyle(Qt.PenCapStyle.RoundCap)
                pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
                painter.setRenderHint(QPainter.RenderHint.Antialiasing, False)
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
        elif self.tool == "circle" and self.start_pos:
            self.end_pos = event.position().toPoint()
            self.update()
        elif self.tool == "roundedrect" and self.start_pos:
            self.end_pos = event.position().toPoint()
            self.update()
        elif self.tool == "rightarrow" and self.start_pos:
            self.end_pos = event.position().toPoint()
            self.update()
        elif self.tool == "pentagon" and self.start_pos:
            self.end_pos = event.position().toPoint()
            self.update()
        elif self.tool == "leftarrow" and self.start_pos:
            self.end_pos = event.position().toPoint()
            self.update()
        elif self.tool == "uparrow" and self.start_pos:
            self.end_pos = event.position().toPoint()
            self.update()
        elif self.tool == "downarrow" and self.start_pos:
            self.end_pos = event.position().toPoint()
            self.update()
        elif self.tool == "triangle" and self.start_pos:
            self.end_pos = event.position().toPoint()
            self.update()
        elif self.tool == "diamond" and self.start_pos:
            self.end_pos = event.position().toPoint()
            self.update()
        elif self.tool == "star" and self.start_pos:
            self.end_pos = event.position().toPoint()
            self.update()
        elif self.tool == "lightning" and self.start_pos:
            self.end_pos = event.position().toPoint()
            self.update()
        elif self.tool == "heart" and self.start_pos:
            self.end_pos = event.position().toPoint()
            self.update()


    def mouseReleaseEvent(self, event):
        if self.drawing:
            self.drawing = False
            self.pos.append((None, None))
        elif self.tool == "rect" and self.start_pos:
            rect = QRect(self.start_pos, event.position().toPoint())

            painter = QPainter(self.image)
            pen = QPen(self.color, self.penSize)
            painter.setPen(pen)
            painter.drawRect(rect)

            self.start_pos = None
            self.end_pos = None
        elif self.tool == "ellipse" and self.start_pos:
            elipse = QRect(self.start_pos, event.position().toPoint())

            painter = QPainter(self.image)
            pen = QPen(self.color, self.penSize)
            painter.setPen(pen)
            painter.drawEllipse(elipse)
        elif self.tool == "line" and self.start_pos:
            painter = QPainter(self.image)
            pen = QPen(self.color, self.penSize)
            painter.setPen(pen)
            painter.drawLine(self.start_pos, self.end_pos)

        elif self.tool == "circle" and self.start_pos:
            painter = QPainter(self.image)
            pen = QPen(self.color, self.penSize)
            painter.setPen(pen)
            rect = QRect(self.start_pos, self.end_pos).normalized()
            side = min(rect.width(), rect.height())
            rect.setWidth(side)
            rect.setHeight(side)
            painter.drawEllipse(rect)
        elif self.tool == "roundedrect" and self.start_pos:
            rect = QRect(self.start_pos, event.position().toPoint())
            painter = QPainter(self.image)
            pen = QPen(self.color, self.penSize)
            painter.setPen(pen)
            painter.drawRoundedRect(rect, 20, 20)
        elif self.tool == "rightarrow" and self.start_pos:
            points = [(20, 12), (12, 22), (12, 16), (3, 16), (3, 7), (12, 7), (12, 2), (20, 12)]
            normalized = [(x / 24, y / 24) for (x, y) in points]

            rect_x = min(self.start_pos.x(), event.position().x())
            rect_y = min(self.start_pos.y(), event.position().y())
            rect_w = abs(self.start_pos.x() - event.position().x())
            rect_h = abs(self.start_pos.y() - event.position().y())

            scaled = [(rect_x + x * rect_w, rect_y + y * rect_h) for (x, y) in normalized]

            path = QPainterPath()
            path.moveTo(QPointF(*scaled[0]))
            for pt in scaled[1:]:
                path.lineTo(QPointF(*pt))
            path.closeSubpath()

            painter = QPainter(self.image)
            pen = QPen(self.color, self.penSize)
            painter.setPen(pen)
            painter.drawPath(path)
        elif self.tool == "pentagon" and self.start_pos:
            points = [(12, 2), (22, 9), (17, 22), (7, 22), (2, 9), (12, 2)]
            normalized = [(x / 24, y / 24) for (x, y) in points]

            rect_x = min(self.start_pos.x(), event.position().x())
            rect_y = min(self.start_pos.y(), event.position().y())
            rect_w = abs(self.start_pos.x() - event.position().x())
            rect_h = abs(self.start_pos.y() - event.position().y())

            scaled = [(rect_x + x * rect_w, rect_y + y * rect_h) for (x, y) in normalized]

            path = QPainterPath()
            path.moveTo(QPointF(*scaled[0]))
            for pt in scaled[1:]:
                path.lineTo(QPointF(*pt))
            path.closeSubpath()

            painter = QPainter(self.image)
            pen = QPen(self.color, self.penSize)
            painter.setPen(pen)
            painter.drawPath(path)
        elif self.tool == "leftarrow" and self.start_pos:
            points = [(4, 12), (12, 22), (12, 16), (21, 16), (21, 7), (12, 7), (12, 2), (4, 12)]
            normalized = [(x / 24, y / 24) for (x, y) in points]

            rect_x = min(self.start_pos.x(), event.position().x())
            rect_y = min(self.start_pos.y(), event.position().y())
            rect_w = abs(self.start_pos.x() - event.position().x())
            rect_h = abs(self.start_pos.y() - event.position().y())

            scaled = [(rect_x + x * rect_w, rect_y + y * rect_h) for (x, y) in normalized]

            path = QPainterPath()
            path.moveTo(QPointF(*scaled[0]))
            for pt in scaled[1:]:
                path.lineTo(QPointF(*pt))
            path.closeSubpath()

            painter = QPainter(self.image)
            pen = QPen(self.color, self.penSize)
            painter.setPen(pen)
            painter.drawPath(path)
        elif self.tool == "uparrow" and self.start_pos:
            points = [(12, 2), (22, 11), (16, 11), (16, 22), (8, 22), (8, 11), (2, 11), (12, 2)]
            normalized = [(x / 24, y / 24) for (x, y) in points]

            rect_x = min(self.start_pos.x(), event.position().x())
            rect_y = min(self.start_pos.y(), event.position().y())
            rect_w = abs(self.start_pos.x() - event.position().x())
            rect_h = abs(self.start_pos.y() - event.position().y())

            scaled = [(rect_x + x * rect_w, rect_y + y * rect_h) for (x, y) in normalized]

            path = QPainterPath()
            path.moveTo(QPointF(*scaled[0]))
            for pt in scaled[1:]:
                path.lineTo(QPointF(*pt))
            path.closeSubpath()

            painter = QPainter(self.image)
            pen = QPen(self.color, self.penSize)
            painter.setPen(pen)
            painter.drawPath(path)

            self.start_pos = None
            self.end_pos = None
            self.update()
        elif self.tool == "downarrow" and self.start_pos:
            points = [(12, 22), (22, 13), (16, 13), (16, 2), (8, 2), (8, 13), (2, 13), (12, 22)]
            normalized = [(x / 24, y / 24) for (x, y) in points]

            rect_x = min(self.start_pos.x(), event.position().x())
            rect_y = min(self.start_pos.y(), event.position().y())
            rect_w = abs(self.start_pos.x() - event.position().x())
            rect_h = abs(self.start_pos.y() - event.position().y())

            scaled = [(rect_x + x * rect_w, rect_y + y * rect_h) for (x, y) in normalized]

            path = QPainterPath()
            path.moveTo(QPointF(*scaled[0]))
            for pt in scaled[1:]:
                path.lineTo(QPointF(*pt))
            path.closeSubpath()

            painter = QPainter(self.image)
            pen = QPen(self.color, self.penSize)
            painter.setPen(pen)
            painter.drawPath(path)
        elif self.tool == "triangle" and self.start_pos:
            points = [(12, 2), (22, 22), (2, 22), (12, 2)]
            normalized = [(x / 24, y / 24) for (x, y) in points]

            rect_x = min(self.start_pos.x(), event.position().x())
            rect_y = min(self.start_pos.y(), event.position().y())
            rect_w = abs(self.start_pos.x() - event.position().x())
            rect_h = abs(self.start_pos.y() - event.position().y())

            scaled = [(rect_x + x * rect_w, rect_y + y * rect_h) for (x, y) in normalized]

            path = QPainterPath()
            path.moveTo(QPointF(*scaled[0]))
            for pt in scaled[1:]:
                path.lineTo(QPointF(*pt))
            path.closeSubpath()

            painter = QPainter(self.image)
            pen = QPen(self.color, self.penSize)
            painter.setPen(pen)
            painter.drawPath(path)
        elif self.tool == "diamond" and self.start_pos:
            points = [(2, 18), (17, 18), (22, 2), (7, 2), (2, 18)]
            normalized = [(x / 24, y / 24) for (x, y) in points]

            rect_x = min(self.start_pos.x(), event.position().x())
            rect_y = min(self.start_pos.y(), event.position().y())
            rect_w = abs(self.start_pos.x() - event.position().x())
            rect_h = abs(self.start_pos.y() - event.position().y())

            scaled = [(rect_x + x * rect_w, rect_y + y * rect_h) for (x, y) in normalized]

            path = QPainterPath()
            path.moveTo(QPointF(*scaled[0]))
            for pt in scaled[1:]:
                path.lineTo(QPointF(*pt))
            path.closeSubpath()

            painter = QPainter(self.image)
            pen = QPen(self.color, self.penSize)
            painter.setPen(pen)
            painter.drawPath(path)
        elif self.tool == "star" and self.start_pos:
            points = [(12, 2), (15, 9), (22, 9), (17, 14), (19, 21), (12, 17), (5, 21), (7, 14), (2, 9), (9, 9)]
            normalized = [(x / 24, y / 24) for (x, y) in points]

            rect_x = min(self.start_pos.x(), event.position().x())
            rect_y = min(self.start_pos.y(), event.position().y())
            rect_w = abs(self.start_pos.x() - event.position().x())
            rect_h = abs(self.start_pos.y() - event.position().y())

            scaled = [(rect_x + x * rect_w, rect_y + y * rect_h) for (x, y) in normalized]

            path = QPainterPath()
            path.moveTo(QPointF(*scaled[0]))
            for pt in scaled[1:]:
                path.lineTo(QPointF(*pt))
            path.closeSubpath()

            painter = QPainter(self.image)
            pen = QPen(self.color, self.penSize)
            painter.setPen(pen)
            painter.drawPath(path)
        elif self.tool == "lightning" and self.start_pos:
            points = [(7, 2), (17, 2), (11, 13), (15, 13), (7, 22), (9, 14), (5, 14)]
            normalized = [(x / 24, y / 24) for (x, y) in points]

            rect_x = min(self.start_pos.x(), event.position().x())
            rect_y = min(self.start_pos.y(), event.position().y())
            rect_w = abs(self.start_pos.x() - event.position().x())
            rect_h = abs(self.start_pos.y() - event.position().y())

            scaled = [(rect_x + x * rect_w, rect_y + y * rect_h) for (x, y) in normalized]

            path = QPainterPath()
            path.moveTo(QPointF(*scaled[0]))
            for pt in scaled[1:]:
                path.lineTo(QPointF(*pt))
            path.closeSubpath()

            painter = QPainter(self.image)
            pen = QPen(self.color, self.penSize)
            painter.setPen(pen)
            painter.drawPath(path)
        elif self.tool == "heart" and self.start_pos:
            rect_x = min(self.start_pos.x(), event.position().x())
            rect_y = min(self.start_pos.y(), event.position().y())
            rect_w = abs(self.start_pos.x() - event.position().x())
            rect_h = abs(self.start_pos.y() - event.position().y())

            figure = [
                ("move", (12 / 24, 22 / 24)),
                ("line", (2 / 24, 8 / 24)),
                ("arc", (2 / 24, 1 / 24, 10 / 24, 10 / 24, 180, -180)),
                ("arc", (12 / 24, 1 / 24, 10 / 24, 10 / 24, 180, -180)),
                ("line", (22 / 24, 8 / 24)),
                ("line", (12 / 24, 22 / 24)),
            ]

            path = QPainterPath()
            for cmd in figure:
                if cmd[0] == "move":
                    x, y = cmd[1]
                    path.moveTo(rect_x + x * rect_w, rect_y + y * rect_h)
                elif cmd[0] == "line":
                    x, y = cmd[1]
                    path.lineTo(rect_x + x * rect_w, rect_y + y * rect_h)
                elif cmd[0] == "arc":
                    x, y, w, h, start, span = cmd[1]
                    path.arcTo(rect_x + x * rect_w,
                               rect_y + y * rect_h,
                               w * rect_w,
                               h * rect_h,
                               start, span)

            painter = QPainter(self.image)
            pen = QPen(self.color, self.penSize)
            painter.setPen(pen)
            painter.drawPath(path)
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawImage(0, 0, self.image)

        if self.tool == "rect" and self.start_pos and self.end_pos:
            pen = QPen(self.color, self.penSize)
            painter.setPen(pen)
            rect = QRect(self.start_pos, self.end_pos)
            painter.drawRect(rect)

        if self.tool == "ellipse" and self.start_pos and self.end_pos:
            pen = QPen(self.color, self.penSize)
            painter.setPen(pen)
            elipse = QRect(self.start_pos, self.end_pos)
            painter.drawEllipse(elipse)

        if self.tool == "line" and self.start_pos and self.end_pos:
            pen = QPen(self.color, self.penSize)
            painter.setPen(pen)
            painter.drawLine(self.start_pos, self.end_pos)

        if self.tool == "roundedrect" and self.start_pos and self.end_pos:
            pen = QPen(self.color, self.penSize)
            painter.setPen(pen)
            rect = QRect(self.start_pos, self.end_pos)
            painter.drawRoundedRect(rect, 20, 20)

        if self.tool == "rightarrow" and self.start_pos and self.end_pos:
            points = [(20, 12), (12, 22), (12, 16), (3, 16), (3, 7), (12, 7), (12, 2), (20, 12)]
            normalized = [(x / 24, y / 24) for (x, y) in points]

            rect_x = min(self.start_pos.x(), self.end_pos.x())
            rect_y = min(self.start_pos.y(), self.end_pos.y())
            rect_w = abs(self.start_pos.x() - self.end_pos.x())
            rect_h = abs(self.start_pos.y() - self.end_pos.y())

            scaled = [(rect_x + x * rect_w, rect_y + y * rect_h) for (x, y) in normalized]

            path = QPainterPath()
            path.moveTo(QPointF(*scaled[0]))
            for pt in scaled[1:]:
                path.lineTo(QPointF(*pt))
            path.closeSubpath()

            pen = QPen(self.color, self.penSize)
            painter.setPen(pen)
            painter.drawPath(path)

        if self.tool == "pentagon" and self.start_pos and self.end_pos:
            points = [(12, 2), (22, 9), (17, 22), (7, 22), (2, 9), (12, 2)]
            normalized = [(x / 24, y / 24) for (x, y) in points]

            rect_x = min(self.start_pos.x(), self.end_pos.x())
            rect_y = min(self.start_pos.y(), self.end_pos.y())
            rect_w = abs(self.start_pos.x() - self.end_pos.x())
            rect_h = abs(self.start_pos.y() - self.end_pos.y())

            scaled = [(rect_x + x * rect_w, rect_y + y * rect_h) for (x, y) in normalized]

            path = QPainterPath()
            path.moveTo(QPointF(*scaled[0]))
            for pt in scaled[1:]:
                path.lineTo(QPointF(*pt))
            path.closeSubpath()

            pen = QPen(self.color, self.penSize)
            painter.setPen(pen)
            painter.drawPath(path)

        if self.tool == "leftarrow" and self.start_pos and self.end_pos:
            points = [(4, 12), (12, 22), (12, 16), (21, 16), (21, 7), (12, 7), (12, 2), (4, 12)]
            normalized = [(x / 24, y / 24) for (x, y) in points]

            rect_x = min(self.start_pos.x(), self.end_pos.x())
            rect_y = min(self.start_pos.y(), self.end_pos.y())
            rect_w = abs(self.start_pos.x() - self.end_pos.x())
            rect_h = abs(self.start_pos.y() - self.end_pos.y())

            scaled = [(rect_x + x * rect_w, rect_y + y * rect_h) for (x, y) in normalized]

            path = QPainterPath()
            path.moveTo(QPointF(*scaled[0]))
            for pt in scaled[1:]:
                path.lineTo(QPointF(*pt))
            path.closeSubpath()

            pen = QPen(self.color, self.penSize)
            painter.setPen(pen)
            painter.drawPath(path)

        if self.tool == "uparrow" and self.start_pos and self.end_pos:
            points = [(12, 2), (22, 11), (16, 11), (16, 22), (8, 22), (8, 11), (2, 11), (12, 2)]
            normalized = [(x / 24, y / 24) for (x, y) in points]

            rect_x = min(self.start_pos.x(), self.end_pos.x())
            rect_y = min(self.start_pos.y(), self.end_pos.y())
            rect_w = abs(self.start_pos.x() - self.end_pos.x())
            rect_h = abs(self.start_pos.y() - self.end_pos.y())

            scaled = [(rect_x + x * rect_w, rect_y + y * rect_h) for (x, y) in normalized]

            path = QPainterPath()
            path.moveTo(QPointF(*scaled[0]))
            for pt in scaled[1:]:
                path.lineTo(QPointF(*pt))
            path.closeSubpath()

            pen = QPen(self.color, self.penSize)
            painter.setPen(pen)
            painter.drawPath(path)

        if self.tool == "downarrow" and self.start_pos and self.end_pos:
            points = [(12, 22), (22, 13), (16, 13), (16, 2), (8, 2), (8, 13), (2, 13), (12, 22)]
            normalized = [(x / 24, y / 24) for (x, y) in points]

            rect_x = min(self.start_pos.x(), self.end_pos.x())
            rect_y = min(self.start_pos.y(), self.end_pos.y())
            rect_w = abs(self.start_pos.x() - self.end_pos.x())
            rect_h = abs(self.start_pos.y() - self.end_pos.y())

            scaled = [(rect_x + x * rect_w, rect_y + y * rect_h) for (x, y) in normalized]

            path = QPainterPath()
            path.moveTo(QPointF(*scaled[0]))
            for pt in scaled[1:]:
                path.lineTo(QPointF(*pt))
            path.closeSubpath()

            pen = QPen(self.color, self.penSize)
            painter.setPen(pen)
            painter.drawPath(path)

        if self.tool == "triangle" and self.start_pos and self.end_pos:
            points = [(12, 2), (22, 22), (2, 22), (12, 2)]
            normalized = [(x / 24, y / 24) for (x, y) in points]

            rect_x = min(self.start_pos.x(), self.end_pos.x())
            rect_y = min(self.start_pos.y(), self.end_pos.y())
            rect_w = abs(self.start_pos.x() - self.end_pos.x())
            rect_h = abs(self.start_pos.y() - self.end_pos.y())

            scaled = [(rect_x + x * rect_w, rect_y + y * rect_h) for (x, y) in normalized]

            path = QPainterPath()
            path.moveTo(QPointF(*scaled[0]))
            for pt in scaled[1:]:
                path.lineTo(QPointF(*pt))
            path.closeSubpath()

            pen = QPen(self.color, self.penSize)
            painter.setPen(pen)
            painter.drawPath(path)

        if self.tool == "diamond" and self.start_pos and self.end_pos:
            points = [(2, 18), (17, 18), (22, 2), (7, 2), (2, 18)]
            normalized = [(x / 24, y / 24) for (x, y) in points]

            rect_x = min(self.start_pos.x(), self.end_pos.x())
            rect_y = min(self.start_pos.y(), self.end_pos.y())
            rect_w = abs(self.start_pos.x() - self.end_pos.x())
            rect_h = abs(self.start_pos.y() - self.end_pos.y())

            scaled = [(rect_x + x * rect_w, rect_y + y * rect_h) for (x, y) in normalized]

            path = QPainterPath()
            path.moveTo(QPointF(*scaled[0]))
            for pt in scaled[1:]:
                path.lineTo(QPointF(*pt))
            path.closeSubpath()

            pen = QPen(self.color, self.penSize)
            painter.setPen(pen)
            painter.drawPath(path)

        if self.tool == "star" and self.start_pos and self.end_pos:
            points = [(12, 2), (15, 9), (22, 9), (17, 14), (19, 21), (12, 17), (5, 21), (7, 14), (2, 9), (9, 9)]
            normalized = [(x / 24, y / 24) for (x, y) in points]

            rect_x = min(self.start_pos.x(), self.end_pos.x())
            rect_y = min(self.start_pos.y(), self.end_pos.y())
            rect_w = abs(self.start_pos.x() - self.end_pos.x())
            rect_h = abs(self.start_pos.y() - self.end_pos.y())

            scaled = [(rect_x + x * rect_w, rect_y + y * rect_h) for (x, y) in normalized]

            path = QPainterPath()
            path.moveTo(QPointF(*scaled[0]))
            for pt in scaled[1:]:
                path.lineTo(QPointF(*pt))
            path.closeSubpath()

            pen = QPen(self.color, self.penSize)
            painter.setPen(pen)
            painter.drawPath(path)

        if self.tool == "lightning" and self.start_pos and self.end_pos:
            points = [(7, 2), (17, 2), (11, 13), (15, 13), (7, 22), (9, 14), (5, 14)]
            normalized = [(x / 24, y / 24) for (x, y) in points]

            rect_x = min(self.start_pos.x(), self.end_pos.x())
            rect_y = min(self.start_pos.y(), self.end_pos.y())
            rect_w = abs(self.start_pos.x() - self.end_pos.x())
            rect_h = abs(self.start_pos.y() - self.end_pos.y())

            scaled = [(rect_x + x * rect_w, rect_y + y * rect_h) for (x, y) in normalized]

            path = QPainterPath()
            path.moveTo(QPointF(*scaled[0]))
            for pt in scaled[1:]:
                path.lineTo(QPointF(*pt))
            path.closeSubpath()

            pen = QPen(self.color, self.penSize)
            painter.setPen(pen)
            painter.drawPath(path)

        if self.tool == "heart" and self.start_pos and self.end_pos:
            rect_x = min(self.start_pos.x(), self.end_pos.x())
            rect_y = min(self.start_pos.y(), self.end_pos.y())
            rect_w = abs(self.start_pos.x() - self.end_pos.x())
            rect_h = abs(self.start_pos.y() - self.end_pos.y())

            figure = [
                ("move", (12 / 24, 22 / 24)),
                ("line", (2 / 24, 8 / 24)),
                ("arc", (2 / 24, 1 / 24, 10 / 24, 10 / 24, 180, -180)),
                ("arc", (12 / 24, 1 / 24, 10 / 24, 10 / 24, 180, -180)),
                ("line", (22 / 24, 8 / 24)),
                ("line", (12 / 24, 22 / 24)),
            ]

            path = QPainterPath()
            for cmd in figure:
                if cmd[0] == "move":
                    x, y = cmd[1]
                    path.moveTo(rect_x + x * rect_w, rect_y + y * rect_h)
                elif cmd[0] == "line":
                    x, y = cmd[1]
                    path.lineTo(rect_x + x * rect_w, rect_y + y * rect_h)
                elif cmd[0] == "arc":
                    x, y, w, h, start, span = cmd[1]
                    path.arcTo(rect_x + x * rect_w,
                               rect_y + y * rect_h,
                               w * rect_w,
                               h * rect_h,
                               start, span)

            pen = QPen(self.color, self.penSize)
            painter.setPen(pen)
            painter.drawPath(path)

        painter.end()

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS  # коли збираємо .exe
    except Exception:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Painter 1.1")

        self.bg = Background()

        self.scene = QGraphicsScene()
        self.scene.setSceneRect(-5000, -5000, 10000, 10000)
        self.scene.setBackgroundBrush(QColor.fromString("#1a1a1a"))

        proxy = MovableProxy()
        proxy.setWidget(self.bg)
        widget_size = self.bg.size()
        x = -widget_size.width() / 2
        y = -widget_size.height() / 2
        proxy.setPos(x, y)
        proxy.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
        self.scene.addItem(proxy)

        mainWidget = QWidget()
        mainWidget.setStyleSheet("background-color: #1e1e1e")

        topWidget = QWidget()
        topWidget.setStyleSheet("""background-color: #2c2c2c;""")
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
        buttonsLayout.setSpacing(0)

        self.colorGroup = QButtonGroup(self)
        self.colorGroup.setExclusive(True)

        for i, color in enumerate(self.colorButtons):
            color.setFixedSize(25, 25)
            color.setCheckable(True)
            name = color.text()

            color.setStyleSheet(f"""
                QPushButton {{
                    background-color: {name};
                    color: {name};   
                    border-radius: 6px;
                    padding: 5px;
                }}

                QPushButton:checked {{
                    border: 2px solid #00c8c8;
                }}
            """)

            row = i // 8
            col = i % 8
            buttonsLayout.addWidget(color, row, col)

            self.colorGroup.addButton(color)

            color.clicked.connect(lambda checked, n=name: self.colorChanged(n))

        buttonsWidget = QWidget()
        buttonsWidget.setStyleSheet("""
        QWidget {
        Background-color: #2c2c2c; 
        border: 1px solid #3b3b3b; 
        border-radius: 5px;
        }""")

        self.fillButton = QPushButton()
        self.fillButton.setIcon(QIcon(resource_path(("icons/icons8-fill-color-26.png"))))
        self.fillButton.setCheckable(True)
        self.fillButton.setFixedSize(50,50)
        self.fillButton.clicked.connect(lambda: self.set_tool("fill"))
        self.fillButton.setStyleSheet("""
                QPushButton {
                border: 2px solid #3b3b3b; 
                border-radius: 5px;
                }
                QPushButton:checked {
                border: 2px solid #00c8c8;
                border-radius: 5px;
                }
                """)

        self.optSlider = QSlider()
        self.sizeSlider = QSlider()
        self.optSlider.setRange(0, 100)
        self.sizeSlider.setRange(0,300)
        self.optSlider.setOrientation(Qt.Orientation.Horizontal)
        self.sizeSlider.setOrientation(Qt.Orientation.Horizontal)

        self.optLabel = QLabel("Transparency:")
        self.sizeLabel = QLabel("Size:")
        self.optLabel.setStyleSheet("""
        QLabel {
        color: #cccccc;
        font-size: 17px;
        font-weight: bold;
        }
        """)
        self.sizeLabel.setStyleSheet("""
                QLabel {
                color: #cccccc;
                font-size: 17px;
                font-weight: bold;
                }
                """)

        self.slidersWidget = QWidget()
        self.slidersLayout = QVBoxLayout()
        self.slidersLayout.addWidget(self.optLabel)
        self.slidersLayout.addWidget(self.optSlider)
        self.slidersLayout.addWidget(self.sizeLabel)
        self.slidersLayout.addWidget(self.sizeSlider)

        self.optSlider.valueChanged.connect(self.chage_opt)
        self.sizeSlider.valueChanged.connect(self.change_size)
        self.optSlider.setSliderPosition(100)
        self.sizeSlider.setSliderPosition(5)

        self.sizeSlider.setStyleSheet("""
        QSlider::groove {
        border: 0px;
        height: 3px;
        background: #707070;
        }
        QSlider::handle {
        width: 6px;
        height: 6px;
        margin: -5px 0;
        background-color: #00c8c8;
        }
        QSlider::add-page {
        background-color: #4a4a4a;
        }
        """)

        self.optSlider.setStyleSheet("""
                QSlider::groove {
                border: 0px;
                height: 3px;
                background: #707070;
                }
                QSlider::handle {
                width: 6px;
                height: 6px;
                margin: -5px 0;
                background-color: #00c8c8;
                }
                QSlider::add-page {
                background-color: #4a4a4a;
                }
                """)

        self.slidersWidget.setObjectName("slidersWidget")
        self.slidersWidget.setStyleSheet("""
            QWidget#slidersWidget {
                background-color: #2c2c2c;
                border: 2px solid #3b3b3b;
                border-radius: 5px;
            }
        """)

        self.slidersWidget.setLayout(self.slidersLayout)

        self.figuresList = []

        self.penButton = QPushButton()
        self.penButton.setCheckable(True)
        self.penButton.setFixedSize(50,50)
        self.penButton.setIcon(QIcon(resource_path("icons/icons8-pencil-50.png")))
        self.penButton.setStyleSheet("""
        QPushButton {
        border: 2px solid #3b3b3b; 
        border-radius: 5px;
        }
        QPushButton:checked {
        border: 2px solid #00c8c8;
        border-radius: 5px;
        }
        """)

        self.lineButton = QPushButton()
        self.figuresList.append(self.lineButton)
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
        self.star = QPushButton()
        self.figuresList.append(self.star)
        self.heart = QPushButton()
        self.figuresList.append(self.heart)
        self.lightning = QPushButton()
        self.figuresList.append(self.lightning)

        self.figuresScroll = QScrollArea()
        self.figuresScroll.setWidgetResizable(True)
        self.figuresScroll.setFixedWidth(150)
        figuresWidget = QWidget()
        figuresWidget.setStyleSheet("Background-color: #2c2c2c; border: 2px solid #3b3b3b; border-radius: 5px;")
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
            border: 2px solid #00c8c8;
            background-color: #3b3b3b;
            }
            """)

            raw = i // 4
            col = i % 4

            figuresLayout.addWidget(button, raw, col, Qt.AlignmentFlag.AlignCenter)

        for btn in self.figuresList:
            btn.setCheckable(True)
            btn.clicked.connect(lambda checked, b=btn: self.on_button_clicked(b))

        figuresWidget.setLayout(figuresLayout)
        self.figuresScroll.setWidget(figuresWidget)

        self.lineButton.setIcon(paint_button("line"))
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
        self.star.setIcon(paint_button("star"))
        self.heart.setIcon(paint_button("heart"))
        self.lightning.setIcon(paint_button("lightning"))

        self.penButton.clicked.connect(lambda: self.set_tool("pen"))
        self.rectButton.clicked.connect(lambda: self.set_tool("rect"))
        self.lineButton.clicked.connect(lambda: self.set_tool("line"))
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
        self.star.clicked.connect(lambda: self.set_tool("star"))
        self.heart.clicked.connect(lambda: self.set_tool("heart"))
        self.lightning.clicked.connect(lambda: self.set_tool("lightning"))

        buttonsWidget.setFixedSize(210, 130)
        buttonsWidget.setLayout(buttonsLayout)
        topLayout.addWidget(buttonsWidget)
        topLayout.addWidget(self.figuresScroll)

        self.downloadButton = QPushButton("Download")
        self.downloadButton.setFixedSize(150, 50)
        self.downloadButton.setIcon(QIcon(resource_path("icons/icons8-download-64.png")))
        self.downloadButton.setStyleSheet("""
        QPushButton {
        font-size: 13px;
        color:#cccccc;
        font-weight: bold;       
        border: 2px solid #3b3b3b; 
        border-radius: 5px;
        }
        QPushButton:pressed {
        border: 2px solid #00c8c8;
        border-radius: 5px;
        }
        """)


        topWidget.setLayout(topLayout)
        topLayout.addWidget(self.fillButton)
        topLayout.addWidget(self.penButton)
        topLayout.addWidget(self.slidersWidget)
        topLayout.addWidget(self.downloadButton)


        mainLayout = QVBoxLayout()
        mainLayout.addWidget(topWidget)
        self.view = GraphicsView(self.scene)
        self.view.centerOn(proxy)
        self.view.setMinimumSize(1000, 600)
        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        mainLayout.addWidget(self.view, alignment=Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)

        mainWidget.setLayout(mainLayout)
        mainWidget.setMinimumSize(1050, 800)

        self.setCentralWidget(mainWidget)

    def colorChanged(self, colorname):
        self.bg.color = QColor(colorname)
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

    def chage_opt(self):
        o = self.optSlider.value()
        print(f"St : {o}")
        o = o / 100
        print(f"Fin : {o}")
        self.bg.opt = o

        self.bg.color.setAlphaF(o)

    def change_size(self):
        s = self.sizeSlider.value()
        self.bg.penSize = s
        print(self.bg.penSize)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    app.setWindowIcon(QIcon(resource_path("icons/icons8-paint-100.ico")))

    window = MainWindow()
    window.show()
    sys.exit(app.exec())