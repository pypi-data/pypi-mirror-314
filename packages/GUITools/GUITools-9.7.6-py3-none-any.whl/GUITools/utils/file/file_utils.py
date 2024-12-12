# -*- coding: latin -*-
import re, io
from os import path, scandir, sep
import pathlib, json
from lxml import etree, html

class FileUtils(object):

    class FolderData:
        def __init__(self, file_path : str):
            self.name = path.basename(file_path)
            self.path = FileUtils.normalize_path(file_path)
            self.subfolders : list[FileUtils.FolderData] = []
            self.files = []

        def get_all_files(self) -> list[str]:
            all_files = [file for file in self.files if not file.endswith('.sln')] 

            for folder_tree in self.subfolders:
                all_files.extend(folder_tree.get_all_files())

            return all_files
        
    def format_path(my_path: str, num_folders: int) -> str:
        # Normaliza o caminho para o formato correto do sistema
        normalized_path = path.normpath(my_path)
        # Divide o caminho em partes
        parts = normalized_path.split(sep)
        
        # Se o número de partes no caminho é menor ou igual ao número desejado, retorna o caminho completo
        if len(parts) <= num_folders:
            return normalized_path
        
        # Retorna as últimas 'num_folders' partes do caminho, precedidas por '.../'
        return path.join("...", *parts[-num_folders:])
  
  
    def get_subpaths(caminho1: str, caminho2: str) -> list[str]:
        """
        Retorna a lista de subpastas de caminho1 que estão dentro de caminho2.

        Args:
            caminho1 (str): O caminho completo para verificar as subpastas.
            caminho2 (str): O caminho base para verificar se caminho1 é uma subpasta.

        Returns:
            list: Lista de subpastas de caminho1 dentro de caminho2.
        """
        path1 = pathlib.Path(caminho1).resolve()
        path2 = pathlib.Path(caminho2).resolve()

        # Verifica se caminho1 é uma subpasta de caminho2
        if not path1.is_relative_to(path2):
            return []  

        subpaths = []
        current_path = path2

        for part in path1.relative_to(path2).parts:
            current_path = current_path / part
            subpaths.append(str(current_path))

        return subpaths

    def is_subpath(path1: str, path2: str) -> bool:
        """
        Verifica se path1 é uma subpasta de path2.

        Args:
            path1 (str): O primeiro caminho (possivelmente subpasta).
            path2 (str): O segundo caminho (pasta pai).

        Returns:
            bool: True se path1 for uma subpasta de path2, caso contrário False.
        """
        path1 = pathlib.Path(path1).resolve()  # Normaliza e resolve o caminho absoluto
        path2 = pathlib.Path(path2).resolve()  # Normaliza e resolve o caminho absoluto

        # Verifica se path1 está dentro de path2
        return path1.is_relative_to(path2)

    def is_file_or_directory(path):
        path = pathlib.Path(path)

        # Verifica se o caminho existe
        if path.exists():
            if path.is_file():
                return 'file'
            elif path.is_dir():
                return 'directory'

        # Lista de extensões comuns para ficheiros de código e outros ficheiros
        common_file_extensions = {
            # Extensões de ficheiros de código
            '.cs', '.vb', '.py', '.js', '.java', '.c', '.cpp', '.h', '.hpp', '.html', '.css',
            '.ts', '.jsx', '.tsx', '.php', '.rb', '.swift', '.kt', '.go', '.rs', '.m', '.sh',
            '.bat', '.pl', '.ps1', '.sql', '.xml', '.json', '.yaml', '.yml', '.toml', '.ini',
            '.conf', '.cfg', '.md', '.rst', '.tex', '.r', '.jl', '.lua', '.scala', '.hs', '.elm',
            '.dart', '.groovy', '.fs', '.asm', '.bas', '.vbs', '.pas', '.erl', '.ex', '.exs',

            # Extensões de ficheiros binários de código
            '.dll', '.exe', '.so', '.dylib', '.lib', '.obj', '.class', '.jar', '.war', '.ear',

            # Outras extensões comuns
            '.txt', '.log', '.csv', '.tsv', '.png', '.jpg', '.jpeg', '.gif', '.bmp', '.ico',
            '.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx', '.zip', '.rar', '.tar',
            '.gz', '.7z', '.mp3', '.mp4', '.avi', '.mov', '.flv', '.mkv', '.iso', '.bin'
        }

        # Verifica se o caminho possui uma extensão comum de ficheiro
        if path.suffix.lower() in common_file_extensions:
            return 'file'

        # Verifica se o caminho termina com um separador de diretório
        if str(path).endswith(sep):
            return 'directory'

        # Verifica se o último componente do caminho parece um ficheiro
        if len(path.parts) > 1 and '.' in path.parts[-1] and not path.parts[-1].startswith('.'):
            return 'file'

        # Se nenhuma das condições anteriores for satisfeita, assume-se que é uma pasta
        return 'directory'

    def create_text_io_wrapper_from_text(text : str, encoding='utf-8'):
        # Converte o texto para bytes usando a codifica��o especificada
        bytes_data = text.encode(encoding)
    
        # Cria um objeto BytesIO a partir dos dados em bytes
        bytes_io = io.BytesIO(bytes_data)
    
        # Envolve o BytesIO com TextIOWrapper para criar uma interface de texto
        text_io_wrapper = io.TextIOWrapper(bytes_io, encoding=encoding)

        return text_io_wrapper
            
    @classmethod
    def read_file(cls, file_path : str):
        # Fun��o interna para ler o conte�do do arquivo com um determinado encoding
        def read(encoding : str):
            try:
                with open(file_path, 'r', encoding=encoding) as file:  # Abre o arquivo com o encoding especificado
                    return cls.create_text_io_wrapper_from_text(file.read())
            except FileNotFoundError:  # Trata o erro de arquivo n�o encontrado
                print("Arquivo n�o encontrado.")
                return None
            except PermissionError:  # Trata o erro de permiss�o negada
                print("Permiss�o negada.")
                return None
            except:  # Trata qualquer outro erro
                return False
 
        content = read('utf-8')  # Tenta ler o arquivo com encoding UTF-8
        if content == False:  # Se falhar, tenta com outro encoding
            content = read('latin')
        if content == False:  # Se ainda falhar, retorna None
            return None
   
        return content if content != False else None  # Retorna o conte�do do arquivo se a leitura for bem-sucedida

    def adjust_text_length(text : str,blank_spaces : int = 0):
        if blank_spaces > 0:
            return f"{' ' * blank_spaces}{text}"
        return text

    def get_blank_space(function_body: str):
        # Divide o corpo da fun��o em linhas
        lines = function_body.splitlines()
        # Itera sobre cada linha
        for line in lines:
            # Verifica se a linha n�o est� vazia
            if line.strip():
                # Retorna o primeiro espa�o em branco encontrado na linha
                return re.findall(r'\s+', line)[0]
        # Retorna uma string vazia se nenhum espa�o em branco for encontrado
        return ""

    def add_indentation(processed_function: str, blank_space: str):
        # Divide a string da fun��o processada em linhas
        linhas = processed_function.splitlines()
        # Adiciona um espa�o em branco especificado antes de cada linha
        linhas_com_espaco = [blank_space + linha for linha in linhas]
        # Une as linhas modificadas em uma �nica string, adicionando uma nova linha no final
        return '\n'.join(linhas_com_espaco) + "\n"

    def replace_with_indentation(original_content: str, marker: str, replacement: str):
        lines = original_content.split('\n')
        replaced_lines = []

        for line in lines:
            if marker in line:
                indentation_match = re.match(r'^(\s*)', line)
                if indentation_match:
                    indentation = indentation_match.group(1)
                    replacement_lines = replacement.split('\n')
                    if not replacement_lines[0].strip():
                        replacement_lines.pop(0)
                    if not replacement_lines[len(replacement_lines) -1].strip():
                        replacement_lines.pop(len(replacement_lines) -1)

                    indented_replacement = '\n'.join([indentation + line for line in replacement_lines])

                    replaced_lines.append(indented_replacement)
                else:
                    replaced_lines.append(replacement)
            else:
                replaced_lines.append(line)

        return '\n'.join(replaced_lines)

    @classmethod
    def get_folder_data(cls, folder_path: str, ignored_folders: list | tuple = [], ignored_file_types: list | tuple = ()):
        def process_folder(current_folder):
            folder_data = cls.FolderData(current_folder)
            for entry in scandir(current_folder):
                if entry.is_dir() and not entry.name.startswith('.') and entry.name not in ignored_folders:
                    subfolder_data = process_folder(cls.normalize_path(entry.path))
                    folder_data.subfolders.append(subfolder_data)
                elif entry.is_file() and not entry.name.lower().endswith(ignored_file_types) and not entry.name.endswith(ignored_file_types) and not entry.name.upper().endswith(ignored_file_types):
                    folder_data.files.append(cls.normalize_path(entry.path))
            return folder_data

        return process_folder(folder_path)

    @classmethod
    def get_project_data(cls, project_path: str, ignored_folders: list | tuple = [], ignored_file_types: list | tuple = ()):
        project_files = []

        # Get the directory of the project path
        folder_path = path.dirname(project_path)
        
        # Check if the project path exists
        if not path.exists(project_path):
            return None

        try:
            with open(project_path, "r") as solution_file:
                for line in solution_file:
                    # Check for lines containing file references
                    if any(line.strip().startswith(tag) for tag in ("<Compile", "<Content", 'Remove')):
                        # Combine the regex pattern to match both Include and Remove attributes
                        match = re.search(r'(?:Include|Remove)="([^"]+)"', line.strip())
                        if match:
                            relative_path = match.group(1)
                            file_name = path.basename(relative_path)
                            folder_name = path.basename(path.dirname(relative_path))
                            
                            if '*' not in file_name:
                                # Validate folder and file names
                                if (not folder_name.startswith('.') and folder_name not in ignored_folders and 
                                    not file_name.lower().endswith(tuple(ext.lower() for ext in ignored_file_types))):
                                    
                                    absolute_path = path.join(folder_path, relative_path)
                                    if cls.is_subpath(absolute_path, folder_path):
                                        if path.exists(absolute_path) and '\\.' not in cls.normalize_path(absolute_path):
                                            project_files.append(absolute_path)
        except Exception as e:
            print(f"Error reading project file: {e}")
            return None

        return cls.create_folder_structure(folder_path, project_files)
        
    @classmethod
    def get_solution_data(cls, solution_path : str, ignored_folders: list | tuple = [], ignored_file_types: list | tuple = ()) -> FolderData:
        folder_data =  cls.FolderData(solution_path)
        folder_data.name = folder_data.name.replace('.sln', '')
        try:
             projects = []

             with open(solution_path, 'r') as file:
                 content = file.read()

                 # Express�o regular para encontrar projetos no formato correto
                 pattern = r'Project\("\{.*?\}"\) = "(.*?)", "(.*?)", "(.*?)"'

                 # Encontrar todos os projetos no arquivo .sln
                 matches = re.findall(pattern, content)
            
                 for match in matches:
                     project_name = match[0]
                     project_file : str = match[1]
                     projects.append(cls.get_project_data(path.join(path.dirname(solution_path), project_file) , ignored_folders, ignored_file_types))
                     
             folder_data.subfolders = projects
        except Exception as e:
             print(f"Erro ao ler o arquivo .sln: {e}")

        for folder in folder_data.subfolders:
            if not folder.files:
                folder.files.append(path.join(folder.path, '.ignore.file'))

        return folder_data
    
    @classmethod
    def find_deepest_common_root(cls, list_path: list[str]) -> str:
        """
        Finds the deepest common root folder that can contain all files in the list.

        Args:
            list_path (List[str]): A list of file paths.

        Returns:
            str: The deepest common root folder.
        """
        # Normalize all paths
        normalized_paths = [cls.normalize_path(p) for p in list_path]

        # Split each path into its components
        split_paths = [p.split(sep) for p in normalized_paths]

        # Find the common prefix among all split paths
        common_path = sep.join(path.commonprefix(split_paths))

        # Ensure the common path is a directory (it could be a partial path)
        while not path.isdir(common_path) and common_path:
            common_path = path.dirname(common_path)

        return common_path

    @classmethod
    def create_folder_structure(cls, root_folder_path: str, list_path: list[str]) -> "FileUtils.FolderData":
        """
        Creates the folder structure based on the given paths.

        Args:
            root_folder_path (str): The provided root folder path.
            list_path (List[str]): A list of paths to determine the structure.

        Returns:
            FileUtils.FolderData: The root folder with the full folder structure.
        """
        list_path = [cls.normalize_path(_file) for _file in list_path]
        list_path = list(set(list_path))
       
        if not root_folder_path.strip():
            root_folder_path = cls.find_deepest_common_root(list_path)
        else:
            root_folder_path = cls.normalize_path(root_folder_path)

        # Create the root folder data object
        raiz = FileUtils.FolderData(root_folder_path)

        # Build the folder structure
        for arquivo in list_path:
            if path.isabs(arquivo):
                relative_path = path.relpath(arquivo, root_folder_path)
            else:
                relative_path = arquivo
            partes_caminho = relative_path.split(sep)
            pasta_atual = raiz

            for i, parte in enumerate(partes_caminho[:-1]):  # Ignore the file itself
                current_full_path = path.join(root_folder_path, *partes_caminho[: i + 1])
                pasta_encontrada = None

                # Check for an existing subfolder with the exact path
                for subpasta in pasta_atual.subfolders:
                    if subpasta.path == current_full_path:
                        pasta_encontrada = subpasta
                        break

                # Create a new folder if not found
                if pasta_encontrada is None:
                    pasta_encontrada = FileUtils.FolderData(current_full_path)
                    pasta_atual.subfolders.append(pasta_encontrada)

                pasta_atual = pasta_encontrada

            # Add the file to the current folder
            file_path = path.join(root_folder_path, *partes_caminho)
            if  not file_path.endswith('.ignore.file'):
                pasta_atual.files.append(cls.normalize_path(file_path))

        return raiz

    @classmethod
    def normalize_path(cls, file_path: str, root_folder_path: str = ""):
        # Check if root_folder_path is provided and file_path is not an absolute path
        if root_folder_path and not path.isabs(file_path):
            # Join root_folder_path and file_path to form an absolute path
            file_path = path.join(root_folder_path, file_path)

        # Normalize the path to remove extra slashes and convert to the system's format
        normalized_path = path.normpath(file_path)
        return normalized_path

    @classmethod
    def write_to_file(cls, file_path : str,  file_lines : list[str]):
         # Abre o arquivo no caminho especificado em modo de escrita
         # Utiliza codifica��o UTF-8 para suportar caracteres especiais
         with open(file_path, 'w', encoding='utf-8') as file:
             # Junta todas as linhas da lista em uma �nica string e escreve no arquivo
             file.write(''.join(file_lines))

    @classmethod
    def is_xml_or_html(cls, file_path : str ,content : str):
            if file_path.endswith(('.ui', '.html', 'xml', 'proj', 'proj.user', '.qrc', '.config'))   :
                return True
            try:
                etree.parse(content)
                return True
            except Exception:
                try:
                    html.parse(content)
                    return True
                except Exception:
                    return False
        
    @classmethod
    def is_json_file(cls, file_path : str ,content : str):
        if file_path.endswith('.json'):
            return True
        try:
            json.load(content)
            return True
        except ValueError:
            try:
                json.loads(content)
                return True        
            except ValueError:
                return False
        except Exception as e:
            return False

    class Scandir(object):

        def __init__(self, dirPath : str, ignore_folders = ['node_modules', '__pycache__'],  ignore_file_types: list | tuple = ()):
            self.dirPath = dirPath
            self.ignore_folders = ignore_folders
            self.ignore_file_types = tuple(ignore_file_types)
  
        def files(self, files_endswith : str | list[str] | tuple[str] | None = None):
            listWindowsPath : list[pathlib.WindowsPath] = []
            self._scandir_file(self.dirPath, files_endswith, listWindowsPath)
            return listWindowsPath

        def folders(self):
            listWindowsPath : list[pathlib.WindowsPath] = []
            self._scandir_folder(self.dirPath, listWindowsPath)
            return listWindowsPath

        def _scandir_file(self, dirPath : str, files_endswith : str | list[str] | tuple[str] | None, listWindowsPath : list):
            subfolders = []

            for entry in pathlib.Path(dirPath).iterdir():
                if entry.is_dir():
                    if not entry.name.startswith('.') and entry.name not in self.ignore_folders:
                        subfolders.append(entry)
                else:
                    if files_endswith:
                        if entry.name.endswith(files_endswith) and not entry.name.endswith(self.ignore_file_types):
                            listWindowsPath.append(entry)
                    else:
                        if not entry.name.endswith(self.ignore_file_types):
                            listWindowsPath.append(entry)

            # Recursivamente escaneia subpastas
            for subdir in subfolders[:]:
                self._scandir_file(subdir, files_endswith, listWindowsPath)


        def _scandir_folder(self, dirPath : str, listWindowsPath : list):
            subfolders = []

            for entry in pathlib.Path(dirPath).iterdir():
                if entry.is_dir():
                    if not entry.name.startswith('.') and entry.name not in self.ignore_folders:
                        subfolders.append(entry)
                        listWindowsPath.append(entry)
          
            # Recursivamente escaneia subpastas
            for subdir in subfolders[:]:
                self._scandir_folder(subdir, listWindowsPath)



        

