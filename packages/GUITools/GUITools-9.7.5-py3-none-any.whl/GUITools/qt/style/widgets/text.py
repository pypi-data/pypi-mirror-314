from .base import BaseWidgetStyleSheet, BaseStyleSheet, BaseColor, BaseProperty

class BaseTextStyleSheet(object):
    
    class Text(BaseStyleSheet):
        def __init__(self, class_name : str, border : bool, prefix : str):
            super().__init__(class_name, prefix)
            self.padding = BaseProperty.Padding(left=4)
            self.background_color = BaseProperty.BackgroundColor(BaseColor.Widget.background)
            self.selection_background_color = BaseProperty.BackgroundColor(BaseColor.Widget.selected_background, 'selection')
            self.selection_color = BaseProperty.Color(BaseColor.Reverse.primary, 'selection')
            self.color = BaseProperty.Color(BaseColor.Reverse.primary)
            self.font = BaseProperty.FontSegoeUI(12)
            if border:
                self.border = BaseProperty.Border(radius=5, color='transparent' , style='outset')
            else:
                 self.border = BaseProperty.Border(radius=5, style='outset')

    class Hover(BaseStyleSheet):
        def __init__(self, class_name : str, border : bool, prefix : str):
            super().__init__(f'{class_name}:hover ', prefix)
            if border:
                self.border = BaseProperty.Border(color=BaseColor.Widget.hover_border)

    class HoverFocus(BaseStyleSheet):
        def __init__(self, class_name : str, border : bool, prefix : str):
            super().__init__(f'{class_name}:hover:focus ', prefix)
            if border:
                self.border = BaseProperty.Border(color=BaseColor.Widget.focus_border)

    class Focus(BaseStyleSheet):
        def __init__(self, class_name : str, border : bool, prefix : str):
            super().__init__(f'{class_name}:focus ', prefix)
            if border:
                self.border = BaseProperty.Border(color=BaseColor.Widget.focus_border)

class TextEditStyleSheet(BaseWidgetStyleSheet):
    def __init__(self, *, border=False, prefix=""):
        super().__init__(f"{prefix} QTextEdit")
        self.textEdit = self.TextEdit(border=border, prefix=prefix)
        self.hover = self.Hover(border=border, prefix=prefix)
        self.focus = self.Focus(border=border, prefix=prefix)
        self.hoverFocus = self.HoverFocus(border=border, prefix=prefix)
     
    class TextEdit(BaseTextStyleSheet.Text):
        def __init__(self, *, border=False, prefix=""):
            super().__init__("QTextEdit", border, prefix)

    class Hover(BaseTextStyleSheet.Hover):
        def __init__(self, *, border=False, prefix=""):
            super().__init__("QTextEdit", border, prefix)

    class Focus(BaseTextStyleSheet.Focus):
        def __init__(self, *, border=False, prefix=""):
            super().__init__("QTextEdit", border, prefix)

    class HoverFocus(BaseTextStyleSheet.HoverFocus):
        def __init__(self, *, border=False, prefix=""):
            super().__init__("QTextEdit", border, prefix)


class TextBrowserStyleSheet(BaseWidgetStyleSheet):
    def __init__(self, *, border=False, prefix=""):
        super().__init__(f"{prefix} QTextBrowser")
        self.textBrowser = self.TextBrowser(border=border, prefix=prefix)
        self.hover = self.Hover(border=border, prefix=prefix)
        self.focus = self.Focus(border=border, prefix=prefix)
        self.hoverFocus = self.HoverFocus(border=border, prefix=prefix)
   
    class TextBrowser(BaseTextStyleSheet.Text):
        def __init__(self, *, border=False, prefix=""):
            super().__init__("QTextBrowser", border, prefix)

    class Hover(BaseTextStyleSheet.Hover):
        def __init__(self, *, border=False, prefix=""):
            super().__init__("QTextBrowser", border, prefix)

    class Focus(BaseTextStyleSheet.Focus):
        def __init__(self, *, border=False, prefix=""):
            super().__init__("QTextBrowser", border, prefix)

    class HoverFocus(BaseTextStyleSheet.HoverFocus):
        def __init__(self, *, border=False, prefix=""):
            super().__init__("QTextEdit", border, prefix)
