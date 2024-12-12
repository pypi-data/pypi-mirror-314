# -*- coding: latin -*-
from .saftOnlinePyResource import *
from .icon import Icons
from PyQt6.QtWidgets import QGraphicsDropShadowEffect, QPushButton, QWidget, QLabel, QMainWindow, QApplication
from .utils import TypeTheme, Global
from .widgets import WidgetsTheme, WidgetsStyleCheet, BaseWidgetStyleSheet
from .styleSheet import BaseColor, set_base_style, ColorTheme, RGBColor
from typing import Literal
import subprocess
from PyQt6.QtGui import QIcon, QPixmap, QPainter
from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtCore import QSize, QByteArray, Qt

class Icon(QIcon):

    def toPixmap(self, size : int = None):
        return Icons.to_pixmap(self, size)

def create_svg_icon_from_string(svg_string, size):
    byte_array = QByteArray(svg_string.encode('utf-8'))
    svg_renderer = QSvgRenderer(byte_array)
    pixmap = QPixmap(size)
    pixmap.fill(Qt.GlobalColor.transparent)  # Preenche com fundo transparente
    painter = QPainter(pixmap)
    svg_renderer.render(painter)
    painter.end()
    return Icon(pixmap)

def mainWindow() -> QMainWindow: 
    app = QApplication.instance()

    if not app:
        return None
    
    if isinstance(app, QMainWindow):
        return widget
    
    for widget in app.topLevelWidgets():
        if isinstance(widget, QMainWindow):
            return widget

class Styles(WidgetsStyleCheet):

    class Icons(Icons):
        ...

    class TypeTheme(TypeTheme):
        ...

    @staticmethod
    def desktop_theme():
        try:
            result = subprocess.run(
                ["gsettings", "get", "org.gnome.desktop.interface", "gtk-theme"],
                stdout=subprocess.PIPE, text=True
            )
            theme = result.stdout.strip().lower()
            return TypeTheme.dark if "dark" in theme else TypeTheme.light
        except Exception:
            return TypeTheme.light

    @staticmethod
    def current_theme():
        return Global.theme
    
    @staticmethod
    def convert_rgb_rgba(rgb : str | ColorTheme | RGBColor, a : str):
        if isinstance(rgb, ColorTheme | RGBColor):
            rgb = rgb.rgb
        if not 'a' in rgb:
            rgb = rgb.replace("rgb", "rgba")
        return rgb.replace(")", f",{a})")

    def set_base_style(theme : TypeTheme, base_color : BaseColor):
        set_base_style(theme, base_color)

    @classmethod 
    def opposite_theme(cls):
        return cls.TypeTheme.dark if Global.theme == cls.TypeTheme.light else cls.TypeTheme.light

    @classmethod
    def load(cls, theme : str):

        if theme not in cls.TypeTheme.list():
            theme = cls.TypeTheme.light

        Global.theme = theme
   
        cls.Icons.Load()
        WidgetsTheme.update(theme)
        mainWindow().signal_toggle_theme.emit()
 
    def set_widget_style_theme(widget_style : BaseWidgetStyleSheet, *widgets : QWidget):
        for widget in widgets:
            WidgetsTheme.set_widget_style_theme(widget, widget_style)
            widget.setStyleSheet(str(widget_style))

    def set_icon_hover(widget : QPushButton | QLabel,  icon_name : Icons.Name, icon_hover_name : Icons.Name , icon_color = Icons.Color.THEME, icon_hover_color = Icons.Color.BLUE, pixmap_size : int = None):
        WidgetsTheme.set_icon_hover(widget, icon_name, icon_hover_name, icon_color, icon_hover_color, pixmap_size)

    @classmethod
    def set_icon_theme(cls, widget : QPushButton | QLabel,  icon_name : Icons.Name, icon_hover_name : Icons.Name = None, icon_color = Icons.Color.THEME, icon_hover_color = Icons.Color.BLUE, pixmap_size : int = None):
        if icon_hover_name:
            WidgetsTheme.set_icon_hover(widget, icon_name, icon_hover_name, icon_color, icon_hover_color, pixmap_size)
        else:
            if isinstance(widget, QPushButton):
                widget.setIcon(Icons.Icon(icon_name))
            elif isinstance(widget, QLabel):
                widget.setPixmap(Icons.Icon(icon_name).toPixmap(pixmap_size))

        WidgetsTheme.set_icon_data(widget, icon_name, icon_hover_name, icon_color, icon_hover_color, pixmap_size)
           
    @classmethod
    def set_icon_theme_from_data(cls, widget : QWidget, data : Icons.Data):
        cls.set_icon_theme(widget, data.name, data.hover_name, data.color, data.hover_color)
        
    @classmethod
    def set_icon_toggle_theme(cls, widget : QWidget, 
                              hover = True,
                              icon_color = Icons.Color.THEME,
                              icon_light = Icons.Name.light_mode,
                              icon_hover_light = Icons.Name.light_mode,
                              icon_hover_light_color = Icons.Color.BLUE,
                              icon_dark = Icons.Name.dark_mode,
                              icon_hover_dark = Icons.Name.dark_mode,
                              icon_hover_dark_color = Icons.Color.BLUE):

        if Global.theme == cls.TypeTheme.light:
            if hover:
                WidgetsTheme.set_icon_hover(widget, icon_light, icon_hover_light, icon_color, icon_hover_light_color)
            else:
                widget.setIcon(Icons.Icon(icon_light, icon_color))
        else:
            if hover:
                WidgetsTheme.set_icon_hover(widget, icon_dark, icon_hover_dark, icon_color, icon_hover_dark_color)
            else:
                widget.setIcon(Icons.Icon(icon_dark, icon_color))

        WidgetsTheme.set_icon_theme_data(widget, hover, icon_color, icon_light, icon_hover_light,
                                         icon_hover_light_color, icon_dark, icon_hover_dark,
                                         icon_hover_dark_color)
    

    def set_pixmap_theme(widget : QLabel,  icon_name : Icons.Name, size : int):
        widget.setPixmap(Icons.Icon(icon_name).toPixmap(size))
        WidgetsTheme.set_pixmap_data(widget, icon_name, size)

    @classmethod
    def set_textEdit_placeholder_theme(cls, widget : QWidget):
        widget.textChanged.connect(lambda : WidgetsTheme.set_text_placeholder_text(widget))
        WidgetsTheme.set_text_placeholder_text(widget)
        WidgetsTheme.set_textEdit_data(widget)

    @classmethod
    def set_text_placeholder_text(cls, widget: QWidget):
        WidgetsTheme.set_text_placeholder_text(widget)

    @classmethod
    def icon_file(cls, file_path : str):
        if file_path.endswith(".vb"):
            return cls.Icons.Icon(cls.Icons.Name.file_vb, cls.Icons.Color.ORIGINAL)
        elif file_path.endswith(".cs"):
            return cls.Icons.Icon(cls.Icons.Name.file_csharp, cls.Icons.Color.ORIGINAL)
        elif file_path.endswith(".py"):
            return cls.Icons.Icon(cls.Icons.Name.file_py, cls.Icons.Color.ORIGINAL)
        elif file_path.endswith(".pdf"):
            return cls.Icons.Icon(cls.Icons.Name.pdf, cls.Icons.Color.ORIGINAL)
        elif file_path.endswith(".xlsx") or file_path.endswith(".xls"):
            return cls.Icons.Icon(cls.Icons.Name.xls, cls.Icons.Color.ORIGINAL)
        elif file_path.endswith(".json"):
            return cls.Icons.Icon(cls.Icons.Name.json, cls.Icons.Color.GRAY)
        elif file_path.endswith('html'):
            svg_content= '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><title>file_type_html</title><polygon points="5.902 27.201 3.655 2 28.345 2 26.095 27.197 15.985 30 5.902 27.201" style="fill:#e44f26"/><polygon points="16 27.858 24.17 25.593 26.092 4.061 16 4.061 16 27.858" style="fill:#f1662a"/><polygon points="16 13.407 11.91 13.407 11.628 10.242 16 10.242 16 7.151 15.989 7.151 8.25 7.151 8.324 7.981 9.083 16.498 16 16.498 16 13.407" style="fill:#ebebeb"/><polygon points="16 21.434 15.986 21.438 12.544 20.509 12.324 18.044 10.651 18.044 9.221 18.044 9.654 22.896 15.986 24.654 16 24.65 16 21.434" style="fill:#ebebeb"/><polygon points="15.989 13.407 15.989 16.498 19.795 16.498 19.437 20.507 15.989 21.437 15.989 24.653 22.326 22.896 22.372 22.374 23.098 14.237 23.174 13.407 22.341 13.407 15.989 13.407" style="fill:#fff"/><polygon points="15.989 7.151 15.989 9.071 15.989 10.235 15.989 10.242 23.445 10.242 23.445 10.242 23.455 10.242 23.517 9.548 23.658 7.981 23.732 7.151 15.989 7.151" style="fill:#fff"/></svg>'
            return create_svg_icon_from_string(svg_content, QSize(32, 32))
        elif file_path.endswith('css'):
            svg_content= '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><title>file_type_css</title><polygon points="5.902 27.201 3.656 2 28.344 2 26.095 27.197 15.985 30 5.902 27.201" style="fill:#1572b6"/><polygon points="16 27.858 24.17 25.593 26.092 4.061 16 4.061 16 27.858" style="fill:#33a9dc"/><polygon points="16 13.191 20.09 13.191 20.372 10.026 16 10.026 16 6.935 16.011 6.935 23.75 6.935 23.676 7.764 22.917 16.282 16 16.282 16 13.191" style="fill:#fff"/><polygon points="16.019 21.218 16.005 21.222 12.563 20.292 12.343 17.827 10.67 17.827 9.24 17.827 9.673 22.68 16.004 24.438 16.019 24.434 16.019 21.218" style="fill:#ebebeb"/><polygon points="19.827 16.151 19.455 20.29 16.008 21.22 16.008 24.436 22.344 22.68 22.391 22.158 22.928 16.151 19.827 16.151" style="fill:#fff"/><polygon points="16.011 6.935 16.011 8.855 16.011 10.018 16.011 10.026 8.555 10.026 8.555 10.026 8.545 10.026 8.483 9.331 8.342 7.764 8.268 6.935 16.011 6.935" style="fill:#ebebeb"/><polygon points="16 13.191 16 15.111 16 16.274 16 16.282 12.611 16.282 12.611 16.282 12.601 16.282 12.539 15.587 12.399 14.02 12.325 13.191 16 13.191" style="fill:#ebebeb"/></svg>'
            return create_svg_icon_from_string(svg_content, QSize(32, 32))
        elif file_path.endswith('js'):
            svg_content= '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><title>file_type_js</title><path d="M18.774,19.7a3.727,3.727,0,0,0,3.376,2.078c1.418,0,2.324-.709,2.324-1.688,0-1.173-.931-1.589-2.491-2.272l-.856-.367c-2.469-1.052-4.11-2.37-4.11-5.156,0-2.567,1.956-4.52,5.012-4.52A5.058,5.058,0,0,1,26.9,10.52l-2.665,1.711a2.327,2.327,0,0,0-2.2-1.467,1.489,1.489,0,0,0-1.638,1.467c0,1.027.636,1.442,2.1,2.078l.856.366c2.908,1.247,4.549,2.518,4.549,5.376,0,3.081-2.42,4.769-5.671,4.769a6.575,6.575,0,0,1-6.236-3.5ZM6.686,20c.538.954,1.027,1.76,2.2,1.76,1.124,0,1.834-.44,1.834-2.15V7.975h3.422V19.658c0,3.543-2.078,5.156-5.11,5.156A5.312,5.312,0,0,1,3.9,21.688Z" style="fill:#f5de19"/></svg>'
            return create_svg_icon_from_string(svg_content, QSize(32, 32))
        elif file_path.endswith('.md'):
            svg_content = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><title>file_type_markdown</title><rect x="2.5" y="7.955" width="27" height="16.091" style="fill:none;stroke:#755838"/><polygon points="5.909 20.636 5.909 11.364 8.636 11.364 11.364 14.773 14.091 11.364 16.818 11.364 16.818 20.636 14.091 20.636 14.091 15.318 11.364 18.727 8.636 15.318 8.636 20.636 5.909 20.636" style="fill:#755838"/><polygon points="22.955 20.636 18.864 16.136 21.591 16.136 21.591 11.364 24.318 11.364 24.318 16.136 27.045 16.136 22.955 20.636" style="fill:#755838"/></svg>'
            return create_svg_icon_from_string(svg_content, QSize(32, 32))
        elif file_path.endswith('.vcxproj'):
            svg_content = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><title>file_type_vcxproj</title><path d="M29.821,4.321,24.023,2,11.493,14.212,3.833,8.385l-1.654.837V22.8l1.644.827,7.65-5.827L24.023,30l5.8-2.321V4.321ZM4.65,19.192V12.818L8.2,15.985ZM16,15.985l7.082-5.3V21.324l-7.092-5.339Z" style="fill:#68217a"/><polygon points="15.995 15.985 23.077 10.686 23.077 21.324 15.985 15.985 15.995 15.985" style="fill:#fff"/><polygon points="4.65 19.192 4.65 12.818 8.196 15.985 4.65 19.192" style="fill:#fff"/><path d="M15.553,32a7.185,7.185,0,0,1-5.541-2.244A8.131,8.131,0,0,1,8,24.05a8.587,8.587,0,0,1,2.222-6.086,7.631,7.631,0,0,1,5.809-2.415,9.876,9.876,0,0,1,3.571.583l.955.372v6.569l-2.3-1.456a3.636,3.636,0,0,0-2-.548,2.127,2.127,0,0,0-1.684.668,2.975,2.975,0,0,0-.663,2.1,2.9,2.9,0,0,0,.62,2.008,1.918,1.918,0,0,0,1.572.618,3.976,3.976,0,0,0,2.165-.607l2.293-1.427v6.292l-.815.419A9.177,9.177,0,0,1,15.553,32Z" style="fill:#efeef0"/><polygon points="24.092 27.909 19.334 27.909 19.334 26.152 17.578 26.152 17.578 21.394 19.334 21.395 19.334 19.638 24.092 19.638 24.092 21.396 25.85 21.396 25.85 26.152 24.092 26.152 24.092 27.909" style="fill:#efeef0"/><polygon points="30.243 27.909 25.485 27.909 25.485 26.152 23.728 26.152 23.728 21.394 25.485 21.395 25.485 19.638 30.243 19.638 30.243 21.396 32 21.396 32 26.152 30.243 26.152 30.243 27.909" style="fill:#efeef0"/><path d="M19.057,29.808a7.682,7.682,0,0,1-3.5.689,5.721,5.721,0,0,1-4.436-1.759A6.657,6.657,0,0,1,9.5,24.05a7.107,7.107,0,0,1,1.817-5.06,6.162,6.162,0,0,1,4.714-1.941,8.364,8.364,0,0,1,3.026.481V20.35a5.129,5.129,0,0,0-2.8-.78,3.61,3.61,0,0,0-2.787,1.152,4.428,4.428,0,0,0-1.06,3.12,4.349,4.349,0,0,0,1,3.007,3.428,3.428,0,0,0,2.693,1.12,5.489,5.489,0,0,0,2.958-.834Z" style="fill:#984c93"/><polygon points="20.834 22.895 20.834 21.137 22.592 21.137 22.592 22.895 24.35 22.895 24.35 24.652 22.592 24.652 22.592 26.409 20.834 26.409 20.834 24.652 19.078 24.652 19.078 22.894 20.834 22.895" style="fill:#984c93"/><polygon points="26.985 22.895 26.985 21.137 28.743 21.137 28.743 22.895 30.5 22.895 30.5 24.652 28.743 24.652 28.743 26.409 26.985 26.409 26.985 24.652 25.228 24.652 25.228 22.894 26.985 22.895" style="fill:#984c93"/></svg>'
            return create_svg_icon_from_string(svg_content, QSize(32, 32))
        elif file_path.endswith('.njsproj'):
            svg_content = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><title>file_type_njsproj</title><path d="M29.821,4.321,24.023,2,11.493,14.212,3.833,8.385l-1.654.837V22.8l1.644.827,7.65-5.827L24.023,30l5.8-2.321V4.321ZM4.65,19.192V12.818L8.2,15.985ZM16,15.985l7.082-5.3V21.324l-7.092-5.339Z" style="fill:#68217a"/><polygon points="15.995 15.985 23.077 10.686 23.077 21.324 15.985 15.985 15.995 15.985" style="fill:#fff"/><polygon points="4.65 19.192 4.65 12.818 8.196 15.985 4.65 19.192" style="fill:#fff"/><path d="M25.9,32.029a6.842,6.842,0,0,1-6.4-3.658l-.6-1.189,3.826-2.223A5.233,5.233,0,0,1,20.2,20.305c0-2.976,2.329-5.135,5.539-5.135a5.568,5.568,0,0,1,5.236,2.971l.661,1.163-3.277,2.105c1.895.938,3.628,2.324,3.628,5.28C31.983,29.884,29.538,32.029,25.9,32.029Zm-1.549-6.216a1.587,1.587,0,0,0,1.484.891,1.52,1.52,0,0,0,.374-.041,11.343,11.343,0,0,0-1.078-.515l-.7-.3Zm-9.319,6.21a5.77,5.77,0,0,1-5.505-3.383L8.983,27.49l4.629-2.8.716,1.268c.413.732.477.732.584.732l.075,0a2.385,2.385,0,0,0,.023-.358v-11h5.642V26.365C20.652,29.855,18.5,32.024,15.032,32.024Z" style="fill:#efeef0"/><path d="M13.1,26.649c.443.786.846,1.45,1.814,1.45.926,0,1.51-.362,1.51-1.771V16.743h2.818v9.622c0,2.918-1.711,4.247-4.209,4.247A4.375,4.375,0,0,1,10.8,28.038Z" style="fill:#83cd29"/><path d="M23.055,26.4a3.07,3.07,0,0,0,2.78,1.712c1.168,0,1.914-.584,1.914-1.39,0-.966-.767-1.309-2.052-1.871l-.7-.3c-2.034-.866-3.385-1.952-3.385-4.247,0-2.114,1.611-3.723,4.128-3.723a4.166,4.166,0,0,1,4.009,2.257l-2.195,1.409a1.917,1.917,0,0,0-1.814-1.208,1.226,1.226,0,0,0-1.349,1.208c0,.846.524,1.188,1.733,1.712l.7.3c2.395,1.027,3.747,2.074,3.747,4.428,0,2.538-1.993,3.928-4.671,3.928a5.415,5.415,0,0,1-5.136-2.882Z" style="fill:#83cd29"/></svg>'
            return create_svg_icon_from_string(svg_content, QSize(32, 32))
        elif file_path.endswith('.vbproj'):
            svg_content = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><title>file_type_vbproj</title><path d="M29.821,4.321,24.023,2,11.493,14.212,3.833,8.385l-1.654.837V22.8l1.644.827,7.65-5.827L24.023,30l5.8-2.321V4.321ZM4.65,19.192V12.818L8.2,15.985ZM16,15.985l7.082-5.3V21.324l-7.092-5.339Z" style="fill:#68217a"/><polygon points="15.995 15.985 23.077 10.686 23.077 21.324 15.985 15.985 15.995 15.985" style="fill:#fff"/><polygon points="4.65 19.192 4.65 12.818 8.196 15.985 4.65 19.192" style="fill:#fff"/><polygon points="17.631 32.03 11.87 32.03 7.511 15.53 14.216 15.53 14.749 18.269 15.282 15.53 21.985 15.53 17.631 32.03" style="fill:#efeef0"/><path d="M27.556,32.03H20.245V15.53l7.37.011a4.517,4.517,0,0,1,3.24,2.115,5.032,5.032,0,0,1,.69,2.592,5.164,5.164,0,0,1-.643,2.471c-.066.114-.137.225-.21.332a4.893,4.893,0,0,1,.6.771,5.041,5.041,0,0,1,.7,2.586,5.757,5.757,0,0,1-.623,2.89,5.328,5.328,0,0,1-3.7,2.713Z" style="fill:#efeef0"/><path d="M13,17.153l1.749,8.993L16.5,17.153H20L16.5,30.407H13L9.5,17.153Z" style="fill:#00519a"/><path d="M21.745,17.153h5.7a3.032,3.032,0,0,1,2.174,1.42,3.26,3.26,0,0,1,.428,1.656,3.437,3.437,0,0,1-.428,1.651,3.119,3.119,0,0,1-1.756,1.431,3.045,3.045,0,0,1,2.2,1.426,3.282,3.282,0,0,1,.435,1.7,4.041,4.041,0,0,1-.434,2.067,3.788,3.788,0,0,1-2.624,1.9h-5.69Zm3.5,5.207h.874a1.393,1.393,0,0,0,1.213-1.528,1.374,1.374,0,0,0-1.213-1.313h-.874Zm0,5.684H26.29A1.619,1.619,0,0,0,27.74,26.3a1.6,1.6,0,0,0-1.45-1.57H25.245Z" style="fill:#00519a"/></svg>'
            return create_svg_icon_from_string(svg_content, QSize(32, 32))
        elif file_path.endswith('.vbhtml.'):
            svg_content = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><title>file_type_vbhtml</title><path d="M23.844,27.692a16.332,16.332,0,0,1-6.645,1.3q-6.364,0-10.013-3.243a11.3,11.3,0,0,1-3.649-8.9A13.716,13.716,0,0,1,7.322,6.951,12.716,12.716,0,0,1,16.9,3.008a11.676,11.676,0,0,1,8.425,3.006,9.994,9.994,0,0,1,3.142,7.533,10.187,10.187,0,0,1-2.318,7.114,7.532,7.532,0,0,1-5.817,2.547,2.613,2.613,0,0,1-1.845-.642,2.323,2.323,0,0,1-.764-1.6,4.9,4.9,0,0,1-4.148,2.243,4.6,4.6,0,0,1-3.507-1.479,5.706,5.706,0,0,1-1.384-4.063,9.913,9.913,0,0,1,2.2-6.357q2.2-2.763,4.8-2.763a5.063,5.063,0,0,1,4.256,1.716l.311-1.338h2.405l-2.081,9.08a10.716,10.716,0,0,0-.352,2.243q0,.972.744.972a4.819,4.819,0,0,0,3.877-2.047,8.93,8.93,0,0,0,1.621-5.681,7.98,7.98,0,0,0-2.675-6.175,9.887,9.887,0,0,0-6.919-2.432A10.6,10.6,0,0,0,8.713,8.352a12.066,12.066,0,0,0-3.2,8.495,9.561,9.561,0,0,0,3.06,7.573q3.06,2.7,8.586,2.7a13.757,13.757,0,0,0,5.675-1.054ZM19.466,12.25a3.977,3.977,0,0,0-3.6-1.716q-1.824,0-3.263,2.23a8.726,8.726,0,0,0-1.439,4.824q0,3.635,2.905,3.635A3.771,3.771,0,0,0,16.72,20.04a6.309,6.309,0,0,0,1.7-3.2Z" style="fill:#004b96"/></svg>'
            return create_svg_icon_from_string(svg_content, QSize(32, 32))
        elif file_path.endswith('.csproj'):
            svg_content = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><title>file_type_csproj</title><path d="M29.821,4.321,24.023,2,11.493,14.212,3.833,8.385l-1.654.837V22.8l1.644.827,7.65-5.827L24.023,30l5.8-2.321V4.321ZM4.65,19.192V12.818L8.2,15.985ZM16,15.985l7.082-5.3V21.324l-7.092-5.339Z" style="fill:#68217a"/><polygon points="15.995 15.985 23.077 10.686 23.077 21.324 15.985 15.985 15.995 15.985" style="fill:#fff"/><polygon points="4.65 19.192 4.65 12.818 8.196 15.985 4.65 19.192" style="fill:#fff"/><polygon points="30.089 28.175 21.345 28.174 21.345 26.259 19.43 26.257 19.43 17.516 21.344 17.517 21.342 15.604 30.087 15.604 30.087 17.519 32.001 17.519 31.999 21.346 32 21.346 32 26.261 30.088 26.261 30.089 28.175" style="fill:#efeef0"/><path d="M15.527,32A7.159,7.159,0,0,1,10,29.758a8.1,8.1,0,0,1-2-5.683,8.56,8.56,0,0,1,2.213-6.063A7.608,7.608,0,0,1,16,15.6a9.836,9.836,0,0,1,3.558.581l.956.372v6.56l-2.3-1.458a3.6,3.6,0,0,0-1.989-.544,2.117,2.117,0,0,0-1.672.662,2.957,2.957,0,0,0-.658,2.091,2.877,2.877,0,0,0,.615,2,1.9,1.9,0,0,0,1.562.614,3.968,3.968,0,0,0,2.153-.6l2.292-1.426v6.28l-.815.419A9.144,9.144,0,0,1,15.527,32Z" style="fill:#efeef0"/><path d="M22.844,17.1h1.915v1.915h1.914V17.1h1.914v1.915H30.5v1.914H28.587v1.913H30.5V24.76H28.587v1.914H26.673V24.762l-1.912,0,0,1.914H22.845V24.761l-1.915,0V22.844h1.915V20.935H20.93V19.017h1.915Zm1.915,5.744h1.914V20.932H24.759Z" style="fill:#368832"/><path d="M19.017,29.81a7.65,7.65,0,0,1-3.49.686,5.7,5.7,0,0,1-4.417-1.752A6.629,6.629,0,0,1,9.5,24.076a7.077,7.077,0,0,1,1.809-5.039A6.136,6.136,0,0,1,16,17.1a8.329,8.329,0,0,1,3.013.479v2.809a5.108,5.108,0,0,0-2.792-.777,3.6,3.6,0,0,0-2.775,1.147,4.409,4.409,0,0,0-1.055,3.107,4.331,4.331,0,0,0,1,2.994,3.413,3.413,0,0,0,2.681,1.115,5.466,5.466,0,0,0,2.945-.831Z" style="fill:#368832"/></svg>'
            return create_svg_icon_from_string(svg_content, QSize(32, 32))
        elif file_path.endswith((".png", ".jpg", ".jpeg", ".gif", ".bmp", ".svg", ".tiff", ".ico", ".webp", ".psd", ".ai", ".eps")):
            svg_content = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><title>file_type_image</title><path d="M30,5.851Q30,16,30,26.149H2Q2,16,2,5.851H30" style="fill:#2dcc9f"/><path d="M24.232,8.541a2.2,2.2,0,1,0,1.127.623,2.212,2.212,0,0,0-1.127-.623" style="fill:#fff"/><path d="M18.111,20.1q-2.724-3.788-5.45-7.575Q8.619,18.147,4.579,23.766q5.449,0,10.9,0,1.316-1.832,2.634-3.663" style="fill:#fff"/><path d="M22.057,16q-2.793,3.882-5.584,7.765,5.584,0,11.169,0Q24.851,19.882,22.057,16Z" style="fill:#fff"/></svg>'
            return create_svg_icon_from_string(svg_content, QSize(32, 32))
        
        return cls.Icons.Icon(cls.Icons.Name.file, cls.Icons.Color.ORIGINAL)

    @classmethod
    def icon_file_from_type(cls, file_type : Literal['vb', 'csharp', 'python', 'pdf', 'xlsx', 'xls', 'json'] = ""):
        if file_type == 'vb':
            return cls.Icons.Icon(cls.Icons.Name.file_vb, cls.Icons.Color.ORIGINAL)
        elif file_type == 'csharp':
            return cls.Icons.Icon(cls.Icons.Name.file_csharp, cls.Icons.Color.ORIGINAL)
        elif file_type == 'python':
            return cls.Icons.Icon(cls.Icons.Name.file_py, cls.Icons.Color.ORIGINAL)
        elif file_type == "pdf":
            return cls.Icons.Icon(cls.Icons.Name.pdf, cls.Icons.Color.ORIGINAL)
        elif file_type == "xlsx" or file_type == "xls":
            return cls.Icons.Icon(cls.Icons.Name.xls, cls.Icons.Color.ORIGINAL)
        elif file_type == "json":
            return cls.Icons.Icon(cls.Icons.Name.json, cls.Icons.Color.GRAY)
        return cls.Icons.Icon(cls.Icons.Name.file, cls.Icons.Color.ORIGINAL)

    @classmethod
    def shadow_effect(cls, XOffset = 1.5, YOffset = 1.5, Offset = 1.5, BlurRadius = 15):
        shadowEffect = QGraphicsDropShadowEffect()
        shadowEffect.setColor(cls.Color.shadow.QColor)
        shadowEffect.setXOffset(XOffset)
        shadowEffect.setYOffset(YOffset)
        shadowEffect.setOffset(Offset)
        shadowEffect.setBlurRadius(BlurRadius)
        return shadowEffect







