
# -*- coding: latin -*-
import gc
from PyQt6.QtWidgets import QWidget, QLayout

class MemoryManager:
        def __init__(self):
            self.tracked_variables = {}

        def track_variable(self, name: str, variable : object):
            """Armazena uma referência a uma variável para facilitar a remoção posteriormente."""
            self.tracked_variables[name] = variable

        def remove_variable(self, name: str):
            """Remove uma variável armazenada e limpa a memória."""
            if name in self.tracked_variables:
                del self.tracked_variables[name]
                gc.collect()

        def clear_variables(self):
            """Remove todas as variáveis armazenadas e limpa a memória."""
            self.tracked_variables.clear()
            gc.collect()

        def remove_widget(self, widget: QWidget):
            """Remove um widget da interface e limpa a memória."""
            if widget is not None:
                widget.setParent(None)
                widget.deleteLater()
                #gc.collect()

        def clear_layout(self, layout: QLayout, remove_itens = False):
            """Remove todos os widgets de um layout e limpa a memória."""
            if layout:
                while layout.count():
                    item = layout.takeAt(0)
                    widget = item.widget()
                    if widget is not None:
                        self.remove_widget(widget)
                    else:
                        if remove_itens:
                            layout.removeItem(item)

        def free_memory(self):
            """Força a coleta de lixo para liberar a memória."""
            gc.collect()
    