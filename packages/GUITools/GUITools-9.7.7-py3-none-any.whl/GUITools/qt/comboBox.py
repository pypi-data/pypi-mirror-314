# -*- coding: latin -*-

from PyQt6.QtWidgets import QComboBox, QWidget, QHBoxLayout, QVBoxLayout
from PyQt6.QtCore import Qt, QEvent
from PyQt6.QtGui import QStandardItem, QIcon
from typing import Any, Callable

class DataUpdate(object):

    class Item:
        def __init__(self, text : str, icon : QIcon = None,  data = ...):
            self.text = text
            self.icon = icon
            self.data = data

    def __init__(self):
        self.items : list[self.Item] = []

    def append(self, text : str, icon : QIcon = None,  data = ...):
        new_item = self.Item(text, icon, data)
        self.items.append(new_item)

def get_properties_names(obj):
     classname = obj.__class__
     components = dir(classname)
     properties = filter(lambda attr: type(getattr(classname, attr)) is property, components)
     return properties

class CustomQComboBox(QComboBox):

    def __init__(self, parent : QWidget = None):
        super().__init__(parent)

        self.wheelEvent = lambda event : event.ignore()

        # Make the combo editable to set a custom text, but readonly
        self.setEditable(True)
        self.lineEdit().setReadOnly(True)
        self.lineEdit().selectionChanged.connect(lambda: self.lineEdit().setSelection(0, 0))
        
        # Hide and show popup when clicking the line edit
        self.lineEdit().installEventFilter(self)
        self.closeOnLineEditClick = False
        
        # Prevent popup from closing when clicking on an item
        self.view().viewport().installEventFilter(self)

    def resizeEvent(self, event):
        # Recompute text to elide as needed
        self.updateText()
        super().resizeEvent(event)

    def showPopup(self):
        super().showPopup()
        # When the popup is displayed, a click on the lineedit should close it
        self.closeOnLineEditClick = True

    def hidePopup(self):
        super().hidePopup()
        # Used to prevent immediate reopening when clicking on the lineEdit
        self.startTimer(100)
        # Refresh the display text when closing
        self.updateText()

    def timerEvent(self, event):
        # After timeout, kill timer, and reenable click on line edit
        self.killTimer(event.timerId())
        self.closeOnLineEditClick = False

    def addItems(self, texts, datalist=None):
        for i, text in enumerate(texts):
            try:
                data = datalist[i]
            except (TypeError, IndexError):
                data = None
            self.addItem(text, data)

class TypeComboBox:
    Checkable = "Checkable"
    Uncheck = 'Uncheck'


class ComboBox(object):

    class TypeComboBox(TypeComboBox):
        ...

    def ignoreWheelEvent(comboBox : QComboBox):
        comboBox.wheelEvent = lambda event : event.ignore() 

    @classmethod
    def New(cls, type_cbx : TypeComboBox, horizontalLayout : QHBoxLayout | QVBoxLayout, fixedText : str = None, size : int = None):
        
        if type_cbx == TypeComboBox.Checkable:
            comboBox = cls.QComboBoxCheckable()
        else:
            comboBox = cls.QComboBoxUncheck()

        if fixedText:
            comboBox.setFixedText(fixedText)

        if size:
            comboBox.setMaximumWidth(size)
            comboBox.setMinimumWidth(size)

        horizontalLayout.addWidget(comboBox)
        return comboBox

    class DataUpdate(DataUpdate):
        ...
        
    @classmethod
    def add_data(cls, comboBox: QComboBox, new_data: DataUpdate):

        if new_data:
            # Adicione os novos itens ao ComboBox
            for item in new_data.items:
                if item.icon:
                    comboBox.addItem(item.icon, str(item.text), item.data)
                else:
                    comboBox.addItem(str(item.text), item.data)


    @classmethod
    def update_data(cls, comboBox: QComboBox, new_data: DataUpdate,  itemSelectAll=False, force_update = False):
        
        all_items = [] if force_update else [comboBox.itemText(i) for i in range(comboBox.count())] 
        if force_update:
            comboBox.clear()

        # Crie uma lista de strings a partir dos novos dados
        new_data_str = [str(item.text) for item in new_data.items]

        if all_items != new_data_str:
            if not new_data_str:

                if itemSelectAll :

                    while comboBox.count() > 1:
                        for index in range(comboBox.count()):
                            if index != 0:
                                comboBox.removeItem(index)
                else:
                    while comboBox.count():
                        for index in range(comboBox.count()):
                             comboBox.removeItem(index)
               
            else:
                for item in new_data.items:
                    if item.text not in all_items:
                        if item.icon:
                            comboBox.addItem(item.icon, str(item.text), item.data)
                        else:
                            comboBox.addItem(str(item.text), item.data)

                for index, item in enumerate(all_items):
                    if item not in new_data_str:
                        if itemSelectAll:
                            if index != 0:
                                comboBox.removeItem(index)
                            else:
                                if not comboBox.itemSelectAll:
                                    comboBox.removeItem(index)
                        else:
                            comboBox.removeItem(index)

        else:
            for index, item in enumerate(new_data.items):
                if item.icon:
                    comboBox.setItemIcon(index, item.icon)
                else:
                    comboBox.setItemIcon(index, QIcon(None))
                comboBox.setItemData(index, item.data)

    @staticmethod
    def update(comboBox : QComboBox, new_data : list[str] | dict[str, QIcon], itemSelectAll = False):

        all_items = [comboBox.itemText(i) for i in range(comboBox.count())]

        new_data_str = []
        for data in new_data:
            new_data_str.append(str(data))

        if all_items != new_data_str:
            if not new_data_str:

                if itemSelectAll :

                    while comboBox.count() > 1:
                        for index in range(comboBox.count()):
                            if index != 0:
                                comboBox.removeItem(index)
                else:
                    while comboBox.count():
                        for index in range(comboBox.count()):
                             comboBox.removeItem(index)
               
            else:
                for data in new_data_str:
                    if data not in all_items:
                        if type(new_data) == list:
                            comboBox.addItem(data)
                        else:
                            comboBox.addItem(new_data[data], data)

                for index, item in enumerate(all_items):
                    if item not in new_data_str:
                        if itemSelectAll:
                            if index != 0:
                                comboBox.removeItem(index)
                            else:
                                if not comboBox.itemSelectAll:
                                    comboBox.removeItem(index)
                        else:
                            comboBox.removeItem(index)

    class QComboBoxCheckable(CustomQComboBox):

        def __init__(self, parent : QWidget = None):
            self._fixedText = ""
            self._itemSelectAll = False
            CustomQComboBox.__init__(self, parent)

        @property
        def itemSelectAll(self) -> bool:
            return self._itemSelectAll

        @itemSelectAll.setter
        def itemSelectAll(self, value):
            self._itemSelectAll = value

        def setFixedText(self, text_fixed: str, text_item_selectAll : str = 'Todos'):
            self._fixedText = text_fixed
            if text_fixed.strip():
                self.insertItem(0, text_item_selectAll)
                self._itemSelectAll = True
                if self.model().item(0):
                    self.model().item(0).setCheckState(Qt.CheckState.Checked)
                
        def removeFixedText(self, text_item_selectAll : str = 'Todos'):
            if self.itemText(0) == text_item_selectAll:
                self.removeItem(0)
                self._itemSelectAll = False

        def setItemSelectAll(self, text_item :str = 'Todos'):
                self.insertItem(0, text_item)
                self._itemSelectAll = True
                if self.model().item(0):
                    self.model().item(0).setCheckState(Qt.CheckState.Checked)

        def itemSelectAllCheckState(self):
            if self._itemSelectAll:
                 if self.model().item(0):
                    check = True if self.model().item(0).checkState() == Qt.CheckState.Checked else False
                    return check
            return False

        def setItemCheckState(self, text : str, check : bool):
            index = self.findText(text, Qt.MatchFlag.MatchFixedString)
            item = self.model().item(index)
            if item:
                self.model().item(index).setCheckState(Qt.CheckState.Checked if check else Qt.CheckState.Unchecked)
                self.updateText()
            return bool(item)
        
        def setItemsCheckState(self, texts : list[str], check : bool):
            for text in texts:
                self.setItemCheckState(text, check)
        
        def setItemCheckStateFromData(self, data : Any, check : bool):
            index = self.findData(data)
            item = self.model().item(index)
            if item:
                self.model().item(index).setCheckState(Qt.CheckState.Checked if check else Qt.CheckState.Unchecked)
                self.updateText()
            return bool(item)
        
        def setItemsCheckStateFromData(self, list_data : list[Any], check : bool):
            for data in list_data:
                self.setItemCheckStateFromData(data, check)

        def setToggleItem(self, toggleItem : Callable):

            def __toggleItem(item):
                if toggleItem:
                    if self._itemSelectAll and item.row() == 0:
                        return
                    check = True if self.model().item(item.row()).checkState() == Qt.CheckState.Checked else False
                    toggleItem(self.itemText(item.row()), check)

                self.updateText()

            # Update the text when an item is toggled
            self.model().dataChanged.connect(__toggleItem)

        def eventFilter(self, object, event):

            if event.type() == QEvent.Type.MouseButtonDblClick:
                return True

            if object == self.lineEdit():

                if event.type() == QEvent.Type.MouseButtonPress:
                    if self.closeOnLineEditClick:
                        self.hidePopup()
                    else:
                        self.showPopup()
                    return True
                return False
           
            if object == self.view().viewport():
                if event.type() == QEvent.Type.MouseButtonRelease:
                    index = self.view().indexAt(event.pos())
                    item = self.model().item(index.row())
                    if item.checkState() == Qt.CheckState.Checked:
                        item.setCheckState(Qt.CheckState.Unchecked)
                        if index.row() == 0 and self._itemSelectAll:
                            for i in range(self.model().rowCount()):
                                if i != 0:
                                    self.model().item(i).setCheckState(Qt.CheckState.Unchecked)
                        elif index.row() != 0 and self._itemSelectAll:
                            if self.model().item(0).checkState() == Qt.CheckState.Checked:
                                    self.model().item(0).setCheckState(Qt.CheckState.Unchecked)
                    else:
                        item.setCheckState(Qt.CheckState.Checked)
                        if index.row() == 0 and self._itemSelectAll:
                            for i in range(self.model().rowCount()):
                                if i != 0:
                                    self.model().item(i).setCheckState(Qt.CheckState.Checked)
                    self.updateText()
                    return True
            return False

        def updateText(self):
            if self._fixedText.strip():
                text = self._fixedText.strip()
                self.setToolTip("")
            else:
                texts = []
                for i in range(self.model().rowCount()):
                    if self._itemSelectAll and i == 0:
                        pass
                    else:
                        if self.model().item(i).checkState() == Qt.CheckState.Checked:
                            texts.append(self.model().item(i).text())

                text = ", ".join(texts)
                # Divide o texto em palavras
                words = text.split()

                # Reagrupa as palavras em grupos de 4, separados por quebras de linha
                lines = [" ".join(words[i:i + 4]) for i in range(0, len(words), 4)]

                # Junta as linhas com quebras de linha
                formatted_text = "\n".join(lines)

                # Define o tooltip com o texto formatado
                self.setToolTip(formatted_text)


            self.lineEdit().setText(str(text))

        def insertItem(self, index, text, data=None):
            item = QStandardItem()
            item.setText(str(text))
            if data is None:
                item.setData(text)
            else:
                item.setData(data)

            item.setFlags(Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsUserCheckable)
            item.setData(Qt.CheckState.Unchecked, Qt.ItemDataRole.CheckStateRole)

            if self._itemSelectAll:
                if self.model().item(0):
                    if self.model().item(0).checkState() == Qt.CheckState.Checked:
                        item.setCheckState(Qt.CheckState.Checked)

            self.model().insertRow(index,item)

        def addItem(self, *args):
            data = None
            icon = None
            if len(args) == 1:
                text = args[0]
            elif len(args) == 2:
                text = args[0]
                data = args[1]
            elif len(args) == 3:
                icon = args[0]
                text = args[1]
                data = args[2]

            item = QStandardItem()
            item.setText(str(text))
            if data is None:
                item.setData(text)
            else:
                item.setData(data)
            if icon:
                item.setIcon(icon)

            item.setFlags(Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsUserCheckable)
            item.setData(Qt.CheckState.Unchecked, Qt.ItemDataRole.CheckStateRole)

            if self._itemSelectAll:
                if self.model().item(0):
                    if self.model().item(0).checkState() == Qt.CheckState.Checked:
                        item.setCheckState(Qt.CheckState.Checked)

            self.model().appendRow(item)

        def findData(self, data, role = ..., flags = ...):
            for i in range(self.model().rowCount()):
                if self.model().item(i).data() == data:
                    return i
            return -1

        def currentData(self):
            # Return the list of selected items data
            res = []
            for i in range(self.model().rowCount()):
                if self._itemSelectAll and i == 0:
                    pass
                else:
                    if self.model().item(i).checkState() == Qt.CheckState.Checked:
                        res.append(self.model().item(i).data())
            return res


    class QComboBoxUncheck(CustomQComboBox):
        def __init__(self, parent : QWidget = None):
            self.fixedText = ""
            CustomQComboBox.__init__(self, parent)

        def __textChanged(self):
            if self.lineEdit().text != self.fixedText:
                self.lineEdit().setText(str(self.fixedText))
            
        def setFixedText(self, text_fixed: str):
            self.fixedText = text_fixed.strip()
            self.lineEdit().setText(str(self.fixedText))

            self.lineEdit().textChanged.connect(self.__textChanged)
         
        def toggleItem(self, item_text : str):
            ...

        def setToggleItem(self, toggleItem : Callable):
            self.toggleItem = toggleItem
            self.model().dataChanged.connect(self.updateText)
 
        def eventFilter(self, object, event):

            if object == self.lineEdit():
                if event.type() == QEvent.Type.MouseButtonPress:
                    if self.closeOnLineEditClick:
                        self.hidePopup()
                    else:
                        self.showPopup()
                    return True
                return False

            if object == self.view().viewport():
                if event.type() == QEvent.Type.MouseButtonPress:
                    index = self.view().indexAt(event.pos())
                    self.toggleItem(self.itemText(index.row()))
                    return True

            return False

        def updateText(self):
            ...

        def addItem(self, *args):
            data = None
            icon = None
            if len(args) == 1:
                text = args[0]
            elif len(args) == 2:
                text = args[0]
                data = args[1]
            elif len(args) == 3:
                icon = args[0]
                text = args[1]
                data = args[2]

            item = QStandardItem()
            item.setText(str(text))
            if data is None:
                item.setData(text)
            else:
                item.setData(data)
            if icon:
                item.setIcon(icon)

            item.setFlags(Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsUserCheckable)
            item.setData(Qt.CheckState.Checked, Qt.ItemDataRole.CheckStateRole)
            
            self.model().appendRow(item)
            self.lineEdit().setText(str(self.fixedText))

        def findData(self, data, role = ..., flags = ...):
            for i in range(self.model().rowCount()):
                if self.model().item(i).data() == data:
                    return i
            return -1
        
        def currentData(self):
            # Return the list of selected items data
            res = []
            for i in range(self.model().rowCount()):
                if self.model().item(i).checkState() == Qt.CheckState.Checked:
                    res.append(self.model().item(i).data())
            return res
            