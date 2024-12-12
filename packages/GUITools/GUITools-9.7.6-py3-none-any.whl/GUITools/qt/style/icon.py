# -*- coding: latin -*-
from PyQt6.QtGui import QIcon, QPixmap, QImage, QColor
from PyQt6.QtCore import QSize
from ...utils import Utils
from pathlib import Path
from .utils import TypeTheme, Global
from PyQt6.QtCore import QFile
import os

class Color(object):
    THEME = "theme"
    THEME_REVERSE = "theme_reverse"
    ORIGINAL = "original"
    LIGHT = "200_200_200"
    DARK = "55_55_55"
    BLUE = "73_145_246"
    GRAY = "130_130_130"

class Data(object):
      dict_icons = {}
      dict_icons_clolor = {}

class CustomResource(object):

    def __init__(self, url : str, icon : QIcon = None):
        self.url = os.path.join(u':', url)
        self.icon = icon if icon else QIcon(self.url)
        self.pixmap = self.to_pixmap()

    def to_pixmap(self, new_size : int = None) -> QPixmap:
        if new_size:
            return self.icon.pixmap(new_size)
        original_size = (32, 32)
        if self.icon.availableSizes():
            original_size = self.icon.availableSizes()[0]
        return self.icon.pixmap(original_size)

class Resource(CustomResource):

    def __init__(self, url : str, suffix = ""):
        if suffix.strip():
            extension = Path(url).suffix
            url = f"{url.replace(extension, '')}_{suffix}{extension}"
        super().__init__(url)

    def from_color(self, new_color : QColor | tuple[int] | list[int] | str):

        color = new_color
        if type(new_color) == str:
            color = QColor(new_color)
        elif type(new_color) == tuple or type(new_color) == list:
            color = QColor(*new_color)

        original_size = (32, 32)
        if self.icon.availableSizes():
            original_size = self.icon.availableSizes()[0]
        pixmap = self.icon.pixmap(original_size)  # Defina o tamanho desejado
        image = pixmap.toImage()

        # Aplica a nova cor � imagem
        new_image = QImage(image.size(), QImage.Format.Format_ARGB32)
        new_image.fill(0)  # Preencha com transpar�ncia

        for x in range(image.width()):
            for y in range(image.height()):
                pixel_color = image.pixelColor(x, y)
                if not pixel_color.alpha():
                    continue

                new_image.setPixelColor(x, y, color)

        # Converta a imagem resultante de volta para um �cone
        new_pixmap = QPixmap.fromImage(new_image)
        new_icon = QIcon(new_pixmap)

        return CustomResource(self.url, new_icon)

class Resources(object):

    class seta_baixo(Resource):

        def __init__(self):
            super().__init__("seta_baixo.png")
            self.dark = Resource("seta_baixo.png", "55_55_55")
            self.light = Resource("seta_baixo.png", "200_200_200")
            
        @property
        def theme(self):
            return self.dark if Global.theme == TypeTheme.light else self.light


class Name(object):

    def add_suffix(icon_name : str, suffix : str):
        extension = Path(icon_name).suffix
        return f"{icon_name.replace(extension, '')}_{suffix}{extension}"

    def add_suffix_theme(icon_name : str):
        suffix = Color.DARK if Global.theme == TypeTheme.light else Color.LIGHT
        extension = Path(icon_name).suffix
        return f"{icon_name.replace(extension, '')}_{suffix}{extension}"
    
    def add_suffix_reverse_theme(icon_name : str):
        suffix = Color.LIGHT if Global.theme == TypeTheme.light else Color.DARK
        extension = Path(icon_name).suffix
        return f"{icon_name.replace(extension, '')}_{suffix}{extension}"

    seta_baixo = "seta-baixo.png"
    seta_cima = "seta-cima.png" 
    seta_esquerda = "seta-esquerda.png"
    seta_direita = "seta-direita.png" 
    entrar_sair = "entrar-sair.png"
    pc = 'pc.png'
    users = 'users.png'
    company = 'company.png'
    entrar = "entrar.png"
    sair = "sair.png"
    limpar = "limpar.png"
    code_power = "code_power.png"
    down_arrow = 'down-arrow.png'
    chat = 'chat.png'
    separator_left = 'separador-left.png'
    user = "user.png"
    openai = "openai.png"
    send = "send.png"
    not_rgb = "not_rgb.png"
    note = "note.png"
    code = "code.png"
    copy = "copy.png"
    code_file = "code-file.png"
    file_csharp = "csharp-file.png"
    file_vb = "vb-file.png"
    check = "check.png"
    stop = "stop.png"
    back = "back.png"
    lixo = "lixo.png"
    terminal = "terminal.png"
    add = "add.png"
    edit = "edit.png"
    reset = "reset.png"
    download_file = "download_file.png"
    file = "file.png"
    save = "save.png"
    system_update = "system-update.png"
    eye = "eye.png"
    download = "download.png"
    folder = "folder.png"
    settings_manager = "settings_manager.png"
    log = "log-file.png"
    exe = "exe.png"
    ui = "ui.png"
    logo_msg = "smg_logo.png"
    logo = "saftonline.png" 
    mini_logo = "mini_logo.png"
    light_mode = "light-mode.png"
    dark_mode = "dark-mode.png"
    recarregar = "recarregar.png"
    proximo = "proximo.png" 
    de_volta = "de-volta.png" 
    file_py = "python-file.png"
    rgb = "rgb.png"
    xls = "xls.png"
    pdf = "pdf.png"
    point = "1ponto.png"
    two_point = "2pontos.png"
    three_point = "3pontos.png"
    eye_slah = "eye_slah.png"
    play = "play.png"
    assistant = 'assistant.png'
    api='api.png'
    process = 'process.png'
    json = 'json.png'
    binary = 'binary.png'
    plus = "plus.png"
    check_alt = "check-alt.png"
    add_file = "add-file.png"
    build= "build.png"
    asterisk = "asterisk.png"
    duplicate = "duplicate.png"
    test = "test.png"
    anexo = "anexo.png"
    start_up = "start_up.png"
    loading = "loading.png"
    mais = "mais.png"
    menos = "menos.png"
    branch_closed = "branch_closed.png"
    branch_end = "branch_end.png"
    branch_more = "branch_more.png"
    branch_open = "branch_open.png"
    vline = "vline.png"
    drag_drop = "drag_drop.png"
    swap = "swap.png"
    agent = "agent.png"
    workers_team = "workers_team.png"
    to_do = "to_do.png"
    data_flow = "data-flow.png"
    ai_flow = "ai_flow.png"
    coment = "coment.png"
    deleted = "deleted.png"
    information="information.png"
    new = "new.png"
    close = "close.png"
    code_solution="code_solution.png"
    code_project = "code_project.png"
    code_folder="code_folder.png"
    answer= "answer.png"
    lock = "lock.png"
    magia = "magia.png"
    variable = 'variable.png'
    ai = 'ai.png'
    category = 'category.png'
    authentication = "authentication.png"

    menu_logo = "menu.png"
    menu_btn_inicio = "programas.png" 
    menu_btn_bots = "bots.png"
    menu_btn_atualizacoes = "nuvem.png"
    menu_btn_sentinela = "sentinela.png"
    menu_btn_ajuda = "ajuda.png"
    menu_btn_config = "configuracoes.png"
    maximize = "maximize.png"
    full_screen = "full_screen.png"
    exit_full_screen = "exit_full_screen.png"


    combo_box_prod = "prod.png" 
    combo_box_manutencao = "manutencao.png" 
    combo_box_dev = "code.png"

class Icon(QIcon):
        def __init__(self, icon_name : Name , icon_color : Color | str = Color.THEME):
            self.name = icon_name
            if icon_name in Data.dict_icons:
                name_icon_color = Color.THEME
                if icon_color == Color.THEME:
                    if Global.theme == "dark":
                        name_icon_color = Color.DARK
                    else:
                        name_icon_color = Color.LIGHT
                else:
                    if icon_color == Color.THEME_REVERSE:
                        if Global.theme == "dark":
                            name_icon_color = Color.LIGHT
                        else:
                            name_icon_color = Color.DARK
                    else:
                        if icon_color in Data.dict_icons[icon_name]:
                            name_icon_color = icon_color

                if name_icon_color != Color.ORIGINAL:
                    if not QFile.exists(u':' + Name.add_suffix(icon_name, name_icon_color)):
                        icon = QIcon(u':' + icon_name)
                    else:
                        icon = Data.dict_icons[icon_name][name_icon_color]
                else:
                    icon = Data.dict_icons[icon_name][name_icon_color]
            else:
                if icon_color != Color.ORIGINAL:
                    print(f"As ver��es do icon <b>{icon_name}</b> ainda n�o foram carregado")
                icon = QIcon(u':' + icon_name)

           

            super().__init__(icon)

        def toPixmap(self, size : int = None):
            return Icons.to_pixmap(self, size)

class Icons(object):

    QMessageBox : Icon = None

    @classmethod
    def change_color(cls, icon : QIcon, new_color : QColor | tuple[int] | list[int] | str, index_available_size = -1):

        color = new_color
        if type(new_color) == str:
            color = QColor(new_color)
        elif type(new_color) == tuple or type(new_color) == list:
            color = QColor(*new_color)

        original_size = QSize(32, 32)
        if icon.availableSizes():
            sizes = icon.availableSizes()
            if 0 <= index_available_size < len(sizes):
                original_size = icon.availableSizes()[index_available_size]
            else:
                original_size = icon.availableSizes()[-1]

        pixmap : QPixmap  = icon.pixmap(original_size)  # Defina o tamanho desejado
        image = pixmap.toImage()

        # Aplica a nova cor � imagem
        new_image = QImage(image.size(), QImage.Format.Format_ARGB32)
        new_image.fill(0)  # Preencha com transpar�ncia
        
        for x in range(image.width()):
            for y in range(image.height()):
                pixel_color = image.pixelColor(x, y)
                if not pixel_color.alpha():
                    continue

                new_image.setPixelColor(x, y, color)

        # Converta a imagem resultante de volta para um �cone
        new_pixmap = QPixmap.fromImage(new_image)
        new_icon = QIcon(new_pixmap)

        return new_icon
    
    @classmethod
    def download(cls, img_path : str, icon : QIcon, img_format = 'png', new_color : QColor | tuple[int] | list[int] | str = None):
        if new_color:
            icon = cls.change_color(icon, new_color)
        original_size = QSize(32, 32)
        if icon.availableSizes():
            original_size = icon.availableSizes()[0]
        pixmap : QPixmap = icon.pixmap(original_size)  # Defina o tamanho desejado
        image = pixmap.toImage()
        return image.save(img_path, img_format)

    class Data(object):
        def __init__(self, name : Name, hover_name : Name = None, color = Color.THEME, hover_color = Color.BLUE):
            self.name = name
            self.hover_name = hover_name
            self.color = color
            self.hover_color = hover_color

    class Color(Color):
        ...

    @Utils.run_once_class
    class Load(object):
        def __init__(self):
            list_args = []
            atributos = vars(Name)
            variaveis_dict = {atributo: valor for atributo, valor in atributos.items() if isinstance(valor, str)}
            
            for variavel in variaveis_dict:
                if variavel != "__module__":
                    icon_name = variaveis_dict[variavel]

                    Data.dict_icons[icon_name] = {Color.LIGHT: None,  Color.DARK : None, "original" : None, Color.BLUE: None, Color.GRAY : None}
                    icon_name_light = Icons.Name.add_suffix(icon_name, Color.LIGHT) 
                    icon_name_dark = Icons.Name.add_suffix(icon_name, Color.DARK) 
                    icon_name_blue = Icons.Name.add_suffix(icon_name, Color.BLUE) 
                    icon_name_gray = Icons.Name.add_suffix(icon_name, Color.GRAY) 

                    Data.dict_icons[icon_name]["original"] = QIcon(u':' + icon_name)
                    Data.dict_icons[icon_name][Color.LIGHT] = QIcon(u':' + icon_name_dark)
                    Data.dict_icons[icon_name][Color.DARK] = QIcon(u':' + icon_name_light)
                    Data.dict_icons[icon_name][Color.BLUE] = QIcon(u':' + icon_name_blue)
                    Data.dict_icons[icon_name][Color.GRAY] = QIcon(u':' + icon_name_gray)

                    if icon_name in Data.dict_icons_clolor:
                        list_args.append(icon_name)

            if list_args:
                Utils.Multiprocessing(list_args, self._target_function, len(list_args))

        def _target_function(self, icon_name : str):
            dict_icon_color : dict[str, str] = Data.dict_icons_clolor[icon_name]
            if not dict_icon_color['color_name'] in Data.dict_icons[icon_name]:
                custom_icon = QIcon(u':' + icon_name)
                custom_icon = Icons.change_color(custom_icon, dict_icon_color['color'])
                Data.dict_icons[icon_name][dict_icon_color['color_name']] = custom_icon

    class Name(Name):
        ...

    @classmethod
    def set_color_icon(cls, icon_name : Name , color_name : str, color : QColor | tuple[int] | list[int] | str):
        Data.dict_icons_clolor[icon_name] = {'color_name': color_name ,'color': color}

    @classmethod
    def to_pixmap(cls, icon : str | QIcon | Icon, new_size : int = None):
        if type(icon) == str:
            icon = QIcon(u':' + icon)

        if new_size:
            return icon.pixmap(new_size)
        original_size = (32, 32)
        if icon.availableSizes():
            original_size = icon.availableSizes()[0]
        return icon.pixmap(original_size)

    class Icon(Icon):
        ...






