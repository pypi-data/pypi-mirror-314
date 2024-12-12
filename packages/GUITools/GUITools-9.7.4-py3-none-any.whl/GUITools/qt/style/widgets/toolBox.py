from .base import BaseWidgetStyleSheet, BaseStyleSheet, BaseColor, BaseProperty
from .text import TextEditStyleSheet, TextBrowserStyleSheet

class ToolBoxStyleSheet(BaseWidgetStyleSheet):
    def __init__(self, prefix=""):
        super().__init__("QToolBox")
        self.tab_hover = self.Tab_hover(prefix)
        self.tab = self.Tab(prefix)
        self.tab_selected = self.Tab_selected(prefix)
        self.tab_selected_hover = self.Tab_selected_hover(prefix)

    class Tab(BaseStyleSheet):
        def __init__(self, prefix=""):
            super().__init__('QToolBox::tab', prefix)
            self.border = BaseProperty.Border(color=BaseColor.division, radius=5)
            self.padding = BaseProperty.Padding(left=5, right=5)
            self.background = BaseProperty.Background(BaseColor.Widget.background)

    class Tab_hover(BaseStyleSheet):
        def __init__(self, prefix=""):
            super().__init__('QToolBox::tab:hover', prefix)
            self.background = BaseProperty.Background(BaseColor.Widget.hover_background)
            self.border = BaseProperty.Border(color=BaseColor.Widget.hover_border)

    class Tab_selected(BaseStyleSheet):
        def __init__(self, prefix=""):
            super().__init__('QToolBox::tab:selected', prefix)
            self.background = BaseProperty.Background(BaseColor.Widget.selected_background)
            self.border = BaseProperty.Border(color=BaseColor.Widget.focus_border)

    class Tab_selected_hover(BaseStyleSheet):
        def __init__(self, prefix=""):
            super().__init__('QToolBox::tab:hover:selected', prefix)
            self.background = BaseProperty.Background(BaseColor.Widget.selected_background)
            self.border = BaseProperty.Border(color=BaseColor.Widget.focus_border)






