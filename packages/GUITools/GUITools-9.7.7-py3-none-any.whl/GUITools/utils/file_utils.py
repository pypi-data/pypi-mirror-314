# -*- coding: latin -*-
from io import TextIOWrapper
import os
from tempfile import NamedTemporaryFile
from time import sleep
import re
import shutil, pathlib
from .utils import Utils
import pkg_resources

def sort_key(versao):
    partes = versao.split('.')
    numeros = [int(parte) if parte.isdigit() else float('inf') for parte in partes]
    return tuple(numeros)

class FileUtils(object):

    class DataFileSetup:
        def __init__(self, path_file : str):
            self.path_file = path_file
            self.name = ""
            self.version = ""
            self.next_version = ""
            self.description = ""
            self.author = ""
            self.versions : list[str] = []
            self.installed_version = ""

        def is_valid(self):
            return self.name.strip() and self.version.strip() and self.next_version.strip()

    
    @classmethod
    def get_data_setup_py(cls, file_setup : str):
        # lê do arquivo e escreve em outro arquivo temporário
        with open(file_setup, 'r') as arquivo:
            return cls._get_data_setup_(os.path.dirname(file_setup), arquivo)
                
    def _get_info(line : str, info : str):
        r = r"\s*=\s*(['\"])([^'\"]+)(['\"])"
        match = re.search(f"{info}{r}", line)
        if match:
             return match.group(2)
 
    @classmethod
    def _get_data_setup_(cls, path_file : str, arquivo :  TextIOWrapper, out : NamedTemporaryFile = None):
        data = cls.DataFileSetup(path_file)
        
        setuptools = False
        for line in arquivo:
            if 'setuptools' in line:
                setuptools = True
            if 'name' in line:
                data.name = cls._get_info(line, 'name')
                data.name = data.name if data.name else ""
            if 'description' in line:
                data.description = cls._get_info(line, 'description')
                data.description = data.description if data.description else ""
            if 'author' in line:
                data.author = cls._get_info(line, 'author')
                data.author = data.author if data.author else ""
            if 'version' in line:
                version = cls._get_info(line, 'version')
                data.version = version if version else ""
                if version:
                    next_version = cls.get_next_setup_version(version)
                    data.next_version = next_version
                    line = f"    version='{next_version}', \n"
            if out:
                out.write(line) # escreve no arquivo temporário

        if setuptools:
            data.versions = cls.get_all_versions_whl(path_file)
            data.installed_version = cls.get_installed_version_module(data.name)
            return data

        return cls.DataFileSetup(path_file)

    @staticmethod
    def get_installed_version_module(module_name : str):
        try:
            versao = pkg_resources.get_distribution(module_name).version
            return versao
        except pkg_resources.DistributionNotFound:
            return ""

    @classmethod
    def get_all_versions_whl(cls, path_file : str):

        dir_dist = os.path.join(path_file, 'dist')
        if os.path.exists(dir_dist):
            fileUi = r"**\*.whl"
            files = list(pathlib.Path(dir_dist).glob(fileUi))
            versions = []
            for _file in files:
                file_version = cls.get_version_whl(str(_file))
                if file_version:
                    versions.append(file_version)

            return sorted(versions, key=sort_key, reverse=True)

        return []

    @staticmethod
    def get_next_setup_version(current_vercion : str):
        n_version = current_vercion.split(".")
        if len(n_version) > 2:
            current_vercion = f'{n_version[0]}.{n_version[1]}{n_version[2]}'
        elif len(n_version) == 2:
            current_vercion = f'{n_version[0]}.{n_version[1]}'
        else:
            current_vercion = f'{n_version[0]}'
        if Utils.validate_number(current_vercion.replace('.', '')):
            current_vercion = float(current_vercion) + 0.01
            current_vercion = "%.2f" % current_vercion
            n_version = current_vercion.split(".")
            return f'{n_version[0]}.{n_version[1][0]}.{n_version[1][1]}'

    @classmethod
    def get_version_whl(cls, file_whl : str):
        # Padrão de expressão regular para extrair a versão do arquivo .whl
        padrao = re.compile(r'-(\d+\.\d+(\.\d+)?.*?)-')

        # Tenta encontrar a correspondência no nome do arquivo
        correspondencia = padrao.search(file_whl)

        if correspondencia:
            # Retorna o grupo de captura que contém a versão
            return str(correspondencia.group(1))
        else:
            # Retorna None se a versão não for encontrada
            return None

    @classmethod
    def get_whl_filename(cls, version: str, folder_path: str):
        # Obtém a lista de arquivos .whl na pasta
        files_in_folder = [f for f in os.listdir(folder_path) if f.endswith(".whl")]

        # Itera sobre os arquivos procurando correspondência com a versão
        for filename in files_in_folder:
            if cls.get_version_whl(filename) == version:
                return filename

        # Retorna None se nenhum arquivo corresponder à versão fornecida
        return None

    @staticmethod
    def install_whl(module_name : str, path_dist : str, file_whl : str):
        desktop_dir =  os.path.join(os.path.expanduser("~"),  "Desktop")
        return Utils.run_cmd(f"cd {desktop_dir}", f"pip uninstall {module_name} -y", f"cd {path_dist}", f"pip install {file_whl} --force-reinstall")
        
    @classmethod
    def create_whl(cls, file_setup : str, subProcessLog : Utils.SubProcessLog = None):

        path_file = os.path.dirname(file_setup)
        # lê do arquivo e escreve em outro arquivo temporário
        with open(file_setup, 'r') as arquivo, NamedTemporaryFile('w', delete=False) as out:
            data = cls._get_data_setup_(path_file, arquivo, out)
            
        if data.is_valid():
            # move o arquivo temporário para o original
            shutil.move(out.name, os.path.join(path_file, 'setup.py'))

            if os.path.exists(os.path.join(path_file, 'build')):
                shutil.rmtree(os.path.join(path_file, 'build'))
            if os.path.exists(os.path.join(path_file, f'{data.name}.egg-info')):
                shutil.rmtree(os.path.join(path_file, f'{data.name}.egg-info'))

            novo_whl = f'{data.name}-{data.next_version}-py3-none-any.whl'
            desktop_dir =  os.path.join(os.path.expanduser("~"),  "Desktop")

            Utils.run_cmd(f"cd {desktop_dir}", f"pip uninstall {data.name} -y", f"cd {path_file} && pip install check-wheel-contents", "python setup.py bdist_wheel", "cd dist", f"pip install {novo_whl} --force-reinstall",
                                  subProcessLog=subProcessLog)

            whl = os.path.join(path_file, "dist", novo_whl)
            while not os.path.exists(whl):
                sleep(2)

            if os.path.exists(os.path.join(path_file, f'{data.name}.egg-info')):
                shutil.rmtree(os.path.join(path_file, f'{data.name}.egg-info'))

            return data.next_version




