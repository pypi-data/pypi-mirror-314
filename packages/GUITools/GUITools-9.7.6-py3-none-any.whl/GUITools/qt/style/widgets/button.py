from .base import BaseWidgetStyleSheet, BaseStyleSheet, BaseColor, BaseProperty

class ButtonMenuStyleSheet(BaseWidgetStyleSheet):
     def __init__(self, *, transparent=True, selected=False, padding=True, height=36, prefix=""):
        super().__init__(f"{prefix} QPushButton")
        self.button = self.Button(transparent=transparent, selected=selected, padding=padding, height=height, prefix=prefix)
        self.hover = self.Hover(selected=selected, prefix=prefix)
        self.pressed = self.Pressed(selected=selected, prefix=prefix)
        
     class Button(BaseStyleSheet):
        def __init__(self, *, height=36, transparent=True, selected=False, padding=True, prefix=""):
            super().__init__('QPushButton', prefix)
            self.padding = BaseProperty.Padding(left=9, right=9) if padding else None
            self.text_align = BaseProperty.TextAlign('left')
            self.border = BaseProperty.Border(radius=6, color='transparent')
            self.font = BaseProperty.FontSegoeUI(12)
            if transparent:
                self.background_color = BaseProperty.BackgroundColor('transparent')
            else:
                self.background_color = BaseProperty.BackgroundColor(BaseColor.primary)
            if selected:
                self.color = BaseProperty.Color("#4c94f4")
                self.background_color = BaseProperty.BackgroundColor(BaseColor.Menu.Button.hover_background.rgba)
                self.border = BaseProperty.Border(radius=6, color=BaseColor.Menu.Button.hover_border.rgba)
            else:
                self.color = BaseProperty.Color(BaseColor.Reverse.primary)
            self.height = BaseProperty.Height(value=height)

     class Hover(BaseStyleSheet):
         def __init__(self, *, selected=False, prefix=""):
            super().__init__('QPushButton:hover', prefix)
            if selected:
                self.background_color = BaseProperty.BackgroundColor(BaseColor.Menu.Button.hover_background.rgba)
                self.border = BaseProperty.Border(color=BaseColor.Menu.Button.hover_border)
            else:
                self.background_color = BaseProperty.BackgroundColor(BaseColor.Menu.Button.pressed_background.rgba)
                self.border = BaseProperty.Border(color=BaseColor.Menu.Button.pressed_border)

     class Pressed(BaseStyleSheet):
         def __init__(self, *, selected=False, prefix=""):
            super().__init__('QPushButton:pressed', prefix)
            if selected:
                self.background_color = BaseProperty.BackgroundColor(BaseColor.Menu.Button.hover_background.rgba)
                self.border = BaseProperty.Border(color=BaseColor.Menu.Button.hover_border)
            else:
                self.background_color = BaseProperty.BackgroundColor(BaseColor.Menu.Button.pressed_background.fromRgba(200))
                self.border = BaseProperty.Border(color=BaseColor.Menu.Button.pressed_border.fromRgba(200))


class ButtonStyleSheet(BaseWidgetStyleSheet):
     def __init__(self, *, transparent=False, hover=True, selected=False, height=25,  prefix=""):
        super().__init__("QPushButton")
        self.button = self.Button(transparent=transparent, selected=selected, height=height, prefix=prefix)
        self.hover = self.Hover(transparent=transparent, hover=hover, selected=selected, prefix=prefix)
        self.pressed = self.Pressed(transparent=transparent, hover=hover, prefix=prefix)
        self.disabled = self.Disabled(transparent=transparent, selected=selected, prefix=prefix)
        self.checked = self.Checked(selected=selected, prefix=prefix)
        self.checkedHover = self.CheckedHover(selected=selected, prefix=prefix)

     class Button(BaseStyleSheet):
          def __init__(self, *, height=25, transparent=False, selected=False, prefix=""):
               super().__init__('QPushButton', prefix)
               self.padding = BaseProperty.Padding(left=3, right=3)
               self.color = BaseProperty.Color(BaseColor.Reverse.primary)
               self.height = BaseProperty.Height(value=height)
               self.margin = BaseProperty.Margin(value=0)
               if transparent:
                   self.border = BaseProperty.Border(radius=5, color='transparent')
                   self.background_color = BaseProperty.BackgroundColor('transparent')
               else:
                   if selected:
                       self.background_color = BaseProperty.BackgroundColor(BaseColor.Button.hover_background.fromRgba(200))
                       self.border = BaseProperty.Border(radius=5, color=BaseColor.Button.hover_background.fromRgba(200))
                       self.color = BaseProperty.Color('#4c94f4')
                   else:
                       self.background_color = BaseProperty.BackgroundColor(BaseColor.Button.background.rgba)
                       self.border = BaseProperty.Border(radius=5, color=BaseColor.Button.background.rgba)

     class Checked(BaseStyleSheet):
        def __init__(self, *, selected=False, prefix=""):
            super().__init__('QPushButton:checked ', prefix)
            if selected:
                self.background_color = BaseProperty.BackgroundColor(BaseColor.Menu.Button.hover_background.rgba)
                self.border = BaseProperty.Border(color=BaseColor.Menu.Button.hover_border)
            else:
                self.background_color = BaseProperty.BackgroundColor(BaseColor.Menu.Button.pressed_background.fromRgba(200))
                self.border = BaseProperty.Border(color=BaseColor.Menu.Button.pressed_border.fromRgba(200))

     class CheckedHover(BaseStyleSheet):
        def __init__(self, *, selected=False, prefix=""):
            super().__init__('QPushButton:checked:hover', prefix)
            if selected:
                self.background_color = BaseProperty.BackgroundColor(BaseColor.Menu.Button.hover_background.rgba)
                self.border = BaseProperty.Border(color=BaseColor.Menu.Button.hover_border)
            else:
                self.background_color = BaseProperty.BackgroundColor(BaseColor.Menu.Button.pressed_background.fromRgba(200))
                self.border = BaseProperty.Border(color=BaseColor.Menu.Button.pressed_border.fromRgba(200))


     class Hover(BaseStyleSheet):
         def __init__(self, *, transparent=False, hover=True, selected=False, prefix=""):
               super().__init__('QPushButton:hover', prefix)

               if hover or not transparent:
                   if selected:
                       self.background_color = BaseProperty.BackgroundColor(BaseColor.Button.hover_background.fromRgba(200))
                       self.border = BaseProperty.Border(color=BaseColor.Button.hover_border.fromRgba(200))
                   else:
                        self.background_color = BaseProperty.BackgroundColor(BaseColor.Button.hover_background.rgba)
                        self.border = BaseProperty.Border(color=BaseColor.Button.hover_border.rgba)
               else:
                   self.border = BaseProperty.Border(color='transparent')

     class Pressed(BaseStyleSheet):
         def __init__(self, *, transparent=False, hover=True, prefix=""):
               super().__init__('QPushButton:pressed', prefix)
               if hover or not transparent:
                    self.background_color = BaseProperty.BackgroundColor(BaseColor.Button.pressed_background.rgba)
                    self.border = BaseProperty.Border(color=BaseColor.Button.pressed_border.rgba)
               else:
                   self.border = BaseProperty.Border(color='transparent')
           
     class Disabled(BaseStyleSheet):
         def __init__(self, *, transparent=False, selected=False, prefix=""):
               super().__init__('QPushButton:disabled', prefix)

               self.color = BaseProperty.Color(BaseColor.Reverse.primary.fromRgba(200))

               if transparent:
                   self.border = BaseProperty.Border(color='transparent')
                   self.background_color = BaseProperty.BackgroundColor('transparent')
               else:
                   if selected:
                       self.background_color = BaseProperty.BackgroundColor(BaseColor.Button.background.fromRgba(150))
                       self.border = BaseProperty.Border(color=BaseColor.Button.background.fromRgba(150))
                   else:
                       self.background_color = BaseProperty.BackgroundColor(BaseColor.Button.background.fromRgba(100))
                       self.border = BaseProperty.Border(color=BaseColor.Button.background.fromRgba(100))
             
    
class ButtonCopyStyleSheet(BaseWidgetStyleSheet):
     def __init__(self, *, transparent=False, height=25, prefix=""):
        super().__init__(f"{prefix} QPushButton")
        self.button = self.Button(transparent=transparent, selected=False, height=height, prefix=prefix)
        self.hover = self.Hover(transparent=transparent, hover=True, selected=False, prefix=prefix)
        self.pressed = self.Pressed(transparent=transparent, prefix=prefix)
        self.disabled = self.Disabled(transparent=transparent, selected=False, prefix=prefix)
       
     class Button(ButtonStyleSheet.Button):
          def __init__(self, *, height=25, transparent=False, selected=False, prefix=""):
               super().__init__(height=height, transparent=transparent, selected=selected, prefix=prefix)
              
     class Hover(ButtonStyleSheet.Hover):
         def __init__(self, *, transparent=False, hover=True, selected=False, prefix=""):
               super().__init__(transparent=transparent, hover=hover, selected=selected, prefix=prefix)

     class Disabled(ButtonStyleSheet.Disabled):
         def __init__(self, *, transparent=False, selected=False, prefix=""):
               super().__init__(transparent=transparent, selected=selected, prefix=prefix)

     class Pressed(BaseStyleSheet):
         def __init__(self, *, transparent=False, prefix=""):
               super().__init__(class_name='QPushButton:pressed', prefix=prefix)
               self.border = BaseProperty.Border(width=2, color="#4c94f4")
               if not transparent:
                   self.background_color = BaseProperty.BackgroundColor(BaseColor.Button.pressed_background.rgba)
                   


