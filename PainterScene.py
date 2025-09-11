import sys
from PyQt6.QtCore import Qt, QSize, QRect, QRectF, QPointF
from PyQt6.QtGui import QPainter, QPen, QColor, QImage, QCursor, QPixmap, QBrush, QIcon, QPainterPath, QWheelEvent
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QGridLayout, \
QScrollArea, QGraphicsView, QGraphicsScene, QGraphicsItem, QGraphicsProxyWidget
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
        elif self.tool == "cloud":
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
        elif self.tool == "cloud" and self.start_pos:
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
        elif self.tool == "circle" and self.start_pos:
            rect = QRect(self.start_pos, event.position().toPoint()).normalized()
            side = min(rect.width(), rect.height())
            rect.setWidth(side)
            rect.setHeight(side)
        elif self.tool == "roundedrect" and self.start_pos:
            rect = QRect(self.start_pos, event.position().toPoint())
            painter = QPainter(self.image)
            pen = QPen(QColor(self.color), 3)
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
            pen = QPen(QColor(self.color), 3)
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
            pen = QPen(QColor(self.color), 3)
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
            pen = QPen(QColor(self.color), 3)
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
            pen = QPen(QColor(self.color), 3)
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
            pen = QPen(QColor(self.color), 3)
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
            pen = QPen(QColor(self.color), 3)
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
            pen = QPen(QColor(self.color), 3)
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
            pen = QPen(QColor(self.color), 3)
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
            pen = QPen(QColor(self.color), 3)
            painter.setPen(pen)
            painter.drawPath(path)
        elif self.tool == "cloud" and self.start_pos:
            rect_x = min(self.start_pos.x(), event.position().x())
            rect_y = min(self.start_pos.y(), event.position().y())
            rect_w = abs(self.start_pos.x() - event.position().x())
            rect_h = abs(self.start_pos.y() - event.position().y())

            figure = [
                ("move", (7 / 24, 22 / 24)),
                ("line", (20 / 24, 22 / 24)),
                ("arc", (14 / 24, 14 / 24, 8 / 24, 8 / 24, 0, 100)),
                ("arc", (8 / 24, 8 / 24, 9 / 24, 9 / 24, 0, 180)),
                ("arc", (2 / 24, 14 / 24, 8 / 24, 8 / 24, 100, 200)),
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
            pen = QPen(QColor(self.color), 3)
            painter.setPen(pen)
            painter.drawPath(path)
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

        if self.tool == "circle" and self.start_pos and self.end_pos:
            pen = QPen(QColor(self.color), 3)
            painter.setPen(pen)
            rect = QRect(self.start_pos, self.end_pos).normalized()
            side = min(rect.width(), rect.height())
            rect.setWidth(side)
            rect.setHeight(side)
            painter.drawEllipse(rect)

        if self.tool == "roundedrect" and self.start_pos and self.end_pos:
            pen = QPen(QColor(self.color), 3)
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

            pen = QPen(QColor(self.color), 3)
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

            pen = QPen(QColor(self.color), 3)
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

            pen = QPen(QColor(self.color), 3)
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

            pen = QPen(QColor(self.color), 3)
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

            pen = QPen(QColor(self.color), 3)
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

            pen = QPen(QColor(self.color), 3)
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

            pen = QPen(QColor(self.color), 3)
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

            pen = QPen(QColor(self.color), 3)
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

            pen = QPen(QColor(self.color), 3)
            painter.setPen(pen)
            painter.drawPath(path)

        if self.tool == "cloud" and self.start_pos and self.end_pos:
            rect_x = min(self.start_pos.x(), self.end_pos.x())
            rect_y = min(self.start_pos.y(), self.end_pos.y())
            rect_w = abs(self.start_pos.x() - self.end_pos.x())
            rect_h = abs(self.start_pos.y() - self.end_pos.y())

            figure = [
                ("move", (7 / 24, 22 / 24)),
                ("line", (20 / 24, 22 / 24)),
                ("arc", (14 / 24, 14 / 24, 8 / 24, 8 / 24, 0, 100)),
                ("arc", (8 / 24, 8 / 24, 9 / 24, 9 / 24, 0, 180)),
                ("arc", (2 / 24, 14 / 24, 8 / 24, 8 / 24, 100, 200)),
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

            pen = QPen(QColor(self.color), 3)
            painter.setPen(pen)
            painter.drawPath(path)

        painter.end()


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Painter 1.1")

        self.bg = Background()

        self.scene = QGraphicsScene()
        self.scene.setSceneRect(-5000, -5000, 10000, 10000)
        self.scene.setBackgroundBrush(QColor("black"))

        proxy = MovableProxy()
        proxy.setWidget(self.bg)
        widget_size = self.bg.size()
        x = -widget_size.width() / 2
        y = -widget_size.height() / 2
        proxy.setPos(x, y)
        proxy.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
        self.scene.addItem(proxy)

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
        self.view = GraphicsView(self.scene)
        self.view.centerOn(proxy)
        self.view.setMinimumSize(1000, 600)
        self.view.setMinimumSize(1400, 600)
        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        mainLayout.addWidget(self.view, alignment=Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)

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
