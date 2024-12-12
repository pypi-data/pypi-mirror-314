from .base import BaseWidgetStyleSheet, BaseStyleSheet, BaseColor, BaseProperty
from .comboBox import ComboBoxStyleCheet
from .scrollBar import ScrollBarStyleSheet
from .progressBar import ProgressBarStyleSheet
from .lineEdit import LineEditStyleCheet
from ..icon import Icons
from .checkBox import indicatorStyleCheet
from ..utils import TypeTheme, Global

class BaseTreeView(BaseStyleSheet):
        def __init__(self, class_name : str, prefix=""):
            super().__init__(class_name, prefix)
            self.font = BaseProperty.FontSegoeUI(12)
            self.border = BaseProperty.Border(radius=5)
            self.padding = BaseProperty.Padding(value=0)
            self.margin = BaseProperty.Margin(value=0)

class TreeViewStyleSheet(BaseWidgetStyleSheet):
    def __init__(self, prefix=""): 
        super().__init__(f"{prefix} QTreeView")
        self.widgetAction = self.WidgetAction(prefix)
        self.treeView = self.TreeView(prefix)
        self.itemOpen = self.ItemOpen(prefix)
        self.itemSelected = self.ItemSelected(prefix)

        #self.branchHasSiblingsNotAdjoinsItem = self.BranchHasSiblingsNotAdjoinsItem()
        #self.branchHasSiblingsAdjoinsItem = self.BranchHasSiblingsAdjoinsItem()
        #self.branchHasNotSiblingsAdjoinsItem = self.BranchHasNotSiblingsAdjoinsItem()
        self.branchHasChildrenNotHasSiblingsClosed = self.BranchHasChildrenNotHasSiblingsClosed()
        self.branchClosedHasChildrenHasSiblings = self.BranchClosedHasChildrenHasSiblings()
        self.branchOpenHasChildrenNotHasSiblings = self.BranchOpenHasChildrenNotHasSiblings()
        self.branchOpenHasChildrenHasSiblings = self.BranchOpenHasChildrenHasSiblings()

        self.progressBar = self.ProgressBar(prefix)
        self.label = self.Label(prefix)
        self.comboBox = self.ComboBox(prefix)
        self.comboBox_abstractItemView = self.ComboBox_abstractItemView(prefix)
        self.comboBox_on = self.ComboBox_on(prefix)
        self.comboBox_hover = self.ComboBox_hover(prefix)

        self.indicator = self.Indicator(prefix)
        self.lineEdit = self.LineEdit(prefix)
        self.pushButton = self.PushButton(prefix)
        self.toolButton = self.ToolButton(prefix)
        self.lineEdit = self.LineEdit(prefix)

        self.treeWidget = self.TreeWidget()
        self.item = self.Item(prefix)
        self.itemSelected = self.ItemSelected(prefix)
        self.itemFocus = self.ItemFocus(prefix)
        self.itemHover = self.ItemHover(prefix)
        self.itemSelectedHover = self.ItemSelectedHover(prefix)
        self.itemNotselected = self.ItemNotselected(prefix)
        self.itemNotselectedHover = self.ItemNotselectedHover(prefix)
        
    class Item(BaseStyleSheet):
        def __init__(self, prefix=""):
            super().__init__('QTreeWidget::item', prefix)
            self.background_color = BaseProperty.Background(BaseColor.table)
            self.color = BaseProperty.Color(value=BaseColor.Reverse.primary)

    class ItemNotselected(BaseStyleSheet):
         def __init__(self, prefix=""):
            super().__init__('QTreeWidget::item:!selected', f"{prefix}")
            self.background_color = BaseProperty.Background(BaseColor.table)
            self.color = BaseProperty.Color(value=BaseColor.Reverse.primary)

    class ItemNotselectedHover(BaseStyleSheet):
         def __init__(self, prefix=""):
            super().__init__('QTreeWidget::item:!selected:hover', f"{prefix}")
            self.background_color = BaseProperty.Background(BaseColor.table_alternate)

    class ItemFocus(BaseStyleSheet):
        def __init__(self, prefix=""):
            super().__init__('QTreeWidget::item:focus', prefix)
            self.background_color = BaseProperty.Background(BaseColor.table_selection_background)

    class ItemHover(BaseStyleSheet):
        def __init__(self, prefix=""):
            super().__init__('QTreeWidget::item:hover', prefix)
            self.background_color = BaseProperty.Background(BaseColor.table_alternate)

    class ItemSelectedHover(BaseStyleSheet):
        def __init__(self, prefix=""):
            super().__init__('QTreeWidget::item:selected:hover', prefix)
            self.background_color = BaseProperty.Background(BaseColor.table_selection_background)

    class WidgetAction(BaseTreeView):
        def __init__(self, prefix=""):
            super().__init__('QTreeWidget QWidgetAction', prefix)

    class TreeWidget(BaseTreeView):
        def __init__(self, prefix=""):
            super().__init__('QTreeWidget', prefix)
            self.background_color = BaseProperty.BackgroundColor(BaseColor.table)

    class TreeView(BaseTreeView):
        def __init__(self, prefix=""):
            super().__init__('QTreeView', prefix)
            self.background_color = BaseProperty.BackgroundColor(BaseColor.table)

    class ItemOpen(BaseStyleSheet):
        def __init__(self, prefix=""):
            super().__init__('QTreeView:item:open', prefix)
            self.color = BaseProperty.Color(value=BaseColor.Reverse.selected)

    class ItemSelected(BaseStyleSheet):
        def __init__(self, prefix=""):
            super().__init__('QTreeView:item:selected', prefix)
            self.background_color = BaseProperty.BackgroundColor(BaseColor.table_selection_background)
            self.color = BaseProperty.Color(value=BaseColor.Reverse.selected)

    class ProgressBar(ProgressBarStyleSheet.ProgressBar):
        def __init__(self, prefix=""):
            super().__init__(f"{prefix} QTreeView")
            self.height = BaseProperty.Height(max=10)
            self.margin = BaseProperty.Margin(value=5, top=10)

    class Label(BaseStyleSheet):
        def __init__(self, prefix=""):
            super().__init__('QLabel', f"{prefix} QTreeView")
            self.background_color = BaseProperty.BackgroundColor("transparent")
            self.padding = BaseProperty.Padding(left=5)

    class ComboBox(ComboBoxStyleCheet.ComboBox):
        def __init__(self, prefix=""):
            super().__init__(f"{prefix} QTreeView")
            self.background_color = BaseProperty.BackgroundColor("transparent")
            self.border.color = "transparent"
            self.border.radius=0
            self.margin = BaseProperty.Margin(value=0)
            self.height = BaseProperty.Height(value=27, max=27)

    class ComboBox_abstractItemView(ComboBoxStyleCheet.AbstractItemView):
        def __init__(self, prefix=""):
            super().__init__(f"{prefix} QTreeView")
            self.background_color = BaseProperty.BackgroundColor(BaseColor.table)

    class ComboBox_on(ComboBoxStyleCheet.On):
        def __init__(self, prefix=""):
            super().__init__(f"{prefix} QTreeView")
            self.border.color = BaseColor.Widget.focus_border

    class ComboBox_hover(ComboBoxStyleCheet.Hover):
        def __init__(self, prefix=""):
            super().__init__(f"{prefix} QTreeView")
            self.border.color = BaseColor.Widget.hover_border

    class Indicator(indicatorStyleCheet):
        def __init__(self, prefix=""):
            super().__init__("QTreeView", prefix)

    class LineEdit(BaseStyleSheet):
        def __init__(self, prefix=""):
            super().__init__('QLineEdit', f"{prefix} QTreeView")
            self.border = BaseProperty.Border(radius=0)
            self.padding = BaseProperty.Padding(left=5, right=5)
            self.height = BaseProperty.Height(value=28, max=28)

    class PushButton(BaseStyleSheet):
        def __init__(self, prefix=""):
            super().__init__('QPushButton', f"{prefix} QTreeView")
            self.border = BaseProperty.Border(radius=2)
            self.margin = BaseProperty.Margin(value=2)

    class ToolButton(BaseStyleSheet):
        def __init__(self, prefix=""):
            super().__init__('QToolButton', f"{prefix} QTreeView")
            self.border = BaseProperty.Border(radius=2)
            self.margin = BaseProperty.Margin(value=2)
            self.height = BaseProperty.Height(value=24, max=24)

    class LineEdit(LineEditStyleCheet.LineEdit):
         def __init__(self, prefix=""):
            super().__init__(prefix=f'{prefix} QTreeView')
            self.border.radius = 0
            self.background_color.value = 'transparent'

    class BranchHasSiblingsNotAdjoinsItem(BaseStyleSheet):
            def __init__(self, prefix=""):
                super().__init__('QTreeView::branch:has-siblings:!adjoins-item', prefix)
                self.image = f'border-image: url(:/{Icons.Name.add_suffix_theme(Icons.Name.vline)}) 0;'
               
    class BranchHasSiblingsAdjoinsItem(BaseStyleSheet):
        def __init__(self, prefix=""):
            super().__init__('QTreeView::branch:has-siblings:adjoins-item', prefix)
            self.image = f'border-image: url(:/{Icons.Name.add_suffix_theme(Icons.Name.vline)}) 0;'
           
    class BranchHasNotSiblingsAdjoinsItem(BaseStyleSheet):
        def __init__(self, prefix=""):
            super().__init__('QTreeView::branch:!has-children:!has-siblings:adjoins-item', prefix)
            self.image = f'border-image: url(:/{Icons.Name.add_suffix_theme(Icons.Name.branch_end)}) 0;'
            
    class BranchHasChildrenNotHasSiblingsClosed(BaseStyleSheet):
        def __init__(self, prefix=""):
            super().__init__('QTreeView::branch:has-children:!has-siblings:closed', prefix)
            self.image = BaseProperty.Image(Icons.Name.branch_closed) 
            self.add_additional_style("border-image: none;")

    class BranchClosedHasChildrenHasSiblings(BaseStyleSheet):
        def __init__(self, prefix=""):
            super().__init__('QTreeView::branch:closed:has-children:has-siblings', prefix)
            self.image = BaseProperty.Image(Icons.Name.branch_closed) 
            self.add_additional_style("border-image: none;")

    class BranchOpenHasChildrenNotHasSiblings(BaseStyleSheet):
        def __init__(self, prefix=""):
            super().__init__('QTreeView::branch:open:has-children:!has-siblings', prefix)
            self.image = BaseProperty.Image(Icons.Name.branch_open) 
            self.add_additional_style("border-image: none;")

    class BranchOpenHasChildrenHasSiblings(BaseStyleSheet):
        def __init__(self, prefix=""):
            super().__init__('QTreeView::branch:open:has-children:has-siblings', prefix)
            self.image = BaseProperty.Image(Icons.Name.branch_open) 
            self.add_additional_style("border-image: none;")

    



