# -*- coding: latin -*-
import re, uuid
from .file_utils import FileUtils
from ...qt.text import DocumentTypeFile
from os import path
from pydantic import BaseModel, Field
from typing import Dict
import json
from typing_extensions import TypeAlias
from typing import Any

IncEx: TypeAlias = 'set[int] | set[str] | dict[int, Any] | dict[str, Any] | None'

class FunctionContext(BaseModel):
    name : str = Field("", description="")
    code : str = Field("", description="")
   
class PathFileContext(BaseModel):
     type : str = Field("", description="")
     content : str = Field("", description="")
     
class PathFolderContext(BaseModel):
     files : Dict[str, PathFileContext] = Field({}, description="")
     folders : Dict[str, "PathFolderContext"] = Field({}, description="")
     
class PathFileTreeContext(BaseModel):
     type : str = Field("", description="")

class TreeContext(BaseModel):
    files : Dict[str, PathFileTreeContext] = Field({}, description="")
    folders : Dict[str, "TreeContext"] = Field({}, description="")

class Context(object):

    def __init__(self, path_folder_context : PathFolderContext):
        self._context = path_folder_context
        self.files = path_folder_context.files
        self.folders = path_folder_context.folders

    def model_dump(self, exclude: IncEx = None, indent=4):
        context = self._context.model_dump(exclude=exclude)
        return json.dumps(context, indent=indent)
    
    def tree(self):
        def convert_to_tree_context(folder_context: PathFolderContext) -> TreeContext:
            tree_context = TreeContext()
            
            # Convert files
            for file_name, file_data in folder_context.files.items():
                tree_context.files[file_name] = PathFileTreeContext(type=file_data.type)
            
            # Convert folders
            for folder_name, subfolder_context in folder_context.folders.items():
                tree_context.folders[folder_name] = convert_to_tree_context(subfolder_context)
            
            return tree_context
        
        # Start conversion from the root context
        return convert_to_tree_context(self._context)
    
    def normalize_path(self, file_path):
        # Remove barras extras e converte para o formato padr�o do sistema operacional
        normalized_path = path.normpath(file_path)
        # Converte para absoluto
        absolute_path = path.abspath(normalized_path)
        return absolute_path

    def get_file_content(self, file_path: str) -> str:
        file_path = self.normalize_path(file_path)

        def _get_files_content(folder_context) -> str:
            # Adiciona arquivos no n�vel atual
            for file_name, file_data in folder_context.files.items():
                if file_path == self.normalize_path(file_name):
                    return file_data.content
        
            # Processa subpastas recursivamente
            for subfolder_path, subfolder_context in folder_context.folders.items():
                content = _get_files_content(subfolder_context)
                if content:  # Verifica se encontrou o conte�do
                    return content

            return ""  # Retorna vazio se nada for encontrado

        return _get_files_content(self._context)

class BaseFunctionData(object):

        def __init__(self, *, id : str, type_file : DocumentTypeFile, name : str, code : str):
            self.id = id
            self.type_file = type_file
            self.name = name
            self.code = code
            self.is_removed = False

class BaseFileData(object):

    class BaseFunctionData(BaseFunctionData):
        ...
    
    def __init__(self, path_file : str, is_directory : bool):
        self.is_directory = is_directory
        self.list_data : list[BaseFileData] = []
        self.parent : BaseFileData = None
        self.path_file = path_file.replace("\\", "/")
        self.file_name = path.basename(path_file)
        self.file_folder_name = path.join(path.basename(path.dirname(path_file)), self.file_name)
        self.type_file : DocumentTypeFile = None
        if self.file_name.endswith(".cs"):
            self.type_file = DocumentTypeFile.CSharp
        elif self.file_name.endswith(".py"):
            self.type_file = DocumentTypeFile.Python
        elif self.file_name.endswith(".vb"):
            self.type_file = DocumentTypeFile.VB

        self.functions : list[BaseFunctionData] = []
        self.original_content = ""
        self.content_with_ids = ""
        self.initialized = False

    def get_parent(self):
        if self.parent:
            return self.parent.get_parent()
        return self

    def __context_folder(self):
        files = {data.path_file : data.__context() for data in self.list_data if not data.is_directory}
        folders = {data.path_file : data.__context() for data in self.list_data if data.is_directory }
        return PathFolderContext(files=files, folders=folders)

    def __context(self):
        if self.is_directory:
            return self.__context_folder()
        else:
            #functions_context = {func.id : FunctionContext(name=func.name, code=func.code) for func in self.functions }
            return PathFileContext(type=self.type_file.name,content=self.original_content)
            #return PathFileContext(type=self.type_file.name, functions=functions_context, content=self.original_content, content_with_functions_ids=self.content_with_ids)

    def context(self):
        if self.is_directory:
            return Context(self.__context_folder())
        else:
            return Context(PathFolderContext(files={self.path_file : self.__context()}))
    
    def all_context(self):
         parent : BaseFileData = self.get_parent()
         return parent.context()
         

class FunctionDict:
    def __init__(self, unique : dict[str, BaseFileData.BaseFunctionData], duplicates : dict[str, BaseFileData.BaseFunctionData]):
        self.unique = unique
        self.duplicates = duplicates
        
class DataCodeFiles(object):

    class Build(object):

        class FunctionBuildData:
            def __init__(self, id : str, content : str, replace_with_indentation : bool):
                self.id = id
                self.content = content
                self.replace_with_indentation = replace_with_indentation

        @classmethod
        def content_with_ids(cls, content_with_ids : str,  functions_build_data : list[FunctionBuildData]):
            content = content_with_ids
            for function_data in functions_build_data:
                #if function_data.replace_with_indentation:
                updated_content = cls.replace_with_indentation(content, function_data.id, function_data.content)
                #else:
                #    updated_content = content.replace(function_data.id, function_data.content)
                content = updated_content
            return content

        @classmethod
        def replace_with_indentation(cls, original_content: str, marker: str, replacement: str):
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

    class BaseFileData(BaseFileData):
        ...

    @classmethod
    def update_file_data(cls, file_data : BaseFileData):
        if not file_data.initialized:
            if file_data.type_file == DocumentTypeFile.Python:
                cls.Python.extract(file_data)
            elif file_data.type_file == DocumentTypeFile.CSharp:
                cls.CSharp.extract(file_data)
            elif file_data.type_file == DocumentTypeFile.VB:
                cls.VB.extract(file_data)
                
    @classmethod     
    def update_content_with_ids(cls, content : str, file_data: BaseFileData):
            if file_data.type_file == DocumentTypeFile.Python:
                cls.Python.update_content_with_ids(content, file_data)
            elif file_data.type_file == DocumentTypeFile.CSharp:
                cls.CSharp.update_content_with_ids(content, file_data)
            elif file_data.type_file == DocumentTypeFile.VB:
                cls.VB.update_content_with_ids(content, file_data)

    @classmethod
    def split_code_by_uuid(cls, file_data : BaseFileData):
        # Regex pattern to match UUIDs
        uuid_pattern = re.compile(r"[a-f0-9\-]{36}")
    
        # Split the code into lines
        lines = file_data.content_with_ids.split('\n')
    
        parts : list[str] = []
        current_part = []
    
        for line in lines:
            if uuid_pattern.fullmatch(line.strip()):
                if current_part:
                    parts.append('\n'.join(current_part))
                    current_part = []
                parts.append(line)
            else:
                current_part.append(line)
    
        if current_part:
            parts.append('\n'.join(current_part))
    
        return [part for part in parts if part.strip()]

    @classmethod
    def is_valid_uuid(cls, uuid_string: str) -> bool:
        """
        Verifica se a string fornecida � um UUID v�lido.
    
        Args:
            uuid_string (str): A string a ser verificada.
        
        Returns:
            bool: True se a string for um UUID v�lido, False caso contr�rio.
        """

        # Regex pattern to match UUIDs
        uuid_pattern = re.compile(r"[a-f0-9\-]{36}")

        # Verifica se a string corresponde ao padr�o UUID
        return bool( uuid_pattern.fullmatch(uuid_string.strip()))

    def create_function_dict(functions : list[BaseFileData.BaseFunctionData]):
        unique = {}
        duplicates = {}

        function_names = set()  # Usado para verificar nomes duplicados
        functions_with_duplicate_names = set()  # Usado para armazenar nomes duplicados

        for function in functions:
            # Verifica se o nome da fun��o j� existe no conjunto
            if function.name not in function_names:
                # Adiciona a fun��o ao dicion�rio
                function_names.add(function.name)  # Adiciona o nome da fun��o ao conjunto
            else:
                functions_with_duplicate_names.add(function.name)

        for function in functions:
            if function.name in functions_with_duplicate_names:
                duplicates[function.name] = function
            else:
                unique[function.name] = function

        return FunctionDict(unique, duplicates)

    class Python(object):

        @classmethod
        def get_function_name(cls, text : str):
            function_name_regex = re.compile(r"def\s+(\w+)\s*\(", re.IGNORECASE)
            match = function_name_regex.search(text)
            if match:
                return match.group(1)
            return text
        
        @classmethod
        def update_content_with_ids(cls, content : str, file_data: BaseFileData):
            if content.strip():
                function_dict = DataCodeFiles.create_function_dict(file_data.functions)
                file_data.functions.clear()

                # Express�es regulares para corresponder a assinaturas de fun��es
                function_signature_regex = re.compile(r"^\s*(async\s+)?def\s+(\w+)\s*\(", re.IGNORECASE)
        
                file_lines = []  # Lista para armazenar as linhas do arquivo processado
                current_function_lines = []  # Lista para armazenar as linhas da fun��o atual sendo processada
       
                inside_function = False  # Flag para indicar se o processamento est� dentro de uma fun��o
                espaco_em_branco = ""  # Vari�vel para armazenar o espa�o em branco antes da defini��o da fun��o
                for line in FileUtils.create_text_io_wrapper_from_text(content):
                    if not inside_function:  # Se n�o estiver dentro de uma fun��o
                        match = function_signature_regex.match(line)  # Procura por uma assinatura de fun��o
                        if match: 
                            espacos_em_branco = re.findall(r'\s+', line)  # Encontra o espa�o em branco antes da fun��o
                            espaco_em_branco = espacos_em_branco[0]
                            inside_function = True  # Marca que est� dentro de uma fun��o
                            current_function_lines.append(line)  # Adiciona a linha � lista de linhas da fun��o atual
                        else:
                            file_lines.append(line)  # Se n�o for uma fun��o, adiciona a linha ao arquivo processado
                    else:  # Se estiver dentro de uma fun��o
                        _espaco_em_branco = re.findall(r'\s+', line)[0]  # Encontra o espa�o em branco da linha atual
                        if _espaco_em_branco > espaco_em_branco or not line.replace("\n", "").strip():  # Se a linha pertencer � fun��o atual
                            current_function_lines.append(line)
                        else:  # Se a linha n�o pertencer � fun��o atual
                            inside_function = False  # Marca que saiu da fun��o
                            espacos_em_branco = re.findall(r'\s+', current_function_lines[0])  # Encontra o espa�o em branco antes da fun��o
                            espaco_em_branco = ""
                            if espacos_em_branco:
                                espaco_em_branco = espacos_em_branco[0]

                            function_name = cls.get_function_name(current_function_lines[0])
                            code = ''.join(current_function_lines).strip() 
                            function_data = function_dict.unique.get(function_name)
                            if function_data:
                                function_id = function_data.id
                                function_data.code = code
                            else:
                                function_id = uuid.uuid4().__str__()
                                function_data = file_data.BaseFunctionData(id=function_id, type_file=file_data.type_file,name=function_name, code=code)
                            file_data.functions.append(function_data)
                      
                            file_lines.extend(FileUtils.adjust_text_length(function_id, len(espaco_em_branco)) + "\n\n")  # Adiciona a fun��o processada ao arquivo
                    
                            current_function_lines = []  # Reseta a lista de linhas da fun��o atual
    
                            match = function_signature_regex.match(line)  # Verifica se a linha atual � uma nova fun��o
                            if match:  # Se for uma nova fun��o
                                espacos_em_branco = re.findall(r'\s+', line)
                                espaco_em_branco = espacos_em_branco[0]
                                inside_function = True  # Marca que est� dentro de uma fun��o
                                current_function_lines.append(line)  # Adiciona a linha � lista de linhas da fun��o atual
                            else:
                                file_lines.append(line)  # Se n�o for uma fun��o, adiciona a linha ao arquivo processado
    
                if current_function_lines:  # Se ainda houver linhas da fun��o atual n�o processadas
            
                    espacos_em_branco = re.findall(r'\s+', current_function_lines[0])  # Encontra o espa�o em branco antes da fun��o
                    espaco_em_branco = ""
                    if espacos_em_branco:
                        espaco_em_branco = espacos_em_branco[0]

                    function_name = cls.get_function_name(current_function_lines[0])
                    code = ''.join(current_function_lines).strip()
                    function_data = function_dict.unique.get(function_name)
                    if function_data:
                        function_id = function_data.id
                        function_data.code = code
                    else:
                        function_id = uuid.uuid4().__str__()
                        function_data = file_data.BaseFunctionData(id=function_id, type_file=file_data.type_file, name=function_name, code=code)
                    file_data.functions.append(function_data)
              
                    file_lines.extend(FileUtils.adjust_text_length(function_id, len(espaco_em_branco)) + "\n\n")  # Adiciona a fun��o processada ao arquivo
                    
                file_data.content_with_ids = ''.join(file_lines)

        @classmethod
        def extract(cls, file_data: BaseFileData):
            file_data.initialized = True

            function_dict = DataCodeFiles.create_function_dict(file_data.functions)
            file_data.functions.clear()

            # Express�es regulares para corresponder a assinaturas de fun��es
            function_signature_regex = re.compile(r"^\s*(async\s+)?def\s+(\w+)\s*\(", re.IGNORECASE)
        
            file_lines = []  # Lista para armazenar as linhas do arquivo processado
            current_function_lines = []  # Lista para armazenar as linhas da fun��o atual sendo processada
            original_content = []

            content = FileUtils.read_file(file_data.path_file)  # L� o conte�do do arquivo
            if content == None:  # Se o conte�do for None, retorna None
                return file_data

            inside_function = False  # Flag para indicar se o processamento est� dentro de uma fun��o
            espaco_em_branco = ""  # Vari�vel para armazenar o espa�o em branco antes da defini��o da fun��o
            for line in content:
                original_content.append(line)
                if not inside_function:  # Se n�o estiver dentro de uma fun��o
                    match = function_signature_regex.match(line)  # Procura por uma assinatura de fun��o
                    if match: 
                        espacos_em_branco = re.findall(r'\s+', line)  # Encontra o espa�o em branco antes da fun��o
                        espaco_em_branco = espacos_em_branco[0]
                        inside_function = True  # Marca que est� dentro de uma fun��o
                        current_function_lines.append(line)  # Adiciona a linha � lista de linhas da fun��o atual
                    else:
                        file_lines.append(line)  # Se n�o for uma fun��o, adiciona a linha ao arquivo processado
                else:  # Se estiver dentro de uma fun��o
                    _espaco_em_branco = re.findall(r'\s+', line)[0]  # Encontra o espa�o em branco da linha atual
                    if _espaco_em_branco > espaco_em_branco or not line.replace("\n", "").strip():  # Se a linha pertencer � fun��o atual
                        current_function_lines.append(line)
                    else:  # Se a linha n�o pertencer � fun��o atual
                        inside_function = False  # Marca que saiu da fun��o
                        espacos_em_branco = re.findall(r'\s+', current_function_lines[0])  # Encontra o espa�o em branco antes da fun��o
                        espaco_em_branco = ""
                        if espacos_em_branco:
                            espaco_em_branco = espacos_em_branco[0]

                        function_name = cls.get_function_name(current_function_lines[0])
                        code = ''.join(current_function_lines).strip() 
                        function_data = function_dict.unique.get(function_name)
                        if function_data:
                            function_id = function_data.id
                            function_data.code = code
                        else:
                            function_id = uuid.uuid4().__str__()
                            function_data = file_data.BaseFunctionData(id=function_id, type_file=file_data.type_file,name=function_name, code=code)
                        file_data.functions.append(function_data)
                      
                        file_lines.extend(FileUtils.adjust_text_length(function_id, len(espaco_em_branco)) + "\n\n")  # Adiciona a fun��o processada ao arquivo
                    
                        current_function_lines = []  # Reseta a lista de linhas da fun��o atual
    
                        match = function_signature_regex.match(line)  # Verifica se a linha atual � uma nova fun��o
                        if match:  # Se for uma nova fun��o
                            espacos_em_branco = re.findall(r'\s+', line)
                            espaco_em_branco = espacos_em_branco[0]
                            inside_function = True  # Marca que est� dentro de uma fun��o
                            current_function_lines.append(line)  # Adiciona a linha � lista de linhas da fun��o atual
                        else:
                            file_lines.append(line)  # Se n�o for uma fun��o, adiciona a linha ao arquivo processado
    
            if current_function_lines:  # Se ainda houver linhas da fun��o atual n�o processadas
            
                espacos_em_branco = re.findall(r'\s+', current_function_lines[0])  # Encontra o espa�o em branco antes da fun��o
                espaco_em_branco = ""
                if espacos_em_branco:
                    espaco_em_branco = espacos_em_branco[0]

                function_name = cls.get_function_name(current_function_lines[0])
                code = ''.join(current_function_lines).strip()
                function_data = function_dict.unique.get(function_name)
                if function_data:
                    function_id = function_data.id
                    function_data.code = code
                else:
                    function_id = uuid.uuid4().__str__()
                    function_data = file_data.BaseFunctionData(id=function_id, type_file=file_data.type_file, name=function_name, code=code)
                file_data.functions.append(function_data)
              
                file_lines.extend(FileUtils.adjust_text_length(function_id, len(espaco_em_branco)) + "\n\n")  # Adiciona a fun��o processada ao arquivo
                    
            file_data.content_with_ids = ''.join(file_lines)
            file_data.original_content = ''.join(original_content)

            return file_data
    
    class VB(object):

        FUNCTION_SIGNATURE_REGEX = re.compile(r"^\s*(Public|Private|Protected)?\s*(Overrides)?\s*(Shared)?\s*(Async)?\s*Function\s+(\w+)", re.IGNORECASE)
        FUNCTION_END = re.compile(r"^\s*End Function", re.IGNORECASE)

        SUB_SIGNATURE_REGEX = re.compile(r"^\s*(Public|Private|Protected)?\s*(Overrides)?\s*(Shared)?\s*(Async)?\s*Sub\s+(\w+)", re.IGNORECASE)
        SUB_END = re.compile(r"^\s*End Sub", re.IGNORECASE)

        @classmethod
        def extract_name_from_signature(cls, signature):
            match = cls.FUNCTION_SIGNATURE_REGEX.match(signature)
            if match:
                return match.group(5)  # Group 5 captures the function name
            else:
                match = cls.SUB_SIGNATURE_REGEX.match(signature)
                if match:
                    return match.group(5)  # Group 5 captures the subroutine name
                else:
                    return "" 

        @classmethod
        def extract_summaries_with_id(cls, code: str):
            # Regex para capturar summaries e ids
            summary_pattern = re.compile(r"''' <summary>(.*?)'''", re.DOTALL)
            id_pattern = re.compile(r"[a-f0-9\-]{36}")

            # Dividir o c�digo em linhas para processamento
            lines = code.split('\n')

            summaries_with_ids = []

            for i in range(len(lines) - 1):
                summary_match = summary_pattern.search(lines[i])
                if summary_match:
                    summary = summary_match.group(1).strip()
                    next_line = lines[i + 1].strip()
                    if id_pattern.fullmatch(next_line):
                        summaries_with_ids.append({
                            "summary": summary,
                            "id": next_line
                        })

            return summaries_with_ids
        
        @classmethod
        def update_content_with_ids(cls, content : str, file_data: BaseFileData):
            if content.strip():
                function_dict = DataCodeFiles.create_function_dict(file_data.functions)
                file_data.functions.clear()

                # Lista para armazenar as linhas da fun��o atual
                current_function_lines = []
                file_lines = []

                for line in FileUtils.create_text_io_wrapper_from_text(content):
                    # Se n�o estiver processando uma fun��o, procura por uma nova fun��o
                    if not current_function_lines:
                        func_match = cls.FUNCTION_SIGNATURE_REGEX.match(line)
                        sub_match = cls.SUB_SIGNATURE_REGEX.match(line)
                        if func_match or sub_match:
                            # Inicia o armazenamento das linhas da fun��o atual
                            current_function_lines.append(line)
                        else:
                            # Se n�o for uma fun��o, adiciona a linha diretamente ao arquivo final
                            file_lines.append(line)
                    else:
                        # Continua armazenando as linhas da fun��o atual
                        current_function_lines.append(line)
                        # Se encontrar o fim da fun��o, processa as linhas acumuladas
                        if cls.FUNCTION_END.match(line) or cls.SUB_END.match(line):
                            function_body = ''.join(current_function_lines)
                   
                            function_lines = current_function_lines.copy()
                            function_lines[len(function_lines) - 1] = function_lines[len(function_lines) - 1].strip()
                            code = ''.join(function_lines).strip()
                            function_name = cls.extract_name_from_signature(current_function_lines[0])
                            function_data = function_dict.unique.get(function_name)
                            if function_data:
                                function_id = function_data.id
                                function_data.code = code
                            else:
                                function_id = uuid.uuid4().__str__()
                                function_data = file_data.BaseFunctionData(id=function_id, type_file=file_data.type_file,name=function_name, code=code)
                        
                            file_data.functions.append(function_data)
                       
                            # Obt�m o espa�o em branco necess�rio para a indenta��o
                            blank_space = FileUtils.get_blank_space(function_body)
                            file_lines.extend(f"\n{FileUtils.adjust_text_length(function_id, len(blank_space))}")  # Adiciona a fun��o processada ao arquivo
                        
                            current_function_lines = []  # Reseta a lista tempor�ria para a pr�xima fun��o

                file_data.content_with_ids = ''.join(file_lines)
                

        @classmethod
        def extract(cls, file_data: BaseFileData):
            file_data.initialized = True
            # L� o conte�do do arquivo

            function_dict = DataCodeFiles.create_function_dict(file_data.functions)
            file_data.functions.clear()

            content = FileUtils.read_file(file_data.path_file)
            # Se o conte�do for None, retorna um dicion�rio vazio
            if content is None:
                return file_data
    
            # Lista para armazenar as linhas da fun��o atual
            current_function_lines = []
            file_lines = []
            original_content = []
            for line in content:
                original_content.append(line)
                # Se n�o estiver processando uma fun��o, procura por uma nova fun��o
                if not current_function_lines:
                    func_match = cls.FUNCTION_SIGNATURE_REGEX.match(line)
                    sub_match = cls.SUB_SIGNATURE_REGEX.match(line)
                    if func_match or sub_match:
                        # Inicia o armazenamento das linhas da fun��o atual
                        current_function_lines.append(line)
                    else:
                        # Se n�o for uma fun��o, adiciona a linha diretamente ao arquivo final
                        file_lines.append(line)
                else:
                    # Continua armazenando as linhas da fun��o atual
                    current_function_lines.append(line)
                    # Se encontrar o fim da fun��o, processa as linhas acumuladas
                    if cls.FUNCTION_END.match(line) or cls.SUB_END.match(line):
                        function_body = ''.join(current_function_lines)
                   
                        function_lines = current_function_lines.copy()
                        function_lines[len(function_lines) - 1] = function_lines[len(function_lines) - 1].strip()
                        code = ''.join(function_lines).strip()
                        function_name = cls.extract_name_from_signature(current_function_lines[0])
                        function_data = function_dict.unique.get(function_name)
                        if function_data:
                            function_id = function_data.id
                            function_data.code = code
                        else:
                            function_id = uuid.uuid4().__str__()
                            function_data = file_data.BaseFunctionData(id=function_id, type_file=file_data.type_file,name=function_name, code=code)
                        
                        file_data.functions.append(function_data)
                       
                        # Obt�m o espa�o em branco necess�rio para a indenta��o
                        blank_space = FileUtils.get_blank_space(function_body)
                        file_lines.extend(f"\n{FileUtils.adjust_text_length(function_id, len(blank_space))}")  # Adiciona a fun��o processada ao arquivo
                        
                        current_function_lines = []  # Reseta a lista tempor�ria para a pr�xima fun��o

    
            file_data.content_with_ids = ''.join(file_lines)
            file_data.original_content = ''.join(original_content)

            return file_data
    
    class CSharp(object):

        @classmethod
        def extract_name_from_pattern(cls, signature):
            pattern = r"^\s*(?:public|private|protected|static|internal|public\s+override|protected\s+internal)?\s+(?:[\w\<\>\[\]]+\s+)+(\w+)\s*\((.*?)\)"
            match = re.match(pattern, signature)
            if match:
                return match.group(1)  # O grupo atualizado para capturar o nome da fun��o
            else:
                return ""  # Sem correspond�ncia encontrada

        @classmethod
        def in_range(cls, interval_list, tuple_to_check):
            for interval in interval_list:
                if interval[0] == tuple_to_check[0] and interval[1] == tuple_to_check[1]:
                    return True
            return False

        @classmethod
        def remove_enclosed_intervals(cls, interval_list):
            intervals_to_remove = []

            # Iterate over each interval in the list
            for i, interval1 in enumerate(interval_list):
                for j, interval2 in enumerate(interval_list):
                    if i != j:  # Ensure we're not comparing the same interval
                        # Check if interval1 is enclosed within interval2
                        if interval2[0] <= interval1[0] <= interval1[1] <= interval2[1]:
                            intervals_to_remove.append(interval1)
                            break  # No need to continue checking with other intervals

            # Remove the enclosed intervals from the original list
            for interval in intervals_to_remove:
                interval_list.remove(interval)

            return interval_list
        
        @classmethod
        def update_content_with_ids(cls, content : str, file_data: BaseFileData):
            if content.strip():
                content = FileUtils.create_text_io_wrapper_from_text(content).read()
                function_dict = DataCodeFiles.create_function_dict(file_data.functions)
                file_data.functions.clear()
      
                # Padr�o regex para identificar o in�cio das fun��es no arquivo C#
                pattern = r"(public|private|protected|static|internal|public\s+override|protected\s+internal)?\s+([\w\<\>\[\]]+\s+[\w\<\>\[\]]+)\s+(\w+)\s*\((.*?)\)\s*(?:=>|{)"
                # Encontra todas as correspond�ncias do padr�o no conte�do do arquivo
                function_starts = [(m.start(0), m.end(0)) for m in re.finditer(pattern, content)]

                ranges = []
                cursor = 0
                # Itera sobre cada fun��o encontrada
                for start, end in function_starts:
                    # Verifica se existe um prompt de controle e se a opera��o deve ser interrompida
    
                    brace_count = 1
                    cursor = end
    
                    # Conta as chaves para encontrar o final da fun��o
                    while brace_count > 0 and cursor < len(content):
                        if content[cursor] == '{':
                            brace_count += 1
                        elif content[cursor] == '}':
                            brace_count -= 1
    
                        cursor += 1

                    ranges.append((start,cursor))

                ranges = cls.remove_enclosed_intervals(ranges)
           
                cursor = 0
                annotated_content = ""

                # Itera sobre cada fun��o encontrada
                for start, end in function_starts:
                    # Verifica se existe um prompt de controle e se a opera��o deve ser interrompida
    
                    # Anexa o conte�do que n�o faz parte de nenhuma fun��o
                    annotated_content += content[cursor:start]
    
                    brace_count = 1
                    cursor = end
    
                    # Conta as chaves para encontrar o final da fun��o
                    while brace_count > 0 and cursor < len(content):
                        if content[cursor] == '{':
                            brace_count += 1
                        elif content[cursor] == '}':
                            brace_count -= 1
    
                        cursor += 1
    
                    if cls.in_range(ranges, (start,cursor)):
                        # Extrai o corpo da fun��o
                        function_body = content[start:cursor]
                 
                        # Obt�m o espa�o em branco necess�rio para a indenta��o
                        blank_space = FileUtils.get_blank_space(function_body)

                        # Adiciona a indenta��o necess�ria
                        annotated_function = function_body #add_indentation(function_body, blank_space)

                        function_name = cls.extract_name_from_pattern(annotated_function)
                        if function_name.strip() not in ["catch", "if", "foreach", "else", "while"]:
                            if function_name.strip():
                                code = annotated_function.rstrip() 
                                function_data = function_dict.unique.get(function_name)
                                if function_data:
                                    function_id = function_data.id
                                    function_data.code = code
                                else:
                                    function_id = uuid.uuid4().__str__()
                                    function_data = file_data.BaseFunctionData(id=function_id, type_file=file_data.type_file,name=function_name, code=code)
                    
                                file_data.functions.append(function_data)

                                # Anexa a fun��o processada ao conte�do anotado
                                annotated_content += f"\n{FileUtils.adjust_text_length(function_id, len(blank_space))}"

                # Anexa qualquer conte�do restante ap�s a �ltima fun��o
                last = content[cursor:]
                file_data.content_with_ids = f'{annotated_content} {last}'
            
        @classmethod
        def extract(cls, file_data: BaseFileData):
            file_data.initialized = True
            # L� o conte�do do arquivo

            function_dict = DataCodeFiles.create_function_dict(file_data.functions)
            file_data.functions.clear()
      
            content = FileUtils.read_file(file_data.path_file)
            # Se o conte�do for None, retorna um dicion�rio vazio
            if content is None:
                return file_data
            
            content = content.read()

            # Padr�o regex para identificar o in�cio das fun��es no arquivo C#
            pattern = r"(public|private|protected|static|internal|public\s+override|protected\s+internal)?\s+([\w\<\>\[\]]+\s+[\w\<\>\[\]]+)\s+(\w+)\s*\((.*?)\)\s*(?:=>|{)"
            # Encontra todas as correspond�ncias do padr�o no conte�do do arquivo
            function_starts = [(m.start(0), m.end(0)) for m in re.finditer(pattern, content)]

            ranges = []
            cursor = 0
            # Itera sobre cada fun��o encontrada
            for start, end in function_starts:
                # Verifica se existe um prompt de controle e se a opera��o deve ser interrompida
    
                brace_count = 1
                cursor = end
    
                # Conta as chaves para encontrar o final da fun��o
                while brace_count > 0 and cursor < len(content):
                    if content[cursor] == '{':
                        brace_count += 1
                    elif content[cursor] == '}':
                        brace_count -= 1
    
                    cursor += 1

                ranges.append((start,cursor))

            ranges = cls.remove_enclosed_intervals(ranges)
           
            cursor = 0
            annotated_content = ""

            # Itera sobre cada fun��o encontrada
            for start, end in function_starts:
                # Verifica se existe um prompt de controle e se a opera��o deve ser interrompida
    
                # Anexa o conte�do que n�o faz parte de nenhuma fun��o
                annotated_content += content[cursor:start]
    
                brace_count = 1
                cursor = end
    
                # Conta as chaves para encontrar o final da fun��o
                while brace_count > 0 and cursor < len(content):
                    if content[cursor] == '{':
                        brace_count += 1
                    elif content[cursor] == '}':
                        brace_count -= 1
    
                    cursor += 1
    
                if cls.in_range(ranges, (start,cursor)):
                    # Extrai o corpo da fun��o
                    function_body = content[start:cursor]
                 
                    # Obt�m o espa�o em branco necess�rio para a indenta��o
                    blank_space = FileUtils.get_blank_space(function_body)

                    # Adiciona a indenta��o necess�ria
                    annotated_function = function_body #add_indentation(function_body, blank_space)

                    function_name = cls.extract_name_from_pattern(annotated_function)
                    if function_name.strip() not in ["catch", "if", "foreach", "else", "while"]:
                        if function_name.strip():
                            code = annotated_function.rstrip() 
                            function_data = function_dict.unique.get(function_name)
                            if function_data:
                                function_id = function_data.id
                                function_data.code = code
                            else:
                                function_id = uuid.uuid4().__str__()
                                function_data = file_data.BaseFunctionData(id=function_id, type_file=file_data.type_file,name=function_name, code=code)
                    
                            file_data.functions.append(function_data)

                            # Anexa a fun��o processada ao conte�do anotado
                            annotated_content += f"\n{FileUtils.adjust_text_length(function_id, len(blank_space))}"

            # Anexa qualquer conte�do restante ap�s a �ltima fun��o
            last = content[cursor:]
            file_data.content_with_ids = f'{annotated_content} {last}'
            file_data.original_content = content

            return file_data

        




