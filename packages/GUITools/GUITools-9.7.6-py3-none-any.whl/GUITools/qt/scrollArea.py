# -*- coding: latin -*-

from PyQt6.QtWidgets import QScrollArea, QWidget, QHBoxLayout, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt, pyqtSignal, QMimeData, pyqtBoundSignal, QCoreApplication
from PyQt6.QtGui import QDrag, QPixmap
from .style import Styles

class DragItem(QWidget):
    def __init__(self, swap: pyqtBoundSignal, index: int, content_widget: QWidget):
        super().__init__()
        self.swap = swap
        self.current = index
        self.setAcceptDrops(True)
        self.setContentsMargins(0, 0, 0, 0)

        # Layout para o DragItem
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)

        # Label de arrastar
        self.drag_label = QLabel(self)
        self.drag_label.setFixedSize(16, 16)
        self.drag_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        Styles.set_icon_theme(self.drag_label, Styles.Icons.Name.drag_drop,Styles.Icons.Name.drag_drop, Styles.Icons.Color.GRAY, Styles.Icons.Color.THEME, 16)

        # Conteúdo personalizado passado ao DragItem
        layout.addWidget(self.drag_label, alignment=Qt.AlignmentFlag.AlignVCenter)
        layout.addWidget(content_widget)
        self.setLayout(layout)
        
    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.acceptProposedAction()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasText():
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event):
        source_pos = int(event.mimeData().text())
        current_pos = self.current
        self.swap.emit(*sorted([source_pos, current_pos]))

    def mouseMoveEvent(self, event):
        if self.drag_label.geometry().contains(event.pos()):
            drag = QDrag(self)
            mime = QMimeData()
            mime.setText(str(self.current))

            pixmap = QPixmap(self.size())
            self.render(pixmap)
            mime.setImageData(pixmap)
            drag.setMimeData(mime)
            drag.setPixmap(pixmap)
            drag.setHotSpot(event.pos())  # Set the drag hot spot
            drag.exec(Qt.DropAction.MoveAction)
           
class ScrollArea(object):

    class DragDrop(QScrollArea):
        swap = pyqtSignal(int, int)

        def __init__(self, *, adjust_height=False, parent=None):
            super().__init__(parent)
            self.adjust_height = adjust_height
            self.setWidgetResizable(True)
            self.contents = QWidget()
            self.contents.setContentsMargins(0, 0, 0, 0)
            self.setWidget(self.contents)
            self.layout = QVBoxLayout(self.contents)
            self.setAcceptDrops(True)
            self.swap.connect(self.swap_widgets)

        def adjustHeight(self, min_height = 0, max_height = 0):
            self.adjustSize()
            height = self.size().height()
            widget_height = height + self.contentsMargins().top() + self.contentsMargins().bottom()
        
            widget_height += self.horizontalScrollBar().maximum()

            new_height = int(widget_height)
        
            if new_height < min_height:
                new_height = min_height
            if new_height > max_height and max_height > 0:
                new_height = max_height

            self.setFixedHeight(new_height)
           

        def add_drag_item(self, content_widget: QWidget):
            index = self.layout.count()
            item = DragItem(self.swap, index , content_widget)
            self.layout.addWidget(item) 
            if index == 0 and self.adjust_height:
                QCoreApplication.processEvents()
            if self.adjust_height:
                self.adjustHeight()

        def swap_widgets(self, pos1, pos2):
            widget1 = self.layout.itemAt(pos1).widget()
            widget2 = self.layout.itemAt(pos2).widget()
            widget1.current, widget2.current = widget2.current, widget1.current
            self.layout.removeWidget(widget1)
            self.layout.removeWidget(widget2)
            self.layout.insertWidget(pos1, widget2)
            self.layout.insertWidget(pos2, widget1)

        def dragEnterEvent(self, event):
            if event.mimeData().hasText():
                event.acceptProposedAction()
            else:
                event.ignore()

        def dragMoveEvent(self, event):
            if event.mimeData().hasText():
                event.acceptProposedAction()
            else:
                event.ignore()

        def dropEvent(self, event):
            event.acceptProposedAction()