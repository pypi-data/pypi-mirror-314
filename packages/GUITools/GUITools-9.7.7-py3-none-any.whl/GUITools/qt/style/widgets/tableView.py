from .base import BaseWidgetStyleSheet, BaseStyleSheet, BaseColor, BaseProperty
from .comboBox import ComboBoxStyleCheet
from .progressBar import ProgressBarStyleSheet
from .lineEdit import LineEditStyleCheet
from .box import DoubleSpinBoxStyleSheet, SpinBoxStyleSheet

class BaseTableView(BaseStyleSheet):
        def __init__(self, class_name : str, prefix=""):
            super().__init__(class_name, prefix)
            self.background_color = BaseProperty.BackgroundColor(BaseColor.table)
            self.gridline_color = BaseProperty.Color(BaseColor.division, 'gridline')
            self.selection_color = BaseProperty.Color('#4c94f4', 'selection')
            self.selection_background_color = BaseProperty.BackgroundColor(BaseColor.table_selection_background, 'selection')
            self.border = BaseProperty.Border(radius=5)
            self.padding = BaseProperty.Padding(value=0)
            self.margin = BaseProperty.Margin(value=0)

class TableViewStyleSheet(BaseWidgetStyleSheet):
    def __init__(self,  prefix=""):
        super().__init__(f"{prefix} QTableView")
        self.tableView = self.TableView(prefix)
        self.tableWidgetItem = self.TableWidgetItem(prefix)
        self.itemFocus = self.ItemFocus(prefix)
        self.itemHover = self.ItemHover(prefix)
        self.itemSelected = self.ItemSelected(prefix)
        self.itemAlternate = self.ItemAlternate(prefix)
        self.itemAlternateHover = self.ItemAlternateHover()
        self.itemAlternateSelectedHover = self.ItemAlternateSelectedHover()
        self.progressBar = self.ProgressBar(prefix)
        self.label = self.Label(prefix)
        self.comboBox = self.ComboBox(prefix)
        self.comboBox_abstractItemView = self.ComboBox_abstractItemView(prefix)
        self.comboBox_on = self.ComboBox_on(prefix)
        self.comboBox_hover = self.ComboBox_hover(prefix)
        self.checkBox = self.CheckBox(prefix)
        self.lineEdit = self.LineEdit(prefix)
        self.pushButton = self.PushButton(prefix)
        self.toolButton = self.ToolButton(prefix)
        self.spinBox = self.SpinBox(prefix)
        self.doubleSpinBox = self.DoubleSpinBox(prefix)
      
    class TableView(BaseTableView):
        def __init__(self, prefix=""):
            super().__init__('QTableView', prefix)
            self.add_additional_style('border-collapse: collapse;')

    class ItemAlternate(BaseStyleSheet):
        def __init__(self, prefix=""):
            super().__init__('QTableWidget::item:alternate', prefix)
            self.background_color = BaseProperty.BackgroundColor(BaseColor.table_alternate)
  
    class ItemFocus(BaseStyleSheet):
        def __init__(self, prefix=""):
            super().__init__('QTableWidget::item:focus', prefix)
            self.background_color = BaseProperty.BackgroundColor(BaseColor.table_selection_background)

    class ItemSelected(BaseStyleSheet):
        def __init__(self, prefix=""):
            super().__init__('QTableWidget::item:selected', prefix)
            self.background_color = BaseProperty.BackgroundColor(BaseColor.table_selection_background)

    class ItemAlternateHover(BaseStyleSheet):
        def __init__(self, prefix=""):
            super().__init__('QTableWidget::item:alternate:hover', prefix)
            self.background_color = BaseProperty.BackgroundColor(BaseColor.table_alternate)

    class ItemAlternateSelectedHover(BaseStyleSheet):
        def __init__(self, prefix=""):
            super().__init__('QTableWidget::item:alternate:selected:hover', prefix)
            self.background_color = BaseProperty.BackgroundColor(BaseColor.table_selection_background)

    class ItemHover(BaseStyleSheet):
        def __init__(self, prefix=""):
            super().__init__('QTableWidget::item:hover', prefix)
            self.background_color = BaseProperty.BackgroundColor("transparent")

    class TableWidgetItem(BaseStyleSheet):
        def __init__(self, prefix=""):
            super().__init__('QTableWidgetItem', prefix)
            self.margin = BaseProperty.Margin(value=0)
            self.padding = BaseProperty.Padding(value=0)
            self.background_color = BaseProperty.BackgroundColor("transparent")

    class ProgressBar(ProgressBarStyleSheet.ProgressBar):
        def __init__(self, prefix=""):
            super().__init__(f"{prefix} QTableView")
            self.height = BaseProperty.Height(max=10)
            self.margin = BaseProperty.Margin(value=5, top=10)
            self.background_color = BaseProperty.BackgroundColor("transparent")

    class Label(BaseStyleSheet):
        def __init__(self, prefix=""):
            super().__init__('QLabel', f"{prefix} QTableView")
            self.background_color = BaseProperty.BackgroundColor("transparent")
            self.padding = BaseProperty.Padding(left=5)

    class ComboBox(ComboBoxStyleCheet.ComboBox):
        def __init__(self, prefix=""):
            super().__init__(f"{prefix} QTableView")
            self.background_color = BaseProperty.BackgroundColor("transparent")
            self.border.color = "transparent"
            self.border.radius=0
            self.margin = BaseProperty.Margin(value=0)
            self.height = BaseProperty.Height(value=27, max=27)

    class ComboBox_abstractItemView(ComboBoxStyleCheet.AbstractItemView):
        def __init__(self, prefix=""):
            super().__init__(f"{prefix} QTableView")
            self.background_color = BaseProperty.BackgroundColor(BaseColor.table)
     

    class ComboBox_on(ComboBoxStyleCheet.On):
        def __init__(self, prefix=""):
            super().__init__(f"{prefix} QTableView")
            self.border.color = BaseColor.Widget.focus_border

    class ComboBox_hover(ComboBoxStyleCheet.Hover):
        def __init__(self, prefix=""):
            super().__init__(f"{prefix} QTableView")
            self.border.color = BaseColor.Widget.hover_border

    class CheckBox(BaseStyleSheet):
        def __init__(self, prefix=""):
            super().__init__('QCheckBox', f"{prefix} QTableView")
            self.background_color = BaseProperty.BackgroundColor("transparent")
            self.margin = BaseProperty.Margin(left=5, right=5)

    class PushButton(BaseStyleSheet):
        def __init__(self, prefix=""):
            super().__init__('QPushButton', f"{prefix} QTableView")
            self.border = BaseProperty.Border(radius=2)
            self.margin = BaseProperty.Margin(value=2)

    class ToolButton(BaseStyleSheet):
        def __init__(self, prefix=""):
            super().__init__('QToolButton', f"{prefix} QTableView")
            self.border = BaseProperty.Border(radius=2)
            self.margin = BaseProperty.Margin(value=2)

    class LineEdit(LineEditStyleCheet):
         def __init__(self, prefix=""):
            super().__init__(prefix=f'{prefix} QTableView')
            self.lineEdit.border.radius = 0
            self.lineEdit.padding = BaseProperty.Padding(left=5, right=5)
            self.lineEdit.height = BaseProperty.Height(value=28, max=28)
            self.hover.border.radius = 0
            self.focus.border.radius = 0

    class SpinBox(SpinBoxStyleSheet):
         def __init__(self, prefix=""):
            super().__init__(prefix=f'{prefix} QTableView')
            self.spinBox.border.radius = 0
            self.hover.border.radius = 0
            self.focus.border.radius = 0

    class DoubleSpinBox(DoubleSpinBoxStyleSheet):
         def __init__(self, prefix=""):
            super().__init__(prefix=f'{prefix} QTableView')
            self.doubleSpinBox.border.radius = 0
            self.hover.border.radius = 0
            self.focus.border.radius = 0
            

         