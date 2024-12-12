# -*- coding: latin -*-
from PyQt6.QtWidgets import QApplication, QTextBrowser, QMainWindow
from PyQt6.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor, QTextOption, QWheelEvent, QGuiApplication
from PyQt6.QtCore import QRegularExpression, Qt
from enum import Enum
from ..style.utils import TypeTheme, Global
import re, textwrap

def mainWindow() -> QMainWindow:
    app = QApplication.instance()

    if not app:
        return None
    
    if isinstance(app, QMainWindow):
        return widget
    
    for widget in app.topLevelWidgets():
        if isinstance(widget, QMainWindow):
            return widget

class PythonSyntaxHighlighter(QSyntaxHighlighter):
    def __init__(self, document):
        super().__init__(document)
        self.highlighting_rules = []
        self.multi_line_string_format = QTextCharFormat()
        
        self.highlighting()

    def highlighting(self):
        self.highlighting_rules.clear()
        self.multi_line_string_format.setForeground(QColor("#CE9178" if Global.theme == TypeTheme.dark else "#8B0000"))

        # Keywords
        keyword_format = QTextCharFormat()
        keyword_format.setForeground(QColor("#569CD6" if Global.theme == TypeTheme.dark else "#00008B"))
        #keyword_format.setFontWeight(QFont.Weight.Bold)
        
        # Decorators
        decorator_format = QTextCharFormat()
        decorator_format.setForeground(QColor("#DCDCAA" if Global.theme == TypeTheme.dark else "#8B8000"))
        self.highlighting_rules.append((QRegularExpression(r"@\w+"), decorator_format))

        # Numbers
        number_format = QTextCharFormat()
        number_format.setForeground(QColor("#B5CEA8" if Global.theme == TypeTheme.dark else "#006400"))
        self.highlighting_rules.append((QRegularExpression(r"\b[+-]?[0-9]+[lL]?\b"), number_format))
        self.highlighting_rules.append((QRegularExpression(r"\b[+-]?0[xX][0-9A-Fa-f]+\b"), number_format))
        self.highlighting_rules.append((QRegularExpression(r"\b[+-]?[0-9]+\.[0-9]*([eE][+-]?[0-9]+)?\b"), number_format))

        # Functions and Class definitions
        function_format = QTextCharFormat()
        function_format.setForeground(QColor("#DCDCAA" if Global.theme == TypeTheme.dark else "#FF0000" ))
        self.highlighting_rules.append((QRegularExpression(r"\bdef\s+\w+\b"), function_format))
        self.highlighting_rules.append((QRegularExpression(r"\b\w+(?=\()"), function_format))

        class_format = QTextCharFormat()
        class_format.setForeground(QColor("#4EC9B0" if Global.theme == TypeTheme.dark else "#008B8B"))
        self.highlighting_rules.append((QRegularExpression(r"\bclass\s+\w+\b"), class_format))

        # Operators
        operator_format = QTextCharFormat()
        operator_format.setForeground(QColor("#D4D4D4" if Global.theme == TypeTheme.dark else "#808080"))
        operators = [
            r"\+", r"-", r"\*", r"/", r"//", r"%", r"\*\*", r"=", r"\+=", r"-=", r"\*=", r"/=", r"%=", r"&=", r"\|=", r"\^=",
            r">>", r"<<", r"==", r"!=", r"<", r">", r"<=", r">=", r"\(", r"\)", r"\[", r"\]", r"\{", r"\}", r"\.", r",", r":", 
            r";", r"\?", r"@", r"&", r"\|", r"~", r"^", r"<<", r">>", r"\\"
        ]
        self.highlighting_rules += [(QRegularExpression(op), operator_format) for op in operators]

        keywords = [
            "cls", "self", "and", "as", "assert", "async", "await", "break", "class", "continue", "def", "del", "elif", "else", "except", 
            "False", "finally", "for", "from", "global", "if", "import", "in", "is", "lambda", "None", "nonlocal", "not", 
            "or", "pass", "raise", "return", "True", "try", "while", "with", "yield"
        ]
        self.highlighting_rules += [(QRegularExpression(f"\\b{keyword}\\b"), keyword_format) for keyword in keywords]

        # Built-in functions
        builtin_format = QTextCharFormat() 
        builtin_format.setForeground(QColor("#C586C0" if Global.theme == TypeTheme.dark else "#7B68EE"))
        builtins = [
            "abs", "all", "any", "ascii", "bin", "bool", "bytearray", "bytes", "callable", "chr", "classmethod", "compile", 
            "complex", "delattr", "dict", "dir", "divmod", "enumerate", "eval", "exec", "filter", "float", "format", "frozenset", 
            "getattr", "globals", "hasattr", "hash", "help", "hex", "id", "input", "int", "isinstance", "issubclass", "iter", 
            "len", "list", "locals", "map", "max", "memoryview", "min", "next", "object", "oct", "open", "ord", "pow", "print", 
            "property", "range", "repr", "reversed", "round", "set", "setattr", "slice", "sorted", "staticmethod", "str", 
            "sum", "super", "tuple", "type", "vars", "zip"
        ]
        self.highlighting_rules += [(QRegularExpression(f"\\b{builtin}\\b"), builtin_format) for builtin in builtins]

        # Strings (single and multi-line)
        string_format = QTextCharFormat()
        string_format.setForeground(QColor("#CE9178" if Global.theme == TypeTheme.dark else "#8B0000"))
        self.highlighting_rules.append((QRegularExpression(r'"[^"\\]*(\\.[^"\\]*)*"'), string_format))
        self.highlighting_rules.append((QRegularExpression(r"'[^'\\]*(\\.[^'\\]*)*'"), string_format))
        
        # Comments
        comment_format = QTextCharFormat()
        comment_format.setForeground(QColor("#6A9955" if Global.theme == TypeTheme.dark else "#228B22"))
        #comment_format.setFontItalic(True)
        self.highlighting_rules.append((QRegularExpression(r"#.*"), comment_format))


    def highlightBlock(self, text):
        """
        Applies the defined highlighting rules to the given text block.

        :param text: The text block to highlight.
        """

        # Apply generic highlighting rules
        for pattern, fmt in self.highlighting_rules:
            expression = QRegularExpression(pattern)
            match_iterator = expression.globalMatch(text)
            while match_iterator.hasNext():
                match = match_iterator.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), fmt)

    
class VbNetSyntaxHighlighter(QSyntaxHighlighter):
    def __init__(self, document):
        super().__init__(document)
        
        self.highlighting_rules = []
        self.highlighting()

    def highlighting(self):
        self.highlighting_rules.clear()

        # Keywords
        keyword_format = QTextCharFormat()
        keyword_format.setForeground(QColor("#569CD6" if Global.theme == TypeTheme.dark else "#00008B"))

        # Decorators or Attributes
        attribute_format = QTextCharFormat()
        attribute_format.setForeground(QColor("#DCDCAA" if Global.theme == TypeTheme.dark else "#8B8000"))
        self.highlighting_rules.append((QRegularExpression(r"<\w+>"), attribute_format))

        # Numbers
        number_format = QTextCharFormat()
        number_format.setForeground(QColor("#B5CEA8" if Global.theme == TypeTheme.dark else "#006400"))
        self.highlighting_rules.append((QRegularExpression(r"\b[+-]?[0-9]+(\.[0-9]+)?\b"), number_format))

        # Functions and Subroutines
        function_format = QTextCharFormat()
        function_format.setForeground(QColor("#DCDCAA" if Global.theme == TypeTheme.dark else "#FF0000"))
        self.highlighting_rules.append((QRegularExpression(r"\b(Sub|Function)\s+\w+\b"), function_format))
        self.highlighting_rules.append((QRegularExpression(r"\b\w+(?=\()"), function_format))

        # Classes and Structures
        class_format = QTextCharFormat()
        class_format.setForeground(QColor("#4EC9B0" if Global.theme == TypeTheme.dark else "#008B8B"))
        self.highlighting_rules.append((QRegularExpression(r"\b(Class|Structure|Enum|Module)\s+\w+\b"), class_format))

        # Operators
        operator_format = QTextCharFormat()
        operator_format.setForeground(QColor("#D4D4D4" if Global.theme == TypeTheme.dark else "#808080"))
        operators = [
            r"\+", r"-", r"\*", r"/", r"\\", r"Mod", r"^", r"=", r"<", r">", r"<=", r">=", r"<>", r"Not", r"And", r"Or",
            r"Xor", r"Is", r"Like", r"&", r"\(", r"\)", r"\[", r"\]", r"\{", r"\}", r"\.", r",", r":", r";"
        ]
        self.highlighting_rules += [(QRegularExpression(op), operator_format) for op in operators]

        # VB.NET Keywords
        keywords = [
            "Dim", "As", "Public", "Private", "Protected", "Friend", "Static", "Shared", "ReadOnly", "WriteOnly", "Const",
            "Option", "Strict", "Infer", "Explicit", "On", "Off", "If", "Then", "Else", "ElseIf", "End", "Select", "Case",
            "For", "Each", "To", "Next", "Do", "While", "Loop", "Until", "With", "Try", "Catch", "Finally", "Throw",
            "Return", "Exit", "Continue", "Goto", "True", "False", "Nothing", "New", "Set", "Get", "Property", "Inherits",
            "Implements", "Overrides", "Overloads", "MustOverride", "NotInheritable", "NotOverridable", "Partial", "Imports"
        ]
        self.highlighting_rules += [(QRegularExpression(f"\\b{keyword}\\b"), keyword_format) for keyword in keywords]

        # Built-in functions
        builtin_format = QTextCharFormat()
        builtin_format.setForeground(QColor("#C586C0" if Global.theme == TypeTheme.dark else "#7B68EE"))
        builtin_format = QTextCharFormat()

        builtins = [
            "MsgBox", "InputBox", "IsNothing", "IsDBNull", "Len", "UCase", "LCase", "Mid", "Replace", "Trim", "Split",
            "Join", "InStr", "Format", "Val", "Chr", "Asc", "DateAdd", "DateDiff", "DatePart", "DateSerial", "DateValue",
            "TimeSerial", "TimeValue", "Now", "Today", "CDate", "CInt", "CLng", "CStr", "CType", "CDbl", "CDec", "CSng"
        ]
        self.highlighting_rules += [(QRegularExpression(f"\\b{builtin}\\b"), builtin_format) for builtin in builtins]

         # Strings
        string_format = QTextCharFormat()
        string_format.setForeground(QColor("#CE9178" if Global.theme == TypeTheme.dark else "#8B0000"))
        self.highlighting_rules.append((QRegularExpression(r'"[^"\\]*(\\.[^"\\]*)*"'), string_format))

        # Comments
        comment_format = QTextCharFormat()
        comment_format.setForeground(QColor("#6A9955" if Global.theme == TypeTheme.dark else "#228B22"))
        #comment_format.setFontItalic(True)
        self.highlighting_rules.append((QRegularExpression(r"'.*"), comment_format))

    def highlightBlock(self, text):
        for pattern, fmt in self.highlighting_rules:
            expression = pattern.globalMatch(text)
            while expression.hasNext():
                match = expression.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), fmt)


class CSyntaxHighlighter(QSyntaxHighlighter):
    def __init__(self, document):
        super().__init__(document)
        self.highlighting_rules = []
        
        self.highlighting()

    def highlighting(self):
        self.highlighting_rules.clear()

        # Keywords
        keyword_format = QTextCharFormat()
        keyword_format.setForeground(QColor("#569CD6" if Global.theme == TypeTheme.dark else "#00008B"))
        keywords = [
            "abstract", "as", "base", "bool", "break", "byte", "case", "catch", "char", "checked", "class", "const", "continue",
            "decimal", "default", "delegate", "do", "double", "else", "enum", "event", "explicit", "extern", "false", "finally",
            "fixed", "float", "for", "foreach", "goto", "if", "implicit", "in", "int", "interface", "internal", "is", "lock",
            "long", "namespace", "new", "null", "object", "operator", "out", "override", "params", "private", "protected",
            "public", "readonly", "ref", "return", "sbyte", "sealed", "short", "sizeof", "stackalloc", "static", "string", 
            "struct", "switch", "this", "throw", "true", "try", "typeof", "uint", "ulong", "unchecked", "unsafe", "ushort", 
            "using", "virtual", "void", "volatile", "while"
        ]
        self.highlighting_rules += [(QRegularExpression(f"\\b{keyword}\\b"), keyword_format) for keyword in keywords]

        # Types (int, float, etc.)
        type_format = QTextCharFormat()
        type_format.setForeground(QColor("#4EC9B0" if Global.theme == TypeTheme.dark else "#008B8B"))
        types = ["int", "float", "double", "string", "char", "bool", "object", "void", "var"]
        self.highlighting_rules += [(QRegularExpression(f"\\b{t}\\b"), type_format) for t in types]

        # Numbers
        number_format = QTextCharFormat()
        number_format.setForeground(QColor("#B5CEA8" if Global.theme == TypeTheme.dark else "#006400"))
        self.highlighting_rules.append((QRegularExpression(r"\b[+-]?[0-9]+(\.[0-9]+)?\b"), number_format))

        # Functions and Methods
        function_format = QTextCharFormat()
        function_format.setForeground(QColor("#DCDCAA" if Global.theme == TypeTheme.dark else "#FF0000"))
        self.highlighting_rules.append((QRegularExpression(r"\b\w+(?=\()"), function_format))

        # Class and Struct definitions
        class_format = QTextCharFormat()
        class_format.setForeground(QColor("#4EC9B0" if Global.theme == TypeTheme.dark else "#008B8B"))
        self.highlighting_rules.append((QRegularExpression(r"\bclass\s+\w+\b"), class_format))
        self.highlighting_rules.append((QRegularExpression(r"\bstruct\s+\w+\b"), class_format))

        # Operators
        operator_format = QTextCharFormat()
        operator_format.setForeground(QColor("#D4D4D4" if Global.theme == TypeTheme.dark else "#808080"))
        operators = [
            r"\+", r"-", r"\*", r"/", r"//", r"%", r"\*\*", r"=", r"\+=", r"-=", r"\*=", r"/=", r"%=", r"&=", r"\|=", r"\^=",
            r">>", r"<<", r"==", r"!=", r"<", r">", r"<=", r">=", r"\(", r"\)", r"\[", r"\]", r"\{", r"\}", r"\.", r",", r":", 
            r";", r"\?", r"@", r"&", r"\|", r"~", r"^", r"<<", r">>", r"\\"
        ]
        self.highlighting_rules += [(QRegularExpression(op), operator_format) for op in operators]

        # Strings (single and multi-line)
        string_format = QTextCharFormat()
        string_format.setForeground(QColor("#CE9178" if Global.theme == TypeTheme.dark else "#8B0000"))
        self.highlighting_rules.append((QRegularExpression(r'"[^"\\]*(\\.[^"\\]*)*"'), string_format))
        self.highlighting_rules.append((QRegularExpression(r'@"[^"]*"'), string_format))

        # Comments (single and multi-line)
        comment_format = QTextCharFormat()
        comment_format.setForeground(QColor("#6A9955" if Global.theme == TypeTheme.dark else "#228B22"))
        #comment_format.setFontItalic(True)
        self.highlighting_rules.append((QRegularExpression(r"//.*"), comment_format))
        self.highlighting_rules.append((QRegularExpression(r"/\*[\s\S]*?\*/"), comment_format))


    def highlightBlock(self, text):
        for pattern, fmt in self.highlighting_rules:
            expression = pattern.globalMatch(text)
            while expression.hasNext():
                match = expression.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), fmt)


class JsonSyntaxHighlighter(QSyntaxHighlighter):
    def __init__(self, document):
        super().__init__(document)
        
        self.highlighting_rules = []
        self.highlighting()

    def highlighting(self):
        self.highlighting_rules.clear()
 
        # Numbers (green)
        number_format = QTextCharFormat()
        number_format.setForeground(QColor("#B5CEA8" if Global.theme == TypeTheme.dark else "#006400"))
        self.highlighting_rules.append((QRegularExpression(r"\b[+-]?[0-9]+(\.[0-9]+)?\b"), number_format))

        # Format for JSON keys (blue)
        key_format = QTextCharFormat()
        key_format.setForeground(QColor("#569CD6" if Global.theme == TypeTheme.dark else "#00008B"))  # Azul para chaves
        self.highlighting_rules.append((QRegularExpression(r'\".*?\"(?=\s*:)'), key_format))  # Keys

        # Format for JSON values (red)
        value_format = QTextCharFormat()
        value_format.setForeground(QColor("#CE9178" if Global.theme == TypeTheme.dark else "#8B0000"))  # Vermelho para valores
        # Ajuste para capturar valores diretamente
        self.highlighting_rules.append((QRegularExpression(r':\s*\".*?\"'), value_format))
       
        # Commas and colons (gray)
        punctuation_format = QTextCharFormat()
        punctuation_format.setForeground(QColor("#CE9178" if Global.theme == TypeTheme.dark else "#8B0000"))
        self.highlighting_rules.append((QRegularExpression(r"[:,]"), punctuation_format))

        # Booleans and Nulls (blue)
        bool_null_format = QTextCharFormat()
        bool_null_format.setForeground(QColor("#569CD6" if Global.theme == TypeTheme.dark else "#00008B"))
        self.highlighting_rules.append((QRegularExpression(r"\b(true|false|null)\b"), bool_null_format))

        # Curly braces `{}` (darker blue)
        brace_format = QTextCharFormat()
        brace_format.setForeground(QColor("#569CD6" if Global.theme == TypeTheme.dark else "#00008B"))  # Azul mais forte
        self.highlighting_rules.append((QRegularExpression(r"[\{\}]"), brace_format))

        # Square brackets `[]` (lilac)
        bracket_format = QTextCharFormat()
        bracket_format.setForeground(QColor("#C586C0" if Global.theme == TypeTheme.dark else "#7B68EE"))  # Lilás
        self.highlighting_rules.append((QRegularExpression(r"[\[\]]"), bracket_format))


    def highlightBlock(self, text):
        for pattern, fmt in self.highlighting_rules:
            expression = pattern.globalMatch(text)
            while expression.hasNext():
                match = expression.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), fmt)


class XmlHtmlSyntaxHighlighter(QSyntaxHighlighter):
    def __init__(self, document):
        super().__init__(document)
        self.highlighting_rules = []
        self.highlighting()

    def highlighting(self):
        self.highlighting_rules.clear()

        # Tags (azul)
        tag_format = QTextCharFormat()
        tag_format.setForeground(QColor("#569CD6" if Global.theme == TypeTheme.dark else "#00008B"))  # Azul
        self.highlighting_rules.append((QRegularExpression(r"</?\b\w+"), tag_format))  # Captura tags de abertura e fechamento

        # Atributos (verde)
        attribute_format = QTextCharFormat()
        attribute_format.setForeground(QColor("#B5CEA8" if Global.theme == TypeTheme.dark else "#006400"))  # Verde
        self.highlighting_rules.append((QRegularExpression(r'\b\w+(?=\=)'), attribute_format))  # Atributos antes do `=`

        # Valores dos atributos (vermelho)
        value_format = QTextCharFormat()
        value_format.setForeground(QColor("#CE9178" if Global.theme == TypeTheme.dark else "#8B0000"))  # Vermelho
        self.highlighting_rules.append((QRegularExpression(r'\".*?\"'), value_format))  # Valores de atributos entre aspas

        # Símbolos de pontuação (cinza)
        punctuation_format = QTextCharFormat()
        punctuation_format.setForeground(QColor("#D4D4D4" if Global.theme == TypeTheme.dark else "#808080"))  # Cinza
        self.highlighting_rules.append((QRegularExpression(r"[<>/=]"), punctuation_format))  # Símbolos especiais do XML/HTML (<, >, =, /)

        # Comentários (cinza escuro)
        comment_format = QTextCharFormat()
        comment_format.setForeground(QColor("#6A9955" if Global.theme == TypeTheme.dark else "#808080"))  # Cinza escuro
        self.highlighting_rules.append((QRegularExpression(r'<!--[\s\S]*?-->'), comment_format))  # Comentários XML/HTML

        # Entidades HTML (laranja)
        entity_format = QTextCharFormat()
        entity_format.setForeground(QColor("#D7BA7D" if Global.theme == TypeTheme.dark else "#FF4500"))  # Laranja
        self.highlighting_rules.append((QRegularExpression(r"&\w+;"), entity_format))  # Entidades HTML (&nbsp;, &amp;, etc.)

        # HTML Doctype (púrpura)
        doctype_format = QTextCharFormat()
        doctype_format.setForeground(QColor("#C586C0" if Global.theme == TypeTheme.dark else "#800080"))  # Púrpura
        self.highlighting_rules.append((QRegularExpression(r"<!DOCTYPE.*?>"), doctype_format))  # Doctype em HTML

    def highlightBlock(self, text):
        # Aplica as regras de realce de sintaxe para cada bloco de texto
        for pattern, fmt in self.highlighting_rules:
            expression = pattern.globalMatch(text)
            while expression.hasNext():
                match = expression.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), fmt)


class GenericSyntaxHighlighter(QSyntaxHighlighter):
    def __init__(self, document):
        """
        Initializes the highlighter with generic highlighting rules suitable for many programming languages.

        :param document: QTextDocument associated with the QTextEdit.
        """
        super().__init__(document)
        
        self.multi_line_string_format = QTextCharFormat()
        self.highlighting_rules = []
        self.highlighting()

    def highlighting(self):
        """
        Sets up generic highlighting rules that can match common syntax across many programming languages.
        """
        self.highlighting_rules.clear()
        self.multi_line_string_format.setForeground(QColor("#CE9178" if Global.theme == TypeTheme.dark else "#8B0000"))

        # Generic keyword format
        keyword_format = QTextCharFormat()
        keyword_format.setForeground(QColor("#569CD6" if Global.theme == TypeTheme.dark else "#00008B"))
        
        # Generic function and class format
        function_format = QTextCharFormat()
        function_format.setForeground(QColor("#DCDCAA" if Global.theme == TypeTheme.dark else "#8B8000"))

        class_format = QTextCharFormat()
        class_format.setForeground(QColor("#4EC9B0" if Global.theme == TypeTheme.dark else "#008B8B"))

        # String format (single, double, multiline)
        string_format = QTextCharFormat()
        string_format.setForeground(QColor("#CE9178" if Global.theme == TypeTheme.dark else "#8B0000"))

        # Number format
        number_format = QTextCharFormat()
        number_format.setForeground(QColor("#B5CEA8" if Global.theme == TypeTheme.dark else "#006400"))

        # Comment format with theme support
        comment_format = QTextCharFormat()
        comment_format.setForeground(QColor("#6A9955" if Global.theme == TypeTheme.dark else "#228B22"))
        #comment_format.setFontItalic(True)

        # Operator format
        operator_format = QTextCharFormat()
        operator_format.setForeground(QColor("#D4D4D4" if Global.theme == TypeTheme.dark else "#808080"))

        # Adding generic regex rules for common elements
        keywords = [
            # Common keywords across multiple languages (only lowercase needed due to case-insensitive regex)
            "using", "from", "if", "else", "for", "while", "return", "class", "def", "function", "import", 
            "export", "try", "catch", "finally", "switch", "case", "break", "continue", "true", 
            "false", "null", "undefined", "new", "delete", "this", "super", "public", "private", 
            "protected", "static", "void", "var", "let", "const", "async", "await", "yield", 
            "throw", "lambda"
        ]

        # Numbers: integers, floats, hexadecimal
        self.highlighting_rules.append((QRegularExpression(r"\b[+-]?[0-9]+[lL]?\b"), number_format))
        self.highlighting_rules.append((QRegularExpression(r"\b[+-]?0[xX][0-9A-Fa-f]+\b"), number_format))
        self.highlighting_rules.append((QRegularExpression(r"\b[+-]?[0-9]+\.[0-9]*([eE][+-]?[0-9]+)?\b"), number_format))

        # Functions and classes
        self.highlighting_rules.append((QRegularExpression(r"\b\w+\s*(?=\()", QRegularExpression.PatternOption.CaseInsensitiveOption), function_format))
        self.highlighting_rules.append((QRegularExpression(r"\bclass\s+\w+\b", QRegularExpression.PatternOption.CaseInsensitiveOption), class_format))
        self.highlighting_rules.append((QRegularExpression(r"\bdef\s+\w+\b", QRegularExpression.PatternOption.CaseInsensitiveOption), function_format))

        
        # Operators: common across languages
        operators = [
            r"\+", r"-", r"\*", r"/", r"//", r"%", r"\*\*", r"=", r"\+=", r"-=", r"\*=", r"/=", r"%=",
            r"&=", r"\|=", r"\^=", r">>", r"<<", r"==", r"!=", r"<", r">", r"<=", r">=", r"\(", r"\)", r"\[", r"\]",
            r"\{", r"\}", r"\.", r",", r":", r";", r"\?", r"@", r"&", r"\|", r"~", r"^", r"\\", r"->"
        ]
        self.highlighting_rules += [(QRegularExpression(op), operator_format) for op in operators]

        # Use case-insensitive regex pattern for keywords
        self.highlighting_rules += [(QRegularExpression(f"\\b{keyword}\\b", QRegularExpression.PatternOption.CaseInsensitiveOption), keyword_format) for keyword in keywords]

        # Strings: single, double, triple quotes
        self.highlighting_rules.append((QRegularExpression(r'"[^"\\]*(\\.[^"\\]*)*"', QRegularExpression.PatternOption.CaseInsensitiveOption), string_format))
        self.highlighting_rules.append((QRegularExpression(r"'[^'\\]*(\\.[^'\\]*)*'", QRegularExpression.PatternOption.CaseInsensitiveOption), string_format))

        # Comments: single line (//, #) and multi-line (/* */)
        self.highlighting_rules.append((QRegularExpression(r"//.*", QRegularExpression.PatternOption.CaseInsensitiveOption), comment_format))
        self.highlighting_rules.append((QRegularExpression(r"#.*", QRegularExpression.PatternOption.CaseInsensitiveOption), comment_format))
        self.highlighting_rules.append((QRegularExpression(r"/\*[\s\S]*?\*/", QRegularExpression.PatternOption.CaseInsensitiveOption), comment_format))

    def highlightBlock(self, text):
        """
        Applies the defined highlighting rules to the given text block.

        :param text: The text block to highlight.
        """

        # Apply generic highlighting rules
        for pattern, fmt in self.highlighting_rules:
            expression = QRegularExpression(pattern)
            match_iterator = expression.globalMatch(text)
            while match_iterator.hasNext():
                match = match_iterator.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), fmt)

class CodeEditor(QTextBrowser):

    class Language(Enum):
        Nothing = 0
        generic = 1
        python = 2
        vb = 3
        csharp = 4
        json = 5
        XmlHtml = 6
        Markdown = 7
  
    def __init__(self, language : Language = Language.generic, adjust_height = False, content : str = None, readOnly = False):
        super().__init__()
        self.adjust_height = adjust_height
        self.language = language
        self.setTabStopDistance(4 * self.fontMetrics().horizontalAdvance(' '))  # Set tab width
        if language == self.Language.python:
            self.highlighter = PythonSyntaxHighlighter(self.document())
        elif language == self.Language.vb:
            self.highlighter = VbNetSyntaxHighlighter(self.document())
        elif language == self.Language.csharp:
            self.highlighter = CSyntaxHighlighter(self.document())
        elif language == self.Language.json:
            self.highlighter = JsonSyntaxHighlighter(self.document())
        elif language == self.Language.generic:
            self.highlighter = GenericSyntaxHighlighter(self.document())
        elif language == self.Language.XmlHtml:
            self.highlighter = XmlHtmlSyntaxHighlighter(self.document())
        else:
            self.highlighter = None

        self.setOpenExternalLinks(True)

        self.setReadOnly(readOnly)

        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

        self.current_font_size = self.font().pointSize()  # Guarda o tamanho atual da fonte
        self.setWordWrapMode(QTextOption.WrapMode.NoWrap)

        if adjust_height:
            self.textChanged.connect(self.autoResize)
 
        if self.highlighter:
            window =  mainWindow()
            if hasattr(window, 'signal_toggle_theme'):
                window.signal_toggle_theme.connect(self.highlighting)

        if content:
            if self.language == self.Language.Markdown:
                self.setMarkdown(content)
            else:
                self.setPlainText(content)

    def setPlainText(self, text: str | None) -> None:
        if self.language == self.Language.Markdown:
            return self.setMarkdown(text)
        return super().setPlainText(text)
    
    def setHtml(self, text: str | None) -> None:
        if self.language == self.Language.Markdown:
            return super().setMarkdown(text)
        return super().setHtml(text)
    
    # def setMarkdown(self, markdown : str):
         
    #     screen = QGuiApplication.primaryScreen()
    #     screen_geometry = screen.geometry()
    #     screen_width = screen_geometry.width()
    #     width = max(70, screen_width // 6)

    #     markdown = markdown.replace("\\\\n", "\n").replace("\\n", "\n")
    #     paragraphs = markdown.strip().split("\n\n")
    #     wrapped_paragraphs = [textwrap.fill(p.strip(), width=width) for p in paragraphs]
    #     processed_text = "\n\n".join(p.replace("\n", "  \n") for p in wrapped_paragraphs)
    #     return super().setMarkdown(processed_text)

    def setMarkdown(self, markdown):
        screen = QGuiApplication.primaryScreen()
        screen_geometry = screen.geometry()
        screen_width = screen_geometry.width()
        width = max(70, screen_width // 6)
        
        text : str = re.sub(r'\.(\d+)\.', r'. \n\1.', markdown)
        text = text.replace('<', '&lt;').replace('>', '&gt;')
        text = text.replace("\\\\n", "\n").replace("\\n", "\n")
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        processed_markdown = ""
        for line in lines:
            processed_markdown += f"{textwrap.fill(line.strip(), width=width)}\n\n"
        processed_markdown = processed_markdown.strip()
        return super().setMarkdown(processed_markdown)
        
    def copy(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.toPlainText())

    def autoResize(self):
        if self.adjust_height:
            self.document().setTextWidth(self.viewport().width())
            margins = self.contentsMargins()
            height = int(self.document().size().height() + margins.top() + margins.bottom())

            if self.horizontalScrollBar().isVisible():
                scrollbar_height = self.horizontalScrollBar().sizeHint().height()
                height += scrollbar_height
            
            self.setFixedHeight(height + 10)

    def resizeEvent(self, event):
        if self.adjust_height:
            self.autoResize()
        super().resizeEvent(event)

    def highlighting(self):
        if self.highlighter:
            vscroll_position = self.verticalScrollBar().value()
            hscroll_position = self.horizontalScrollBar().value()

            code = self.toPlainText()
            self.clear()
            self.highlighter.highlighting()
            self.setPlainText(code)

            self.verticalScrollBar().setValue(vscroll_position)
            self.horizontalScrollBar().setValue(hscroll_position)

    def wheelEvent(self, event: QWheelEvent):
        # Verifica se a tecla Ctrl está pressionada
        if event.modifiers() == Qt.KeyboardModifier.ControlModifier:
            # Aumenta ou diminui o tamanho da fonte dependendo da direção do scroll
            if event.angleDelta().y() > 0:
                self.current_font_size += 1
            else:
                self.current_font_size -= 1

            # Define o novo tamanho da fonte, garantindo que não fique muito pequeno
            if self.current_font_size < 1:
                self.current_font_size = 1

            # Atualiza a fonte do QTextEdit com o novo tamanho
            self.setStyleSheet(f'font: {self.current_font_size}pt "Segoe UI"')

            # Ignora o evento padrão de rolagem para evitar a rolagem do conteúdo
            event.accept()
        else:
            # Se Ctrl não está pressionado, continua com o comportamento normal do scroll
            super().wheelEvent(event)

