from .utils import TypeTheme, Global
from PyQt6.QtGui import QColor

base_styles_themes = {
    "dark": {
        "widget": { "background" :"rgb(27, 31, 39)",
            "hover_background" : "rgb(30, 34, 43)",
            "hover_border" : "rgb(64, 71, 88)",
            "focus_border" : "rgb(86, 96, 119)",
            "selected_background" : "rgb(43, 49, 57)"
            },
        "button": {
            "background": "rgb(52, 59, 72)",
            "hover": {
                "background": "rgb(57, 65, 80)",
                "border": "rgb(61, 70, 86)"
            }, 
            "pressed": {
                "background": "rgb(50, 57, 70)",
                "border": "rgb(57, 68, 82)"
            }
        },
        "menu": {
            "background": "rgb(20, 25, 32)",
            "button": {
                "background": "rgb(52, 59, 72)",
                "hover": {
                    "background": "rgb(57, 65, 80)",
                    "border": "rgb(61, 70, 86)"
                }, 
                "pressed": {
                    "background": "rgb(50, 57, 70)",
                    "border": "rgb(57, 68, 82)"
                }
            }
        },
        "reverse": {
            "primary": "rgb(200, 200, 200)",
            "secondary": "rgb(220, 220, 220)",
            "selected" : "rgb(250, 250, 250)"
        },
        "qcolor":{ 
            "dark_green" : "rgb(53,110,58)",
            "light_green" : "rgb(87, 166, 74)",
            "yellow" : "rgb(220, 219, 155)",
            "blue" : "rgb(50, 97, 195)",
            "lilac" : "rgb(182, 141, 213)",
            "maron": "rgb(214,157, 133)",
            "difference": "rgb(55,55, 55)"
            },
        "progress_bar" : {
            "background" : "rgb(20, 24, 32)",
            "chunk_background" : "rgb(61, 70, 86)",
        },
        "division": "rgb(44, 49, 58)",
        "footer": "rgb(20, 25, 32)",
        "shadow": "rgb(15, 15, 15)",
        "table": "rgb(22, 28, 35)",
        "table_alternate": "rgb(15, 22, 30)",
        "table_selection_background": "rgb(10, 15, 22)",
        "primary": "rgb(33, 37, 43)",
        "secondary": "rgb(40, 44, 52)",
        "tertiary": "rgb(47, 51, 59)",
        "placeholder" : "rgb(130, 130, 130)",
    },

    "light": {
        "widget": { "background" :"rgb(245, 245, 245)",
            "hover_background" : "rgb(240, 240, 240)",
            "hover_border" : "rgb(200, 200, 200)",
            "focus_border" : "rgb(180, 180, 180)",
            "selected_background" : "rgb(210, 210, 210)"
            },
        "button": {
            "background": "rgba(225, 225, 225, 220)",
            "hover": {
                "background": "rgba(220, 220, 220, 250)",
                "border": "rgb(215, 215, 215)"
            },
            "pressed": {
                "background": "rgba(210, 210, 210, 250)",
                "border": "rgb(225, 225, 225)"
            }
        },
        "menu": {
            "background": "rgb(245, 245, 245)",
            "button": {
                "background": "rgba(225, 225, 225, 220)",
                "hover": {
                    "background": "rgba(220, 220, 220, 250)",
                    "border": "rgb(215, 215, 215)"
                },
                "pressed": {
                    "background": "rgba(230, 230, 230, 230)",
                    "border": "rgb(225, 225, 225)"
            }
        },
        },
        "division": "rgb(225, 225, 225)",
        "footer": "rgb(245, 245, 245)",
        "primary": "rgb(255, 255, 255)",
        "secondary": "rgb(235, 235, 235)",
        "tertiary": "rgb(220, 220, 220)",
        "reverse": {
            "primary": "rgb(60, 60, 60)",
            "secondary": "rgb(80, 80, 80)",
            "selected" : "rgb(20, 20, 20)"
        },
        "placeholder" : "rgb(170, 170, 170)",
        "qcolor":{
            "dark_green" : "rgb(53,110,58)",
            "light_green" : "rgb(87, 166, 74)",
            "yellow" : "rgb(180, 170, 0)",
            "blue" : "rgb(50, 97, 195)",
            "lilac" : "rgb(200, 0, 255)",
            "maron": "rgb(135,70, 39)",
            "difference": "rgb(200,200, 200)"
            },
        "progress_bar" : {
            "background" : "rgb(220, 220, 220)",
            "chunk_background" : "rgb(180,180,180)",
        },
        "shadow": "rgb(230, 230, 230)",
        "table": "rgb(245, 245, 245)",
        "table_alternate": "rgb(240, 240, 240)",
        "table_selection_background": "rgb(255, 255, 255)",
    }
}

class RGBAColor:
    def __init__(self, rgba : str):
        self._rgba = rgba

    @property
    def rgba(self):
        return self._rgba

    def __str__(self):
        return self.rgba

class RGBColor:
    def __init__(self, rgb : str, alpha = 255):
        if 'a' in rgb:
            rgb_values = rgb.replace("rgba(", "").replace(")", "").split(",")[:-1]
            self._rgb = "rgb(" + ",".join(rgb_values) + ")"
            self._rgba = RGBAColor(rgb)
        else:
            self._rgb = rgb
            self._rgba = self.fromRgba(alpha)

    @property
    def rgb(self):
        return self._rgb

    @property
    def rgba(self):
        return self._rgba

    def fromRgba(self, alpha : int):
        rgb = self.rgb
        if not 'a' in self.rgb:
            rgb = self.rgb.replace("rgb", "rgba")
        return RGBAColor(rgb.replace(")", f",{alpha})"))

    def __str__(self):
        return self.rgb

class AlphaColorTheme:
    def __init__(self, styles : dict):
        self._styles = styles

    @property
    def styles(self):
        return self._styles

    def __str__(self):
        return str(self._styles[Global.theme].rgba)


class FromAlphaColorTheme:
    def __init__(self, styles : dict[str, RGBColor], alpha : int):
        self._styles = styles
        self._alpha = alpha

    @property
    def alpha(self):
        return self._alpha

    @property
    def styles(self):
        return self._styles

    def __str__(self):
        return str(self._styles[Global.theme].fromRgba(self._alpha))


class ColorTheme:
    def __init__(self, *style_properties : list[str]):

        self._styles = {}

        for theme in TypeTheme.list():
            rgb = base_styles_themes[theme]
            for property_name in style_properties:
                rgb = rgb[property_name]

            self._styles[theme] = RGBColor(rgb)

        self._rgba = AlphaColorTheme(self.styles)

    @property
    def styles(self):
        return self._styles

    @property
    def rgb(self) -> str:
        return self._styles[Global.theme].rgb

    @property
    def rgba(self):
        return self._rgba

    def fromRgba(self, alpha : int):
        return FromAlphaColorTheme(self._styles, alpha)

    def vertical_gradient(self, stops = [0, 0.407273, 0.6825, 1]):
        return f'''qlineargradient(spread: pad, x1: 0, y1: 1, x2: 0, y2: 0,
                    stop: {stops[0]} rgba(255, 255, 255, 0),
                    stop: {stops[1]} {self.__str__()},
                    stop: {stops[2]} {self.fromRgba(230)},
                    stop: {stops[3]} rgba(255, 255, 255, 0)
                ); '''

    def horizontal_gradient(self, stops = [0, 0.407273, 0.6825, 1]):
        return f'''qlineargradient(spread: pad, x1: 1, y1: 0, x2: 0, y2: 0,
                    stop: {stops[0]} rgba(255, 255, 255, 0),
                    stop: {stops[1]} {self.__str__()},
                    stop: {stops[2]} {self.fromRgba(230)},
                    stop: {stops[3]} rgba(255, 255, 255, 0)
                ); '''

    @property
    def QColor(self, rgba=False):
        if rgba:
            r, g, b, a = self.rgba.replace('rgba(', '').replace(")", "").split(",")
            return QColor(int(r), int(g), int(b), int(a))
        else:
            r, g, b = self.rgb.replace('rgb(', '').replace(")", "").split(",")
            return QColor(int(r), int(g), int(b))

    def fromQColor(self, alpha=255):
        r, g, b, a = self.fromRgba(alpha).replace('rgba(', '').replace(")", "").split(",")
        return QColor(int(r), int(g), int(b), int(a))

    def __str__(self):
        return self._styles[Global.theme].rgb


class IntTheme:
    def __init__(self, *style_properties : list[str]):
        self._styles : dict[str, int] = {}

        for theme in TypeTheme.list():
            rgb = base_styles_themes[theme]
            for property_name in style_properties:
                rgb = rgb[property_name]
            self._styles[theme] = rgb

    @property
    def styles(self):
        return self._styles

    def __repr__(self) -> str:
        return repr(self._styles[Global.theme])

class BaseColor(object):
    division = ColorTheme('division')
    footer = ColorTheme('footer')
    primary = ColorTheme('primary')
    secondary = ColorTheme('secondary')
    tertiary = ColorTheme('tertiary')
    placeholder = ColorTheme('placeholder')
    table = ColorTheme('table')
    table_alternate = ColorTheme('table_alternate')
    table_selection_background = ColorTheme('table_selection_background')
    shadow = ColorTheme('shadow')
    dark_green = ColorTheme('qcolor', 'dark_green')
    light_green = ColorTheme('qcolor', 'light_green')
    yellow = ColorTheme('qcolor','yellow')
    blue = ColorTheme('qcolor', 'blue')
    lilac = ColorTheme('qcolor', 'lilac')
    maron = ColorTheme('qcolor','maron')
    
    class Widget(object):
         background = ColorTheme('widget', 'background')
         hover_border = ColorTheme('widget', 'hover_border')
         focus_border = ColorTheme('widget', 'focus_border')
         hover_background = ColorTheme('widget', 'hover_background')
         selected_background = ColorTheme('widget', "selected_background")

    class Button(object):
         background = ColorTheme('button', 'background')
         hover_background = ColorTheme('button', 'hover', 'background')
         hover_border = ColorTheme('button', 'hover', 'border')
         pressed_background = ColorTheme('button','pressed', 'background')
         pressed_border = ColorTheme('button', 'pressed', 'border')

    class Menu(object):
        background = ColorTheme('menu', 'background')
        class Button(object):
            background = ColorTheme('menu', 'button', 'background')
            hover_background = ColorTheme('menu','button', 'hover', 'background')
            hover_border = ColorTheme('menu','button', 'hover', 'border')
            pressed_background = ColorTheme('menu','button','pressed', 'background')
            pressed_border = ColorTheme('menu','button', 'pressed', 'border')

    class ProgressBar:
         background = ColorTheme('progress_bar', 'background')
         chunk_background = ColorTheme('progress_bar', 'chunk_background')

    class Reverse(object):
         primary = ColorTheme('reverse', 'primary')
         secondary = ColorTheme('reverse', 'secondary')
         selected = ColorTheme('reverse', 'selected')

def set_base_style(theme : TypeTheme, base_color : BaseColor):
    atributos = vars(base_color)
    variaveis_dict = {atributo: valor for atributo, valor in atributos.items() if isinstance(valor, str)}
    for variavel in variaveis_dict:
        if variavel != "__module__":
            base_styles_themes[theme][variavel] = variaveis_dict[variavel]




