# -*- coding: latin -*-
from .style import Styles
from PyQt6.QtCore import  QBuffer, QIODevice
import io
import PIL.Image as Image
from os import path, makedirs
from winotify import audio
from winotify import Notification as WinNotification
from tempfile import gettempdir
from PyQt6.QtCore import Qt, QTimer, QPropertyAnimation, QRect, QEasingCurve, QSize
from PyQt6.QtWidgets import QLabel, QHBoxLayout, QPushButton, QWidget, QVBoxLayout, QFrame, QMainWindow, QApplication, QDockWidget
from typing import Literal
from enum import Enum
from .custom_widgets.resizeLabel import ResizeLabel
from .msg import Msg

class DataNotification(object):

    def __init__(self, image_name : str, icon_name : Styles.Icons.Name, icon_color = Styles.Icons.Color.ORIGINAL):
        self.image_name = image_name
        self.image_extension : str = icon_name.split('.')[-1]
        self.icon_name = icon_name
        self.icon_color = icon_color

data_notification = {'Standard': DataNotification('LogoStandard', Styles.Icons.Name.mini_logo)}

class NotificationType(Enum):
          Information  = 0
          Error = 1
          Success = 3

class Notification(object):

     currentWidget = None

     class NotificationType(Enum):
          Information  = 0
          Error = 1
          Success = 3

     class Widget(QWidget):


          class StyleSheet(Styles.Standard.StyleSheet):
               def __init__(self, color = Styles.Color.division):
                    super().__init__()
                    self.border_color : Styles.Color | str = color

               def style(self):

                    style = f'''
                    #NotificationWidget {{border: 1px solid {self.border_color}}}
                    #NotificationWidget, #NotificationWidget QLabel, #NotificationWidget QFrame {{background-color: {Styles.Color.primary}; border-radius: 10px;}}
                    {Styles.button(transparent=True)}

                    '''

                    return f'{Styles.standard()} {style}'
               
          def __init__(self, title : str, message : str, duration : int, type : NotificationType):
               super().__init__(self.mainWindow())
               self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Tool)
               self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
               self.setAttribute(Qt.WidgetAttribute.WA_ShowWithoutActivating)
          
               self.is_hidden = False
               frame = QFrame()
               frame.setObjectName("NotificationWidget")

               # Layout principal vertical para o título e o corpo
               main_layout = QVBoxLayout()
               main_layout.setContentsMargins(10, 10, 10, 10)
               main_layout.setSpacing(5)

               # Layout horizontal para o título e o botão de fechar
               title_layout = QHBoxLayout()

               # Título
               label_title = QLabel(title)
               label_title.setStyleSheet('font: 63 12pt "Segoe UI Semibold"')
               title_layout.addWidget(label_title)

               # Botão de fechar
               btn_close = QPushButton()
               btn_close.setFixedSize(20, 20)
               btn_close.setIconSize(QSize(12, 12))
               Styles.set_icon_hover(btn_close, Styles.Icons.Name.close, Styles.Icons.Name.close,  Styles.Icons.Color.GRAY, Styles.Icons.Color.THEME)
               btn_close.clicked.connect(self._close)
               title_layout.addWidget(btn_close)

               # Adiciona o layout do título ao layout principal
               main_layout.addLayout(title_layout)

               # Corpo da mensagem
               message = [Msg.p_nowrap(msg) for msg in message.split('\n')]
               label_message = ResizeLabel('\n'.join(message))
               main_layout.addWidget(label_message)

               # Configurações do layout e estilo
               frame.setLayout(main_layout)
               layout = QVBoxLayout()
               layout.setContentsMargins(0, 0, 0, 0)
               layout.addWidget(frame)
               self.setLayout(layout)

               color = Styles.Color.division
               if type.value == NotificationType.Error.value:
                    color = 'rgba(255, 0, 0, 0.3)'
               elif type.value == NotificationType.Success.value:
                    color = 'rgba(0, 255, 0, 0.3)'

               Styles.set_widget_style_theme(self.StyleSheet(color), self)
               self.adjustSize()

               # Temporizador para fechar automaticamente após 10 segundos
               self.timer = QTimer(self)
               self.timer.timeout.connect(self.start_closing_animation)
               self.timer.start(duration)

               # Inicializar animação de entrada
               self.init_animations()

               # Iniciar animação de entrada
               self.start_opening_animation()
               self.show()

          def mainWindow(self) -> QMainWindow:
               app = QApplication.instance()
          
               if not app:
                    return None
               
               if isinstance(app, QMainWindow) or isinstance(app, QDockWidget):
                    return widget
               
               for widget in app.topLevelWidgets():
                    if isinstance(widget, QMainWindow) or isinstance(app, QDockWidget):
                         return widget

          def _close(self):
               self.closing_animation.setDuration(500)
               self.start_closing_animation()

          def init_animations(self):
               # Inicializa as animações de entrada e saída
               self.opening_animation = QPropertyAnimation(self, b"geometry")
               self.opening_animation.setDuration(1000)
               self.opening_animation.setEasingCurve(QEasingCurve.Type.OutBounce)

               self.closing_animation = QPropertyAnimation(self, b"windowOpacity")
               self.closing_animation.setDuration(1000)
               self.closing_animation.setEasingCurve(QEasingCurve.Type.OutQuad)

               # Definir ação de fechamento ao término da animação de fechamento
               self.closing_animation.finished.connect(self.close)

          def start_opening_animation(self):
               parent = self.parentWidget()
               if parent:
                    parent_geometry = parent.geometry()
                    x = parent_geometry.x() + (parent_geometry.width() - self.width()) // 2
                    y = parent_geometry.y() + 10 
                    self.move(x, parent_geometry.y() - 10)

                    # Configura a animação de entrada: descer do topo até a posição correta
                    final_geometry = QRect(x, y, self.geometry().width(), self.geometry().height())
                    start_geometry = QRect(x, parent_geometry.y() - 10, self.geometry().width(), self.geometry().height())
                    self.setGeometry(start_geometry)

                    self.opening_animation.setStartValue(start_geometry)
                    self.opening_animation.setEndValue(final_geometry)
                    self.opening_animation.start()

          def start_closing_animation(self):
               self.is_hidden = True
               self.closing_animation.setStartValue(1.0)
               self.closing_animation.setEndValue(0.0)
               self.closing_animation.start()
               
          def center_notification(self):
               # Centraliza a notificação com relação à janela principal (parent)
               parent = self.parentWidget()
               if parent:
                    parent_geometry = parent.geometry()
                    x = parent_geometry.x() + (parent_geometry.width() - self.width()) // 2
                    y = parent_geometry.y() + 20  # A notificação aparece perto do topo da janela principal
                    self.move(x, y)

          def pause_timer(self):
               if self.timer.isActive():
                    self.remaining_time = self.timer.remainingTime()
                    self.timer.stop()

          def resume_timer(self):
               if not self.timer.isActive():
                    self.timer.start(self.remaining_time)


     @classmethod
     def convert_icon_to_img(cls, icon : Styles.Icons.Icon, save_path = None, save_name = "image", size=None, fmt: str = "png"):
          if size is None:
               size = icon.availableSizes()[0]
     
          pixmap = icon.pixmap(size)
     
          # Converte o QPixmap em QImage para preservar a transparáncia
          image = pixmap.toImage()
     
          # Cria um buffer para salvar a imagem em bytes
          buffer = QBuffer()
          buffer.open(QIODevice.OpenModeFlag.WriteOnly)
          image.save(buffer, fmt)
          buffer.close()
     
          # Cria a imagem PIL a partir dos bytes
          image_pil = Image.open(io.BytesIO(buffer.data()))
     
          if save_path:
               image_pil.save(path.join(save_path, f"{save_name}.{fmt}"))
          else:
               image_pil.save(f"{save_name}.{fmt}")

     @classmethod
     def setSystemData(cls, app_name : str, image_name : str, icon_name : Styles.Icons.Name, icon_color = Styles.Icons.Color.ORIGINAL):
          data_notification[app_name] = DataNotification(image_name, icon_name, icon_color)

     @classmethod
     def system(cls, title, message, duration : Literal["short", "long"] = "short", app_name : str = 'GUIAppStandard'):
          pdir = gettempdir()
          temp_folder = path.join(pdir, 'GUIApps')

          if not path.exists(temp_folder):
               makedirs(temp_folder)

          if app_name in data_notification:
               data = data_notification[app_name]
          else:
               data = data_notification['Standard']

          temp_image = path.join(temp_folder, f"{data.image_name}.{data.image_extension}")
          if not path.exists(temp_image):
               try:
                    pdir = gettempdir()
                    icon = Styles.Icons.Icon(data.icon_name, data.icon_color)
                    cls.convert_icon_to_img(icon, save_path=temp_folder, save_name=data.image_name, fmt=data.image_extension)
               except Exception as e:
                    print(e)
                    ...
               if not path.exists(temp_image):
                    temp_image = ""

          toast = WinNotification(app_id=app_name,
                                   title=title,
                              msg=message,
                              duration=duration,
                              icon=temp_image
                              )
          toast.set_audio(audio.Default, loop=False)
          #toast.add_actions(label="Clicar aqui", launch="https://google.com")
          toast.show()

     @classmethod
     def information(cls, title, message ,duration = 5000):
          if cls.currentWidget:
               currentWidget = cls.currentWidget
               if cls.currentWidget.timer.isActive():
                    currentWidget._close()
                    QTimer.singleShot(1000, currentWidget.deleteLater)
               else:
                    currentWidget.deleteLater()
          cls.currentWidget = cls.Widget(title, message, duration, NotificationType.Information)


     @classmethod
     def error(cls, title, message ,duration = 5000):
          if cls.currentWidget:
               currentWidget = cls.currentWidget
               if cls.currentWidget.timer.isActive():
                    currentWidget._close()
                    QTimer.singleShot(1000, currentWidget.deleteLater)
               else:
                    currentWidget.deleteLater()
          cls.currentWidget = cls.Widget(title, message, duration,  NotificationType.Error)

     @classmethod
     def success(cls, title, message ,duration = 5000):
          if cls.currentWidget:
               currentWidget = cls.currentWidget
               if cls.currentWidget.timer.isActive():
                    currentWidget._close()
                    QTimer.singleShot(1000, currentWidget.deleteLater)
               else:
                    currentWidget.deleteLater()
          cls.currentWidget = cls.Widget(title, message, duration, NotificationType.Success)