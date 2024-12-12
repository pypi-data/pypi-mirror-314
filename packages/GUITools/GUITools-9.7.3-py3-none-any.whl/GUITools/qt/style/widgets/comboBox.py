from .base import BaseWidgetStyleSheet, BaseStyleSheet, BaseColor, BaseProperty
from ..icon import Icons
from .checkBox import CheckBoxStyleCheet
from .listView import ListViewStyleCheet

class ComboBoxStyleCheet(BaseWidgetStyleSheet):
    def __init__(self, prefix=""):
        super().__init__(f"{prefix} QComboBox")
        self.comboBox = self.ComboBox(prefix)
        self.drop_down_on = self.Drop_down_on(prefix)
        self.drop_down_hover = self.Drop_down_hover(prefix)
        self.abstractItemView = self.AbstractItemView(prefix)
        self.hover = self.Hover(prefix)
        self.on = self.On(prefix)
        self.listView = self.ListView(prefix)
        self.checkBox = self.CheckBox(prefix)

    class ComboBox(BaseStyleSheet):
        def __init__(self, prefix=""):
            super().__init__('QComboBox', prefix)
            self.font = BaseProperty.FontSegoeUI(12)
            self.height = BaseProperty.Height(value=25, min=25, max=25)
            self.border = BaseProperty.Border(radius=5, color=BaseColor.Widget.background)
            self.padding = BaseProperty.Padding(left=2)
            self.background_color = BaseProperty.BackgroundColor(BaseColor.Widget.background)
            self.color = BaseProperty.Color(BaseColor.Reverse.primary)
            self.selection_background_color = BaseProperty.BackgroundColor(BaseColor.Widget.selected_background, 'selection')
            self.selection_color = BaseProperty.Color(BaseColor.Reverse.primary, 'selection')

    class Drop_down_on(BaseStyleSheet):
        def __init__(self, prefix=""):
            super().__init__('QComboBox::drop-down:on', prefix)
            self.image = BaseProperty.Image(Icons.Name.seta_baixo, Icons.Color.BLUE)

    class Drop_down_hover(BaseStyleSheet):
        def __init__(self, prefix=""):
            super().__init__('QComboBox::drop-down:hover', prefix)
            self.image = BaseProperty.Image(Icons.Name.seta_baixo, Icons.Color.BLUE)

    class AbstractItemView(BaseStyleSheet):
        def __init__(self, prefix=""):
            super().__init__('QComboBox QAbstractItemView', prefix)
            self.background_color = BaseProperty.BackgroundColor(BaseColor.Widget.background)
            self.border = BaseProperty.Border(color=BaseColor.Widget.focus_border, bottom_left_radius=4, bottom_right_radius=0, top_left_radius=0, top_right_radius=0)

    class Hover(BaseStyleSheet):
        def __init__(self, prefix=""):
            super().__init__('QComboBox:hover', prefix)
            self.border = BaseProperty.Border(color=BaseColor.Widget.hover_border)

    class On(BaseStyleSheet):
        def __init__(self, prefix=""):
            super().__init__('QComboBox:on', prefix)
            self.border = BaseProperty.Border(color=BaseColor.Widget.focus_border, bottom_left_radius=0, bottom_right_radius=0)

    class ListView(ListViewStyleCheet):
        def __init__(self, prefix=""):
            super().__init__(f"{prefix} QComboBox")

    class CheckBox(CheckBoxStyleCheet):
        def __init__(self, prefix=""):
            super().__init__(f"{prefix} QComboBox")
