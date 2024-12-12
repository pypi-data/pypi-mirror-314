from .base import BaseWidgetStyleSheet, BaseStyleSheet, BaseColor, BaseProperty
from .button import ButtonStyleSheet

class TabWidgetStyleSheet(BaseWidgetStyleSheet):
    def __init__(self, prefix=""):
        super().__init__(f"{prefix} QTabWidget")
        self.tabBar = self.TabBar(prefix)
        self.tabBar_frame = self.TabBar_frame(prefix)
        self.pane = self.Pane(prefix)
        self.tab_first = self.Tab_first(prefix)
        self.tab_only_one = self.Tab_only_one(prefix)
        self.tab_last = self.Tab_last(prefix)
        self.tab = self.Tab(prefix)
        self.tab_selected = self.Tab_selected(prefix)
        self.tabBarButton = self.TabBarButton(prefix)

    class TabBar(BaseStyleSheet):
        def __init__(self, prefix=""):
            super().__init__('QTabWidget QTabBar', prefix)
            self.border = BaseProperty.Border(top_right_radius=5, bottom_left_radius=5, bottom_right_radius=5, top_left_radius=0)

    class TabBar_frame(BaseStyleSheet):
        def __init__(self, prefix=""):
            super().__init__('QTabWidget QTabBar QWidget', prefix)
            self.border = BaseProperty.Border(top_right_radius=5, bottom_left_radius=5, bottom_right_radius=5, top_left_radius=0)

    class Pane(BaseStyleSheet):
        def __init__(self, prefix=""):
            super().__init__('QTabWidget::pane', prefix)
            self.border = BaseProperty.Border(color=BaseColor.division, top_right_radius=5, bottom_left_radius=5, bottom_right_radius=5, top_left_radius=0)
            self.top = BaseProperty.Top(-1)
            self.background = BaseProperty.Background(BaseColor.primary)

    class Tab_first(BaseStyleSheet):
        def __init__(self, prefix=""):
            super().__init__('QTabWidget QTabBar::tab:first', prefix)
            self.border = BaseProperty.Border(color=BaseColor.division, top_left_radius=5, top_right_radius=0, bottom_left_radius=0, bottom_right_radius=0)

    class Tab_only_one(BaseStyleSheet):
        def __init__(self, prefix=""):
            super().__init__('QTabWidget QTabBar::tab:only-one', prefix)
            self.border = BaseProperty.Border(color=BaseColor.division, top_left_radius=5, top_right_radius=5, bottom_left_radius=0, bottom_right_radius=0)

    class Tab_last(BaseStyleSheet):
        def __init__(self, prefix=""):
            super().__init__('QTabWidget QTabBar::tab:last', prefix)
            self.border = BaseProperty.Border(color=BaseColor.division, top_right_radius=5, top_left_radius=0, bottom_right_radius=0, bottom_left_radius=0)

    class Tab(BaseStyleSheet):
        def __init__(self, prefix=""):
            super().__init__('QTabWidget QTabBar::tab', prefix)
            self.border = BaseProperty.Border(color=BaseColor.division)
            self.padding = BaseProperty.Padding(left=5, right=5, top=2, bottom=2)
            self.background = BaseProperty.Background(BaseColor.secondary)
            self.font = BaseProperty.Font("Segoe UI Semibold", "63 12")
           
    class Tab_selected(BaseStyleSheet):
        def __init__(self, prefix=""):
            super().__init__('QTabWidget QTabBar::tab:selected', prefix)
            self.background = BaseProperty.Background(BaseColor.primary)
            #self.margin = BaseProperty.Margin(bottom=-1)
            self.border_bottom = BaseProperty.Border(color='transparent', bottom=1)

    class TabBarButton(ButtonStyleSheet):
        def __init__(self, prefix=""):
            super().__init__(transparent=True, hover=False, prefix=f"{prefix} QTabWidget QTabBar::tab")
   
    class South(BaseWidgetStyleSheet):
        def __init__(self, prefix=""):
            super().__init__(f"{prefix} QTabWidget")
            self.tabBar = self.TabBar(prefix)
            self.tabBar_frame = self.TabBar_frame(prefix)
            self.pane = self.Pane(prefix)
            self.tab_first = self.Tab_first(prefix)
            self.tab_only_one = self.Tab_only_one()
            self.tab_last = self.Tab_last(prefix)
            self.tab = self.Tab(prefix)
            self.tab_selected = self.Tab_selected(prefix)
            self.tabBarButton = self.TabBarButton(prefix)
            

        class TabBar(BaseStyleSheet):
            def __init__(self, prefix=""):
                super().__init__('QTabWidget QTabBar', prefix)
                self.border = BaseProperty.Border(top_right_radius=5, top_left_radius=5, bottom_right_radius=5, bottom_left_radius=0)

        class TabBar_frame(BaseStyleSheet):
            def __init__(self, prefix=""):
                super().__init__('QTabWidget QTabBar QWidget', prefix)
                self.border = BaseProperty.Border(top_right_radius=5, top_left_radius=5, bottom_right_radius=5, bottom_left_radius=0)

        class Pane(BaseStyleSheet):
            def __init__(self, prefix=""):
                super().__init__('QTabWidget::pane', prefix)
                self.border = BaseProperty.Border(color=BaseColor.division, top_right_radius=5, top_left_radius=5, bottom_right_radius=5, bottom_left_radius=0)
                self.top = BaseProperty.Top(0)
                self.bottom = BaseProperty.Bottom(-1)
                self.background = BaseProperty.Background(BaseColor.primary)

        class Tab_first(BaseStyleSheet):
            def __init__(self, prefix=""):
                super().__init__('QTabWidget QTabBar::tab:first', prefix)
                self.border = BaseProperty.Border(color=BaseColor.division, bottom_left_radius=5, top_left_radius=0, top_right_radius=0, bottom_right_radius=0)

        class Tab_only_one(BaseStyleSheet):
            def __init__(self, prefix=""):
                super().__init__('QTabWidget QTabBar::tab:only-one', prefix)
                self.border = BaseProperty.Border(color=BaseColor.division, bottom_left_radius=5, bottom_right_radius=5, top_left_radius=0, top_right_radius=0)

        class Tab_last(BaseStyleSheet):
            def __init__(self, prefix=""):
                super().__init__('QTabWidget QTabBar::tab:last', prefix)
                self.border = BaseProperty.Border(color=BaseColor.division, bottom_right_radius=5, top_right_radius=0, bottom_left_radius=0, top_left_radius=0)

        class Tab(BaseStyleSheet):
            def __init__(self, prefix=""):
                super().__init__('QTabWidget QTabBar::tab', prefix)
                self.border = BaseProperty.Border(color=BaseColor.division)
                self.padding = BaseProperty.Padding(left=5, right=5, top=1, bottom=3)
                self.background = BaseProperty.Background(BaseColor.secondary)
                self.bottom = BaseProperty.Bottom(0)
                self.top = BaseProperty.Top(0)
                self.font = BaseProperty.Font("Segoe UI Semibold", "63 12")

        class Tab_selected(BaseStyleSheet):
            def __init__(self, prefix=""):
                super().__init__('QTabWidget QTabBar::tab:selected', prefix)
                self.background = BaseProperty.Background(BaseColor.primary )
                self.margin = BaseProperty.Margin(top=-1, bottom=0)

        class TabBarButton(ButtonStyleSheet):
            def __init__(self, prefix=""):
                super().__init__(transparent=True, hover=False, prefix=f"{prefix} QTabWidget QTabBar::tab")



