from .base import BaseWidgetStyleSheet, BaseStyleSheet, BaseColor, BaseProperty, StyleSheets


class ScrollBarStyleSheet(BaseWidgetStyleSheet):
    def __init__(self, prefix=""):
        super().__init__(f"{prefix} QScrollBar")
        self.scrollBar = self.ScrollBar(prefix)
        self.up_arrow_vertical = self.Up_arrow_vertical(prefix)
        self.down_arrow_vertical = self.Down_arrow_vertical(prefix)
        self.add_page_vertical = self.Add_page_vertical(prefix)
        self.sub_page_vertical = self.Sub_page_vertical(prefix)
        self.up_arrow_horizontal = self.Up_arrow_horizontal(prefix)
        self.down_arrow_horizontal = self.Down_arrow_horizontal(prefix)
        self.add_page_horizontal = self.Add_page_horizontal(prefix)
        self.sub_page_horizontal = self.Sub_page_horizontal(prefix)
        self.add_line_horizontal = self.Add_line_horizontal(prefix)
        self.sub_line_horizontal = self.Sub_line_horizontal(prefix)
        self.sub_line_vertical = self.Sub_line_vertical(prefix)
        self.add_line_vertical = self.Add_line_vertical(prefix)
        self.aandle_vertical = self.Handle_vertical(prefix)
        self.handle_horizontal = self.Handle_horizontal(prefix)
        self.horizontal = self.Horizontal(prefix)
        self.vertical = self.Vertical(prefix)

    class ScrollBar(BaseStyleSheet):
        def __init__(self, prefix=""):
            super().__init__('QScrollBar', prefix)
            #self.background_color = BaseProperty.BackgroundColor(BaseColor.table)

    class Up_arrow_vertical(StyleSheets.BackgroundNone):
        def __init__(self, prefix=""):
            super().__init__('QScrollBar::up-arrow:vertical', prefix)

    class Down_arrow_vertical(StyleSheets.BackgroundNone):
        def __init__(self, prefix=""):
            super().__init__('QScrollBar::down-arrow:vertical', prefix)

    class Add_page_vertical(StyleSheets.BackgroundNone):
        def __init__(self, prefix=""):
            super().__init__('QScrollBar::add-page:vertical', prefix)

    class Sub_page_vertical(StyleSheets.BackgroundNone):
        def __init__(self, prefix=""):
            super().__init__('QScrollBar::sub-page:vertical', prefix)

    class Up_arrow_horizontal(StyleSheets.BackgroundNone):
        def __init__(self, prefix=""):
            super().__init__('QScrollBar::up-arrow:horizontal', prefix)

    class Down_arrow_horizontal(StyleSheets.BackgroundNone):
        def __init__(self, prefix=""):
            super().__init__('QScrollBar::down-arrow:horizontal', prefix)

    class Add_page_horizontal(StyleSheets.BackgroundNone):
        def __init__(self, prefix=""):
            super().__init__('QScrollBar::add-page:horizontal', prefix)

    class Sub_page_horizontal(StyleSheets.BackgroundNone):
        def __init__(self, prefix=""):
            super().__init__('QScrollBar::sub-page:horizontal', prefix)
       
    class Add_line_horizontal(StyleSheets.WidthAndHeight):
        def __init__(self, prefix=""):
            super().__init__('QScrollBar::add-line:horizontal', prefix)

    class Sub_line_horizontal(StyleSheets.WidthAndHeight):
        def __init__(self, prefix=""):
            super().__init__('QScrollBar::sub-line:horizontal', prefix)

    class Sub_line_vertical(StyleSheets.WidthAndHeight):
        def __init__(self, prefix=""):
            super().__init__('QScrollBar::sub-line:vertical', prefix)

    class Add_line_vertical(StyleSheets.WidthAndHeight):
        def __init__(self, prefix=""):
            super().__init__('QScrollBar::add-line:vertical', prefix)

    class Handle_vertical(BaseStyleSheet):
        def __init__(self, prefix=""):
            super().__init__('QScrollBar::handle:vertical', prefix)
            self.background_color = BaseProperty.BackgroundColor(BaseColor.tertiary)
            self.height = BaseProperty.Height(min=20)
            self.border = BaseProperty.Border(radius=3)

    class Handle_horizontal(BaseStyleSheet):
        def __init__(self, prefix=""):
            super().__init__('QScrollBar::handle:horizontal', prefix)
            self.background_color = BaseProperty.BackgroundColor(BaseColor.tertiary)
            self.width = BaseProperty.Width(min=20)
            self.border = BaseProperty.Border(radius=3)
           
    class Horizontal(BaseStyleSheet):
        def __init__(self, prefix=""):
            super().__init__('QScrollBar:horizontal', prefix)
            self.height = BaseProperty.Height(value=10)
            self.background_color = BaseProperty.BackgroundColor(BaseColor.table)
            self.border = BaseProperty.Border(radius=3)
            self.padding  = BaseProperty.Padding(value=2)

    class Vertical(BaseStyleSheet):
        def __init__(self, prefix=""):
            super().__init__('QScrollBar:vertical', prefix)
            self.width = BaseProperty.Width(value=10)
            self.background_color = BaseProperty.BackgroundColor(BaseColor.table)
            self.border = BaseProperty.Border(radius=3)
            self.padding  = BaseProperty.Padding(value=2)


class ScrollAreaStyleSheet(ScrollBarStyleSheet):
    def __init__(self, prefix=""):
        super().__init__(f"{prefix} QScrollArea")
        self.vertical.background_color.value = BaseColor.primary
        self.horizontal.background_color.value = BaseColor.primary





