# -*- coding: latin -*-
from os import path, remove, environ
import shutil
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QSize
from PIL import Image
from ..utils import Utils
from .style.icon import Name

class ResultCreateExe:
    def __init__(self, status, error_msg = ""):
        self.success = status
        self.msg_error = error_msg

def create_exe(caminho_ficheiro : str, interface_grafica : bool, sem_console : bool, remover_pasta_dist : bool, remover_pasta_build : bool, subProcessLog : Utils.SubProcessLog = None, icon_path : str = "", pyinstaller_args : str = ""):

        comand_icon = None
        ico_path = ""
      
        if path.exists(icon_path.strip()) :
            icon = QIcon(icon_path.strip())
        else:
            icon = QIcon(u':' + Name.mini_logo)

        # Converte o QIcon em um QPixmap
        pixmap = icon.pixmap(QSize(64, 64))  # Ajuste o tamanho conforme necess�rio

        # Converte o QPixmap em uma imagem PIL (Pillow)
        image = Image.fromqpixmap(pixmap)

        # Salva a imagem como um arquivo .ico

        ico_name = "ico_app.ico"
        ico_path = path.join(path.dirname(caminho_ficheiro), ico_name)
        image.save(ico_path)
        comand_icon = f"--icon={ico_name}"

        nome_ficheiro_exe = path.basename(caminho_ficheiro.strip().replace('.py', ''))

        comand_sem_console = ""
        comand_interface = ""
        if interface_grafica:
            comand_interface = "--windowed"
        if sem_console:
            comand_sem_console = "--noconsole"
        #--collect-data=langchain --hidden-import=tiktoken_ext.openai_public --hidden-import=tiktoken_ext
        comando = f'pyinstaller {pyinstaller_args} --debug all --onefile --upx-dir={caminho_ficheiro} {path.basename(caminho_ficheiro)} {comand_sem_console} {comand_interface}'
        subproc_env = environ.copy()
        subproc_env.pop('TCL_LIBRARY', None)
        subproc_env.pop('TK_LIBRARY', None)

        if comand_icon:
             comando = f'pyinstaller {pyinstaller_args} --debug all --onefile --upx-dir={caminho_ficheiro} {path.basename(caminho_ficheiro)} {comand_sem_console} {comand_interface} {comand_icon}'

        success = Utils.run_cmd(f"cd {path.dirname(caminho_ficheiro)}",comando, subProcessLog=subProcessLog, env=subproc_env)

        if success:
            result = ResultCreateExe(True)
        else:
            if subProcessLog:
                if subProcessLog.error:
                    result = ResultCreateExe(False, subProcessLog.log)
                else:
                    result = ResultCreateExe(False, "Ocorreu um erro ao crial executavel")
            
        if success:
            exe = path.join(path.dirname(caminho_ficheiro), "dist", f"{nome_ficheiro_exe}.exe")
       
            if path.exists(exe):

                if path.exists(caminho_ficheiro.replace("py", "exe")):
                    try:
                        remove(caminho_ficheiro.replace("py", "exe"))
                        shutil.copy(exe, path.dirname(caminho_ficheiro))
                    except:
                        ...
                else:
                    shutil.copy(exe, path.dirname(caminho_ficheiro))

                if remover_pasta_dist:
                    if path.exists(path.join(path.dirname(caminho_ficheiro), "dist")):
                        try:
                            shutil.rmtree(path.join(path.dirname(caminho_ficheiro), "dist"))
                        except:
                            ...

        if ico_path.strip():
            if path.exists(ico_path):
                remove(ico_path)

        if path.exists(caminho_ficheiro.replace("py", "spec")):
            remove(caminho_ficheiro.replace("py", "spec"))

        if remover_pasta_build:
            try:
                if path.exists(path.join(path.dirname(caminho_ficheiro), "build")):
                    shutil.rmtree(path.join(path.dirname(caminho_ficheiro), "build"))
            except:
                ...

        return result




