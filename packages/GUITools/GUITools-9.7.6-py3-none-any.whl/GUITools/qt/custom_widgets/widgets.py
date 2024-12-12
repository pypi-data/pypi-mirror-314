from PyQt6.QtWidgets import QSizePolicy, QLabel, QPushButton, QHBoxLayout, QWidget, QCheckBox, QComboBox, QWidget, QWidgetAction, QVBoxLayout, QScrollArea, QFrame, QSpacerItem
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt
from .chat_message import WidgetMessage
from ..style import Styles
from ..comboBox import ComboBox
from .webEngineView import CustomWebEngineView
from .sideBar import SideBar
from .dockWidget import TabWidgetDock, StackedWidgetDock
from .resizeLabel import ResizeLabel
from .codeEditor import CodeEditor

class CustomWidgets(object):

    class Widget(QWidget):
        def __init__(self, *, children : QWidget = None, parent = None):
            super().__init__(parent)
            layout = QHBoxLayout()
            layout.setContentsMargins(0, 0, 0, 0)
            if children is not None:
                layout.addWidget(children)
            self.setStyleSheet("background-color: 'transparent';")
            self.setLayout(layout)

    class CodeEditor(CodeEditor):
        ...

    class StackedWidgetDock(StackedWidgetDock):
        ...

    class TabWidgetDock(TabWidgetDock):
        ...
            
    class SideBar(SideBar):
        ...

    class WebEngineView(CustomWebEngineView):
        ...

    class WidgetMessage(WidgetMessage):
        ...

    class ResizeLabel(ResizeLabel):
        ...

    class ActionDelete(QWidgetAction):
        def __init__(self, parent : object, action_delete : object = None, text = "Delete"):
             super().__init__(parent)
             self.btn_delete = QPushButton(text)
             Styles.set_icon_theme(self.btn_delete, Styles.Icons.Name.lixo, Styles.Icons.Name.lixo, Styles.Icons.Color.GRAY, Styles.Icons.Color.THEME)
             Styles.set_widget_style_theme(Styles.button(transparent=True), self.btn_delete)
             self.action_delete = action_delete
             self.btn_delete.clicked.connect(self.delete)
             widget = QWidget()
             layout = QHBoxLayout()
             layout.setContentsMargins(0, 0, 0, 0)
             layout.addWidget(self.btn_delete)
             widget.setLayout(layout)
             self.setDefaultWidget(widget)

        def delete(self):
            if self.action_delete != None:
             self.action_delete()

    class LabelAndPushButton(QWidget):
        def __init__(self, label_text : str, pushButton_func : object, icon_data : Styles.Icons.Data = None,  parent = None):
            super().__init__(parent)

            self.label = QLabel()
            self.label.setText(label_text)
            self.label.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred))
            self.pushButton = QPushButton()
            self.pushButton.clicked.connect(pushButton_func)

            if icon_data:
                Styles.set_icon_theme_from_data(self.pushButton, icon_data)
            self.pushButton.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred))
            layout = QHBoxLayout()
            layout.addWidget(self.label)
            layout.addWidget(self.pushButton)
            layout.setContentsMargins(0, 0, 0, 0)
            self.setLayout(layout)

    class IconLabelPushButton(QWidget):
        def __init__(self, text, pushButton_func : object, pushButton_icon_data : Styles.Icons.Data = None, label_icon_data : Styles.Icons.Data = None, icon_size = 16, margins = (0, 0, 0, 0),  parent=None):
            super().__init__(parent)
            self.selected = False
            layout = QHBoxLayout()
            layout.setContentsMargins(*margins)
            self.icon_label = QLabel()
            self.label_text = QLabel()
            self.label_text.setText(text)
            self.label_text.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding))
            self.icon_label.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding))
            self.pushButton = QPushButton()
            self.pushButton.setMinimumWidth(40)
            self.pushButton.setSizePolicy( QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding))
            self.pushButton.clicked.connect(pushButton_func)
            self.label_icon_data = label_icon_data
            self.icon_size = icon_size

            if label_icon_data:
                if label_icon_data.color == Styles.Icons.Color.THEME:
                    Styles.set_pixmap_theme(self.icon_label, label_icon_data.name, icon_size)
                else:
                    self.icon_label.setPixmap(Styles.Icons.Icon(label_icon_data.name, label_icon_data.color).toPixmap(icon_size))
                layout.addWidget(self.icon_label)
    
            if pushButton_icon_data:
                Styles.set_icon_theme_from_data(self.pushButton, pushButton_icon_data)

            btn_style = Styles.button(transparent=True)
            btn_style.button.border.radius = 2
            Styles.set_widget_style_theme(btn_style, self.pushButton)


            layout.addWidget(self.label_text)
            layout.addWidget(self.pushButton)

            self.setStyleSheet('''
                        background-color: 'transparent';
            ''')

            self.setLayout(layout)

        def SelectionChanged(self, selected : bool):
            if self.label_icon_data:
                if selected != self.selected:
                    if selected:
                        if self.label_icon_data.color == Styles.Icons.Color.THEME:
                            Styles.set_pixmap_theme(self.icon_label, self.label_icon_data.hover_name, self.icon_size)
                        else:
                            self.icon_label.setPixmap(Styles.Icons.Icon(self.label_icon_data.hover_name, self.label_icon_data.hover_color).toPixmap(self.icon_size))
                    else:
                        if self.label_icon_data.color == Styles.Icons.Color.THEME:
                            Styles.set_pixmap_theme(self.icon_label, self.label_icon_data.name, self.icon_size)
                        else:
                            self.icon_label.setPixmap(Styles.Icons.Icon(self.label_icon_data.name, self.label_icon_data.color).toPixmap(self.icon_size))
            self.selected = selected


    class CheckBoxAndComboBox(QWidget):
        def __init__(self, checkBox_text : str, comboBox_data : ComboBox.DataUpdate, checked : bool = False, checkBox_func : object = None, comboBox_func : object = None, index_comboBox = 0,  parent = None):
            super().__init__(parent)

            self.comboBox = QComboBox()
            ComboBox.update_data(self.comboBox, comboBox_data)
            if comboBox_data.items:
                self.comboBox.setCurrentIndex(index_comboBox)
            self.checkBox = QCheckBox()
            self.checkBox.setText(checkBox_text)
            self.checkBox.setChecked(checked)
            self.checkBox.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed))
            self.comboBox.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred))
            
            ComboBox.ignoreWheelEvent(self.comboBox)
        
            if checkBox_func:
                self.checkBox.toggled.connect(checkBox_func)
            if comboBox_func:
                self.comboBox.activated.connect(comboBox_func)

            layout = QHBoxLayout()
            layout.addWidget(self.checkBox)
            layout.addWidget(self.comboBox)
            layout.setContentsMargins(0, 0, 0, 0)
            layout.setSpacing(0)
            self.setLayout(layout)


    class IconLabel(QWidget):
        def __init__(self, text, icon : Styles.Icons.Icon = None, icon_data : Styles.Icons.Data = None, icon_size = 16, margins = (0, 0, 0, 0), parent=None):
            super().__init__(parent)
            self.selected = False
            self.icon = icon
            self.icon_data = icon_data
            self.icon_size = icon_size
            layout = QHBoxLayout()
            layout.setContentsMargins(*margins)
            self.icon_label = QLabel()
            self.label_text = QLabel()
            self.label_text.setText(text)
            size_policy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
            self.icon_label.setSizePolicy(size_policy)

            if icon_data:
                if icon_data.color == Styles.Icons.Color.THEME:
                    Styles.set_pixmap_theme(self.icon_label, icon_data.name, icon_size)
                else:
                    self.icon_label.setPixmap(Styles.Icons.Icon(icon_data.name, icon_data.color).toPixmap(icon_size))
            elif icon:
                self.update_icon(icon, icon_size)

            layout.addWidget(self.icon_label)
            layout.addWidget(self.label_text)
            self.setStyleSheet('''
                        background-color: 'transparent';
            ''')

            self.setLayout(layout)

        def update_icon(self, icon : QIcon, icon_size = 16):
            if icon:
                pixmap = icon.pixmap(icon_size, icon_size)  # Ajuste o tamanho do �cone conforme necess�rio
                self.icon_label.setPixmap(pixmap)

        def SelectionChanged(self, selected : bool):
            if self.icon_data:
                if selected != self.selected:
                    if selected:
                        if self.icon_data.color == Styles.Icons.Color.THEME:
                            Styles.set_pixmap_theme(self.icon_label, self.icon_data.hover_name, self.icon_size)
                        else:
                            self.icon_label.setPixmap(Styles.Icons.Icon(self.icon_data.hover_name, self.icon_data.hover_color).toPixmap(self.icon_size))
                    else:
                        if self.icon_data.color == Styles.Icons.Color.THEME:
                            Styles.set_pixmap_theme(self.icon_label, self.icon_data.name, self.icon_size)
                        else:
                            self.icon_label.setPixmap(Styles.Icons.Icon(self.icon_data.name, self.icon_data.color).toPixmap(self.icon_size))
            self.selected = selected


    class StateLabel(QWidget):
        def __init__(self, style = "", size : int = 10, parent=None):
            super().__init__(parent)
            self.style = style
            self.size = size
            layout = QHBoxLayout()
            layout.setContentsMargins(0, 0, 0, 0)
            self.label = QLabel()
            size_policy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
            self.label.setSizePolicy(size_policy)
            layout.addWidget(self.label)
            self.label.setMaximumSize(size, size)
            self.label.setStyleSheet(self.style)
            self.setStyleSheet('''
                        background-color: 'transparent';
            ''')

            self.setLayout(layout)


    class Label(QLabel):
        def __init__(self, text='', func_double_click = None,  parent=None):
            super().__init__(text, parent)
            self.func_double_click = func_double_click

        def mouseDoubleClickEvent(self, event):
            if self.func_double_click:
                self.func_double_click()


    class IconCheckBox(QWidget):
        def __init__(self, text, icon : QIcon = None, icon_size = 16, margins = [0, 0, 0, 0], spacing : int = None, parent=None):
            super().__init__(parent)
        
            self.margins = margins
            layout = QHBoxLayout()

            self.icon_label = QLabel()
            self.checkbox = QCheckBox(text)
            size_policy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
            self.icon_label.setSizePolicy(size_policy)
            if icon:
                pixmap = icon.pixmap(icon_size, icon_size)  # Ajuste o tamanho do �cone conforme necess�rio
                self.icon_label.setPixmap(pixmap)
                layout.addWidget(self.icon_label)

            if spacing != None:
                layout.setSpacing(0)
            layout.setContentsMargins(*margins)
            layout.addWidget(self.checkbox)
        
            self.setStyleSheet('''
                        background-color: 'transparent';
            ''')

            self.setLayout(layout)

        def setIcon(self, icon : QIcon, icon_size = 16):
            pixmap = icon.pixmap(icon_size, icon_size)  
            self.icon_label.setPixmap(pixmap)
            layout = QHBoxLayout()
            layout.setContentsMargins(*self.margins)
            layout.addWidget(self.icon_label)
            layout.addWidget(self.checkbox)
            self.setLayout(layout)


    class VerticalScrollArea(QScrollArea):
        def __init__(self, parent: QWidget = None):
            super().__init__(parent)
            
            # Main content widget
            content_widget = QWidget()
            content_widget_layout = QVBoxLayout(content_widget)
            content_widget_layout.setContentsMargins(0, 0, 0, 0)
            content_widget_layout.setSpacing(0)
            
            self.setWidget(content_widget)
            self.setWidgetResizable(True)

            # Scroll layout for adding items
            self.scroll_layout = QVBoxLayout()
            self.scroll_layout.setContentsMargins(10, 10, 10, 10)
            self.scroll_layout.setSpacing(20)
            self.scroll_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

            # Content frame that holds the layout
            content_frame = QFrame()
            content_frame.setLayout(self.scroll_layout)

            # Add the content frame to the main content widget
            content_widget_layout.addWidget(content_frame)

            # Set minimum height for content frame to prevent extra scroll space
            content_frame.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
           
        def add_item(self, widget : QWidget):
            """
            Adds a new widget to the scroll area layout.
            """
            widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
            self.scroll_layout.addWidget(widget)
          


    


