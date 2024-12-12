# -*- coding: latin -*-
from PyQt6.QtWidgets import QMenu, QWidgetAction, QApplication, QWidget
from PyQt6.QtCore import QCoreApplication

class Menu(QMenu):

    def __init__(self, widget : QWidget, parent : QWidget | None = None):
        super().__init__(parent)
        self.widget = widget
        self.original_leave_event = self.widget.leaveEvent
        self.is_open = False
        self.widget.leaveEvent = self.widget_leaveEvent
        self.aboutToHide.connect(self.on_menu_about_to_hide)
        self.aboutToShow.connect(self.on_menu_about_to_show)

    def widget_leaveEvent(self, *args, **kwargs):
        if not self.is_open:
            self.original_leave_event(*args, **kwargs)

    def on_menu_about_to_show(self):
        self.widget.setFocus()
        self.is_open = True
       
    def on_menu_about_to_hide(self):
        focused_widget = QApplication.focusWidget()
        if focused_widget:
            focused_widget.clearFocus()
        self.is_open = False
        self.original_leave_event(None)

    def show_near_widget(self, target_widget: QWidget, margin=20):
        """
        Shows the menu positioned and sized relative to the given target widget with a specified margin.

        :param target_widget: The widget relative to which the menu should be positioned and sized.
        :param margin: The margin to apply around the menu (default is 20 pixels).
        """
        QCoreApplication.processEvents()
        # Get the geometry of the target widget
        widget_geometry = target_widget.geometry()
        widget_pos = target_widget.mapToGlobal(widget_geometry.topLeft())  # Convert to global coordinates
        widget_x = widget_pos.x()
        widget_y = widget_pos.y()
        widget_width = widget_geometry.width()
        widget_height = widget_geometry.height()

        # Calculate new size and position with margin
        width = max(0, widget_width - 2 * margin)
        height = max(0, widget_height - 2 * margin)
        pos_x = widget_x + margin
        pos_y = widget_y + margin

        # Set the size and position of the menu
        self.setFixedSize(width, height)
        self.move(pos_x, pos_y)

        # Adjust size of the default widget if the menu has a single QWidgetAction
        actions = self.actions()
        if len(actions) == 1:
            action = actions[0]
            if isinstance(action, QWidgetAction):
                action.defaultWidget().setFixedSize(width - 2, height - 2)

        # Show the menu
        self.exec()

    def show_fullscreen(self, percentage_screen_available = 0.95):
        QCoreApplication.processEvents()
        instance = QCoreApplication.instance().activeWindow()
        if instance:
            if percentage_screen_available > 1 or percentage_screen_available < 0:
                percentage_screen_available = 0.95
            screen = instance.windowHandle().screen()
            available_geometry = screen.availableGeometry()
            available_width = available_geometry.width()
            available_height = available_geometry.height()
            width = int(available_width * percentage_screen_available)
            height = int(available_height * percentage_screen_available)

            # Set the size of the menu to almost full screen
            self.setFixedSize(width, height)
        
            # Calculate the position to center the menu
            pos_x = int((available_width - width) / 2 + available_geometry.left())
            pos_y = int((available_height - height) / 2 + available_geometry.top())

            self.move(pos_x, pos_y)

            actions = self.actions()
            if len(actions) == 1:
                action = actions[0]
                if isinstance(action, QWidgetAction):
                     action.defaultWidget().setFixedSize(width - 2, height - 2)

            self.exec()
        else:
            print('Animation: Active window not found')

    def show_bottom_left(self, widget_left_edge: QWidget | None = None, widget_for_height: QWidget | None = None, additional_width_right=0, margin_left=0, margin_right=0, margin_top=4, margin_bottom=4):
        QCoreApplication.processEvents()
        # Definir largura e altura padrão com base no tamanho do menu
        menu_height = self.sizeHint().height()
        menu_width = self.sizeHint().width()
        widget_geometry = self.widget.geometry()

        # Obter o ponto da borda inferior esquerda do widget
        point = self.widget.rect().bottomRight()

        # Ajustar a largura com base no widget_left_edge
        if widget_left_edge:
            left_edge = widget_left_edge.geometry().left()
            # Atualizar a largura do menu de acordo com o widget_left_edge
            menu_width = widget_geometry.left() - left_edge + widget_geometry.width()
            menu_width = (menu_width + additional_width_right) - (margin_left + margin_right)

        point.setX(point.x() - margin_left - menu_width)  # Ajuste para posicionar o menu à esquerda
        global_point = self.widget.mapToGlobal(point)
            
        # Ajustar a altura com base no widget_for_height
        if widget_for_height:
            bottom_edge = widget_for_height.geometry().height()
            # Atualizar a altura do menu com base no widget_for_height
            menu_height = bottom_edge - widget_geometry.top()

        self.setFixedSize(menu_width, menu_height)

        # Ajustar os widgets internos do menu, se necessário
        for action in self.actions():
            if isinstance(action, self.CustomWidgetAction) or isinstance(action, QWidgetAction):
                action.defaultWidget().setFixedSize(menu_width - 2, menu_height - 2)

        # Obter a altura da tela
        screen_height = QApplication.primaryScreen().geometry().height()

        # Verificar se há espaço suficiente abaixo do widget para o menu
        if global_point.y() + menu_height > screen_height:
            # Se não houver espaço suficiente, exibir o menu acima do widget
            point = self.widget.rect().topLeft()
            global_point = self.widget.mapToGlobal(point)
            global_point.setY(global_point.y() - menu_height - margin_top)  # Ajuste para exibir o menu acima
        else:
            global_point.setY(global_point.y() + margin_bottom)  # Ajuste para exibir o menu abaixo

        # Exibir o menu
        self.exec(global_point)

    def show_menu_over_widget(self, target_widget: QWidget):
        QCoreApplication.processEvents()
        # Obter a posição global do widget (em relação à tela)
        widget_position = target_widget.mapToGlobal(target_widget.rect().topLeft())
        
        # Obter o tamanho do widget
        widget_width = target_widget.width()
        widget_height = target_widget.height()

        # Ajustar o tamanho do menu para cobrir o widget
        self.setFixedSize(widget_width, widget_height)
        # Ajustar os widgets internos do menu, se necessário
        for action in self.actions():
            if isinstance(action, self.CustomWidgetAction) or isinstance(action, QWidgetAction):
                action.defaultWidget().setFixedSize(widget_width - 2, widget_height - 2)
        
        # Mostrar o menu na posição do widget
        
        self.exec(widget_position)


    def show_bottom_right(self, widget_right_edge: QWidget | None = None, widget_for_height: QWidget | None = None, additional_width_left=0, margin_left=0, margin_right=0, margin_top=4, margin_bottom=4):
        QCoreApplication.processEvents()
        # Obter o ponto da borda inferior do widget
        point = self.widget.rect().bottomLeft()
        point.setX((point.x() - additional_width_left) + margin_left)
        global_point = self.widget.mapToGlobal(point)

        # Definir largura e altura padrão com base no tamanho do menu
        menu_height = self.sizeHint().height()
        menu_width = self.sizeHint().width()
        widget_geometry = self.widget.geometry()

        # Ajustar a largura com base no widget_right_edge
        if widget_right_edge:
            right_edge = widget_right_edge.geometry().width()

            # Atualizar a largura do menu de acordo com o widget_right_edge
            menu_width = right_edge - widget_geometry.right() + widget_geometry.width()
            menu_width = (menu_width + additional_width_left) - (margin_right + margin_left)

        # Ajustar a altura com base no widget_for_height
        if widget_for_height:
            bottom_edge = widget_for_height.geometry().height()

            # Atualizar a altura do menu com base no widget_for_height
            menu_height = bottom_edge - widget_geometry.bottom()

        self.setFixedSize(menu_width, menu_height)

        # Ajustar os widgets internos do menu, se necessário
        for action in self.actions():
            if isinstance(action, self.CustomWidgetAction) or isinstance(action, QWidgetAction):
                action.defaultWidget().setFixedSize(menu_width - 2, menu_height - 2)

        # Obter a altura da tela
        screen_height = QApplication.primaryScreen().geometry().height()

        # Verificar se há espaço suficiente abaixo do widget para o menu
        if global_point.y() + menu_height > screen_height:
            # Se não houver espaço suficiente, exibir o menu acima do widget
            point = self.widget.rect().topLeft()
            point.setX((point.x() - additional_width_left) + margin_left)
            global_point = self.widget.mapToGlobal(point)
            global_point.setY(global_point.y() - menu_height - margin_top)  # Ajuste para exibir o menu acima
        else:
            global_point.setY(global_point.y() + margin_bottom)  # Ajuste para exibir o menu abaixo

        # Exibir o menu
        self.exec(global_point)

    def show_top_left(self, widget_left_edge: QWidget | None = None, widget_for_height: QWidget | None = None, additional_width_right=0, margin_left=0, margin_right=0, margin_top=4, margin_bottom=4):
        QCoreApplication.processEvents()
        # Definir largura e altura padrão com base no tamanho do menu
        menu_height = self.sizeHint().height()
        menu_width = self.sizeHint().width()
        widget_geometry = self.widget.geometry()

        # Obter o ponto da borda inferior esquerda do widget
        point = self.widget.rect().bottomRight()

        # Ajustar a largura com base no widget_left_edge
        if widget_left_edge:
            left_edge = widget_left_edge.geometry().left()
            # Atualizar a largura do menu de acordo com o widget_left_edge
            menu_width = widget_geometry.left() - left_edge + widget_geometry.width()
            menu_width = (menu_width + additional_width_right) - (margin_left + margin_right)

        point.setX(point.x() - margin_left - menu_width)  # Ajuste para posicionar o menu à esquerda
        point.setY(point.y() - self.widget.height())
        global_point = self.widget.mapToGlobal(point)
            
        # Ajustar a altura com base no widget_for_height
        if widget_for_height:
            bottom_edge = widget_for_height.geometry().height()
            # Atualizar a altura do menu com base no widget_for_height
            menu_height = bottom_edge - widget_geometry.top()

        self.setFixedSize(menu_width, menu_height)

        # Ajustar os widgets internos do menu, se necessário
        for action in self.actions():
            if isinstance(action, self.CustomWidgetAction) or isinstance(action, QWidgetAction):
                action.defaultWidget().setFixedSize(menu_width - 2, menu_height - 2)

        global_point.setY(global_point.y() - menu_height - margin_top)  # Ajuste para exibir o menu acima
       
        # Exibir o menu
        self.exec(global_point)

    def show_top_right(self, widget_right_edge: QWidget | None = None, widget_for_height: QWidget | None = None, additional_width_left = 0, margin_left = 0, margin_right = 0,  margin_top = 4, margin_bottom = 4):
        QCoreApplication.processEvents()
        # Obter o ponto da borda superior do widget
        point = self.widget.rect().topLeft()
        point.setX((point.x() - additional_width_left) + margin_left)
        global_point = self.widget.mapToGlobal(point)

        # Definir largura e altura padrão com base no tamanho do menu
        menu_height = self.sizeHint().height()
        menu_width = self.sizeHint().width()
        widget_geometry = self.widget.geometry()

        # Ajustar a largura com base no widget_right_edge
        if widget_right_edge:
            right_edge = widget_right_edge.geometry().width()

            # Atualizar a largura do menu de acordo com o widget_right_edge
            menu_width = right_edge - widget_geometry.right() + widget_geometry.width() 
            menu_width = (menu_width + additional_width_left) - (margin_right + margin_left)

        # Ajustar a altura com base no widget_for_height
        if widget_for_height:
            bottom_edge = widget_for_height.geometry().height()

            # Atualizar a altura do menu com base no widget_for_height
            menu_height = bottom_edge - widget_geometry.top()

        self.setFixedSize(menu_width, menu_height)
        # Ajustar os widgets internos do menu, se necessário
        for action in self.actions():
            if isinstance(action, self.CustomWidgetAction) or isinstance(action, QWidgetAction):
                action.defaultWidget().setFixedSize(menu_width - 2, menu_height - 2)

        # Verificar se há espaço suficiente acima do widget para o menu
        if global_point.y() - menu_height < 0:
            # Se não houver espaço suficiente, exibir o menu abaixo do widget
            point = self.widget.rect().bottomLeft()
            point.setX((point.x() - additional_width_left) + margin_left)
            global_point = self.widget.mapToGlobal(point)
            global_point.setY(global_point.y() + margin_bottom)  # Ajuste para exibir o menu abaixo
        else:
            global_point.setY(global_point.y() - menu_height - margin_top)  # Ajuste para exibir o menu acima

        # Exibir o menu
        self.exec(global_point)

    class CustomWidgetAction(QWidgetAction):
        def __init__(self, parent : QWidget = None):
            super().__init__(parent)
         
        
