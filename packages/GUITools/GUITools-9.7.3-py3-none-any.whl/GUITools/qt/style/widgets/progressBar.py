from .base import BaseWidgetStyleSheet, BaseStyleSheet, BaseColor, BaseProperty

class ProgressBarStyleSheet(BaseWidgetStyleSheet):

    def __init__(self, prefix=""):
        super().__init__(f"{prefix} QProgressBar")
        self.progressBar = self.ProgressBar(prefix)
        self.chunk = self.Chunk(prefix)

    class ProgressBar(BaseStyleSheet):
        def __init__(self, prefix=""):
            super().__init__('QProgressBar', prefix)
            self.background_color = BaseProperty.BackgroundColor(BaseColor.ProgressBar.background)
            self.color = BaseProperty.Color(BaseColor.Reverse.secondary)
            self.border = BaseProperty.Border(radius=3, color=BaseColor.Button.hover_border)
            self.text_align = BaseProperty.TextAlign('left')

    class Chunk(BaseStyleSheet):
        def __init__(self, prefix=""):
            super().__init__('QProgressBar::chunk', prefix)
            self.border = BaseProperty.Border(bottom_right_radius=2, top_right_radius=2)
            self.background_color = BaseProperty.BackgroundColor(BaseColor.ProgressBar.chunk_background)




