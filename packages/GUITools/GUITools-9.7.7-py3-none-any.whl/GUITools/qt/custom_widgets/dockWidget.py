
# -*- coding: latin -*-
from PyQt6.QtWidgets import QTabWidget, QWidget, QDockWidget, QApplication, QMainWindow, QPushButton, QTabBar, QVBoxLayout, QStackedWidget
from PyQt6.QtGui import QCloseEvent, QResizeEvent
from PyQt6.QtCore import QEvent, Qt, pyqtSignal, QSize, QCoreApplication
from ..style import Styles
from typing import Callable

class TabWidgetDock(QDockWidget):
    resized = pyqtSignal()

    class StyleSheet(Styles.Standard.StyleSheet):
        def __init__(self, style_sheet : Callable | None):
            super().__init__()
            self.custom_style_sheet = style_sheet

        def style(self):
            ustom_style_sheet = ""
            if self.custom_style_sheet != None:
                ustom_style_sheet = self.custom_style_sheet()
            return f'{Styles.standard()} {ustom_style_sheet}'

    class TitleWidget(QWidget):
        def __init__(self, dock_widget : QDockWidget, parent=None):
            super().__init__(parent)
            self.dock = dock_widget

   
    def __init__(self, *, tabWidget : QTabWidget, widget : QWidget,  tab_title : str, doc_title : str, icon_data : Styles.Icons.Data , style_sheet : Callable | None = None, insert_position : int | None = None, action_delete : Callable = None, delete_enabled = False):
        super().__init__(doc_title)
        tabWidget.setIconSize(QSize(20, 20))
        self.tab = QWidget()
    
        self.tab_title = tab_title
        self.icon = Styles.Icons.Icon(icon_data.name, icon_data.color)
        self.setWindowIcon(Styles.Icons.Icon(icon_data.hover_name, icon_data.hover_color))
        self.icon_data = icon_data
        self.tabWidget = tabWidget
        self.tab_index = self.tabWidget.indexOf(self.tab)
        self.action_delete = action_delete
        self.delete_enabled = delete_enabled

        self.setWindowFlags(Qt.WindowType.CustomizeWindowHint |  Qt.WindowType.Widget | Qt.WindowType.WindowMinimizeButtonHint |
        Qt.WindowType.WindowMaximizeButtonHint | Qt.WindowType.WindowCloseButtonHint)

        self.setWidget(widget)

       
        tab_layout = QVBoxLayout(self.tab)

        tab_layout.addWidget(self)
        tab_layout.setContentsMargins(0, 0, 0, 0)

       
        if insert_position != None:
            self.tab_index = self.tabWidget.insertTab(insert_position, self.tab, self.icon , tab_title)
        else:
            self.tab_index = self.tabWidget.addTab(self.tab, self.icon , tab_title)

        self.add_toggle_button()
        self.setTitleBarWidget(self.TitleWidget(self))
        
        self.installEventFilter(self)

        self.connTabChanged = tabWidget.currentChanged.connect(self.toggle_tab)

        Styles.set_widget_style_theme(self.StyleSheet(style_sheet), self)

    def activate(self):
        if self.parent() != None:
            self.tabWidget.setCurrentWidget(self.tab)
        else:
            if self.isHidden():
                self.show()
                self.setWindowState((self.windowState() & ~Qt.WindowState.WindowMinimized) | Qt.WindowState.WindowActive)
                self.activateWindow()
            else:
                self.setWindowState((self.windowState() & ~Qt.WindowState.WindowMinimized) | Qt.WindowState.WindowActive)
                self.activateWindow()

    def update_title(self, tab_title : str, doc_title : str):
        self.tab_title = tab_title
        self.setWindowTitle(doc_title)
        tab_index = self.tabWidget.indexOf(self.tab)
        if tab_index != -1:
            self.tabWidget.setTabText(tab_index, tab_title)
    
    def update_icon_data(self, icon_data : Styles.Icons.Data):
        self.icon_data = icon_data
        self.icon = Styles.Icons.Icon(icon_data.name, icon_data.color)
        self.setWindowIcon(Styles.Icons.Icon(icon_data.hover_name, icon_data.hover_color))
        self.toggle_tab()

    def toggle_tab(self, *args):
        position = self.tabWidget.indexOf(self.tab)
        if position != -1:
            if self.tabWidget.currentWidget() == self.tab:
                self.tabWidget.setTabIcon(position, Styles.Icons.Icon(self.icon_data.hover_name, self.icon_data.hover_color))
            else:
                self.tabWidget.setTabIcon(position, Styles.Icons.Icon(self.icon_data.name, self.icon_data.color))

    def resizeEvent(self, a0: QResizeEvent) -> None:
        self.resized.emit()
        return super().resizeEvent(a0)

    def resizeConnect(self, func : object):
          self.resized.connect(func)

    def set_enabled_delete(self, enebled : bool):
        self.delete_enabled = enebled
        if self.parent() != None:
            if enebled:
                btn_delete = QPushButton()
                if self.action_delete:
                    btn_delete.clicked.connect(self.action_delete)
                btn_delete.setIconSize(QSize(14, 14))
                btn_delete.setCursor(Qt.CursorShape.PointingHandCursor)
                Styles.set_icon_theme(btn_delete, Styles.Icons.Name.lixo, Styles.Icons.Name.lixo, Styles.Icons.Color.GRAY, Styles.Icons.Color.ORIGINAL)
                self.tabWidget.tabBar().setTabButton(self.tab_index, QTabBar.ButtonPosition.RightSide, btn_delete)
            else:
                btn_delete = self.tabWidget.tabBar().tabButton(self.tab_index, QTabBar.ButtonPosition.RightSide)
                if btn_delete:
                    btn_delete.setParent(None) 

    def add_toggle_button(self):

        if self.delete_enabled:
            btn_delete = QPushButton()
            if self.action_delete:
                btn_delete.clicked.connect(self.action_delete)
            btn_delete.setIconSize(QSize(14, 14))
            btn_delete.setCursor(Qt.CursorShape.PointingHandCursor)
            Styles.set_icon_theme(btn_delete, Styles.Icons.Name.lixo, Styles.Icons.Name.lixo, Styles.Icons.Color.GRAY, Styles.Icons.Color.ORIGINAL)
            self.tabWidget.tabBar().setTabButton(self.tab_index, QTabBar.ButtonPosition.RightSide, btn_delete)
           
        btn_maximize = QPushButton()
        btn_maximize.setIconSize(QSize(14, 14))
        btn_maximize.setCursor(Qt.CursorShape.PointingHandCursor)

        Styles.set_icon_hover(btn_maximize, Styles.Icons.Name.maximize, Styles.Icons.Name.maximize, Styles.Icons.Color.GRAY)
        btn_maximize.clicked.connect(self.toggle_dock)
        self.tabWidget.tabBar().setTabButton(self.tab_index, QTabBar.ButtonPosition.LeftSide, btn_maximize)

    def mainWindow(self) -> QMainWindow:
        app = QApplication.instance()
    
        if not app:
            return None
        
        if isinstance(app, QMainWindow):
            return widget
        
        for widget in app.topLevelWidgets():
            if isinstance(widget, QMainWindow):
                return widget

    def center(self):
        # Obtém a tela onde a janela atual está sendo exibida
        mainWindow = self.mainWindow()
        current_screen = QApplication.screenAt(mainWindow.geometry().center())
        
        if current_screen is None:
            # Se a tela não for encontrada, usa a tela primária como fallback
            current_screen = QApplication.primaryScreen()

        # Obtém a geometria da tela onde a janela está sendo exibida
        screen_geometry = current_screen.geometry()

        # Calcula as coordenadas X e Y para centralizar a janela
        x = (screen_geometry.width() - self.width()) // 2 + screen_geometry.x()
        y = (screen_geometry.height() - self.height()) // 2 + screen_geometry.y()

        # Move a janela para a posição central na tela correta
        self.move(x, y)

    def toggle_dock(self):
        if self.parent() != None:
            self.removeDock()
        else:
            self.restoreDock()
     
    def eventFilter(self, obj, event):
      
        if event.type() == QEvent.Type.NonClientAreaMouseButtonDblClick:
            return True
        return super().eventFilter(obj, event)

    def removeDock(self):
        self.setParent(None)
        index = self.tabWidget.indexOf(self.tab)
        if index != -1:  # Verifica se a tab foi encontrada
            self.tab_index = index
            self.tabWidget.removeTab(index) 
            self.show()
            
    def restoreDock(self):
        self.tab.layout().addWidget(self)
        self.tabWidget.insertTab(self.tab_index ,self.tab, self.icon, self.tab_title)
        self.tabWidget.setCurrentIndex(self.tab_index)
        self.add_toggle_button()
        self.show()

    def show(self):
        self.resize(1200, 700)
        self.center()
        return super().show()
        
    def closeEvent(self, event: QCloseEvent) -> None:
        self.restoreDock()
        event.ignore()

    def deleteLater(self) -> None:
        self.tab.setParent(None)
        self.tab.deleteLater()
        self.tabWidget.disconnect(self.connTabChanged)
        return super().deleteLater()
    

class StackedWidgetDock(QDockWidget):
    resized = pyqtSignal()

    class StyleSheet(Styles.Standard.StyleSheet):
        def __init__(self, style_sheet : Callable | None):
            super().__init__()
            self.custom_style_sheet = style_sheet

        def style(self):
            ustom_style_sheet = ""
            if self.custom_style_sheet != None:
                ustom_style_sheet = self.custom_style_sheet()
            return f'{Styles.standard()} {ustom_style_sheet}'

    class TitleWidget(QWidget):
        def __init__(self, dock_widget : QDockWidget, parent=None):
            super().__init__(parent)
            self.dock = dock_widget

   
    def __init__(self, *, stackedWidget : QStackedWidget, widget : QWidget, btn_maximize : QPushButton, doc_title : str, icon : Styles.Icons.Icon , style_sheet : Callable | None = None):
        super().__init__(doc_title)

        self.page = QWidget()
        self.btn_maximize = btn_maximize
        self.btn_maximize.setCursor(Qt.CursorShape.PointingHandCursor)
        Styles.set_icon_hover(self.btn_maximize, Styles.Icons.Name.maximize, Styles.Icons.Name.maximize, Styles.Icons.Color.GRAY)
        self.btn_maximize.clicked.connect(self.toggle_dock)

        self.setWindowIcon(icon)
        self.stackedWidget = stackedWidget
       
        self.setWindowFlags(Qt.WindowType.CustomizeWindowHint |  Qt.WindowType.Widget | Qt.WindowType.WindowMinimizeButtonHint |
        Qt.WindowType.WindowMaximizeButtonHint | Qt.WindowType.WindowCloseButtonHint)

        self.setWidget(widget)

        page_layout = QVBoxLayout(self.page)

        page_layout.addWidget(self)
        page_layout.setContentsMargins(0, 0, 0, 0)

        self.stackedWidget.addWidget(self.page)

        self.setTitleBarWidget(self.TitleWidget(self))
        
        self.installEventFilter(self)
        Styles.set_widget_style_theme(self.StyleSheet(style_sheet), self)

    def activate(self):
        if self.parent() != None:
            self.stackedWidget.setCurrentWidget(self.page)
        else:
            if self.isHidden():
                self.show()
                self.setWindowState((self.windowState() & ~Qt.WindowState.WindowMinimized) | Qt.WindowState.WindowActive)
                self.activateWindow()
            else:
                self.setWindowState((self.windowState() & ~Qt.WindowState.WindowMinimized) | Qt.WindowState.WindowActive)
                self.activateWindow()

    def update_title(self,  doc_title : str):
        self.setWindowTitle(doc_title)

    def update_icon_data(self, icon : Styles.Icons.Icon):
        self.setWindowIcon(icon)

    def resizeEvent(self, a0: QResizeEvent) -> None:
        self.resized.emit()
        return super().resizeEvent(a0)

    def resizeConnect(self, func : object):
          self.resized.connect(func)

    def mainWindow(self) -> QMainWindow:
        app = QApplication.instance()
    
        if not app:
            return None
        
        if isinstance(app, QMainWindow):
            return widget
        
        for widget in app.topLevelWidgets():
            if isinstance(widget, QMainWindow):
                return widget

    def center(self):
        # Obtém a tela onde a janela atual está sendo exibida
        mainWindow = self.mainWindow()
        current_screen = QApplication.screenAt(mainWindow.geometry().center())
        
        if current_screen is None:
            # Se a tela não for encontrada, usa a tela primária como fallback
            current_screen = QApplication.primaryScreen()

        # Obtém a geometria da tela onde a janela está sendo exibida
        screen_geometry = current_screen.geometry()

        # Calcula as coordenadas X e Y para centralizar a janela
        x = (screen_geometry.width() - self.width()) // 2 + screen_geometry.x()
        y = (screen_geometry.height() - self.height()) // 2 + screen_geometry.y()

        # Move a janela para a posição central na tela correta
        self.move(x, y)

    def toggle_dock(self):
        if self.parent() != None:
            self.removeDock()
        else:
            self.restoreDock()
     
    def eventFilter(self, obj, event):
        if event.type() == QEvent.Type.NonClientAreaMouseButtonDblClick:
            return True
        return super().eventFilter(obj, event)

    def removeDock(self):
        self.setParent(None)
        self.btn_maximize.close()
        index = self.stackedWidget.indexOf(self.page)
        if index != -1:  
            self.stackedWidget.removeWidget(self.page) 
            self.show()
            
    def restoreDock(self):
        self.page.layout().addWidget(self)
        self.btn_maximize.show()
        self.stackedWidget.addWidget(self.page)
        self.stackedWidget.setCurrentWidget(self.page)
        self.show()
        QCoreApplication.processEvents()

    def show(self):
        self.resize(1200, 700)
        self.center()
        return super().show()
        
    def closeEvent(self, event: QCloseEvent) -> None:
        self.restoreDock()
        event.ignore()

    def deleteLater(self) -> None:
        self.page.setParent(None)
        self.page.deleteLater()
        return super().deleteLater()
    
    
    
