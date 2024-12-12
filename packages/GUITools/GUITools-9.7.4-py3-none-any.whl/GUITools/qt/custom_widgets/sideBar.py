# -*- coding: latin -*-
from functools import partial
from .Interface.SideBar import Ui_FrameSideBar
from PyQt6.QtWidgets import QFrame, QPushButton, QWidget
from ..style import Styles
from ..animation import Animation
from PyQt6.QtCore import QSize, Qt, QObject, QEvent
from PyQt6.QtGui import QCursor

class ClickFilter(QObject):
    action : object = None
    def eventFilter(self, obj, event):
        if event.type() == QEvent.Type.MouseButtonPress:
            if self.action:
                self.action()
            return True
        return super().eventFilter(obj, event)

class PushButton(QPushButton):
        def __init__(self, text : str, icon_data : Styles.Icons.Data, selcted_icon_data : Styles.Icons.Data = None, icon_size_w = 18, icon_size_h = 18):
            super().__init__(text, None)
            self.icon_data = icon_data
            self.selcted_icon_data = selcted_icon_data
            self.setIconSize(QSize(icon_size_w, icon_size_h))
            
        def toggle_icon(self, selcted : bool):
            if selcted and self.selcted_icon_data != None:
                self.setIcon(Styles.Icons.Icon(self.selcted_icon_data.name, self.selcted_icon_data.color))
            else:
                self.setIcon(Styles.Icons.Icon(self.icon_data.name, self.icon_data.color))

class SideBar(Ui_FrameSideBar, QFrame):
    
    class WidgetStyleSheet(Styles.WidgetStyleSheet):
        def __init__(self, action : object):
            super().__init__()
            self.action = action

        def style(self):
            self.action()
            style = f'''
                #frame_logo {{ border-bottom: 1px solid {Styles.Color.division}; border-radius: 0px;}}
            '''
            return f'{style}'

    def __init__(self, parent : QWidget):
        super().__init__(None)
        super().setupUi(self)
        self.opened = False
        self.widge_parent = parent
        self.widge_parent.layout().addWidget(self)
        self.whide_icon : Styles.Icons.Icon = None
        self.whide_icon_size = QSize(40, 40)
        self.icon : Styles.Icons.Icon = None
        self.icon_size = QSize(40, 40)
        self.btn_selected : PushButton = None
        self.btns : list[PushButton] = []
        self._text_bts : dict[str, str]  = {}

        self.label_logo.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.label_logo.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.label_text_logo.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_toggle.setIcon(Styles.Icons.Icon(Styles.Icons.Name.separator_left, Styles.Icons.Color.GRAY))
        self.btn_toggle.clicked.connect(self.toggle)
        Styles.set_widget_style_theme(self.WidgetStyleSheet(self.update_btns_styles), self)
        
    def set_icon(self, icon : Styles.Icons.Icon, size_w = 40, size_h = 40):
        self.icon = icon
        self.icon_size = QSize(size_w, size_h)
        self.label_logo.setPixmap(icon.pixmap(self.icon_size))
      
    def set_whide_icon(self, icon : Styles.Icons.Icon, size_w = 40, size_h = 40):
        self.whide_icon = icon
        self.whide_icon_size = QSize(size_w, size_h)
        
    def set_icon_action(self, action : object):
        click_filter = ClickFilter(self.label_logo)
        click_filter.action = action
        self.label_logo.installEventFilter(click_filter)
        click_filter = ClickFilter(self.label_text_logo)
        click_filter.action = action
        self.label_logo.installEventFilter(click_filter)

    def set_title(self, title : str):
        self.label_text_logo.setText(title)
        
    def add_btn(self, text : str, icon = Styles.Icons.Icon, selcted_icon : Styles.Icons.Icon = None, icon_size_w = 18, icon_size_h = 18):
        style_normal = Styles.button_menu(padding=self.opened)
        btn = PushButton(text, icon, selcted_icon, icon_size_w, icon_size_h)
        btn.setStyleSheet(str(style_normal))
        btn.clicked.connect(partial(self.select, btn_select=btn))
        self.frame_side_bar_btns.layout().addWidget(btn)
        self._text_bts[btn] = btn.text()
        self.btns.append(btn)
        return btn

    def toggle(self):

        if self.opened:
            Animation.minimumWidth(self.widge_parent, 250, 60)
            self.opened = False
            if self.whide_icon:
                self.label_logo.setMinimumWidth(40)
                self.label_logo.setPixmap(self.icon.pixmap(self.icon_size))
                
        else:
            style_selected = Styles.button_menu(selected=True)
            style_selected.button.font = Styles.Property.Font("Segoe UI Semibold", "63 12")
            style_normal = Styles.button_menu()
            Animation.minimumWidth(self.widge_parent, 60, 250)
            for btn in self.btns:
                btn.setText(f'  {self._text_bts[btn]}')
                if self.btn_selected == btn:
                    btn.setStyleSheet(style_selected.styleSheet())
                else:
                    btn.setStyleSheet(style_normal.styleSheet())

            style_btn_toggle = Styles.button_menu()
            style_btn_toggle.button.font.size = 10
            style_btn_toggle.button.color.value = Styles.Color.Reverse.primary.fromRgba(200)

            self.btn_toggle.setStyleSheet(style_btn_toggle.styleSheet())
            self.btn_toggle.setText("  Ocultar painel lateral")
            self.opened = True
            if self.whide_icon:
                self.label_logo.setMinimumWidth(230)
                self.label_logo.setPixmap(self.whide_icon.pixmap(self.whide_icon_size))

    def select(self, btn_select : QPushButton):
        if not self.opened:
            for btn in self.btns:
                    btn.setText("")
            self.btn_toggle.setText("")

        style_selected  = Styles.button_menu(selected=True, padding=self.opened)
        style_selected.button.font = Styles.Property.Font("Segoe UI Semibold", "63 12")
        style_normal = Styles.button_menu(padding=self.opened)
        style_btn_toggle = Styles.button_menu(padding=self.opened)
        style_btn_toggle.button.font.size = 10
        style_btn_toggle.button.color.value = Styles.Color.Reverse.primary.fromRgba(200)

        self.btn_toggle.setStyleSheet(style_btn_toggle.styleSheet())
        for btn in self.btns:
            if btn_select == btn:
                self.btn_selected = btn_select
                btn.setStyleSheet(str(style_selected))
                btn.toggle_icon(True)
            else:
                btn.toggle_icon(False)
                btn.setStyleSheet(str(style_normal))
                
    def update_btns_styles(self):
        style_selected  = Styles.button_menu(selected=True, padding=self.opened)
        style_selected.button.font = Styles.Property.Font("Segoe UI Semibold", "63 12")
        style_normal = Styles.button_menu(padding=self.opened)
        style_btn_toggle = Styles.button_menu(padding=self.opened)
        style_btn_toggle.button.font.size = 10
        style_btn_toggle.button.color.value = Styles.Color.Reverse.primary.fromRgba(200)

        self.btn_toggle.setStyleSheet(style_btn_toggle.styleSheet())
        for btn in self.btns:
            if self.btn_selected == btn:
                btn.toggle_icon(True)
                btn.setStyleSheet(str(style_selected))
            else:
                btn.toggle_icon(False)
                btn.setStyleSheet(str(style_normal))

