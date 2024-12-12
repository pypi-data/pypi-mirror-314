# -*- coding: latin -*-

from ..icon import Icons
from ..styleSheet import BaseColor
from functools import partial
from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QEnterEvent
from PyQt6.QtCore import QEvent
from PyQt6.QtWidgets import QWidget, QPushButton, QLabel

def leaveEvent(a0: QEvent, widget : QPushButton | QLabel, icon : Icons.Icon, pixmap_size : int = None) -> None:
    if isinstance(widget, QPushButton):
        if not widget.isChecked():
            widget.setIcon(icon)  
    elif isinstance(widget, QLabel):
        widget.setPixmap(icon.toPixmap(pixmap_size))

def enterEvent(event: QEnterEvent, widget : QPushButton | QLabel, icon : Icons.Icon, pixmap_size : int = None) -> None:
    if widget.isEnabled():
        if isinstance(widget, QPushButton):
            widget.setIcon(icon)  
        elif isinstance(widget, QLabel):
            widget.setPixmap(icon.toPixmap(pixmap_size))

class WidgetsTheme(object):
    widget_data = []
    icon_theme_data = []
    icon_data = []
    pixmap_data = []
    textEdit_data = []

    @classmethod
    def set_widget_style_theme(cls, widget : QWidget, style : object):
        cls.widget_data.append([widget, style])

    @classmethod
    def set_icon_theme_data(cls, widget : QWidget, hover : bool, icon_color : Icons.Color,
                              icon_light : Icons.Name, icon_hover_light : Icons.Name,
                              icon_hover_light_color : Icons.Color, icon_dark : Icons.Name,
                              icon_hover_dark : Icons.Name, icon_hover_dark_color : Icons.Color):
        
        cls.icon_theme_data.append([widget, hover, icon_color, icon_light, icon_hover_light,
                                    icon_hover_light_color, icon_dark, icon_hover_dark, icon_hover_dark_color])

    @classmethod
    def set_icon_data(cls, widget : QPushButton | QLabel,  icon_name : Icons.Name, icon_hover_name : Icons.Name, icon_color : Icons.Color ,  icon_hover_color : Icons.Color, pixmap_size : int = None):
        cls.icon_data.append([widget, icon_name, icon_hover_name, icon_color, icon_hover_color, pixmap_size])

    @classmethod
    def set_pixmap_data(cls, widget : QWidget,  icon_name : Icons.Name, size : int):
        cls.pixmap_data.append([widget, icon_name, size])

    @classmethod
    def set_textEdit_data(cls, widget : QWidget):
        cls.textEdit_data.append(widget)

    @classmethod
    def update(cls, theme : str):
        cls.update_icons_theme(theme)
        cls.update_icons()
        cls.update_pixmaps()
        cls.update_placeholderText()
        cls.update_widget_style_theme()

    @classmethod
    def update_widget_style_theme(cls):
        list_remove = []
        for d in cls.widget_data:
            try:
                d[0].setStyleSheet(str(d[1]))
            except RuntimeError:
                list_remove.append(d)
            except Exception as ex:
                ...
        for i in list_remove:
            cls.widget_data.remove(i)

    @classmethod
    def update_icons_theme(cls, theme : str):
        list_remove = []
        for d in cls.icon_theme_data:
            try:
                if theme == 'dark':
                    d[0].setIcon(Icons.Icon(d[3], d[2]))
                    if d[1]:
                        d[0].leaveEvent = partial(leaveEvent, widget=d[0], icon=Icons.Icon(d[4]))
                        d[0].enterEvent = partial(enterEvent, widget=d[0], icon=Icons.Icon(d[4], d[5]))
                else:
                    d[0].setIcon(Icons.Icon(d[6], d[2]))
                    if d[1]:
                        d[0].leaveEvent = partial(leaveEvent, widget=d[0], icon=Icons.Icon(d[7]))
                        d[0].enterEvent = partial(enterEvent, widget=d[0], icon=Icons.Icon(d[7], d[8]))

            except RuntimeError:
                list_remove.append(d)
        for i in list_remove:
            cls.icon_theme_data.remove(i)

    @classmethod
    def update_icons(cls):
        list_remove = []
        for d in cls.icon_data:
            try:
                if d[2]:
                    cls.set_icon_hover(d[0], d[1], d[2], d[3], d[4], d[5])
                else:
                    if isinstance(d[0], QPushButton):
                        d[0].setIcon(Icons.Icon(d[1], d[3]))
                    elif isinstance(d[0], QLabel):
                        d[0].setPixmap(Icons.Icon(d[1], d[3]).toPixmap(d[5]))

            except RuntimeError:
                list_remove.append(d)
        for i in list_remove:
            cls.icon_data.remove(i)

    @classmethod
    def update_pixmaps(cls):
        list_remove = []
        for d in cls.pixmap_data:
            try:
                d[0].setPixmap(Icons.Icon(d[1]).toPixmap(d[2]))
            except RuntimeError:
                list_remove.append(d)
        for i in list_remove:
            cls.pixmap_data.remove(i)


    @classmethod
    def update_placeholderText(cls):
        list_remove = []
        for textEdit in cls.textEdit_data:
            try:
                cls.set_text_placeholder_text(textEdit)
            except RuntimeError:
                list_remove.append(textEdit)
        for i in list_remove:
            cls.textEdit_data.remove(i)

    @staticmethod
    def set_icon_hover(widget : QPushButton | QLabel,  icon_name : Icons.Name, icon_hover_name : Icons.Name , icon_color = Icons.Color.THEME, icon_hover_color = Icons.Color.BLUE, pixmap_size : int = None):
        if isinstance(widget, QPushButton):
            widget.setIcon(Icons.Icon(icon_name, icon_color))
        elif isinstance(widget, QLabel):
            widget.setPixmap(Icons.Icon(icon_name, icon_color).toPixmap(pixmap_size))
        else:
            return
        widget.leaveEvent = partial(leaveEvent, widget=widget, icon=Icons.Icon(icon_name, icon_color), pixmap_size=pixmap_size)
        widget.enterEvent = partial(enterEvent, widget=widget, icon=Icons.Icon(icon_hover_name, icon_hover_color), pixmap_size=pixmap_size)
       

    @staticmethod
    def set_text_placeholder_text(widget: QWidget):
        class_name = widget.metaObject().className()
        style_template = f'{class_name} {{ color: {BaseColor.Reverse.primary}; }}'
        placeholder_style = f'{class_name} {{ color: {BaseColor.placeholder}; }}'
        widget.setStyleSheet(style_template if widget.toPlainText().strip() else placeholder_style)




