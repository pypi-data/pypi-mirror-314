# -*- coding: latin -*-

from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QFrame, QSizePolicy
from PyQt6.QtCore import Qt, pyqtSignal, QMimeData, pyqtBoundSignal
from PyQt6.QtGui import QDrag, QPixmap
from .style import Styles
from typing import Type, TypeVar
T = TypeVar('T')
           
class DragDrop(QWidget):
        
    class DragItem(QFrame):
        def __init__(self, swap: pyqtBoundSignal, index: int, content_widget: QWidget):
            super().__init__()
            self._widget = content_widget
            self.swap = swap
            self.current = index
            self.setAcceptDrops(True)
            self.setContentsMargins(0, 0, 0, 0)

            # Layout para o DragItem
            layout = QHBoxLayout(self)
            layout.setContentsMargins(5, 0, 0, 0)
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
            self.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed))

        def widget(self, type : Type[T] = QWidget) -> T:
            return self._widget
            
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

    swap = pyqtSignal(int, int)

    def __init__(self, *, parent=None):
        super().__init__(parent)
        self.contents = QWidget()
        self.contents.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed))
        self.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed))
        self.contents.setContentsMargins(0, 0, 0, 0)
        self.vlayout = QVBoxLayout(self)
        self.vlayout.setContentsMargins(0, 0, 0, 0)
        self.vlayout.setSpacing(5)
        self.setAcceptDrops(True)
        self.swap.connect(self.swap_widgets)

    def add_drag_item(self, content_widget: QWidget):
        index = self.vlayout.count()
        item = self.DragItem(self.swap, index , content_widget)
        self.vlayout.addWidget(item) 
        return item

    def swap_widgets(self, pos1, pos2):
        widget1 = self.vlayout.itemAt(pos1).widget()
        widget2 = self.vlayout.itemAt(pos2).widget()
        widget1.current, widget2.current = widget2.current, widget1.current
        self.vlayout.removeWidget(widget1)
        self.vlayout.removeWidget(widget2)
        self.vlayout.insertWidget(pos1, widget2)
        self.vlayout.insertWidget(pos2, widget1)

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