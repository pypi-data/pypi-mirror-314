# -*- coding: latin -*-
from functools import partial
import string, random, os
import psutil as ps
from tempfile import NamedTemporaryFile
from shutil import move, rmtree
from threading import Event, Thread
from queue import Queue
from time import sleep
import subprocess
import re
from tempfile import gettempdir
import wmi, re, hashlib, base64
from urllib.parse import urlparse
import socket, importlib, unicodedata


class ImportData:
    def __init__(self, import_module : object, action_exec_module : partial):
        self.import_module = import_module
        self.action_exec_module = action_exec_module

class Utils(object):

    class SubProcessLog(object):
        def __init__(self):
            self.percentage = 0
            self.in_process = False
            self.error = False
            self.log = ""

    def is_python_installed():
        try:
            subprocess.check_output(["python", "--version"])
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False

    def import_module(mudule_path : str):
         spec = importlib.util.spec_from_file_location(os.path.basename(mudule_path).split('.')[0], mudule_path)
         icons_rc = importlib.util.module_from_spec(spec)
         return ImportData(icons_rc, partial(spec.loader.exec_module, icons_rc))
    
    def masked_text(text: str, last_visible = 5, masked = '*'):
        if len(text) > last_visible:
            masked_text = masked * (len(text) - 5) + text[-5:]
        else:
            masked_text = text
        
        return masked_text

    def run_once_class(cls):
        class WrapperClass(cls):
            _initialized = False
            def __new__(cls, *args, **kwargs):
                if not cls._initialized:
                    instance = super().__new__(cls)
                    cls._initialized = True
                    return instance
                else:
                    return None

        return WrapperClass

    def run_once(func):
        def wrapper(*args, **kwargs):
            if not wrapper._initialized:
                func(*args, **kwargs)
                wrapper._initialized = True
            return func(*args, **kwargs)

        wrapper._initialized = False
        return wrapper

    def temp_folder(folder : str = None, folder_name = "MyGuiTempFolder"):
        pdir = gettempdir()
        temp = os.path.join(pdir, folder_name)
        if folder:
            temp = os.path.join(temp, folder)
        if not os.path.exists(temp):
            os.makedirs(temp)
        return temp

    def remove_dict_key(remove_key, comparison_value, _dict : dict):
        keys_to_remove = [key for key, value in _dict.items() if value[comparison_value] == remove_key]
        for key in keys_to_remove:
            del _dict[key]

    def is_valid_filename(name : str):
        if not name or '.' in name or name.isnumeric():
            return False

        invalid_chars = r'[\/:*?"<>|]'
        if re.search(invalid_chars, name):
            return False

        if name.startswith(' ') or name.endswith(' '):
            return False

        reserved_names = ['con', 'prn', 'aux', 'nul']  # Exemplos de palavras reservadas do Windows
        if name.lower() in reserved_names:
            return False

        return True

    def is_valid_sql_string( input_string):
        if re.match(r'^[a-zA-Z0-9_\s]*$', input_string):
            return True
        else:
            return False

    def adjust_text_length(text : str, length : int, blank_spaces : int = 0):
        if len(text) < length:
            espacos_faltantes = length - len(text)
            texto_ajustado = f"{text}{' ' * espacos_faltantes}"
            return f"{texto_ajustado}{' ' * blank_spaces}"
        else:
            return f"{text}{' ' * blank_spaces}"

    @classmethod
    def duplicate_name(cls, name : str):
        match = re.search(r"_(\d+)$", name)
        if match:
            number = int(match.group(1)) + 1
            name = re.sub(r"_(\d+)$", f"_{number}", name)
        else:
            name = name.rstrip('_')
            name += "_2"
        return name

    @classmethod
    def duplicate_file_name(cls, name: str):
        base_name, ext = name.rsplit('.', 1) if '.' in name else (name, '')
        match = re.search(r"_(\d+)$", base_name)
        if match:
            number = int(match.group(1)) + 1
            base_name = re.sub(r"_(\d+)$", f"_{number}", base_name)
        else:
            base_name += "_2"
        return f"{base_name}.{ext}"

    @classmethod
    def generate_slug(cls, name, lower = True):
        name = cls.remove_special_characters(name)
        if lower:
            slug = re.sub(r'\W+', '_', name.lower().strip())
        else:
            slug = re.sub(r'\W+', '_', name.strip())
        slug = re.sub(r'_+', '_', slug)
        slug = slug.strip('_')
        return slug

    def remove_special_characters(texto : str):
        texto_normalizado = unicodedata.normalize('NFD', texto)
        texto_sem_acento = ''.join(char for char in texto_normalizado if unicodedata.category(char) != 'Mn')
        return texto_sem_acento

    @classmethod
    def create_folder(cls, caminho : str):
        if not os.path.isdir(caminho):
             os.makedirs(caminho) # cria a pasta
        return caminho

    @classmethod
    def delete_folder(cls, folder_path : str):
        try:
            # Excluindo a pasta e todo o seu conte�do
            rmtree(folder_path)
            return True, ""
        except Exception as e:
            return False, e

    @classmethod
    def run_cmd(cls, *commands : str, subProcessLog : SubProcessLog = None, env = None):
        success = True
        if subProcessLog:
            subProcessLog.in_process = True

        """Launches 'command' windowless and waits until finished"""
        temp_folter = cls.temp_folder()
        file_command = os.path.join(temp_folter, f'{cls.random_string(5)}commands.cmd')
        if os.path.isfile(file_command):
                os.remove(file_command)

        f = open(file_command, "w")
        for i, command in enumerate(commands):
            if i == len(command) - 1:
                f.write(command)
            else:
                f.write(f'{command} &&')
        f.close()

        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        if env:
             process = subprocess.Popen([file_command, "-d", "myfile.gz"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, startupinfo=startupinfo, env=env)
        else:
             process = subprocess.Popen([file_command, "-d", "myfile.gz"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, startupinfo=startupinfo)

        with process.stdout:
            try:
                for line in iter(process.stdout.readline, b''): # b'\n'-separated lines
                    print(line.decode("utf-8").strip())
                    if subProcessLog:
                        log = line.decode("utf-8").strip()
                        if " from 'C:" in log:
                            subProcessLog.log = log.split(" from 'C:")[0]
                        else:
                            subProcessLog.log = log

                        if 'pyinstaller: error' in subProcessLog.log or 'AttributeError:' in subProcessLog.log:
                            subProcessLog.error = True
                            success = False

                        subProcessLog.percentage += 1

            except Exception as e:
                    print(f"{str(e)}")
                    if subProcessLog:
                        subProcessLog.error = True
                        subProcessLog.log = f"{str(e)}"
                        subProcessLog.percentage += 1
                        success = False

        process.wait() 
        if subProcessLog:
            subProcessLog.in_process = False

        if os.path.isfile(file_command):
            os.remove(file_command)

        return success


    def validate_url(url):
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except ValueError:
            return False

    @classmethod
    def validate_nif(cls, nif):
        if cls.validate_number(nif):
            if len(nif) == 9:
                return True
            return False
        return False

    @staticmethod
    def validate_number(string : str):
        if not string.strip():
            return False
        for s in string:
            try:
                int(s)
            except:
                return False
        return True

    @staticmethod
    def clean_folder(pasta: str):
        """Limpar todos os arquivos de uma pasta.
        
        Este método verifica se a pasta existe e, se existir, remove todos os arquivos contidos nela.
        
        Args:
            pasta (str): Caminho da pasta a ser limpa.

        """
        if os.path.isdir(pasta):
            for file in os.scandir(pasta):
                if file.is_file():  # Verifica se é um arquivo antes de tentar removê-lo
                    os.remove(file.path)
        else:
            print(f'A pasta: {pasta} não foi encontrada!')

    def random_string(length : int):
        # choose from all lowercase letter
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(length))

    def deleteObjects(*objs : object | list[object]):
        for obj in objs:
             del obj

    def process_iter():
        return [proc.name() for proc in ps.process_iter()]

    @classmethod
    def update_txt(cls, fichiro : str, dados : dict[str, str], msg=False):

        """atualizar um ficheiro
        
        args:
            fichiro(str): nome ou caminho do ficheiro
            dados(str): dados a atualizar
            msg(str): mensagem a exibir
        
        """
 
        with open(fichiro, 'r') as arquivo, \
                NamedTemporaryFile('w', delete=False) as out:
            for linha in arquivo:
                for d in dados:
                    if d['codigo'] in linha:
                        linha = linha.replace(d['codigo'], d['novo_codigo'])
                out.write(linha) 

        move(out.name, fichiro)

        if msg:
            print(msg)

    @staticmethod
    def list_files(caminho_pasta : str, pastas_ignoradas=[], tipos_arquivo : list | tuple = (), tipos_arquivo_ignorados: list | tuple = ()):
        resultados = []

        for pasta_atual, subpastas, arquivos in os.walk(caminho_pasta):
            # Ignorar pastas especificadas
            subpastas[:] = [pasta for pasta in subpastas if pasta not in pastas_ignoradas]

            for arquivo in arquivos:
                if not arquivo.lower().endswith(tuple(tipos_arquivo_ignorados)) and not arquivo.endswith(tuple(tipos_arquivo_ignorados)) and not arquivo.upper().endswith(tuple(tipos_arquivo_ignorados)):
                    if arquivo.lower().endswith(tuple(tipos_arquivo)) or arquivo.endswith(tuple(tipos_arquivo)) or arquivo.upper().endswith(tuple(tipos_arquivo)):
                        caminho = f'{pasta_atual}/{arquivo}'
                        caminho = caminho.replace("\\", "/")
                        resultados.append(caminho)

        return resultados


    class Multiprocessing(object):

        def __init__(self, listaArgsTrabalho : list , target, n_threads = 5, whait = True):
            self.event = Event()
            self._target = target
            self.__fila = Queue(maxsize=len(listaArgsTrabalho) + 1)
            for Trabalho in listaArgsTrabalho:
                self.__fila.put(Trabalho)

            self.event.set()
            self.__fila.put('Kill')

            if len(listaArgsTrabalho) < n_threads:
                n_threads = len(listaArgsTrabalho)

            thrs = self.get_pool(n_threads)
            [th.start() for th in thrs]
            if whait:
                [th.join() for th in thrs]

        def get_pool(self, n_th: int):
            return [self.Worker(event=self.event, target=self._target, queue=self.__fila)
                    for n in range(n_th)]

        class Worker(Thread):
            def __init__(self, event, target, queue : Queue):
                super().__init__()
                self.event = event
                self.queue = queue
                self._target = target
                self._stoped = False

            def run(self):
                self.event.wait()
                while not self.queue.empty():
                    trabalho = self.queue.get()
                    if trabalho == 'Kill':
                        self.queue.put(trabalho)
                        self._stoped = True
                        break
                    if type(trabalho) == list or type(trabalho) == tuple:
                        self._target(*trabalho)
                    else:
                        self._target(trabalho)

            def join(self):
                while not self._stoped:
                    sleep(0.1)

    class ExtractVariables:
        def __init__(self, texts: list[str]):
            unique_matches = set()
            
            # Iterar sobre cada texto na lista
            for text in texts:
                # Encontrar todas as ocorrências de texto entre chaves {}
                matches = re.findall(r'\{(.*?)\}', text)
                # Adicionar os resultados ao conjunto para garantir elementos únicos
                unique_matches.update(matches)

            self.valid : list[str] = []
            self.invalid : list[str] = []

            for variable in list(unique_matches):
                if variable.isidentifier():
                    self.valid.append(variable)
                else:
                    self.invalid.append(variable)


    class System(object):

        MACHINE_NAME = socket.gethostname()

        @classmethod
        def machine_id(cls):
            _MAQUINA_ID = ""

            if not _MAQUINA_ID:
                processador_id = cls.get_processador_id()
                disco_id = cls.get_disco_id()
                bios_id = cls.get_bios_id()

                combined_id = f"{processador_id}-{disco_id}-{bios_id}"

                bytes_id = combined_id.encode('utf-8')
                hashed_bytes = hashlib.sha256(bytes_id).digest()
                base64_encoded = base64.b64encode(hashed_bytes).decode('utf-8')

                _MAQUINA_ID = base64_encoded[25:]

            return _MAQUINA_ID

        @staticmethod
        def get_processador_id():
            ID = ""
    
            # Conecta-se ao sistema Windows Management Instrumentation (WMI)
            c = wmi.WMI()
    
            for cpu in c.Win32_Processor():
                ID = cpu.ProcessorId.strip()
                break

            return ID[:4]

        @staticmethod
        def get_disco_id():
            ID = ""

            # Conecta-se ao sistema Windows Management Instrumentation (WMI)
            c = wmi.WMI()

            for disk in c.Win32_DiskDrive():
                if "PHYSICALDRIVE0" in disk.Name.upper():
                    ID = disk.SerialNumber.strip()
                    break

            return ID[:4]

        @staticmethod
        def get_bios_id():
            ID = ""

            # Conecta-se ao sistema Windows Management Instrumentation (WMI)
            c = wmi.WMI()

            for bios in c.Win32_BIOS():
                Versao = bios.Version.strip()
                collection = re.findall(r'\d+', Versao)
                for match in collection:
                    ID += match

                if len(ID) == 0:
                    ID = Versao
                break

            return ID[:4]


            



