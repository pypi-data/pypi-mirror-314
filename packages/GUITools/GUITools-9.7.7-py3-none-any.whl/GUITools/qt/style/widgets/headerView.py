from .base import BaseWidgetStyleSheet, BaseStyleSheet, BaseColor, BaseProperty
from ..icon import Icons
from .comboBox import ComboBoxStyleCheet
from .listView import ListViewStyleCheet

class GlobalVar:
        HeaderView_horizontal_height = 28

class HeaderViewStyleSheet(BaseWidgetStyleSheet):

    def __init__(self, prefix=""):
        super().__init__(f"{prefix} QHeaderView")
        self.section = self.Section(prefix)
        self.frame = self.Frame(prefix)
        self.section_horizontal_pushButton = self.Section_horizontal_pushButton(prefix)
        self.section_horizontal_pushButton_hover = self.Section_horizontal_pushButton_hover(prefix)
        self.section_horizontal_pushButton_pressed = self.Section_horizontal_pushButton_pressed(prefix)
        self.pushButton = self.PushButton(prefix)
        self.poolButton = self.ToolButton(prefix)
        self.section_horizontal = self.Section_horizontal(prefix)
        self.section_horizontal_label = self.Section_horizontal_label(prefix)
        self.section_horizontal_comboBox = self.Section_horizontal_comboBox(prefix)
        self.section_horizontal_listView = self.Section_horizontal_listView(prefix)
        self.section_horizontal_only_one = self.Section_horizontal_only_one(prefix)
        self.section_horizontal_first = self.Section_horizontal_first(prefix)
        self.section_horizontal_last = self.Section_horizontal_last(prefix)
        self.section_vertical = self.Section_vertical(prefix)
        self.section_vertical_only_one = self.Section_vertical_only_one(prefix)
        self.section_vertical_first = self.Section_vertical_first(prefix)
        self.section_vertical_Last = self.Section_vertical_Last(prefix)
        self.down_arrow = self.Down_arrow(prefix)
        self.up_arrow = self.Up_arrow(prefix)

    class Section(BaseStyleSheet):
        def __init__(self, prefix=""):
            super().__init__('QHeaderView:section', prefix)
            self.border = BaseProperty.Border(width=0, color=False)

    class Frame(BaseStyleSheet):
        def __init__(self, prefix=""):
            super().__init__('QHeaderView QFrame', prefix)
            self.background = BaseProperty.Background("transparent")

    class Section_horizontal_pushButton(BaseStyleSheet):
        def __init__(self, prefix=""):
            super().__init__('QHeaderView:section:horizontal QPushButton', prefix)
            self.background_color = BaseProperty.BackgroundColor(BaseColor.primary.fromRgba(100))
            self.border = BaseProperty.Border(radius=2)
            self.margin = BaseProperty.Margin(value=0)
            self.height = BaseProperty.Height(value=GlobalVar.HeaderView_horizontal_height-2)

    class Section_horizontal_pushButton_hover(BaseStyleSheet):
        def __init__(self, prefix=""):
            super().__init__('QHeaderView:section:horizontal QPushButton:hover', prefix)
            self.background_color = BaseProperty.BackgroundColor(BaseColor.primary)

    class Section_horizontal_pushButton_pressed(BaseStyleSheet):
        def __init__(self, prefix=""):
            super().__init__('QHeaderView:section:horizontal QPushButton:pressed', prefix)
            self.background_color = BaseProperty.BackgroundColor(BaseColor.secondary)

    class PushButton(BaseStyleSheet):
        def __init__(self, prefix=""):
            super().__init__('QHeaderView QPushButton', prefix)
            self.border = BaseProperty.Border(radius=2)
            self.margin = BaseProperty.Margin(value=0)

    class ToolButton(BaseStyleSheet):
        def __init__(self, prefix=""):
            super().__init__('QHeaderView QToolButton', prefix)
            self.border = BaseProperty.Border(radius=2)
            self.margin = BaseProperty.Margin(value=0)

    class Section_horizontal(BaseStyleSheet):
        def __init__(self, prefix=""):
            super().__init__('QHeaderView:section:horizontal', prefix)
            self.height = BaseProperty.Height(value=GlobalVar.HeaderView_horizontal_height)
            self.color = BaseProperty.Color(BaseColor.Reverse.primary)
            self.background_color = BaseProperty.BackgroundColor(BaseColor.tertiary)
            self.text_align = BaseProperty.TextAlign('left')

    class Section_horizontal_label(BaseStyleSheet):
        def __init__(self, prefix=""):
            super().__init__('QHeaderView:section:horizontal QLabel', prefix)
            self.border = BaseProperty.Border(radius=5)
            self.color = BaseProperty.Color(BaseColor.Reverse.primary)
            self.background_color = BaseProperty.BackgroundColor(BaseColor.tertiary)
            self.text_align = BaseProperty.TextAlign('left')

    class Section_horizontal_comboBox(ComboBoxStyleCheet):
        def __init__(self, prefix=""):
            super().__init__(f'{prefix} QHeaderView:section:horizontal')
            self.comboBox.border = BaseProperty.Border(radius=2, color=BaseColor.tertiary)
            self.comboBox.background_color = BaseProperty.BackgroundColor(BaseColor.tertiary)
            self.comboBox.height = BaseProperty.Height(value=GlobalVar.HeaderView_horizontal_height-2)
            self.abstractItemView.background_color = BaseProperty.BackgroundColor(BaseColor.tertiary)
            self.on.border = BaseProperty.Border(bottom_left_radius=0, bottom_right_radius=0, color=BaseColor.Widget.focus_border)
            self.hover.border = BaseProperty.Border(color=BaseColor.Widget.hover_border)

    class Section_horizontal_listView(ListViewStyleCheet):
        def __init__(self, prefix=""):
            super().__init__(f'{prefix} QHeaderView:section:horizontal')
    

    class Section_horizontal_only_one(BaseStyleSheet):
        def __init__(self, prefix=""):
            super().__init__('QHeaderView::section:horizontal:only-one', prefix)
            self.height = BaseProperty.Height(value=GlobalVar.HeaderView_horizontal_height)
            self.border = BaseProperty.Border(top_left_radius=5, top_right_radius=5)

    class Section_horizontal_first(BaseStyleSheet):
        def __init__(self, prefix=""):
            super().__init__('QHeaderView::section:horizontal:first', prefix)
            self.border = BaseProperty.Border(top_left_radius=5, top_right_radius=0, bottom_right_radius=0, bottom_left_radius=0)
          
    class Section_horizontal_last(BaseStyleSheet):
        def __init__(self, prefix=""):
            super().__init__('QHeaderView::section:horizontal:last', prefix)
            self.height = BaseProperty.Height(value=GlobalVar.HeaderView_horizontal_height)
            self.border = BaseProperty.Border(top_left_radius=0, top_right_radius=5, bottom_right_radius=0,bottom_left_radius=0)
            
    class Section_vertical(BaseStyleSheet):
        def __init__(self, prefix=""):
            super().__init__('QHeaderView::section:vertical', prefix)
            self.background_color = BaseProperty.BackgroundColor(BaseColor.tertiary)
            self.color = BaseProperty.Color(BaseColor.secondary)
            self.margin = BaseProperty.Margin(left=3, right=3)
            self.width = BaseProperty.Width(value=20)

    class Section_vertical_only_one(BaseStyleSheet):
        def __init__(self, prefix=""):
            super().__init__('QHeaderView::section:vertical:only-one', prefix)
            self.margin = BaseProperty.Margin(top=2, bottom=2)

    class Section_vertical_first(BaseStyleSheet):
        def __init__(self, prefix=""):
            super().__init__('QHeaderView::section:vertical:first', prefix)
            self.margin = BaseProperty.Margin(top=2)

    class Section_vertical_Last(BaseStyleSheet):
        def __init__(self, prefix=""):
            super().__init__('QHeaderView::section:vertical:last', prefix)
            self.margin = BaseProperty.Margin(bottom=2)

    class Down_arrow(BaseStyleSheet):
        def __init__(self, prefix=""):
            super().__init__('QHeaderView::down-arrow', prefix)
            self.height = BaseProperty.Height(value=12)
            self.width = BaseProperty.Width(value=12)
            self.image = BaseProperty.Image(Icons.Name.branch_open)

    class Up_arrow(BaseStyleSheet):
        def __init__(self, prefix=""):
            super().__init__('QHeaderView::up-arrow', prefix)
            self.height = BaseProperty.Height(value=12)
            self.width = BaseProperty.Width(value=12)
            self.image = BaseProperty.Image(Icons.Name.seta_cima)






