from ..styleSheet import BaseColor
from ..icon import Icons
from abc import ABC
from os import path
import inspect

class BaseBox:
    def __init__(self, property_name : str, value : int = None, top : int = None, bottom : int = None, left : int = None, right : int = None):
        self.value = value
        self.top = top
        self.bottom = bottom
        self.right = right
        self.left = left
        self._property_name = property_name

    @property
    def property_name(self):
        return self._property_name

    def __str__(self):
        return f'''
            {f'{self.property_name}: {self.value}px;' if self.value != None else ''}
            {f'{self.property_name}-top: {self.top}px;' if self.top != None else ''}
            {f'{self.property_name}-bottom: {self.bottom}px;' if self.bottom != None else ''}
            {f'{self.property_name}-right: {self.right}px;' if self.right != None else ''}
            {f'{self.property_name}-left: {self.left}px;' if self.left != None else ''}
        '''

class BaseProperty:

    class SubcontrolOrigin:
        def __init__(self, origin : str = "content"):
            self.origin = origin
        def __str__(self):
            return f"subcontrol-origin: {self.origin};"

    class SubcontrolPosition:
        def __init__(self, horizontal : str, vertical : str):
            self.horizontal = horizontal
            self.vertical = vertical
        def __str__(self):
            return f"subcontrol-position: {self.horizontal} {self.vertical};"


    class BackgroundColor:
        def __init__(self, value : str, prefix = ''):
            self.value = value
            self.prefix = prefix
        def __str__(self):
            if self.value == 'transparent':
                self.value = "'transparent'"
            return f"{self.prefix}-background-color: {self.value};" if self.prefix.strip() else f"background-color: {self.value};"

    class Color:
        def __init__(self, value : str, prefix = ''):
            self.value = value
            self.prefix = prefix
        def __str__(self):
            if self.value == 'transparent':
                self.value = "'transparent'"
            return f"{self.prefix}-color: {self.value};" if self.prefix.strip() else f"color: {self.value};"

    class TextAlign:
        def __init__(self, value : str):
            self.value = value
        def __str__(self):
            return f"text-align: {self.value};"

    class Background:
        def __init__(self, value : str = 'transparent'):
            self.value = value
        def __str__(self):
            if self.value == 'transparent':
                self.value = "'transparent'"
            return f'background: {self.value};'

    class Image:
        def __init__(self, icon_name : str, color = "theme", suffix = ""):
            self.icon_name = icon_name
            self.color = color
            self.suffix = suffix
        def __str__(self):
            if self.color == "theme":
                icon_name = Icons.Name.add_suffix_theme(self.icon_name)
            else:
                icon_name = Icons.Name.add_suffix(self.icon_name, self.color)
            return f"image: url(:/{icon_name}) {self.suffix};"
  
    class BorderImage:
        def __init__(self, icon_name : str = None, color = "theme", suffix = ""):
            self.icon_name = icon_name
            self.color = color
            self.suffix = suffix
        def __str__(self):
            if icon_name == None:
                return "border-image: none;"

            if self.color == "theme":
                icon_name = Icons.Name.add_suffix_theme(self.icon_name)
            else:
                icon_name = Icons.Name.add_suffix(self.icon_name, self.color)
            return f"border-image: url(:/{icon_name}) {self.suffix};"

    class BackgroundImage:
        def __init__(self, icon_name : str, color : str | None = "theme"):
            self.icon_name = icon_name
            self.color = color
        def __str__(self):
            icon_name = self.icon_name
            if self.color == "theme":
                icon_name = Icons.Name.add_suffix_theme(self.icon_name)
            elif self.color != None:
                icon_name = Icons.Name.add_suffix(self.icon_name, self.color)
            return f"background-image: url({path.join(u':', icon_name)});"

    class Font:
        def __init__(self, name : str, size : int | str):
            self.name = name
            self.size = size
        def __str__(self):
            return f'font: {self.size}pt "{self.name}";'

    class FontSegoeUI(Font):
        def __init__(self, size : int):
            super().__init__("Segoe UI", size)

    class Top:
        def __init__(self, value : int):
            self.value = value
        def __str__(self):
            return f'top: {self.value}px;'
        
    class Bottom:
        def __init__(self, value : int):
            self.value = value
        def __str__(self):
            return f'bottom: {self.value}px;'
        
    class Left:
        def __init__(self, value : int):
            self.value = value
        def __str__(self):
            return f'left: {self.value}px;'
        
    class Right:
        def __init__(self, value : int):
            self.value = value
        def __str__(self):
            return f'right: {self.value}px;'
        

    class Padding(BaseBox):
        def __init__(self, *, value : int = None, top : int = None, bottom : int = None, left : int = None, right : int = None):
            super().__init__('padding', value, top, bottom, left, right)

    class Margin(BaseBox):
        def __init__(self, *, value : int = None, top : int = None, bottom : int = None, left : int = None, right : int = None):
            super().__init__('margin', value, top, bottom, left, right)

    class Width:
        def __init__(self, *, value : int = None, min : int = None, max : int = None):
            self.value = value
            self.min = min
            self.max = max

        def __str__(self):
            return f'''
                {f'width: {self.value}px;' if self.value != None else ''}
                {f'min-width: {self.min}px;' if self.min != None else ''}
                {f'max-width: {self.max}px;' if self.max != None else ''}
            '''

    class Height:
        def __init__(self, *, value : int = None, min : int = None, max : int = None):
            self.value = value
            self.min = min
            self.max= max

        def __str__(self):
            return f'''
                {f'height: {self.value}px;' if self.value else ''}
                {f'min-height: {self.min}px;' if self.min != None else ''}
                {f'max-height: {self.max}px;' if self.max != None else ''}
            '''
 
    class Border:
        def __init__(self, *, color : BaseColor | str | None | bool = None, width=1, radius : int | None = None,
                    bottom : int = None, top : int = None, left : int = None, right : int = None,
                    top_left_radius : int = None, top_right_radius : int = None,
                    bottom_left_radius : int = None, bottom_right_radius : int = None, style : str = None):

            self.color = color
            self.width = width
            self.bottom = bottom
            self.top = top
            self.left = left
            self.right = right

            self.radius = radius
            self.top_left_radius = top_left_radius
            self.top_right_radius = top_right_radius
            self.bottom_left_radius = bottom_left_radius
            self.bottom_right_radius = bottom_right_radius
            self.style = style

        def __str__(self):
            border = ""
            if self.color != None:
                if self.color == 'transparent':
                    self.value = "'transparent'"
                if self.bottom != None:
                    border = f'border-bottom: {self.bottom}px solid {self.color if self.color else ""};'
                if self.top != None:
                    border = f'{border} border-top: {self.top}px solid {self.color if self.color else ""};'
                if self.left != None:
                    border = f'{border} border-left: {self.left}px solid {self.color if self.color else ""};'
                if self.right != None:
                    border = f'{border} border-right: {self.right}px solid {self.color if self.color else ""};'
                if self.bottom == None and self.top == None and self.left == None and self.right == None:
                    border = f'border: {self.width}px solid {self.color if self.color else ""};'
            elif self.width == 0:
                border = 'border: 0px solid;'

            return f'''
                {border}
                {f'border-radius: {self.radius}px;' if self.radius != None else ''}
                {f'border-top-left-radius: {self.top_left_radius}px;' if self.top_left_radius != None else ''}
                {f'border-top-right-radius: {self.top_right_radius}px;' if self.top_right_radius != None else ''}
                {f'border-bottom-left-radius: {self.bottom_left_radius}px;' if self.bottom_left_radius != None else ''}
                {f'border-bottom-right-radius: {self.bottom_right_radius}px;' if self.bottom_right_radius != None else ''}
                {f'border-style: {self.style};' if self.style != None else ''}
            '''

def format_widget_style(style: str, prefix : str, class_name: str, use_class_name: bool):
    # Verifica se class_name é uma string válida
    if isinstance(class_name, str) and class_name.strip():
        # Quando use_class_name for True, aplica prefixo e class_name diretamente
        if use_class_name:
            return f'{prefix} {class_name} {{{style}}}'
        else:
            # Lidar com pseudoelementos (::) ou pseudoclasses (:)
            if '::' in class_name:
                if prefix.strip():
                    return f'{prefix}::{class_name.split("::")[1]} {{{style}}}'
                return f'::{class_name.split("::")[1]} {{{style}}}'
            elif ':' in class_name:
                if prefix.strip():
                    return f'{prefix}:{class_name.split(":")[1]} {{{style}}}'
                return f':{class_name.split(":")[1]} {{{style}}}'
            # Lidar com classes compostas ou hierarquias (ex: QTreeWidget QWidgetAction)
            else:
                return f'{prefix} {{{style}}}'

    # Se class_name não for válido, retorna o estilo apenas com o prefixo ou o próprio estilo
    if prefix.strip():
        return f'{prefix} {{{style}}}'
    return style


class BaseWidgetStyleSheet(ABC):
    def __init__(self, class_name = "" ,*, use_class_name = True):
        self.use_class_name = use_class_name
        self.class_name = class_name
        if not class_name.strip():
            self.use_class_name = False

    def _get_class_variables_(classe):
        list_ignore = ['additional_style', 'class_name', 'use_class_name']
        attributes = [attribute for attribute in dir(classe) if not callable(getattr(classe, attribute)) and not attribute.startswith("_") and attribute not in list_ignore]
        return [attribute for attribute in attributes if not inspect.ismethod(getattr(classe, attribute)) and not inspect.isfunction(getattr(classe, attribute))]

    def _get_class_methods_(self):
        methods = [
        method_name for method_name, method in inspect.getmembers(self, predicate=inspect.ismethod)
        if not method_name.startswith("_") and method_name not in ['styleSheet']
        ]
        return methods

    def styleSheet(self, *, use_class_name = True):
        attributes = self._get_class_variables_()
        methods = self._get_class_methods_()
        style_sheet = ""
        for attribute in attributes:
            value = getattr(self, attribute)
            if value != None:
                if hasattr(value, 'styleSheet'):
                    style_sheet = f'{style_sheet} {value.styleSheet(use_class_name=use_class_name)}'

        for method in methods:
            func = getattr(self, method)
            if callable(func):
                result = func()
                if isinstance(result, str):
                    style_sheet = f'{style_sheet} {result}'

        return style_sheet

    def __str__(self):
        return self.styleSheet(use_class_name=self.use_class_name)


class BaseStyleSheet(ABC):
    def __init__(self, class_name : str = "", prefix = ""):
        self._class_name = class_name
        self._additional_style = ""
        self.prefix = prefix
        self.use_class_name = True

    def add_additional_style(self, additional_style : str):
        self._additional_style = f'{self._additional_style} {additional_style}'

    @property
    def additional_style(self):
        return self._additional_style

    @property
    def class_name(self):
        return self._class_name

    def _get_class_variables_(classe):
        list_ignore = ['additional_style', 'class_name', 'prefix', 'use_class_name']
        attributes = [attribute for attribute in dir(classe) if not callable(getattr(classe, attribute)) and not attribute.startswith("_") and attribute not in list_ignore]
        return [attribute for attribute in attributes if not inspect.ismethod(getattr(classe, attribute)) and not inspect.isfunction(getattr(classe, attribute))]

    def _create_instance_of_class_(self, class_name : str, use_class_name : bool):
        cls = getattr(self, class_name, None)
        if cls and issubclass(cls, BaseStyleSheet):
            instance = cls()
            instance.use_class_name = use_class_name
            return f'{instance}'

    def _get_all_nested_classes_(self):
        nested_classes = [cls for cls in dir(self) if inspect.isclass(getattr(self, cls)) and cls != '__class__']
        return nested_classes

    def styleSheet(self, *, use_class_name : bool = None, prefix = ''):

        attributes = self._get_class_variables_()
        style = ""
        for attribute in attributes:
            value = getattr(self, attribute)
            style = f'{style} {value}'
      
        style = f'{style} {self.additional_style}' 
        prefix = prefix if prefix.strip() else self.prefix
        use_class_name = use_class_name if use_class_name != None else self.use_class_name
        style_sheet = f"{format_widget_style(style, prefix, self.class_name, use_class_name)}" if style.strip() else ''
        
        return style_sheet.replace('\n', '').replace('  ', '')

    def __str__(self):
        return self.styleSheet()
    


class CreateStyleSheet:
        def __init__(self, *properties : BaseProperty):
            self._properties = list(properties)
            self._widgets_name : list[str] = []
            self._widgets_id : list[str] = []

        @property
        def properties(self):
            return self._properties

        @property
        def widgets_name(self):
            return self._widgets_name

        @property
        def widgets_id(self):
            return self._widgets_id

        def add_property(self, property : BaseProperty):
            self._properties.append(property)

        def add_class_name(self, *widgets_name : str, suffix : str = ''):
            for widget_name in widgets_name:
                self._widgets_name.append(f'{widget_name}{suffix}')
            return self.__str__()

        def add_ids(self, *widgets_id : str, suffix : str = ''):
            for widget_id in widgets_id:
                self._widgets_id.append(f'#{widget_id}{suffix}')
            return self.__str__()

        def clone(self, *properties : BaseProperty):
            """Returns a new instance of CreateStyleSheet with the same properties."""
            new_properties = list(properties)
            new_properties.extend(self.properties)
            return self.__class__(*new_properties)

       
        def __str__(self):
            # Junta os nomes dos widgets com v�rgula entre eles, se houver
            widgets_name = ', '.join(self.widgets_name)
            widgets_id = ', '.join(self.widgets_id)
    
            # Combina os nomes dos widgets e os IDs dos widgets, se houver
            all_widgets = f'{widgets_name}, {widgets_id}' if widgets_name and widgets_id else widgets_name or widgets_id

            # Obt�m a representa��o em string de cada propriedade e junta os resultados em uma �nica string
            properties_str = ''.join(str(prop) for prop in self.properties)

            # Retorna uma string vazia se n�o houver widgets
            if not all_widgets or not properties_str:
                return ''

            # Retorna a string formatada com os widgets e propriedades
            return f'{all_widgets} {{\n{properties_str}\n}}'.replace('\n', '').replace('  ', '')

class StyleSheets(object):
    
    class BaseStyle(BaseStyleSheet):
        def __init__(self,  prefix=""):
            super().__init__("", prefix)
            self.base = f'''
            {CreateStyleSheet(BaseProperty.Border(radius=5), BaseProperty.Margin(value=0)).add_class_name(
                f"{prefix} QFrame", f"{prefix} QWidget", f"{prefix} QWidget QFrame", f"{prefix} QFrame QWidget")
            }

            {CreateStyleSheet(BaseProperty.Color(BaseColor.Reverse.primary.fromRgba(200))).add_class_name(
                f"{prefix} QFrame", f"{prefix} QWidget", f"{prefix} QWidgetAction QFrame", f"{prefix} QWidgetAction QWidget", suffix=":disabled")
            }

            {CreateStyleSheet(BaseProperty.BackgroundColor(BaseColor.primary),
                                    BaseProperty.Color(BaseColor.Reverse.primary),
                                    BaseProperty.FontSegoeUI(12),
                                    BaseProperty.Margin(value=0)).add_class_name(
                                    f"{prefix} QFrame", f"{prefix} QWidget", f"{prefix} QWidgetAction QFrame", f"{prefix} QWidgetAction QWidget")}

            {CreateStyleSheet(BaseProperty.Color(BaseColor.Reverse.primary)).add_class_name(f"{prefix} QLabel")
            }

            QToolTip, QFrame QToolTip, Qwidget QToolTip {{
                {BaseProperty.FontSegoeUI(10)}
                color: {BaseColor.Reverse.primary};
                border: 2px solid {BaseColor.division};
                padding: 3px;
                border-radius: 3px;
                background-color: {BaseColor.primary};
                opacity: 200;
            }}

            '''
            

    class BackgroundNone(BaseStyleSheet):
        def __init__(self, class_name : str, prefix=""):
            super().__init__(class_name, prefix)
            self.background = BaseProperty.Background('none')

    class WidthAndHeight(BaseStyleSheet):
        def __init__(self, class_name : str, prefix="", *, width = 0, min_width : int = None, max_width: int = None, height = 0, min_height : int = None, max_height : int = None):
            super().__init__(class_name, prefix)
            self.width = BaseProperty.Width(value=width, min=min_width, max=max_width)
            self.height = BaseProperty.Height(value=height, min=min_height, max=max_height)