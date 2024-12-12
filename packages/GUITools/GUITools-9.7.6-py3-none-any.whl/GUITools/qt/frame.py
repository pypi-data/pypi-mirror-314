# -*- coding: latin -*-
from PyQt6.QtWidgets import QFrame, QWidget, QStackedWidget, QPushButton, QVBoxLayout, QSplitter, QMainWindow, QApplication
from PyQt6.QtCore import Qt
from .style import Styles

def mainWindow() -> QMainWindow:
    app = QApplication.instance()

    if not app:
        return None
    
    if isinstance(app, QMainWindow):
        return widget
    
    for widget in app.topLevelWidgets():
        if isinstance(widget, QMainWindow):
            return widget

class Frame(object):

    class Expandable:
        def __init__(self, frame: QFrame, stackedWidget: QStackedWidget, btn_toggle: QPushButton, contentsMargins = [0, 0, 0, 0]):
            self.frame = frame
            self.stackedWidget = stackedWidget
            self.btn_toggle = btn_toggle
            self.contentsMargins = contentsMargins
        
            # Detecta o layout ou o splitter do pai
            parent = frame.parentWidget()
            if isinstance(parent, QSplitter):
                self.parent_widget = parent
                self.is_splitter = True
            else:
                self.parent_widget = parent.layout()
                self.is_splitter = False

            # Conecta o botão ao método toggle
            btn_toggle.clicked.connect(lambda: self.toggle())
            self.btn_toggle.setIcon(Styles.Icons.Icon(Styles.Icons.Name.full_screen, Styles.Icons.Color.GRAY))
            self.btn_toggle.setCursor(Qt.CursorShape.PointingHandCursor)


        def save_widget_state(self, widget):
            """
            Salva o estado de widgets que possuem funções relacionadas ao cursor.
            """
            state = {}
            if hasattr(widget, 'cursorPosition') and callable(widget.cursorPosition):
                state['cursor_position'] = widget.cursorPosition()
            elif hasattr(widget, 'textCursor') and callable(widget.textCursor):
                state['cursor_position'] = widget.textCursor().position()
            elif hasattr(widget, 'lineEdit') and callable(widget.lineEdit):
                line_edit = widget.lineEdit()
                if hasattr(line_edit, 'cursorPosition') and callable(line_edit.cursorPosition):
                    state['cursor_position'] = line_edit.cursorPosition()
            return state

        def restore_widget_state(self, widget, state):
            """
            Restaura o estado de widgets que possuem funções relacionadas ao cursor.
            """
            if 'cursor_position' in state:
                if hasattr(widget, 'setCursorPosition') and callable(widget.setCursorPosition):
                    widget.setCursorPosition(state['cursor_position'])
                elif hasattr(widget, 'textCursor') and callable(widget.textCursor):
                    cursor = widget.textCursor()
                    cursor.setPosition(state['cursor_position'])
                    widget.setTextCursor(cursor)
                elif hasattr(widget, 'lineEdit') and callable(widget.lineEdit):
                    line_edit = widget.lineEdit()
                    if hasattr(line_edit, 'setCursorPosition') and callable(line_edit.setCursorPosition):
                        line_edit.setCursorPosition(state['cursor_position'])

        def toggle(self):
            focused_widget = mainWindow().get_lasts_focused_widgets()[0]
            widget_state = {}
            if focused_widget:
                if self.frame.isAncestorOf(focused_widget):
                    widget_state = self.save_widget_state(focused_widget) 

            self.btn_toggle.leaveEvent(None)

            if self.frame.parent() == self.stackedWidget.currentWidget():
                self.btn_toggle.setIcon(Styles.Icons.Icon(Styles.Icons.Name.full_screen, Styles.Icons.Color.GRAY))

                parent_page = self.frame.parentWidget()
                if parent_page:
                    parent_page.layout().removeWidget(self.frame)

                self.frame.setParent(None)

                if self.is_splitter:
                    self.parent_widget.insertWidget(self.parent_widget.indexOf(self.frame), self.frame)
                else:
                    self.parent_widget.insertWidget(self.parent_widget.count(), self.frame)

                self.stackedWidget.removeWidget(parent_page)
                parent_page.deleteLater()
            else:
                self.btn_toggle.setIcon(Styles.Icons.Icon(Styles.Icons.Name.exit_full_screen, Styles.Icons.Color.GRAY))

                if self.is_splitter:
                    self.parent_widget = self.frame.parentWidget()
                    index = self.parent_widget.indexOf(self.frame)
                    self.parent_widget.widget(index).setParent(None)
                else:
                    self.parent_widget.removeWidget(self.frame)

                self.frame.setParent(None)

                page_expand = QWidget()
                page_expand.setObjectName('PageToggleExpand')

                layout = QVBoxLayout(page_expand)
                layout.setContentsMargins(*self.contentsMargins)
                layout.addWidget(self.frame)

                self.stackedWidget.addWidget(page_expand)
                self.stackedWidget.setCurrentWidget(page_expand)

            # Restaura o foco e o estado do widget
            if focused_widget and widget_state:
                focused_widget.setFocus()
                if widget_state:
                    self.restore_widget_state(focused_widget, widget_state)