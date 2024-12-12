# -*- coding: latin -*-

from PyQt6.QtWidgets import QToolButton, QMenu
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction

class ToolButton(QToolButton):
        def __init__(self, text : str ,actions : list[QAction], parent=None):
            super().__init__(parent)
            self.setText(text)
            # Crie um menu suspenso
            self.menu = QMenu(self)
            self.menu.addActions(actions)
            
            self.setArrowType(Qt.ArrowType.NoArrow)
            # Associe o menu suspenso ao botão
            self.setMenu(self.menu)
            self.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)
            



'''

# Crie um menu suspenso
            self.menu = QMenu(self)
            self.setArrowType(Qt.ArrowType.NoArrow)
       
            action1 = self.menu.addAction("Action 1")
            action2 = self.menu.addAction("Action 2")
            action3 = self.menu.addAction("Action 3")

            # Connect the actions to methods
            action1.triggered.connect(self.action1_triggered)
            action2.triggered.connect(self.action2_triggered)
            action3.triggered.connect(self.action3_triggered)

            # Associe o menu suspenso ao botão
            self.setMenu(self.menu)
            self.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)
       
        def action1_triggered(self):
            # Handle the "Action 1" action
            print("action1_triggered")

        def action2_triggered(self):
            # Handle the "Action 2" action
            print("action2_triggered")

        def action3_triggered(self):
            # Handle the "Action 3" action
            print("action3_triggered")

'''



