from .base import BaseWidgetStyleSheet, BaseStyleSheet, BaseColor, BaseProperty, StyleSheets

class MenuStyleCheet(BaseWidgetStyleSheet):
    def __init__(self, width : int = None, height : int = None, background_color = BaseColor.secondary, prefix=""):
        super().__init__(f"{prefix} QMenu")
        self.base = StyleSheets.BaseStyle("QMenu")
        self.menu = self.Menu(width=width, height=height, background_color=background_color, prefix=prefix)
        self.item = self.Item(prefix)
        self.item_selected = self.Item_selected(prefix)
        self.separator = self.Separator(prefix)
       
    class Menu(BaseStyleSheet):
        def __init__(self,*, width : int = None, height : int = None, background_color = BaseColor.secondary, prefix=""):
            super().__init__('QMenu', prefix)
            self.background_color = BaseProperty.BackgroundColor(background_color)
            self.color = BaseProperty.Color(BaseColor.Reverse.primary)
            self.border = BaseProperty.Border(radius=5, bottom_right_radius=0 ,color=BaseColor.Widget.hover_border)
            self.font = BaseProperty.FontSegoeUI(12)

            if width != None:
                self.width = BaseProperty.Width(value=width, min=width)
            if height != None:
                self.height = BaseProperty.Height(value=height, min=height)

    class Item(BaseStyleSheet):
        def __init__(self, prefix=""):
            super().__init__('QMenu:item', prefix)
            self.padding = BaseProperty.Padding(value=2)
            self.margin = BaseProperty.Margin(value=2)
            self.border = BaseProperty.Border(radius=5, color=BaseColor.secondary)

    class Item_selected(BaseStyleSheet):
        def __init__(self, prefix=""):
            super().__init__('QMenu::item:selected', prefix)
            self.background_color = BaseProperty.BackgroundColor(BaseColor.Button.hover_background)
            self.border = BaseProperty.Border(color=BaseColor.Button.hover_border)

    class Item_hover(BaseStyleSheet):
        def __init__(self, prefix=""):
            super().__init__('QMenu::item:hover', prefix)
            self.background_color = BaseProperty.BackgroundColor(BaseColor.Button.hover_background)
            self.border = BaseProperty.Border(color=BaseColor.Button.hover_border)

    class Separator(BaseStyleSheet):
        def __init__(self, prefix=""):
            super().__init__('QMenu::separator', prefix)
            self.background = BaseProperty.Background(BaseColor.division)
            self.margin = BaseProperty.Margin(left=7, right=7, top=2, bottom=2)
            self.height = BaseProperty.Height(value=1)


