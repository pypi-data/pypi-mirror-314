# -*- coding: latin -*-
from .comboBox import ComboBox
from .tableWidget import TableWidget
from .listWidget import ListWidget
from .toolButton import ToolButton
from .text import Text
from .dialog import Dialog
from .msg import Msg 
from .style import Styles
from .style.utils import Global
import psutil
from PyQt6.QtCore import QCoreApplication, Qt, QObject, QEvent
from PyQt6.QtGui import QResizeEvent
from .exe import create_exe
from .thread import Thread
from .layout import Layout
from ..utils import Utils
from PyQt6.QtWidgets import QApplication, QFrame, QLabel, QMainWindow, QWidget, QLineEdit, QCheckBox, QRadioButton, QMenu, QScrollBar
from .custom_widgets import CustomWidgets
from .animation import Animation
from .menu import Menu
from .dragDrop import DragDrop
from .memory_manager import MemoryManager
from .notification import Notification
from .frame import Frame
from PyQt6.QtCore import pyqtSignal, QTimer


class ClickFilter(QObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    def eventFilter(self, obj, event):
        event_type = event.type()
        if event_type == QEvent.Type.MouseButtonPress or event_type == QEvent.Type.MouseButtonDblClick or event_type == QEvent.Type.MouseButtonRelease :
            if isinstance(obj, (QFrame, QLabel)):
                return True
        return super().eventFilter(obj, event)

class PyQt(object):

    CLICK_FILTER = ClickFilter()
   
    @staticmethod
    def update_app():
        QCoreApplication.processEvents()

    @staticmethod
    def clearFocus():
        focused_widget = QApplication.focusWidget()
        if focused_widget:
            focused_widget.clearFocus()

    @staticmethod
    def copy(text : str):
        clipboard = QApplication.clipboard()
        clipboard.setText(text)

    def activeWindow() -> QMainWindow:
        return QCoreApplication.instance().activeWindow()
    
    def mainWindow() -> 'MainWindow':
        app = QApplication.instance()
    
        if not app:
            return None
        
        if isinstance(app, QMainWindow):
            return widget
        
        for widget in app.topLevelWidgets():
            if isinstance(widget, QMainWindow):
                return widget

    class MainWindow(QMainWindow):
        signal_toggle_theme = pyqtSignal()
        resizedConnections = []

        class CustomFilters(QObject):
            icons = {}
            def eventFilter(self, obj : QWidget, event : QEvent):
                if event.type() == QEvent.Type.ContextMenu:
                    obj.blockSignals(True)
                    menu : QMenu = None
                    # Cria o menu contextual padrão
                    if hasattr(obj, 'createStandardContextMenu'):
                        menu = obj.createStandardContextMenu() 
                    else:   
                        parent = obj.parentWidget()
                        if hasattr(parent, 'createStandardContextMenu'):
                            menu = parent.createStandardContextMenu() 
                            
                    if menu:
                        for action in menu.actions():
                            icon = action.icon()
                            if icon:
                                if Global.theme == Styles.TypeTheme.dark:
                                    new_icon = Styles.Icons.change_color(icon, [200, 200, 200])
                                    action.setIcon(new_icon) 
                            
                        # Exibe o menu modificado
                        menu.exec(event.globalPos())
                        obj.blockSignals(False)
                        return True
                    obj.blockSignals(False)
                return super().eventFilter(obj, event)
            
        def enabled_track_focusChanged(self):
            self.last_focused_widget = None
            self.penultimate_focused_widget = None
            # Conecta o sinal focusChanged para rastrear widgets com foco
            QApplication.instance().focusChanged.connect(self._track_focus)

        def get_lasts_focused_widgets(self):
            return (self.penultimate_focused_widget, self.last_focused_widget)
            
        def _track_focus(self, old, new):
            """
            Atualiza os widgets com foco.
            """
            if new:  # Apenas atualiza se houver um widget com foco
                self.penultimate_focused_widget = self.last_focused_widget
                self.last_focused_widget = new
              
        def initWebEngineView(self):
            for child in self.children():
                if isinstance(child, QWidget):
                    layout = child.layout()
                    if layout is not None:
                        webView = CustomWidgets.WebEngineView()
                        layout.addWidget(webView)
                        layout.removeWidget(webView)
                        webView.deleteLater()
                        return True
            return False
        
        def resizeEvent(self, a0: QResizeEvent) -> None:   
            try:
                TableWidget.Headers.update_resize()
                if PyQt.Notification.currentWidget and PyQt.Notification.currentWidget.isVisible():
                    PyQt.Notification.currentWidget.center_notification()
                for connection in self.resizedConnections:
                    try:
                        connection()
                    except:
                        ...
            except Exception as ex:
                print('resizeEvent', ex)

            return super().resizeEvent(a0)

        @classmethod
        def resizeConnect(cls, func : object):
            if func not in cls.resizedConnections:
                cls.resizedConnections.append(func)

        def moveEvent(self, event):
            super().moveEvent(event)
            # Reposiciona a notificação quando a janela principal é movida
            if PyQt.Notification.currentWidget and PyQt.Notification.currentWidget.isVisible():
                PyQt.Notification.currentWidget.center_notification()

        def changeEvent(self, event):
            if event.type() == event.Type.WindowStateChange:
                try:
                    if self.isMinimized() and PyQt.Notification.currentWidget and PyQt.Notification.currentWidget.isVisible():
                        PyQt.Notification.currentWidget.pause_timer()

                    elif not self.isMinimized() and Notification.currentWidget and not PyQt.Notification.currentWidget.is_hidden:
                        PyQt.Notification.currentWidget.resume_timer()
                except Exception as ex:
                    print(ex)

            return super().changeEvent(event)

        
    class Frame(Frame):
        ...

    class Menu(Menu):
        ...

    class Animation(Animation):
        ...

    class ComboBox(ComboBox):
        ...

    class DragDrop(DragDrop):
        ...

    class ToolButton(ToolButton):
        ...

    class ListWidget(ListWidget):
        ...

    class TableWidget(TableWidget):
        ...

    class Msg(Msg):
        ...

    class Styles(Styles):
        ...

    class Thread(Thread):
        ...

    class Text(Text):
        ...
        
    class Dialog(Dialog):
        ...

    class Layout(Layout):
        ...

    class CustomWidgets(CustomWidgets):
        ...
    
    class Notification(Notification):
        ...

    class ApiKeyMasker(object):
        def __init__(self, line_edit: QLineEdit, api_key: str = ''):
            """
            Initializes the ApiKeyMasker with the given QLineEdit and the original API key.

            :param line_edit: The QLineEdit widget to mask.
            :param api_key: The original API key to mask.
            """
            self.line_edit = line_edit
            self.original_api_key = api_key

            if api_key.strip():
                # Set initial masked text
                self._set_masked_text()

            # Connect focus events
            self.line_edit.focusInEvent = self._focus_in_event
            self.line_edit.focusOutEvent = self._focus_out_event
            self.line_edit.textChanged.connect(self._update_api_key)

        def update_original_api_key(self, api_key : str):
            self.original_api_key = api_key
            self.line_edit.blockSignals(True)
            if self.line_edit.hasFocus():
                self.line_edit.setText(api_key)
            else:
                self._set_masked_text()
            self.line_edit.blockSignals(False)

        def _set_masked_text(self):
            """Set the masked version of the API key in the line edit."""
            masked_text = Utils.masked_text(self.original_api_key)
            self.line_edit.setText(masked_text)

        def _focus_in_event(self, event):
            """Show the full API key when focused."""
            self.line_edit.setText(self.original_api_key)
            QLineEdit.focusInEvent(self.line_edit, event)

        def _focus_out_event(self, event):
            """Mask the API key when losing focus."""
            self._set_masked_text()
            QLineEdit.focusOutEvent(self.line_edit, event)

        def _update_api_key(self):
            """Update the original_api_key if the line edit text changes while focused."""
            if self.line_edit.hasFocus():
                self.original_api_key = self.line_edit.text()

    def setup_exclusive_selection(*widgets : QCheckBox | QRadioButton):
        def on_widget_clicked(selected_widget : QCheckBox | QRadioButton):
            # Desmarcar todos os botões exceto o botão selecionado
            for widget in widgets:
                if widget is not selected_widget:
                    widget.blockSignals(True)
                    widget.setChecked(False)
                    widget.blockSignals(False)
            
            # Garantir que pelo menos um botão esteja marcado
            if not selected_widget.isChecked():
                selected_widget.blockSignals(True)
                selected_widget.setChecked(True)
                selected_widget.blockSignals(False)
        
        # Conectar o evento de clique para cada botão
        for widget in widgets:
            widget.toggled.connect(lambda _, b=widget: on_widget_clicked(b))
 
    def create_exe(caminho_ficheiro : str, interface_grafica : bool, sem_console : bool, remover_pasta_dist : bool, remover_pasta_build : bool, subProcessLog : Utils.SubProcessLog = None, icon_path : str = "", pyinstaller_args = ""):
        return create_exe(caminho_ficheiro, interface_grafica, sem_console, remover_pasta_dist, remover_pasta_build, subProcessLog, icon_path, pyinstaller_args)

    def window_control(window : QMainWindow):
        if window.isHidden():
            window.show()
            window.setWindowState((window.windowState() & ~Qt.WindowState.WindowMinimized) | Qt.WindowState.WindowActive)
            window.activateWindow()
        else:
            window.setWindowState((window.windowState() & ~Qt.WindowState.WindowMinimized) | Qt.WindowState.WindowActive)
            window.activateWindow()

    def validate_process(pid_number):

        p = psutil.Process(pid = pid_number)
        with p.oneshot():
            status = p.status()                                                                                 
                   
            if status == 'running':
                return True
            else:
                return False
            
    @classmethod
    def scrool_to_bottom(cls, scrool : QScrollBar):
        cls.update_app()
        QTimer.singleShot(50, lambda : scrool.setValue(scrool.maximum()))
            
    class MemoryManager(MemoryManager):
       ...





    

    

