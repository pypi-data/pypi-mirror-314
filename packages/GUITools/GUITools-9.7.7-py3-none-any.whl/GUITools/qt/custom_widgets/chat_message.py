# -*- coding: latin -*-
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QFrame, QLabel, QSizePolicy, QPushButton, QVBoxLayout, QHBoxLayout
from ..style import Styles
from ..text import Text
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt


class LabelIcon(QLabel):
    def __init__(self, icon : QIcon, size : int,  parent=None):
        super().__init__(parent)

        size_policy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        self.setSizePolicy(size_policy)
        pixmap = icon.pixmap(size, size)  # Ajuste o tamanho do ícone conforme necessário
        self.setPixmap(pixmap)


class IconLabelStyle(Styles.WidgetStyleSheet):
    def __init__(self):
        super().__init__("QLabel",use_class_name=False)
        self.label = self.Label()

    class Label(Styles.StyleSheet):
        def __init__(self):
            super().__init__("QLabel")
            self.border = Styles.Property.Border(radius=5)
            self.padding = Styles.Property.Padding(value=5)
            self.background_color = Styles.Property.BackgroundColor(Styles.Color.tertiary)
            self.height = Styles.Property.Height(value=30)
            self.width =  Styles.Property.Width(value=30)

class FrameStyle(Styles.WidgetStyleSheet):
    def __init__(self):
        super().__init__("QFrame",use_class_name=False)
        self.frame = self.Frame()

    class Frame(Styles.StyleSheet):
        def __init__(self):
            super().__init__("QFrame")
            self.border = Styles.Property.Border(color=Styles.Color.division, top=1)

class WidgetStyle(Styles.WidgetStyleSheet):
    def __init__(self):
        super().__init__("QFrame",use_class_name=False)
        self.widget = self.Widget()

    class Widget(Styles.StyleSheet):
        def __init__(self):
            super().__init__("QFrame")
            self.background_color = Styles.Property.BackgroundColor(Styles.Color.primary)


class User(QWidget):
    def __init__(self, id : int, font_size : int, parent=None):
        super().__init__(parent)

        self.font_size = font_size

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0,0)

        self.frame = QFrame(self)
        layout_frame =  QHBoxLayout()

        self.frame_content = QFrame()
        self.frame_content.setMaximumWidth(1000)
        layout_frame_content =  QHBoxLayout()
        layout_frame_content.setContentsMargins(35, 0, 35,0)
        self.icon_label = LabelIcon(Styles.Icons.Icon(Styles.Icons.Name.user, Styles.Icons.Color.BLUE), 16, self)

        self.text_browser = Text.Browser(True, True, False, True, self.font_size) 
        self.text_browser.setReadOnly(True)
        self.text_browser.max_font_size = 25
        self.text_browser.min_height = 30

        layout_frame_content.addWidget(self.icon_label)
        layout_frame_content.addWidget(self.text_browser)

        layout_frame_content.setAlignment(self.icon_label, Qt.AlignmentFlag.AlignTop)

        self.frame_content.setLayout(layout_frame_content)
        layout_frame.addWidget(self.frame_content)
        self.frame.setLayout(layout_frame)
        layout.addWidget(self.frame)

        self.frame_content.setStyleSheet('''
            border-bottom: 0px solid red;
            border-top: 0px solid red;
        ''')

        Styles.set_widget_style_theme(IconLabelStyle(), self.icon_label)
        if id > 0:
            Styles.set_widget_style_theme(FrameStyle(), self.frame)

        self.setLayout(layout)
        self.text_browser.adjustWidgetHeight()


class Assistant(QWidget):
    def __init__(self, font_size : int, gpt_icon : Styles.Icons.Icon, parent=None):
        super().__init__(parent)

        self.font_size = font_size
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0,0)

        frame = QFrame(self)
        layout_frame =  QHBoxLayout()

        frame_content = QFrame()
        frame_content.setMaximumWidth(1000)
        layout_frame_content =  QHBoxLayout()
        layout_frame_content.setContentsMargins(35, 0, 35,0)
        self.icon_label = LabelIcon(gpt_icon, 18, self)

        self.text_browser = Text.Browser(True, True, True, True ,self.font_size) 

        self.text_browser.setReadOnly(True)
        self.text_browser.min_height = 30
        self.text_browser.max_font_size = 25
        
        self.btn_copy = QPushButton(self)

        size_policy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.btn_copy.setSizePolicy(size_policy)
        self.btn_copy.setMinimumHeight(25)
        self.btn_copy.setEnabled(False)
        self.btn_copy.clicked.connect(lambda : Text.copy(self.text_browser))
  
        layout_frame_content.addWidget(self.icon_label)
        layout_frame_content.addWidget(self.text_browser)
        layout_frame_content.addWidget(self.btn_copy)

        layout_frame_content.setAlignment(self.btn_copy, Qt.AlignmentFlag.AlignTop)
        layout_frame_content.setAlignment(self.icon_label, Qt.AlignmentFlag.AlignTop)

        frame_content.setLayout(layout_frame_content)
        layout_frame.addWidget(frame_content)
        frame.setLayout(layout_frame)
        layout.addWidget(frame)
 
        Styles.set_widget_style_theme(Styles.button_copy(transparent=True), self.btn_copy)
        Styles.set_widget_style_theme(IconLabelStyle(), self.icon_label)
        Styles.set_icon_theme(self.btn_copy, Styles.Icons.Name.copy, Styles.Icons.Name.copy, Styles.Icons.Color.GRAY)

        self.setLayout(layout)
        self.text_browser.adjustWidgetHeight()
        

class WidgetMessage(QWidget):
    
    def __init__(self, *, id : int, font_size : int, assistant_icon : Styles.Icons.Icon = None, parent_layout :  QVBoxLayout | QHBoxLayout = None):
        super().__init__()

        self.id = id

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0,0)

        self.user = User(id, font_size, self)

        if not assistant_icon:
            assistant_icon = Styles.Icons.Icon(Styles.Icons.Name.openai, Styles.Icons.Color.BLUE)
        self.assistant = Assistant(font_size, assistant_icon, self)
        layout.addWidget(self.user)
        layout.addWidget(self.assistant)

        size_policy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        self.setSizePolicy(size_policy)

        self.setLayout(layout)

        if parent_layout:
            parent_layout.addWidget(self.chat.current_widget)




