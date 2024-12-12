from .base import BaseWidgetStyleSheet, BaseStyleSheet, BaseColor, BaseProperty

class LineEditStyleCheet(BaseWidgetStyleSheet):
    def __init__(self, prefix="", *, transparent=False, border=True):
        super().__init__(f"{prefix} QLineEdit")
        self.lineEdit = self.LineEdit(transparent=transparent, border=border, prefix=prefix)
        self.hover = self.Hover(border=border, prefix=prefix)
        self.focus = self.Focus(border=border, prefix=prefix)
        self.hoverFocus = self.HoverFocus(border=border, prefix=prefix)
   
    class LineEdit(BaseStyleSheet):
        def __init__(self, *, transparent=False, border=True, prefix=""):
            super().__init__('QLineEdit', prefix)
            self.padding = BaseProperty.Padding(value=0)
            if border:
                self.border = BaseProperty.Border(color=BaseColor.Widget.background)
            else:
                self.border = BaseProperty.Border(width=0, color='transparent')

            self.height =  BaseProperty.Height(value=25)
            self.selection_color = BaseProperty.Color(BaseColor.Reverse.primary, 'selection')
            if transparent:
                self.background_color = BaseProperty.BackgroundColor('transparent')
                self.selection_background_color = BaseProperty.BackgroundColor('transparent', 'selection')
            else:
                self.background_color = BaseProperty.BackgroundColor(BaseColor.Widget.background)
                self.selection_background_color = BaseProperty.BackgroundColor(BaseColor.Widget.selected_background, 'selection')
         
    class Hover(BaseStyleSheet):
        def __init__(self, *, border=True, prefix=""):
            super().__init__('QLineEdit:hover', prefix)
            if border:
                self.border = BaseProperty.Border(color=BaseColor.Widget.hover_border)
            else:
                self.border = BaseProperty.Border(width=0, color='transparent')

    class Focus(BaseStyleSheet):
        def __init__(self, *, border=True, prefix=""):
            super().__init__('QLineEdit:focus', prefix)
            if border:
                self.border = BaseProperty.Border(color=BaseColor.Widget.focus_border)
            else:
                self.border = BaseProperty.Border(width=0, color='transparent')

    class HoverFocus(BaseStyleSheet):
        def __init__(self, *, border=True, prefix=""):
            super().__init__('QLineEdit:hover:focus', prefix)
            if border:
                self.border = BaseProperty.Border(color=BaseColor.Widget.focus_border)
            else:
                self.border = BaseProperty.Border(width=0, color='transparent')

        