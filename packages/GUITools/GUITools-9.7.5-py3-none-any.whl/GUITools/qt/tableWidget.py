# -*- coding: latin -*-

from PyQt6.QtWidgets import (QStyledItemDelegate, QHeaderView, QLabel, QPushButton, QWidget, QDoubleSpinBox, QSpinBox, QCheckBox, QSizePolicy, QAbstractSpinBox, QComboBox,
                             QTableWidget, QApplication, QTableWidgetItem, QTreeWidget, QProgressBar, QLineEdit)
from PyQt6.QtGui import QBrush, QColor
from PyQt6 import QtCore
from PyQt6.QtCore import QSize, Qt
from ..utils import Utils
import numpy as np
from functools import partial
from .comboBox import ComboBox
from .toolButton import ToolButton
import pandas as pd
from PyQt6.QtGui import QIcon, QAction
from time import sleep
from .thread import Thread
from .style import Styles
from typing import TypeVar, overload, Type
from .custom_widgets import CustomWidgets

T = TypeVar('T')

class AlignDelegate(QStyledItemDelegate):
        def initStyleOption(self, option, index):
            super(AlignDelegate, self).initStyleOption(option, index)
            option.displayAlignment = QtCore.Qt.AlignmentFlag.AlignCenter

class QData(object):

        @staticmethod
        def customToolButton(text : str, actions : list[QAction], func : object | None, enabled : bool = True, icon : QIcon = None):
            return {'type': 'QToolButton', 'id': f'QToolButton_{Utils.random_string(10)}', 'text': str(text), 'actions' : actions ,'func' : func, 'enabled': enabled, 'icon': icon}

        @staticmethod
        def pushButton(text : str, func : object | None, enabled : bool = True, icon : QIcon = None, icon_data : Styles.Icons.Data = None,  style : str = None ):
            return {'type': 'QPushButton', 'id': f'QPushButton_{Utils.random_string(10)}', 'text': str(text), 'func' : func, 'enabled': enabled, 'icon' : icon , 'icon_data': icon_data, 'style': style}

        @staticmethod
        def spinBox(func : object | None, minimum : int, value : int = None, maximum : int = None):
            return {'type': 'QSpinBox', 'id': f'QSpinBox_{Utils.random_string(10)}', 'func' : func, 'minimum' : minimum, 'value': value, 'maximum' : maximum}
        
        @staticmethod
        def doubleSpinBox(func : object | None, minimum : float, decimals : int, single_step = 1.00, value : int = None, maximum : int = None):
            return {'type': 'QDoubleSpinBox', 'id': f'QDoubleSpinBox_{Utils.random_string(10)}', 'func' : func, 'minimum' : minimum, 'decimals' : decimals, 'single_step': single_step, 'value': value, 'maximum' : maximum}

        @staticmethod
        def checkbox(text : str, func : object = None, checked : bool = False, toolTip : str | None = ""):
            return {'type': 'QCheckBox', 'id': f'QCheckBox_{Utils.random_string(10)}', 'text': str(text), 'func' : func, 'checked' : checked, 'toolTip': toolTip}

        @staticmethod
        def iconCheckBox(text : str, func : object = None, checked : bool = False, icon : QIcon = None, spacing : int = None):
            return {'type': 'IconQCheckBox', 'id': f'IconQCheckBox_{Utils.random_string(10)}', 'text': str(text), 'func' : func, 'checked' : checked, 'icon': icon, 'spacing' : spacing}

        @staticmethod
        def comboBox(func : object = None, dados : list[str] | ComboBox.DataUpdate = [], index : int = 0):
            return {'type': 'QComboBox', 'id': f'QComboBox_{Utils.random_string(10)}', 'func' : func, 'dados' : dados, 'index' : index}

        @staticmethod
        def comboBoxUncheck(text : str, func : object = None, dados : list[str] = []):
            return {'type': 'ComboBoxUncheck', 'id': f'ComboBoxUncheck_{Utils.random_string(10)}', 'text': str(text), 'func' : func, 'dados' : dados}

        @staticmethod
        def comboBoxCheckable(text : str, func : object = None, dados : list[str] = []):
            return {'type': 'CheckBoxCheckable', 'id': f'CheckBoxCheckable_{Utils.random_string(10)}', 'text': str(text), 'func' : func, 'dados' : dados}
     
        @staticmethod
        def customWidget(func_create_widget : object):
            return {'type': 'QWidget', 'id': f'QWidget_{Utils.random_string(10)}', 'func_create_widget': func_create_widget}


class QDataRow(QData):

    @staticmethod
    def iconLabelpushButton(text,  pushButton_func : object, pushButton_icon_data : Styles.Icons.Data = None, label_icon_data : Styles.Icons.Data = None, icon_size = 16, margins = (0, 0, 0, 0)):
        return {'type': 'IconLabelPushButton', 'id': f'IconLabel_{Utils.random_string(10)}',  'text': str(text), 'pushButton_func': pushButton_func, 'pushButton_icon_data': pushButton_icon_data, 'label_icon_data': label_icon_data, 'icon_size' : icon_size, 'margins': margins}

    @staticmethod
    def iconLabel(text : str, icon : QIcon = None , icon_data : Styles.Icons.Data = None, icon_size = 16, margins = (0, 0, 0, 0)):
        return {'type': 'IconLabel', 'id': f'IconLabel_{Utils.random_string(10)}',  'text': str(text), 'icon': icon, 'icon_data': icon_data, 'icon_size': icon_size, 'margins': margins}

    @staticmethod
    def label(text : str, icon : QIcon = None , icon_size = 16, func_double_click : object = None, cursor_pointer = False, alignment = None , style_sheet = ""):
        return {'type': 'QLabel', 'id': f'QLabel_{Utils.random_string(10)}',  'text': str(text), 'icon': icon, 'icon_size': icon_size, "func_double_click": func_double_click, "cursor_pointer": cursor_pointer, "alignment": alignment, "style_sheet": style_sheet}

    @staticmethod
    def stateLabel(style : str, size : int = 10):
        return {'type': 'StateLabel', 'id': f'StateLabel_{Utils.random_string(10)}',  'style': str(style), 'size': size}

    @staticmethod
    def tableWidgetItem(text : str , alignment = QtCore.Qt.AlignmentFlag.AlignVCenter,  *foreground : int) -> dict[str, tuple | None]:
        return {'type': 'QTableWidgetItem', 'text': str(text), 'alignment': alignment, 'foreground' : foreground if foreground else None}

    @staticmethod
    def lineEdit(text : str, readOnly : bool = False, MaxLength : int = None):
        return {'type' : 'QLineEdit', 'id': f'QLineEdit_{Utils.random_string(10)}', 'text': str(text), 'readOnly' : readOnly, 'MaxLength' : MaxLength }

    @staticmethod
    def progressBar(value = 0, format = ""):
        return {'type': 'QProgressBar', 'id': f'QProgressBar{Utils.random_string(10)}', 'value' : value, 'format': format}


    @staticmethod
    def cellNone():
        return {'type': None}
        

class QDataHeader(QData):

        @staticmethod
        def HeaderItem(text : str, styleSheet : str = "", alignment = QtCore.Qt.AlignmentFlag.AlignLeft, icon : Styles.Icons.Icon = None, icon_size = 16) -> dict[str, tuple | None]:
            return {'type': 'HeaderItem', 'styleSheet' : styleSheet, 'text': str(text), 'alignment': alignment,'icon' : icon, 'icon_size': icon_size}

        @staticmethod
        def HeaderItemFilter(text : str, styleSheet : str = "", alignment = QtCore.Qt.AlignmentFlag.AlignLeft ) -> dict[str, tuple | None]:
            return {'type': 'HeaderItemFilter', 'styleSheet' : styleSheet, 'text': str(text), 'alignment': alignment}
        

class TableModel(QtCore.QAbstractTableModel):

    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data

    def data(self, index, role):
        if role == QtCore.Qt.ItemDataRole.DisplayRole:
            value = self._data.iloc[index.row(), index.column()]
            return str(value)

    def rowCount(self, index):
        return self._data.shape[0]

    def columnCount(self, index):
        return self._data.shape[1]

    def headerData(self, section, orientation, role):
        # section is the index of the column/row.
        if role == QtCore.Qt.ItemDataRole.DisplayRole:
            if orientation == QtCore.Qt.Orientation.Horizontal:
                return str(self._data.columns[section])

            if orientation == QtCore.Qt.Orientation.Vertical:
                return str(self._data.index[section])

class HorizontalHeader(QHeaderView):
    def __init__(self, dataHeaders : list[QDataHeader], parent=None ):
        super(HorizontalHeader, self).__init__(QtCore.Qt.Orientation.Horizontal, parent)
        self.setSectionsMovable(False)
        column_count = parent.columnCount()
        self.itens = []
        if len(dataHeaders) < column_count:
            while len(dataHeaders) < column_count:
                dataHeaders.append(QDataHeader.HeaderItem("", ""))

        self.dataHeaders = dataHeaders
        self.sectionResized.connect(self.handleSectionResized)
        self.sectionMoved.connect(self.handleSectionMoved)
        
        data = pd.DataFrame([
          [i for i in range(column_count)],
        ], columns = ['' for i in range(column_count)], index=[])

        self.setModel(TableModel(data))
        self.setSectionsMovable(False)
        self.setSectionResizeMode(QHeaderView.ResizeMode.Fixed)
       
     
    def cellHeader(self, column : int):
        return self.itens[column] if len(self.itens) > column else None

    def updateComboBoxUncheck(self, column : int, data : list):
        if self.itens:
            item = self.itens[column]
            ComboBox.update(item, data)
        if self.dataHeaders:
            self.dataHeaders[column]['dados'] = data

    def updateComboBoxCheckable(self, column : int, data : list):
        if self.itens:
            item = self.itens[column]
            ComboBox.update(item, data, True)
        if self.dataHeaders:
            self.dataHeaders[column]['dados'] = data

    def updateStyleSheetHeaderItem(self, styleSheet):
        for i, header in enumerate(self.dataHeaders):
            if header['type'] == 'HeaderItemFilter':
                if self.itens:
                  item = self.itens[i]
                  item.setStyleSheet(styleSheet)
                  header['styleSheet'] = styleSheet

    def showEvent(self, event):
        for i in range(self.count()):

            dataHeader = self.dataHeaders[i]
            if i < len(self.itens):
                item = self.itens[i]
            else:
                item = None
                if dataHeader['type'] == 'HeaderItem' or dataHeader['type'] == 'HeaderItemFilter':
                    item = QLabel(self)
                    item.setStyleSheet(dataHeader['styleSheet'] + '''
                        QLabel{ 
                            background-color: 'transparent';
                         }
                     ''')
                    item.setText(dataHeader['text'])
                    if dataHeader['icon'] is not None:
                        icon : Styles.Icons.Icon = dataHeader['icon']
                        item.setPixmap(icon.toPixmap(dataHeader['icon_size']))
                    #item.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum))
                    self.itens.append(item)

                elif dataHeader['type'] == 'QWidget':
                    item = dataHeader['func_create_widget'](parent=self)
                    self.itens.append(item)
  
                elif dataHeader['type'] == 'QPushButton':
                    item = QPushButton(self)
                    item.setText(dataHeader['text'])
                    item.setEnabled(dataHeader['enabled'])
                    if dataHeader['style']:
                        item.setStyleSheet(dataHeader['style'])
                    if dataHeader['func']:
                        item.clicked.connect(dataHeader['func'])
                    if dataHeader['icon_data']:
                        data : Styles.Icons.Data = dataHeader['icon_data']
                        Styles.set_icon_theme(item, data.name, data.hover_name, data.color, data.hover_color )
                    elif dataHeader['icon']:
                        try:
                            item.setIcon(dataHeader['icon'])
                        except:
                            ...

                    self.itens.append(item)

                elif dataHeader['type'] == 'QSpinBox':
                    item = QSpinBox(self)
                    item.setMinimum(dataHeader['minimum'])
                    if dataHeader['func']:
                        item.editingFinished.connect(dataHeader['func'])
                    if dataHeader['maximum'] != None:
                        item.setMaximum(dataHeader['maximum'])
                    if dataHeader['value'] != None:
                        item.setValue(dataHeader['value'])
                    self.itens.append(item)

                elif dataHeader['type'] == 'QDoubleSpinBox':
                    item = QDoubleSpinBox(self)
                    step_type = QAbstractSpinBox.StepType.AdaptiveDecimalStepType
                    item.setStepType(step_type)
                    item.setDecimals(dataHeader['decimals'])
                    item.setMinimum(dataHeader['minimum'])
                    if dataHeader['maximum'] != None:
                         item.setMaximum(dataHeader['maximum'])
                    if dataHeader['func']:
                        item.editingFinished.connect(dataHeader['func'])
                    if dataHeader['value'] != None:
                        item.setValue(dataHeader['value'])
                    self.itens.append(item)

                elif dataHeader['type'] == 'QCheckBox':
                    item = QCheckBox(self)
                    size_policy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding )
                    item.setSizePolicy(size_policy)
                    item.setText(dataHeader['text'])
                    item.setChecked(dataHeader['checked'])
                    if dataHeader['func']:
                        func = partial(dataHeader['func'], item)
                        item.toggled.connect(func)
                    if dataHeader['toolTip'] != None:
                        toolTip : str = dataHeader['toolTip'] 
                        item.setToolTip(toolTip if toolTip.strip() else dataHeader['text'])
                    
                    self.itens.append(item)

                elif dataHeader['type'] == 'IconQCheckBox':
                    item = CustomWidgets.IconCheckBox(dataHeader['text'], dataHeader['icon'] , parent=self, spacing=dataHeader['spacing'])
                    item.checkbox.setChecked(dataHeader['checked'])
                    if dataHeader['func']:
                        func = partial(dataHeader['func'], item)
                        item.checkbox.toggled.connect(func)

                    self.itens.append(item)

                elif dataHeader['type'] == 'ComboBoxUncheck':
                    item = ComboBox.QComboBoxUncheck(self)
                    item.setFixedText(dataHeader['text'])
                    ComboBox.update(item, dataHeader['dados'])
                    ComboBox.ignoreWheelEvent(item)
                    if dataHeader['func']:
                        item.setToggleItem(dataHeader['func'])
                    self.itens.append(item)

                elif dataHeader['type'] == 'CheckBoxCheckable':

                    item = ComboBox.QComboBoxCheckable(self)
                    item.setFixedText(dataHeader['text'])
                    ComboBox.update(item, dataHeader['dados'], True)
                    ComboBox.ignoreWheelEvent(item)
                    if dataHeader['func']:
                        item.setToggleItem(dataHeader['func'])
                    self.itens.append(item)

                elif dataHeader['type'] == 'QComboBox':
                    item = QComboBox(self)
                    ComboBox.update(item, dataHeader['dados'])
                    item.setFocusPolicy(Qt.FocusPolicy.NoFocus)
                    ComboBox.ignoreWheelEvent(item)
                    if dataHeader['dados']:
                        item.setCurrentIndex(dataHeader['index'])
                    if dataHeader['func']:
                        item.activated.connect(partial(dataHeader['func'], combo_box = item))
                    self.itens.append(item)

                item.setGeometry(self.sectionViewportPosition(i), 0, self.sectionSize(i) , self.height())
                item.show()

        if len(self.itens) > self.count():
            for i in range(self.count(), len(self.itens)):
                self.itens[i].deleteLater()

        super(HorizontalHeader, self).showEvent(event)

    def handleSectionResized(self, i = 0):
        if self.itens:
            for i in range(self.count()):
                j = self.visualIndex(i)
                logical = self.logicalIndex(j)
                self.itens[i].setGeometry(self.sectionViewportPosition(logical), 0, self.sectionSize(logical), self.height())

    def handleSectionMoved(self, i, oldVisualIndex, newVisualIndex):
        for i in range(min(oldVisualIndex, newVisualIndex), self.count()):
            logical = self.logicalIndex(i)
            self.itens[i].setGeometry(self.sectionViewportPosition(logical) , 0, self.sectionSize(logical), self.height())
 
    def fixItensPositions(self):
        if self.itens:
            for i in range(self.count()):
                self.itens[i].setGeometry(self.sectionViewportPosition(i) , 0, self.sectionSize(i) , self.height() )


class QDataTable(object):
       
    def __init__(self, tableWidget : QTableWidget ):
        self.array = np.zeros((0, tableWidget.columnCount()), np.dtype(dict))
        self.tableWidget = tableWidget

    @property
    def rowCount(self) -> int:
        return self.array.shape[0]

    @rowCount.setter
    def rowCount(self, value):
        ...
 
    def addRow(self, row : int, column : int, dataRow : QDataRow):
            difference = row - self.array.shape[0] + 1
            if difference > 0:
                for index in range(difference):
                    row_to_be_added = []
                    for i in range(self.array.shape[1]):
                         row_to_be_added.append(QDataRow.cellNone())

                    row_to_be_added = np.array(row_to_be_added)
                    
                    self.array = np.vstack((self.array, row_to_be_added))
                    self.array[row, column] = dataRow
            else:
                self.array[row, column] = dataRow

class QDataTableRow(object):
       
    def __init__(self, tableWidget : QTableWidget, row):
        self.array = np.zeros((0, tableWidget.columnCount()), np.dtype(dict))
        self.row = row
        self.tableWidget = tableWidget

    @property
    def rowCount(self) -> int:
        return self.array.shape[0]

    @rowCount.setter
    def rowCount(self, value):
        ...
 
    def addItem(self, column : int, dataRow : QDataRow):
            difference = 0 - self.array.shape[0] + 1
            if difference > 0:
                for index in range(difference):
                    row_to_be_added = []
                    for i in range(self.array.shape[1]):
                         row_to_be_added.append(QDataRow.cellNone())

                    row_to_be_added = np.array(row_to_be_added)
                    
                    self.array = np.vstack((self.array, row_to_be_added))
                    self.array[0, column] = dataRow
            else:
                self.array[0, column] = dataRow


class TableWidget(object):

    class Headers(object):

        lista = []

        @classmethod
        def update_resize(cls):
            deleted = []
            for h in cls.lista:
                try:
                    h.handleSectionResized()
                except:
                    deleted.append(h)
            for hd in deleted:
                cls.lista.remove(hd)

        @classmethod
        def updateStyleSheetHeaderItem(cls, styleSheet : str):
            for h in cls.lista:
                h.updateStyleSheetHeaderItem(styleSheet)

    def update_resize(tableWidget : QTableWidget):
        tableWidget.resize(QSize(tableWidget.width() - 1, tableWidget.height()))
        tableWidget.resize(QSize(tableWidget.width() + 1, tableWidget.height()))

    def action_toggling_vertical_scroll(tableWidget, action : object):
        total_height = sum(tableWidget.rowHeight(row) for row in range(tableWidget.rowCount()))
        if total_height > tableWidget.viewport().height():
            action(True)
        else:
            action(False)

    def action_toggling_horizontal_scroll(tableWidget, action : object):
        total_width = sum(tableWidget.columnWidth(col) for col in range(tableWidget.columnCount()))
        if total_width > tableWidget.viewport().width():
            action(True)
        else:
            action(False)

  
    class QDataTable(QDataTable):
        ...

    class QDataTableRow(QDataTableRow):
        ...

    class QDataHeader(QDataHeader):
        ...
        
    class QDataRow(QDataRow):
        ...


    class CellWidget:

        @staticmethod
        def update(tableWidget : QTableWidget, data : dict , row : int, column : int, update_resize = True):

            cell = tableWidget.cellWidget(row, column)
            item = tableWidget.item(row, column)
            
            if cell:
                if data['type'] != None:
                        TableWidget.addItem(tableWidget, row, column, data)
                else:
                    tableWidget.removeCellWidget(row, column)

            if item:
                if data['type'] != None:
                    TableWidget.addItem(tableWidget, row, column, data)
                else:
                    tableWidget.takeItem()

            if not cell and not item:
                if data['type'] != None:
                    TableWidget.addItem(tableWidget, row, column, data)

            if update_resize:
                TableWidget.update_resize(tableWidget)

        @overload
        @staticmethod
        def widget(tableWidget : QTableWidget, row : int, column : int) -> QWidget:
            pass

        @overload
        @staticmethod
        def widget(type : Type[T], tableWidget : QTableWidget, row : int, column : int) -> T:
            pass

        def widget(*args):
            index = -1
            if len(args) == 4:
                index = 0
            tableWidget = args[index + 1]
            row = args[index + 2] 
            column = args[index + 3] 
            return tableWidget.cellWidget(row, column)

        @staticmethod
        def enabled(tableWidget : QTableWidget, enabled : bool, ignore_rows : list[int] = [], ignore_column : list[int] = []):
            for column in range(tableWidget.columnCount()):
                if column not in ignore_column:
                    for row in range(tableWidget.rowCount()):
                        if row not in ignore_rows:
                            item = tableWidget.cellWidget(row, column)
                            if item:
                                tableWidget.cellWidget(row, column).setEnabled(enabled)

        @staticmethod
        def enabled_row(tableWidget : QTableWidget, enabled : bool, row : int, ignore_columns : list[int] = []):
            for column in range(tableWidget.columnCount()):
                if column not in ignore_columns:
                    item = tableWidget.cellWidget(row, column)
                    if item:
                        tableWidget.cellWidget(row, column).setEnabled(enabled)

        @staticmethod
        def enabled_column(tableWidget : QTableWidget, enabled : bool, column : int, ignore_rows : list[int] = []):
            for row in range(tableWidget.rowCount()):
                if row not in ignore_rows:
                    item = tableWidget.cellWidget(row, column)
                    if item:
                        tableWidget.cellWidget(row, column).setEnabled(enabled)

        @staticmethod
        def single_selection_chekBox(tableWidget : QTableWidget, current_check_box : QCheckBox, column : int):
            if current_check_box.isChecked():
                for row in range(tableWidget.rowCount()):
                   check_box = TableWidget.CellWidget.widget(QCheckBox, tableWidget, row, column)
                   if check_box:
                       if check_box != current_check_box:
                           if check_box.isChecked():
                               check_box.setChecked(False)


        @staticmethod
        def get_selected_chekBox(tableWidget : QTableWidget, column : int):
            for row in range(tableWidget.rowCount()):
                check_box = TableWidget.CellWidget.widget(QCheckBox, tableWidget, row, column)
                if check_box:
                    if check_box.isChecked():
                        return check_box
            return None

        @classmethod
        def copy_on_cell_double_click(cls, tableWidget : QTableWidget, foreground_color = (73, 145, 246)):
            # Chamada da fun��o para copiar o conte�do da c�lula clicada duas vezes
            tableWidget.cellDoubleClicked.connect(partial(cls.copy_cell_content, tableWidget=tableWidget, foreground_color=foreground_color))

        @staticmethod
        def copy_cell_content(row, column, tableWidget : QTableWidget, foreground_color = (73, 145, 246)):
            # Verifica se a c�lula existe no QTableWidget
            if tableWidget.item(row, column):
                item = tableWidget.item(row, column)
          
                foreground = item.foreground()
                item.setForeground(QColor(*foreground_color))
                content = item.text()

                # Copiar o conte�do da c�lula para a �rea de transfer�ncia
                QApplication.clipboard().setText(content)

                def target():
                    sleep(1)
                    item.setForeground(foreground)
                Thread.new(target)

    @staticmethod
    def alingCenterItems(tableWidget : QTableWidget, list_index : list = [], ResizeModeStretch = True):
        list_index = list_index if list_index else [index for index in range(tableWidget.columnCount())]
        for index in list_index:
            delegate = AlignDelegate(tableWidget)
            tableWidget.setItemDelegateForColumn(index, delegate)
            if ResizeModeStretch:
                tableWidget.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)

    class CellData(object):
        def __init__(self, widget : QWidget | QTableWidgetItem, row : int, column : int):
            self.widget = widget
            self.type = type(widget)
            self.row = row
            self.column = column

    @classmethod
    def get_data_column(cls, tableWidget : QTableWidget, column : int) -> list[CellData | None]:
        data = []
        for row in range(tableWidget.rowCount()):
            item = tableWidget.item(row, column)
            if item:
                data.append(cls.CellData(item, row, column))
            else:
                widget = tableWidget.cellWidget(row, column)
                if widget:
                    data.append(cls.CellData(widget, row, column))
                else:
                    data.append(None)
        return data

    @classmethod
    def get_data_row(cls, tableWidget : QTableWidget, row : int) -> list[CellData | None]:
        data = []
        for column in range(tableWidget.columnCount()):
            item = tableWidget.item(row, column)
            if item:
                data.append(cls.CellData(item, row, column))
            else:
                widget = tableWidget.cellWidget(row, column)
                if widget:
                    data.append(cls.CellData(widget, row, column))
                else:
                    data.append(None)
        return data
  
    class SetHorizontalHeader(object):

        def __init__(self, tableWidget : QTableWidget, dataHeaders : list[QDataHeader]):
            self.tableWidget = tableWidget
            tableWidget.setHorizontalHeader(HorizontalHeader(dataHeaders, tableWidget))
            tableWidget.scrollContentsBy = self.scrollContentsBy
            TableWidget.Headers.lista.append(tableWidget.horizontalHeader())

        def scrollContentsBy(self, dx, dy):
            QTableWidget.scrollContentsBy(self.tableWidget, dx, dy)
            if dx != 0:
                self.tableWidget.horizontalHeader().fixItensPositions()


    class Header(object):

        def __init__(self, tableWidget : QTableWidget | QTreeWidget):
            self.tableWidget = tableWidget
            if isinstance(tableWidget, QTreeWidget):
                 self.horizontalHeader = self.tableWidget.header()
            else:
                self.horizontalHeader = self.tableWidget.horizontalHeader()

        def update_resize(self):
             self.horizontalHeader.handleSectionResized()

        def fixItensPositions(self):
            self.horizontalHeader.fixItensPositions()
          
        def updateComboBoxUncheck(self, column : int, data : list):
            self.horizontalHeader.updateComboBoxUncheck(column, data)

        def updateComboBoxCheckable(self, column : int, data : list):
           self.horizontalHeader.updateComboBoxCheckable(column, data)

        def update_style_HeaderItemFilter(self, column, value):
            label = self.horizontalHeader.cellHeader(column)
            if label:
                style_activsted = '''
                    background-color: #4c94f4;
                    border-radius: 8px;
                    color: rgb(0, 0, 0);
                    font: 10pt "Segoe UI";
                    margin: 3px;
                '''

                style_disabled = '''
                    font: 10pt "Segoe UI";
                    background-color: transparent;
                    color: transparent;
                    margin: 3px;
                '''
          
                if int(value) > 0:
                    label.setStyleSheet(style_activsted)
                else:
                    label.setStyleSheet(style_disabled)

                label.setText(str(value))

        @staticmethod
        def toggle_chekBox_in_table(check_box : QCheckBox, tableWidget : QTableWidget, table_column : int):
            if check_box.text() != "ignore_event":
                chek = check_box.isChecked()
                for row in range(tableWidget.rowCount()):
                    check_box = TableWidget.CellWidget.widget(QCheckBox, tableWidget, row, table_column)
                    if chek != check_box.isChecked():
                        check_box.setChecked(chek)

        @staticmethod
        def toggle_iconChekBox_in_table(icon_check_box : CustomWidgets.IconCheckBox , tableWidget : QTableWidget, table_column : int):
            if icon_check_box.checkbox.text() != "ignore_event":
                chek = icon_check_box.checkbox.isChecked()
                for row in range(tableWidget.rowCount()):
                    icon_check_box = TableWidget.CellWidget.widget(CustomWidgets.IconCheckBox, tableWidget, row, table_column)
                    if chek != icon_check_box.checkbox.isChecked():
                        icon_check_box.checkbox.setChecked(chek)

        @overload
        def widget(self, column : int) -> QWidget:
            pass

        @overload
        def widget(self, type : Type[T], column : int) -> T:
            pass

        def widget(self, *args):
            column = args[0] if len(args) == 1 else args[1]
            return self.horizontalHeader.cellHeader(column)

        def enabled(self, enabled : bool, columns : int | list[int] = None):
            if isinstance(columns, str):
                columns = [columns]
            if not columns:
                columns = list(range(self.tableWidget.columnCount()))
            for col in columns:
                item = self.horizontalHeader.cellHeader(col)
                if item:
                    self.horizontalHeader.cellHeader(col).setEnabled(enabled)
    
    @staticmethod
    def setHorizontalHeaderItem(tableWidget : QTableWidget, column : int, text : str, alignment = QtCore.Qt.AlignmentFlag.AlignVCenter):
        if tableWidget.horizontalHeaderItem(column).text() != str(text):
            tableWidget.setHorizontalHeaderItem(column, QTableWidgetItem(str(text)))
            tableWidget.horizontalHeaderItem(column).setTextAlignment(alignment)
           
    @staticmethod
    def setForegroundItem(item : QTableWidgetItem , *rgb : int):
        item.setForeground(QBrush(QColor(*rgb)))

    @staticmethod
    def setForegroundRow(tableWidget : QTableWidget , row : int , *rgb : int):
        for column in range(tableWidget.columnCount()):
            tableWidget.item(row, column).setForeground(QBrush(QColor(*rgb)))

    @classmethod
    def addItem(cls, tableWidget : QTableWidget, row : int, column : int, dataRow : QDataRow):
            _id = f'id###id{Utils.random_string(10)}'
            if dataRow['type'] == 'QTableWidgetItem':
                new_item = QTableWidgetItem(str(dataRow['text']))
                new_item.setTextAlignment(dataRow['alignment'])
         
                if dataRow['foreground']:
                    cls.setForegroundItem(new_item, *dataRow['foreground'])
                tableWidget.setItem(row, column, new_item)

            elif dataRow['type'] == 'QWidget':
                widget = dataRow['func_create_widget']()
                widget.setObjectName(f"{dataRow['id']}{_id}")
                tableWidget.setCellWidget(row, column, widget)

            elif dataRow['type'] == 'IconLabelPushButton':
                icon_label_pushButton = CustomWidgets.IconLabelPushButton(str(dataRow['text']), dataRow['pushButton_func'], dataRow['pushButton_icon_data'], dataRow['label_icon_data'], dataRow['icon_size'], dataRow['margins'], tableWidget)
                icon_label_pushButton.setObjectName(f"{dataRow['id']}{_id}")
                tableWidget.setCellWidget(row, column, icon_label_pushButton)

            elif dataRow['type'] == 'IconLabel':
                icon_label = CustomWidgets.IconLabel(str(dataRow['text']), dataRow['icon'], dataRow['icon_data'], dataRow['icon_size'], dataRow['margins'], tableWidget)
                icon_label.setObjectName(f"{dataRow['id']}{_id}")
                tableWidget.setCellWidget(row, column, icon_label)

            elif dataRow['type'] == 'StateLabel':
                state_label = CustomWidgets.StateLabel(dataRow['style'], dataRow['size'], tableWidget)
                state_label.setObjectName(f"{dataRow['id']}{_id}")
                tableWidget.setCellWidget(row, column, state_label)

            elif dataRow['type'] == 'QLabel':
                label = CustomWidgets.Label(dataRow['text'] , dataRow['func_double_click'], tableWidget)
                if dataRow['alignment']:
                    label.setAlignment(dataRow['alignment']) 
                if dataRow['icon']:
                    pixmap = dataRow['icon'].pixmap(dataRow['icon_size'], dataRow['icon_size']) 
                    label.setPixmap(pixmap)

                if dataRow['cursor_pointer']:
                    label.setCursor(Qt.CursorShape.PointingHandCursor)

                label.setStyleSheet(f"{dataRow['style_sheet']}; background-color: 'transparent'")
                label.setObjectName(f"{dataRow['id']}{_id}")
                tableWidget.setCellWidget(row, column, label)

            elif dataRow['type'] == 'QToolButton':
                btn = ToolButton(dataRow['text'], dataRow['actions'],tableWidget)
                btn.setObjectName(f"{dataRow['id']}{_id}")
                btn.setEnabled(dataRow['enabled'])
                if dataRow['func']:
                    btn.clicked.connect(dataRow['func'])
                if dataRow['icon']:
                    try:
                        btn.setIcon(dataRow['icon'])
                    except:
                        ...
                tableWidget.setCellWidget(row, column, btn)
        
            elif dataRow['type'] == 'QPushButton':
                btn = QPushButton(dataRow['text'], parent=tableWidget)
                btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
                btn.setObjectName(f"{dataRow['id']}{_id}")
                btn.setEnabled(dataRow['enabled'])
                if dataRow['style']:
                        btn.setStyleSheet(dataRow['style'])
                if dataRow['func']:
                    btn.clicked.connect(dataRow['func'])

                if dataRow['icon_data']:
                    data : Styles.Icons.Data = dataRow['icon_data']
                    Styles.set_icon_theme(btn, data.name, data.hover_name, data.color, data.hover_color)
                elif dataRow['icon']:
                    btn.setIcon(dataRow['icon'])

                tableWidget.setCellWidget(row, column, btn)

            elif dataRow['type'] == 'QSpinBox':
                spinBox = QSpinBox(tableWidget)
                spinBox.setObjectName(f"{dataRow['id']}{_id}")
                spinBox.setMinimum(dataRow['minimum'])
                if dataRow['maximum'] != None:
                    spinBox.setMaximum(dataRow['maximum'])
                if dataRow['func']:
                    spinBox.editingFinished.connect(dataRow['func'])
                if dataRow['value'] != None:
                    spinBox.setValue(dataRow['value'])
                tableWidget.setCellWidget(row, column, spinBox)

            elif dataRow['type'] == 'QDoubleSpinBox':
                dSpinBox = QDoubleSpinBox(tableWidget)
                dSpinBox.setObjectName(f"{dataRow['id']}{_id}")
                step_type = QAbstractSpinBox.StepType.AdaptiveDecimalStepType
                dSpinBox.setStepType(step_type)
                dSpinBox.setDecimals(dataRow['decimals'])
                dSpinBox.setMinimum(dataRow['minimum'])
                dSpinBox.setSingleStep(dataRow['single_step'])
                if dataRow['maximum'] != None:
                    dSpinBox.setMaximum(dataRow['maximum'])
                if dataRow['func']:
                    dSpinBox.editingFinished.connect(dataRow['func'])
                if dataRow['value'] != None:
                    dSpinBox.setValue(dataRow['value'])
                tableWidget.setCellWidget(row, column, dSpinBox)

            elif dataRow['type'] == 'QCheckBox':
                checkBox = QCheckBox(dataRow['text'])
                checkBox.setObjectName(f"{dataRow['id']}{_id}")
                checkBox.setChecked(dataRow['checked'])
                if dataRow['func']:
                    func = partial(dataRow['func'], checkBox)
                    checkBox.toggled.connect(func)
                if dataRow['toolTip'] != None:
                        toolTip : str = dataRow['toolTip'] 
                        checkBox.setToolTip(toolTip if toolTip.strip() else dataRow['text'])
                     
                tableWidget.setCellWidget(row, column, checkBox)

            elif dataRow['type'] == 'IconQCheckBox':
                checkBox = CustomWidgets.IconCheckBox(dataRow['text'], dataRow['icon'], spacing=dataRow['spacing'])
                checkBox.setObjectName(f"{dataRow['id']}{_id}")
                checkBox.checkbox.setChecked(dataRow['checked'])
                if dataRow['func']:
                    func = partial(dataRow['func'], checkBox)
                    checkBox.checkbox.toggled.connect(func)

                tableWidget.setCellWidget(row, column, checkBox)

            elif dataRow['type'] == 'ComboBoxUncheck':
                comboBox = ComboBox.QComboBoxUncheck()
                comboBox.setFocusPolicy(Qt.FocusPolicy.NoFocus)
                comboBox.setObjectName(f"{dataRow['id']}{_id}")
                comboBox.setFixedText(dataRow['text'])
                ComboBox.update(comboBox, dataRow['dados'])
                if dataRow['func']:
                    comboBox.setToggleItem(dataRow['func'])
                tableWidget.setCellWidget(row, column, comboBox)

            elif dataRow['type'] == 'QComboBox':
                comboBox = QComboBox()
                comboBox.setFocusPolicy(Qt.FocusPolicy.NoFocus)
                comboBox.setObjectName(f"{dataRow['id']}{_id}")
                ComboBox.ignoreWheelEvent(comboBox)
                if type(dataRow['dados']) == ComboBox.DataUpdate:
                    ComboBox.update_data(comboBox ,dataRow['dados'])
                else:
                    ComboBox.update(comboBox, dataRow['dados'])
                if dataRow['dados']:
                        comboBox.setCurrentIndex(dataRow['index'])

                if dataRow['func']:
                    comboBox.activated.connect(partial(dataRow['func'], combo_box = comboBox))
                size = QtCore.QSize()
                size.setHeight(15)
                size.setWidth(15)
                comboBox.setIconSize(size)
                tableWidget.setCellWidget(row, column, comboBox)

            elif dataRow['type'] == 'QLineEdit':
                lineEdit = QLineEdit()
                if dataRow['MaxLength']:
                    lineEdit.setMaxLength(dataRow['MaxLength'])
                lineEdit.setObjectName(f"{dataRow['id']}{_id}")
                lineEdit.setReadOnly(dataRow['readOnly'])
                lineEdit.setText(dataRow['text'])
                tableWidget.setCellWidget(row, column, lineEdit)

            elif dataRow['type'] == 'QProgressBar':
                progressBar = QProgressBar(tableWidget)
                progressBar.setValue(dataRow['value'])
                progressBar.setFormat(dataRow['format'])
                tableWidget.setCellWidget(row, column, progressBar)


    @classmethod
    def update(cls, dataTable : QDataTable, force_update = False, update_resize = False):
        tableWidget = dataTable.tableWidget

        if force_update:
            tableWidget.clear()
            tableWidget.setRowCount(0)

        if dataTable.rowCount:

            tableWidget.setRowCount(dataTable.rowCount)
       
            for column in range(tableWidget.columnCount()):
                for row in range(dataTable.rowCount):
                    cell = tableWidget.cellWidget(row, column)
                    item = tableWidget.item(row, column)
                    
                    if cell:
                        new_data = dataTable.array[row, column]
                        if new_data['type'] != None:
                            if str(new_data['id']) != str(cell.objectName().split('id###id')[0]):
                                cls.addItem(tableWidget, row, column, new_data)
                        else:
                            tableWidget.removeCellWidget(row, column)

                    if item:
                        new_data = dataTable.array[row, column]
                        if new_data['type'] != None:
                            if str(new_data['text']) != item.text():
                               cls.addItem(tableWidget, row, column, new_data)
                        else:
                            tableWidget.takeItem(row)

                    if not cell and not item:
                        try:
                            new_data = dataTable.array[row, column]
                            cls.addItem(tableWidget, row, column, new_data)
                        except:
                            ...
        else:
            tableWidget.setRowCount(0)

        if update_resize:
            TableWidget.update_resize(tableWidget)

    @classmethod
    def addDataTable(cls, dataTable : QDataTable, update_resize = False):
        tableWidget = dataTable.tableWidget
        
        if dataTable.rowCount:
            rowCount = tableWidget.rowCount()
            tableWidget.setRowCount(rowCount + dataTable.rowCount)
       
            for column in range(tableWidget.columnCount()):
                for row in range(dataTable.rowCount):
                    try:
                        new_data = dataTable.array[row, column]
                        cls.addItem(tableWidget,row + rowCount, column, new_data)
                    except:
                        ...
        if update_resize:
            TableWidget.update_resize(tableWidget)

    @classmethod
    def insertRow(cls, data_row : QDataTableRow):
        tableWidget = data_row.tableWidget
        tableWidget.insertRow(0)

        if data_row.rowCount:
            for column in range(tableWidget.columnCount()):
                    try:
                        new_data = data_row.array[0, column]
                        cls.addItem(tableWidget,data_row.row, column, new_data)
                    except:
                        ...

    @classmethod
    def toggle_chekBox_in_header(cls, check_box : QCheckBox, tableWidget : QTableWidget, table_column : int, header_column : int):
        header_check_box = cls.Header(tableWidget).widget(QCheckBox, header_column)
        chek = check_box.isChecked()
        text = header_check_box.text()
        header_check_box.setText("ignore_event")
        if not chek:
            if header_check_box.isChecked():
                header_check_box.setChecked(False)
            header_check_box.setText(text)
            return
        result = []
        for row in range(tableWidget.rowCount()):
                check_box = cls.CellWidget.widget(QCheckBox, tableWidget, row, table_column)
                result.append(check_box.isChecked())
        if False not in result:
            if not header_check_box.isChecked():
                header_check_box.setChecked(True)

        header_check_box.setText(text)

    @classmethod
    def toggle_iconChekBox_in_header(cls, icon_check_box : CustomWidgets.IconCheckBox, tableWidget : QTableWidget, table_column : int, header_column : int):
        header_icon_check_box = cls.Header(tableWidget).widget(CustomWidgets.IconCheckBox, header_column)
        header_check_box = header_icon_check_box.checkbox
        chek = icon_check_box.checkbox.isChecked()

        text = header_check_box.text()
        header_check_box.setText("ignore_event")
        if not chek:
            if header_check_box.isChecked():
                header_check_box.setChecked(False)
            header_check_box.setText(text)
            return
        result = []
        for row in range(tableWidget.rowCount()):
                icon_check_box = cls.CellWidget.widget(QCheckBox, tableWidget, row, table_column)
                result.append(icon_check_box.checkbox.isChecked())
        if False not in result:
            if not header_check_box.isChecked():
                header_check_box.setChecked(True)

        header_check_box.setText(text)










    

