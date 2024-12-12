from .base import BaseWidgetStyleSheet, BaseStyleSheet, BaseColor, BaseProperty
from ..icon import Icons

class indicatorStyleCheet(BaseWidgetStyleSheet):
    def __init__(self, class_name : str, prefix=""):
        super().__init__(f"{prefix} {class_name}")
        self.widget = self.Widget(class_name, prefix)
        self.indicator = self.Indicator(class_name, prefix)
        self.indicator_hover = self.Indicator_hover(class_name, prefix)
        self.indicator_checked = self.Indicator_checked(class_name,prefix)
        self.indicator_checked_hover = self.Indicator_checked_hover(class_name,prefix)

    class Widget(BaseStyleSheet):
        def __init__(self,class_name : str, prefix=""):
            super().__init__(class_name, prefix)
            self.color = BaseProperty.Color(BaseColor.Reverse.primary)
            self.font = BaseProperty.FontSegoeUI(12)
            self.height = BaseProperty.Height(value=24)

    class Indicator(BaseStyleSheet):
        def __init__(self, class_name : str, prefix=""):
            super().__init__(f'{class_name}::indicator', prefix)
            self.border = BaseProperty.Border(radius=4, color=BaseColor.Widget.hover_border)
            self.width = BaseProperty.Width(value=15)
            self.height = BaseProperty.Height(value=15)
            self.margin = BaseProperty.Margin(top=2)
            self.background = BaseProperty.Background()
            self.add_additional_style('subcontrol-origin: content; subcontrol-position: center left;')
            
    class Indicator_hover(BaseStyleSheet):
        def __init__(self,class_name : str, prefix=""):
            super().__init__(f'{class_name}::indicator:hover', prefix)
            self.border = BaseProperty.Border(color=BaseColor.Widget.focus_border)
            self.background = BaseProperty.Background(BaseColor.Widget.background)

    class Indicator_checked_hover(BaseStyleSheet):
        def __init__(self,class_name : str, prefix=""):
            super().__init__(f'{class_name}::indicator:hover:checked', prefix)
            self.background = BaseProperty.Background(BaseColor.blue.fromRgba(230))
            self.add_additional_style(f"background-image: url(:/{Icons.Name.check_alt});")
           
    class Indicator_checked(BaseStyleSheet):
        def __init__(self,class_name : str, prefix=""):
            super().__init__(f'{class_name}::indicator:checked', prefix)
            self.background = BaseProperty.Background(BaseColor.blue)
            self.add_additional_style(f"background-image: url(:/{Icons.Name.check_alt});")

class CheckBoxStyleCheet(indicatorStyleCheet):
    def __init__(self, prefix=""):
        super().__init__(f"QCheckBox", prefix)
        