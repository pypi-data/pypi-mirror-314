# -*- coding: latin -*-
from enum import Enum
from PyQt6.QtCore import  Qt
from PyQt6.QtWidgets import QWidget, QSplitter, QVBoxLayout, QHBoxLayout
from typing import Type, TypeVar
from .memory_manager import MemoryManager

T = TypeVar('T')

class Layout(object):
        
        MemoryManager = MemoryManager()

        class Size(Enum):
            ONE_HALF = 1/2
            ONE_THIRD = 1/3
            TWO_THIRDS = 2/3
            ONE_QUARTERS = 1/4
            TWO_QUARTERS = 2/4
            THREE_QUARTERS = 3/4

        @classmethod
        def custom_size(cls, frame : QWidget, sizes : list[int | Size]):
            size_frame = frame.height()
            _sizes = []
            for size in sizes:
                if type(size) == cls.Size:
                    _sizes.append(int(size_frame * size.value))
                else:
                    _sizes.append(size)
            return _sizes

        @classmethod
        def splitter_vertical(cls, frame : QWidget, widgets : list[QWidget], sizes : list[int | Size] | None = None):
          
            splitter = QSplitter(Qt.Orientation.Vertical)
            for widget in widgets:
                widget.setParent(splitter)
            if sizes:
                custom_size = cls.custom_size(frame, sizes)
                splitter.setSizes(custom_size)

            frame.layout().addWidget(splitter)
            return splitter


        @classmethod
        def splitter_horizontal(cls, frame : QWidget, widgets : list[QWidget], sizes : list[int] | None = None):
            splitter = QSplitter(Qt.Orientation.Horizontal)
            for widget in widgets:
                widget.setParent(splitter)
            if sizes:
                custom_size = cls.custom_size(frame, sizes)
                splitter.setSizes(custom_size)

            frame.layout().addWidget(splitter)
            return splitter

        @classmethod
        def clear(cls, layout : QVBoxLayout | QHBoxLayout, remove_itens = False):
            cls.MemoryManager.clear_layout(layout, remove_itens)

        @classmethod
        def get_widgets(cls, layout : QVBoxLayout | QHBoxLayout, type : Type[T] = QWidget) -> list[T]:
            widgets = []
            if layout:
                for i in range(layout.count()):
                    item = layout.itemAt(i)
                    widgets.append(item.widget())
            return widgets

        @classmethod
        def find_parent_by_name(cls, widget: QWidget, target_name: str) -> QWidget | None:
            """
            Finds the parent widget by its object name.

            Args:
                widget (QWidget): The starting widget to begin the search from.
                target_name (str): The name of the target widget to find.

            Returns:
                QWidget | None: The found widget with the matching name, or None if not found.
            """
            # Start with the current widget's parent
            parent = widget.parentWidget()
            
            # Traverse up the widget hierarchy
            while parent is not None:
                # Check if the current parent has the target object name
                if parent.objectName() == target_name:
                    return parent
                # Move up to the next parent
                parent = parent.parentWidget()

        @classmethod
        def find_all_children_in_parent(cls, widget: QWidget, target_name: str) -> list[QWidget]:
            """
            Finds the parent widget by its object name and returns all its child widgets recursively.

            Args:
                widget (QWidget): The starting widget to begin the search from.
                target_name (str): The name of the target widget to find.

            Returns:
                List[QWidget] | None: A list of all widgets inside the found parent, or None if the parent is not found.
            """
            # Start with the current widget's parent
            parent = widget.parentWidget()
            
            # Traverse up the widget hierarchy to find the parent with the matching name
            while parent is not None:
                if parent.objectName() == target_name:
                    # If the parent is found, recursively find all children
                    return cls.get_all_children(parent)
                # Move up to the next parent
                parent = parent.parentWidget()
            
            return []

        @classmethod
        def get_all_children(cls, parent: QWidget) -> list[QWidget]:
            """
            Recursively retrieves all children of a given parent widget.

            Args:
                parent (QWidget): The parent widget to search within.

            Returns:
                List[QWidget]: A list of all child widgets.
            """
            all_children = []
            # Use findChildren to get all direct and nested children
            children = parent.findChildren(QWidget)
            
            for child in children:
                all_children.append(child)
                # Recursively add children's children
                all_children.extend(cls.get_all_children(child))
            
            return all_children



