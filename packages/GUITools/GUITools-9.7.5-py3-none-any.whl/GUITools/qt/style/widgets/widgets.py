
from .base import BaseColor, BaseWidgetStyleSheet, BaseProperty, BaseStyleSheet, CreateStyleSheet, StyleSheets
from ..icon import Icons
from .comboBox import ComboBoxStyleCheet
from .scrollBar import ScrollBarStyleSheet, ScrollAreaStyleSheet
from .progressBar import ProgressBarStyleSheet
from .tableView import TableViewStyleSheet
from .treeView import TreeViewStyleSheet
from .listView import ListViewStyleCheet
from .headerView import HeaderViewStyleSheet
from .menu import MenuStyleCheet
from .checkBox import CheckBoxStyleCheet
from .lineEdit import LineEditStyleCheet
from .tabWidget import TabWidgetStyleSheet
from .box import SpinBoxStyleSheet, DoubleSpinBoxStyleSheet, TimeEditStyleSheet, DateTimeEditStyleSheet
from .text import TextEditStyleSheet, TextBrowserStyleSheet
from .button import ButtonMenuStyleSheet, ButtonStyleSheet, ButtonCopyStyleSheet
from .toolBox import ToolBoxStyleSheet
from .splitter import SplitterStyleSheet

class Property(BaseProperty):
        ...

class Standard:

    class StyleSheet(BaseWidgetStyleSheet):
        def __init__(self):
            super().__init__()

        def style(self):
            return Standard.__str__()

    menu = MenuStyleCheet()
    button = ButtonStyleSheet()
    button_menu = ButtonMenuStyleSheet()
    button_copy = ButtonCopyStyleSheet()
    scrollBar = ScrollBarStyleSheet()
    scrollArea = ScrollAreaStyleSheet()
    headerView = HeaderViewStyleSheet()
    tableView = TableViewStyleSheet()
    treeView = TreeViewStyleSheet()
    lineEdit = LineEditStyleCheet()
    checkBox = CheckBoxStyleCheet()
    comboBox = ComboBoxStyleCheet()
    textEdit = TextEditStyleSheet()
    textBrowser = TextBrowserStyleSheet()
    spinBox = SpinBoxStyleSheet()
    timeEdit = TimeEditStyleSheet()
    dateTimeEdit = DateTimeEditStyleSheet()
    doubleSpinBox = DoubleSpinBoxStyleSheet()
    tabWidget = TabWidgetStyleSheet()
    listView = ListViewStyleCheet()
    progressBar = ProgressBarStyleSheet()
    toolBox = ToolBoxStyleSheet()
    splitter = SplitterStyleSheet()
   
    @classmethod
    def __str__(cls):

        indicator = CreateStyleSheet(Property.SubcontrolPosition('center', 'right'),
                                  Property.Image(Icons.Name.seta_baixo),
                                  Property.Height(value=9))

        return f'''

            {StyleSheets.BaseStyle()}
            
            {cls.button}
            {cls.scrollBar}
            {cls.scrollArea}
            {cls.tableView}
            {cls.treeView}
            {cls.headerView}
            {cls.lineEdit}
            {cls.checkBox}
            {cls.comboBox}
            {cls.textEdit}
            {cls.textBrowser}
            {cls.spinBox}
            {cls.timeEdit}
            {cls.dateTimeEdit}
            {cls.doubleSpinBox}
            {cls.tabWidget}
            {cls.listView}
            {cls.progressBar}
            {cls.toolBox}
            {cls.menu}
            
            {CreateStyleSheet(Property.BackgroundColor(BaseColor.Widget.background),
                                  Property.Color(BaseColor.Reverse.primary),
                                  Property.Border(radius=5, width=0),
                                  Property.Padding(value=3)
                                  ).add_class_name(
                                  "QToolButton") }

            {indicator.add_class_name("QToolButton::menu-indicator")}

            {indicator.clone(Property.Border(radius=5)).add_class_name("QComboBox::drop-down", "QDateEdit::drop-down", "QToolButton::arrow")}

             {CreateStyleSheet(Property.Image(Icons.Name.seta_baixo, Icons.Color.GRAY)).add_class_name(
                "QComboBox::drop-down", "QDateEdit::drop-down", "QToolButton::arrow", suffix=":disabled")
             }
             
             {CreateStyleSheet(Property.Image(Icons.Name.seta_baixo)).add_class_name(
                "QComboBox::drop-down", "QDateEdit::drop-down", "QToolButton::arrow")
             }
             
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

            QCalendarWidget {{
                border-radius: 0px;
                color: #4c94f4;
                selection-color: {BaseColor.Reverse.secondary};
                selection-background-color: {BaseColor.secondary};
                border: 0px solid;
                font: 10pt "Segoe UI";
            }}

            #centralwidget {{ border-radius: 0px;}} 

            QFrame, Qwidget {{outline: none;}}

        '''


class WidgetsStyleCheet(object):

    class line(BaseWidgetStyleSheet):
        def __init__(self):
            super().__init__()

        def style(self):
            return f'{Property.BackgroundColor(BaseColor.secondary.horizontal_gradient([0, 0.45, 0.55, 1]) )} {Property.Border(radius=0)} '

    class Color(BaseColor):
        ...

    class Property(BaseProperty):
        ...

    class StyleSheet(BaseStyleSheet):
        ...

    class CreateStyleSheet(CreateStyleSheet):
        ...

    class comboBox(ComboBoxStyleCheet):
        ...

    class progressBar(ProgressBarStyleSheet):
        ...

    class scrollBar(ScrollBarStyleSheet):
        ...

    class tableView(TableViewStyleSheet):
        ...

    class treeView(TreeViewStyleSheet):
        ...

    class listView(ListViewStyleCheet):
        ...

    class headerView(HeaderViewStyleSheet):
        ...

    class menu(MenuStyleCheet):
        ...

    class checkBox(CheckBoxStyleCheet):
        ...

    class lineEdit(LineEditStyleCheet):
        ...

    class tabWidget(TabWidgetStyleSheet):
        ...

    class toolBox(ToolBoxStyleSheet):
        ...

    class spinBox(SpinBoxStyleSheet):
        ...

    class timeEdit(TimeEditStyleSheet):
        ...

    class dateTimeEdit(DateTimeEditStyleSheet):
        ...

    class doubleSpinBox(DoubleSpinBoxStyleSheet):
        ...

    class textEdit(TextEditStyleSheet):
        ...

    class textBrowser(TextBrowserStyleSheet):
        ...

    class button_menu(ButtonMenuStyleSheet):
        ...

    class button(ButtonStyleSheet):
        ...

    class button_copy(ButtonCopyStyleSheet):
        ...

    class splitter(SplitterStyleSheet):
        ...

    class WidgetStyleSheet(BaseWidgetStyleSheet):
        ...

    class Standard(Standard):
        ...

    @classmethod
    def standard(cls):
        return cls.Standard.__str__()
