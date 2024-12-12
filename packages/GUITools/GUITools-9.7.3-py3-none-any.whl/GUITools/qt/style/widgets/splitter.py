from .base import BaseWidgetStyleSheet, BaseStyleSheet, BaseColor, BaseProperty

class SplitterStyleSheet(BaseWidgetStyleSheet):
    """
    QSplitter::handle:horizontal
            {{
                background-color: qlineargradient(spread: pad, x1: 0, y1: 1, x2: 0, y2: 0,
                    stop: 0 rgba(255, 255, 255, 0),
                    stop: 0.407273 {BaseColor.tertiary.rgba},
                    stop: 0.6825 {BaseColor.tertiary.fromRgba(230)},
                    stop: 1 rgba(255, 255, 255, 0)
                );
                margin: 1px;
            }}

            QSplitter::handle:vertical
            {{
                background-color: qlineargradient(spread: pad, x1: 1, y1: 0, x2: 0, y2: 0,
                    stop: 0 rgba(255, 255, 255, 0),
                    stop: 0.407273 {BaseColor.tertiary.rgba},
                    stop: 0.6825 {BaseColor.tertiary.fromRgba(230)},
                    stop: 1 rgba(255, 255, 255, 0)
                );
                margin: 1px;
            }}
    """

    def __init__(self, *, handle_background_color=BaseColor.tertiary, prefix=""):
        super().__init__(f"{prefix} QSplitter")
        self.handleHorizontal = self.HandleHorizontal(handle_background_color, prefix)
        self.handleVertical = self.HandleVertical(handle_background_color, prefix)

    class HandleHorizontal(BaseStyleSheet):
        def __init__(self, handle_background_color=BaseColor.tertiary , prefix=""):
            super().__init__('QSplitter::handle:horizontal', prefix)
            self.background_color = BaseProperty.BackgroundColor(value=f'''
            background-color: qlineargradient(spread: pad, x1: 0, y1: 1, x2: 0, y2: 0,
                    stop: 0 rgba(255, 255, 255, 0),
                    stop: 0.407273 {BaseColor.tertiary.rgba},
                    stop: 0.6825 {BaseColor.tertiary.fromRgba(230)},
                    stop: 1 rgba(255, 255, 255, 0)
                )''')
            self.padding = BaseProperty.Padding(value=1)
            
    class HandleVertical(BaseStyleSheet):
        def __init__(self, handle_background_color=BaseColor.tertiary, prefix=""):
            super().__init__('QSplitter::handle:horizontal', prefix)
            self.background_color = BaseProperty.BackgroundColor(value=f'''
            background-color: qlineargradient(spread: pad, x1: 1, y1: 0, x2: 0, y2: 0,
                    stop: 0 rgba(255, 255, 255, 0),
                    stop: 0.407273 {BaseColor.tertiary.rgba},
                    stop: 0.6825 {BaseColor.tertiary.fromRgba(230)},
                    stop: 1 rgba(255, 255, 255, 0)
                )''')
            self.padding = BaseProperty.Padding(value=1)

