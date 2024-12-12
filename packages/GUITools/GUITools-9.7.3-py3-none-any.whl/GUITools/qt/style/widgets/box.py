from .base import BaseWidgetStyleSheet, BaseStyleSheet, BaseColor, BaseProperty
from ..icon import Icons

class BaseBoxStyleSheet(object):
    
    class Box(BaseStyleSheet):
        def __init__(self, class_name : str, prefix : str):
            super().__init__(class_name, prefix)
            self.padding = BaseProperty.Padding(left=0)
            self.background_color = BaseProperty.BackgroundColor(BaseColor.Widget.background)
            self.color = BaseProperty.Color(BaseColor.Reverse.primary)
            self.selection_background_color = BaseProperty.BackgroundColor(BaseColor.Widget.selected_background, 'selection')
            self.selection_color = BaseProperty.Color(BaseColor.Reverse.primary, 'selection')
            self.border = BaseProperty.Border(radius=5, color=BaseColor.Widget.background)
            self.height = BaseProperty.Height(value=24)

    class Hover(BaseStyleSheet):
        def __init__(self, class_name : str, prefix : str):
            super().__init__(f'{class_name}:hover', prefix)
            self.background_color = BaseProperty.BackgroundColor(BaseColor.Widget.hover_background)
            self.border = BaseProperty.Border(color=BaseColor.Widget.hover_border)

    class Focus(BaseStyleSheet):
        def __init__(self, class_name : str, prefix : str):
            super().__init__(f'{class_name}:focus', prefix)
            self.border = BaseProperty.Border(color=BaseColor.Widget.focus_border)

    class HoverFocus(BaseStyleSheet):
        def __init__(self, class_name : str, prefix : str):
            super().__init__(f'{class_name}:hover:focus', prefix)
            self.border = BaseProperty.Border(color=BaseColor.Widget.focus_border)
          
    class Down_button(BaseStyleSheet):
        def __init__(self, class_name : str, prefix : str):
            super().__init__(f'{class_name}::down-button', prefix)
            self.border = BaseProperty.Border(radius=5)
            self.height = BaseProperty.Height(value=6)
            self.padding = BaseProperty.Padding(bottom=3)
            self.image = BaseProperty.Image(Icons.Name.seta_baixo)

    class Up_button(BaseStyleSheet):
        def __init__(self, class_name : str, prefix : str):
            super().__init__(f'{class_name}::up-button', prefix)
            self.border = BaseProperty.Border(radius=5)
            self.height = BaseProperty.Height(value=6)
            self.padding = BaseProperty.Padding(top=3)
            self.image = BaseProperty.Image(Icons.Name.seta_cima)


    class Down_button_hover(BaseStyleSheet):
        def __init__(self, class_name : str, prefix : str):
            super().__init__(f'{class_name}::down-button:hover', prefix)
            self.height = BaseProperty.Height(value=8)
            self.padding = BaseProperty.Padding(bottom=2)
            self.image = BaseProperty.Image(Icons.Name.seta_baixo, Icons.Color.BLUE)

    class Up_button_hover(BaseStyleSheet):
        def __init__(self, class_name : str, prefix : str):
            super().__init__(f'{class_name}::up-button:hover', prefix)
            self.height = BaseProperty.Height(value=8)
            self.padding = BaseProperty.Padding(top=2)
            self.image = BaseProperty.Image(Icons.Name.seta_cima, Icons.Color.BLUE)


class SpinBoxStyleSheet(BaseWidgetStyleSheet):
    def __init__(self, prefix=""):
        super().__init__(f"{prefix} QSpinBox")
        self.spinBox = self.SpinBox(prefix)
        self.hover = self.Hover(prefix)
        self.focus = self.Focus(prefix)
        self.hoverFocus = self.HoverFocus(prefix)
        self.down_button = self.Down_button(prefix)
        self.up_button = self.Up_button(prefix)
        self.down_button_hover = self.Down_button_hover(prefix)
        self.up_button_hover = self.Up_button_hover(prefix)
        
    class SpinBox(BaseBoxStyleSheet.Box):
        def __init__(self, prefix=""):
            super().__init__("QSpinBox", prefix)

    class Hover(BaseBoxStyleSheet.Hover):
        def __init__(self, prefix=""): 
            super().__init__("QSpinBox", prefix)

    class Focus(BaseBoxStyleSheet.Focus):
        def __init__(self, prefix=""):
            super().__init__("QSpinBox", prefix)

    class HoverFocus(BaseBoxStyleSheet.HoverFocus):
        def __init__(self, prefix=""):
            super().__init__("QSpinBox", prefix)
     
    class Down_button(BaseBoxStyleSheet.Down_button):
        def __init__(self, prefix=""):
            super().__init__("QSpinBox", prefix)

    class Up_button(BaseBoxStyleSheet.Up_button):
        def __init__(self, prefix=""):
            super().__init__("QSpinBox", prefix)

    class Down_button_hover(BaseBoxStyleSheet.Down_button_hover):
        def __init__(self, prefix=""):
            super().__init__("QSpinBox", prefix)

    class Up_button_hover(BaseBoxStyleSheet.Up_button_hover):
        def __init__(self, prefix=""):
            super().__init__("QSpinBox", prefix)


class TimeEditStyleSheet(BaseWidgetStyleSheet):
    def __init__(self, prefix=""):
        super().__init__(f"{prefix} QTimeEdit")
        self.timeEdit = self.TimeEdit(prefix)
        self.hover = self.Hover(prefix)
        self.focus = self.Focus(prefix)
        self.hoverFocus = self.HoverFocus(prefix)
        self.down_button = self.Down_button(prefix)
        self.up_button = self.Up_button(prefix)
        self.down_button_hover = self.Down_button_hover(prefix)
        self.up_button_hover = self.Up_button_hover(prefix)
        
    class TimeEdit(BaseBoxStyleSheet.Box):
        def __init__(self, prefix=""):
            super().__init__("QTimeEdit", prefix)

    class Hover(BaseBoxStyleSheet.Hover):
        def __init__(self, prefix=""): 
            super().__init__("QTimeEdit", prefix)

    class Focus(BaseBoxStyleSheet.Focus):
        def __init__(self, prefix=""):
            super().__init__("QTimeEdit", prefix)

    class HoverFocus(BaseBoxStyleSheet.HoverFocus):
        def __init__(self, prefix=""):
            super().__init__("QTimeEdit", prefix)
     
    class Down_button(BaseBoxStyleSheet.Down_button):
        def __init__(self, prefix=""):
            super().__init__("QTimeEdit", prefix)

    class Up_button(BaseBoxStyleSheet.Up_button):
        def __init__(self, prefix=""):
            super().__init__("QTimeEdit", prefix)

    class Down_button_hover(BaseBoxStyleSheet.Down_button_hover):
        def __init__(self, prefix=""):
            super().__init__("QTimeEdit", prefix)

    class Up_button_hover(BaseBoxStyleSheet.Up_button_hover):
        def __init__(self, prefix=""):
            super().__init__("QTimeEdit", prefix)

class DateTimeEditStyleSheet(BaseWidgetStyleSheet):
    def __init__(self, prefix=""):
        super().__init__(f"{prefix} QDateTimeEdit")
        self.dateTimeEdit = self.DateTimeEdit(prefix)
        self.hover = self.Hover(prefix)
        self.focus = self.Focus(prefix)
        self.hoverFocus = self.HoverFocus(prefix)
        self.down_button = self.Down_button(prefix)
        self.up_button = self.Up_button(prefix)
        self.down_button_hover = self.Down_button_hover(prefix)
        self.up_button_hover = self.Up_button_hover(prefix)
        
    class DateTimeEdit(BaseBoxStyleSheet.Box):
        def __init__(self, prefix=""):
            super().__init__("QDateTimeEdit", prefix)

    class Hover(BaseBoxStyleSheet.Hover):
        def __init__(self, prefix=""): 
            super().__init__("QDateTimeEdit", prefix)

    class Focus(BaseBoxStyleSheet.Focus):
        def __init__(self, prefix=""):
            super().__init__("QDateTimeEdit", prefix)

    class HoverFocus(BaseBoxStyleSheet.HoverFocus):
        def __init__(self, prefix=""):
            super().__init__("QDateTimeEdit", prefix)
     
    class Down_button(BaseBoxStyleSheet.Down_button):
        def __init__(self, prefix=""):
            super().__init__("QDateTimeEdit", prefix)

    class Up_button(BaseBoxStyleSheet.Up_button):
        def __init__(self, prefix=""):
            super().__init__("QDateTimeEdit", prefix)

    class Down_button_hover(BaseBoxStyleSheet.Down_button_hover):
        def __init__(self, prefix=""):
            super().__init__("QDateTimeEdit", prefix)

    class Up_button_hover(BaseBoxStyleSheet.Up_button_hover):
        def __init__(self, prefix=""):
            super().__init__("QDateTimeEdit", prefix)


class DoubleSpinBoxStyleSheet(BaseWidgetStyleSheet):
    def __init__(self, prefix=""):
        super().__init__(f"{prefix} QDoubleSpinBox")
        self.doubleSpinBox = self.DoubleSpinBox(prefix)
        self.hover = self.Hover(prefix)
        self.focus = self.Focus(prefix)
        self.hoverFocus = self.HoverFocus(prefix)
        self.down_button = self.Down_button(prefix)
        self.up_button = self.Up_button(prefix)
        self.down_button_hover = self.Down_button_hover(prefix)
        self.up_button_hover = self.Up_button_hover(prefix)
        
    class DoubleSpinBox(BaseBoxStyleSheet.Box):
        def __init__(self, prefix=""):
            super().__init__("QDoubleSpinBox", prefix)

    class Hover(BaseBoxStyleSheet.Hover):
        def __init__(self, prefix=""): 
            super().__init__("QDoubleSpinBox", prefix)

    class Focus(BaseBoxStyleSheet.Focus):
        def __init__(self, prefix=""):
            super().__init__("QDoubleSpinBox", prefix)

    class HoverFocus(BaseBoxStyleSheet.HoverFocus):
        def __init__(self, prefix=""):
            super().__init__("QDoubleSpinBox", prefix)
     
    class Down_button(BaseBoxStyleSheet.Down_button):
        def __init__(self, prefix=""):
            super().__init__("QDoubleSpinBox", prefix)

    class Up_button(BaseBoxStyleSheet.Up_button):
        def __init__(self, prefix=""):
            super().__init__("QDoubleSpinBox", prefix)

    class Down_button_hover(BaseBoxStyleSheet.Down_button_hover):
        def __init__(self, prefix=""):
            super().__init__("QDoubleSpinBox", prefix)

    class Up_button_hover(BaseBoxStyleSheet.Up_button_hover):
        def __init__(self, prefix=""):
            super().__init__("QDoubleSpinBox", prefix)
