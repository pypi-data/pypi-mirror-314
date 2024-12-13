
from datamodel_code_generator import DataModelType, PythonVersion
from datamodel_code_generator.model import get_data_model_types
from datamodel_code_generator.parser.jsonschema import JsonSchemaParser
import random, string
from pydantic import BaseModel, Field, create_model, AnyUrl, EmailStr
from typing import List, Any, Type, Union, Optional, Dict, get_args, get_origin
from datetime import date, datetime, time, timedelta
import json
from pydantic_core import PydanticUndefined
import tree_sitter_languages
import re

class PydanticUtils(object):

     class DataModel(BaseModel):
          name : str = Field("", description="")
          source_code : str = Field("", description="")
          source_model_classes : str = Field("", description="")
          main_class : Union[Type[BaseModel], None] = Field(None, description="")


     BASIC_TYPE_MAP = {
          # Tipos básicos do Python
          "string": str,
          "int": int,
          "integer": int,
          "float": float,
          "bool": bool,
          "boolean": bool,
          "none": type(None),  # NoneType para valores nulos
          "any": Any,  # aceita qualquer tipo

          # Tipos numéricos especializados
          "decimal": float,  # normalmente para representar decimais com precisão

          # Tipos complexos e coleções do Python
          "list": list,
          "array": list,
          "dict": dict,
          "dictionary": dict,
          "tuple": tuple,
          "set": set,
          "frozenset": frozenset,

          # Tipos de string especializados
          "date": date,  # datas no formato string (ex: "2023-01-01")
          "time": time,  # horas no formato string (ex: "13:45:30")
          "date-time": datetime,  # timestamps ISO 8601 (ex: "2023-01-01T00:00:00Z")
          "timedelta": timedelta,  # duração/intervalo de tempo
          "uri": AnyUrl,  # URLs válidas
          "email": EmailStr,  # e-mails válidos
          
          # Outros tipos avançados e comuns
          "object": dict,  # frequentemente usado para qualquer objeto JSON
          "null": type(None),  # nulo (null)
          "uuid": str,  # usado para UUIDs em JSON, pode ser validado
          "binary": bytes,  # para dados binários
          "number": float,  # cobre qualquer número
          "integer": int

          }
     
     @classmethod
     def get_base_model_classes(cls, code_str: str) -> str:
          parser = tree_sitter_languages.get_parser('python')
          # Parse o código fornecido
          tree = parser.parse(bytes(code_str, "utf8"))
          root_node = tree.root_node

          base_model_classes = []

          # Função para verificar se a classe herda de BaseModel
          def is_base_model_class(class_node):
               for child in class_node.children:
                    if child.type == "argument_list":
                         # Verificar se "BaseModel" está na lista de argumentos (herança)
                         if "BaseModel" in code_str[child.start_byte:child.end_byte]:
                              return True
               return False

          # Percorrer a árvore de sintaxe para encontrar definições de classes
          for node in root_node.children:
               if node.type == "class_definition":
                    class_name = node.child_by_field_name("name")
                    if class_name and is_base_model_class(node):
                         # Extrair o código da classe inteira
                         class_code = code_str[node.start_byte:node.end_byte]
                         base_model_classes.append(class_code)

          # Concatenar todas as classes em uma única string
          return "\n\n".join(base_model_classes)

     @classmethod
     def get_model_json_schema_from_code(cls, code_str: str):
          try:
               match = re.findall(r'class\s+(\w+)\s*\(\s*BaseModel\s*\)\s*:', code_str)
                
               # Se não houver uma classe que herda de BaseModel, retorna erro
               if not match:
                    return {'error': "No BaseModel subclass found in the provided code."}
               
               last_class_name = match[-1]

               # Prepare and execute the code with necessary imports
               code_str = f'''from __future__ import annotations
from typing import *
from pydantic import *
{code_str}
            '''
                # Define um dicionário de contexto com os imports necessários
               context = {}
                
                # Executa o código no contexto definido
               exec(code_str.strip(), context)

               last_class = context.get(last_class_name)

               if last_class and issubclass(last_class, BaseModel):
                    # Check if the model_json_schema function exists in the last class
                    if hasattr(last_class, 'model_json_schema'):
                         return {'model_json_schema': last_class.model_json_schema()}
                    else:
                         return {'error': 'model_json_schema function is not defined in the last BaseModel class'}
               else:
                    return {'error': 'No class inheriting from BaseModel found'}

          except SyntaxError as e:
               return {'error': f'Syntax error in the provided code: {e}'}
          except NameError as e:
               return {'error': f'Name error: {e}'}
          except Exception as e:
               return {'error': f'An unexpected error occurred: {e}'}

     @classmethod
     def create_data_model_from_json_schema(cls, model_json_schema: Union[str, dict]):
          # Se o JSON Schema for um dicionário, converta para uma string JSON
          try:
               dict_model_json_schema = model_json_schema
               if isinstance(model_json_schema, dict):
                    model_json_schema = json.dumps(model_json_schema)
               elif isinstance(model_json_schema, str):
                    dict_model_json_schema = json.loads(model_json_schema)
               else:
                    return PydanticUtils.DataModel()

               if not model_json_schema.strip():
                    return PydanticUtils.DataModel()
               
               # Configurar os tipos de modelo de dados para Pydantic
               data_model_types = get_data_model_types(
                    DataModelType.PydanticV2BaseModel,
                    PythonVersion.PY_311,
                    None
               )
               
               # Inicializar o parser com o JSON Schema
               parser = JsonSchemaParser(
                    model_json_schema,
                    data_model_type=data_model_types.data_model,
                    data_model_root_type=data_model_types.root_model,
                    data_model_field_type=data_model_types.field_model,
                    data_type_manager_type=data_model_types.data_type_manager,
                    dump_resolve_reference_action=data_model_types.dump_resolve_reference_action,
                         )
               
               # Gerar o código fonte da classe
               source_code = parser.parse()
               
               # Criar um namespace para a execução do código
               namespace = {}
               exec(source_code, namespace)  # Executa o código fonte no namespace

               source_model_classes = cls.get_base_model_classes(source_code)
               
               # Identificar a classe BaseModel gerada (presume-se que seja a única derivada de BaseModel)
               name = dict_model_json_schema.get('title')
               model_class : BaseModel = namespace.get(name)
               # Retornar a classe e o código fonte
               return PydanticUtils.DataModel(name=name, source_code=source_code, main_class=model_class, source_model_classes=source_model_classes)
          except:
               return PydanticUtils.DataModel()
     
     @classmethod
     def generate_fake_instance(cls, model: Type[BaseModel]) -> BaseModel:
          def fake_data(field_type: Any) -> Any:
               # Verifica se field_type é uma classe antes de tentar usar issubclass
               if isinstance(field_type, type):
                    if issubclass(field_type, BaseModel):
                         return cls.generate_fake_instance(field_type)
                    elif field_type == str:
                         return ''.join(random.choices(string.ascii_letters + string.digits, k=10))
                    elif field_type == int:
                         return random.randint(1, 100)
                    elif field_type == float:
                         return round(random.uniform(1, 5), 2)
                    elif field_type == bool:
                         return random.choice([True, False])
                    elif field_type == list:
                         return []
               # Verifica se field_type é um tipo genérico, como List ou Optional
               origin = get_origin(field_type)
               if origin is list:
                    item_type = get_args(field_type)[0]
                    return [fake_data(item_type) for _ in range(3)]
               elif origin is Optional:
                    return fake_data(get_args(field_type)[0])

               return None
          
     @classmethod
     def generate_model_code(cls, model: Type[BaseModel]) -> str:
          """Generate source code for a model and all its dependencies."""
          related_models = cls.get_all_related_classes(model)
          related_models.append(model)  # Include the main model at the end
          code = ""

          for model_class in related_models:
               code += f"class {model_class.__name__}(BaseModel):\n"
               for field_name, field in model_class.model_fields.items():
                    # Obtemos o tipo e a descrição diretamente do campo
                    field_type = field.annotation
                    if 'typing' in str(field_type):
                         origin = get_origin(field_type)
                         args = get_args(field_type)
                         field_type_name = str(field_type).replace('typing.', '')
                    else:
                         field_type_name = field_type.__name__
               
                    # Definimos o campo com Field(...)
                    code += f"    {field_name}: {field_type_name} = Field("
                    if field.default is not None and field.default != PydanticUndefined:
                         code += f"{field.default}"
                    else:
                         code += "..."
                    # Acessamos a descrição diretamente
                    description = getattr(field, "description", "")
                    code += f", description=\"{description}\")\n"
               code += "\n"

          return code
     
     @classmethod
     def get_all_related_classes(cls, model: Type[BaseModel]) -> List[Type[BaseModel]]:
          """Recursively get all related models used within the given model."""
          related_models = []
          for field_name, field in model.model_fields.items():
               field_type = field.annotation
               # Check if the type is a BaseModel or a list of BaseModel subclasses
               if hasattr(field_type, "__origin__") and field_type.__origin__ is list:
                    sub_model = field_type.__args__[0]
                    if issubclass(sub_model, BaseModel) and sub_model not in related_models:
                         related_models.extend(cls.get_all_related_classes(sub_model))
                         related_models.append(sub_model)
               elif isinstance(field_type, type) and issubclass(field_type, BaseModel):
                    if field_type not in related_models:
                         related_models.extend(cls.get_all_related_classes(field_type))
                         related_models.append(field_type)
          return related_models
     
     @classmethod
     def create_pydantic_model_from_json_schema(cls, klass: str, schema: Dict[str, Any], defs: Optional[Dict[str, Any]] = None) -> Type[BaseModel]:
          """
          Função recursiva para criar um modelo Pydantic a partir de um schema JSON.
          """
          fields = {}
          defs = defs or schema.get("$defs", {})

          for prop_name, prop_info in schema["properties"].items():
               field_type = prop_info.get("type", "default")

               # Verificar se o tipo do campo é `anyOf`
               if field_type == "default":
                    any_of = prop_info.get("anyOf", [])
                    if any_of:
                         field_type = "anyOf"

               # Processar tipo do campo
               py_type = None
               if field_type == "anyOf":
                    types = []
                    for item in prop_info.get("anyOf", []):
                         item_type = item.get("type", "object")
                         
                         # Lidar com objetos dentro de anyOf
                         if item_type == "object":
                              ref = item.get("$ref", "").split("/")[-1]
                              if ref and ref in defs:
                                   types.append(cls.create_pydantic_model_from_json_schema(ref, defs[ref], defs))
                              else:
                                   types.append(Dict[str, Any])  # Quando não há referência ou tipo
                         elif item_type == "array":
                              items = item.get("items", {})
                              item_subtype = items.get("type", "object")
                              if item_subtype == "object" and "$ref" in items:
                                   ref = items["$ref"].split("/")[-1]
                                   if ref in defs:
                                        types.append(List[cls.create_pydantic_model_from_json_schema(ref, defs[ref], defs)])
                                   else:
                                        types.append(List[Dict[str, Any]])
                              else:
                                   types.append(List[cls.BASIC_TYPE_MAP.get(item_subtype, Any)])
                         else:
                              types.append(cls.BASIC_TYPE_MAP.get(item_type, Any))

                    if types:
                         py_type = Union[tuple(types)]
                    else:
                         py_type = Any  # Caso não tenha nenhum tipo válido

               elif field_type == "array":
                    items = prop_info["items"]
                    item_type = items.get("type", "object")
                    if item_type == "object" and "$ref" in items:
                         ref = items["$ref"].split("/")[-1]
                         if ref in defs:
                              py_type = List[cls.create_pydantic_model_from_json_schema(ref, defs[ref], defs)]
                         else:
                              py_type = List[Dict[str, Any]]
                    else:
                         py_type = List[cls.BASIC_TYPE_MAP.get(item_type, Any)]
               
               elif field_type == "object":
                    if "$ref" in prop_info:
                         ref = prop_info["$ref"].split("/")[-1]
                         if ref in defs:
                              py_type = cls.create_pydantic_model_from_json_schema(ref, defs[ref], defs)
                         else:
                              py_type = Dict[str, Any]
                    else:
                         py_type = Dict[str, Any]
               
               elif field_type in cls.BASIC_TYPE_MAP:
                    py_type = cls.BASIC_TYPE_MAP[field_type]
               
               if not py_type:
                    raise Exception(f"Error, None for {field_type} in {prop_name}")

               # Configurar o campo do modelo
               default = prop_info.get("default") if "default" in prop_info else ...
               description = prop_info.get("description", "")
               fields[prop_name] = (py_type, Field(default, description=description))

          # Criar e retornar o modelo Pydantic com todos os campos
          model = create_model(klass, **fields)
          return model
     


     
                              