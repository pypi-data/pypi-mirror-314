# -*- coding: latin -*-
from PyQt6.QtWidgets import QTextEdit, QApplication, QTextBrowser, QWidget, QHBoxLayout
from PyQt6.QtGui import QTextCharFormat, QTextCursor, QColor, QWheelEvent, QBrush, QSyntaxHighlighter
from PyQt6.QtCore import Qt, QRegularExpression
import re
from bs4 import BeautifulSoup
from .style import Styles
from enum import Enum
from functools import partial
import time

class DocumentOptions:
    def __init__(self, word : str, color : QColor):
        self.word = word
        self.color = color

class DocumentTypeFile(Enum):
        VB = 0
        CSharp = 1
        Python = 2
        Json = 3

class ReservedWords(object):
    def words() -> list[DocumentOptions]:
        list_blue = ['AddHandler', 'AddressOf', 'Alias', 'AndAlso', 'As', 'Boolean', 'ByRef', 
                        'Byte', 'ByVal', 'Call', 'CBool', 'CByte', 'CChar', 'CDate', 'CDbl', 'Char', 'Class',
                        'CLng', 'CObj', 'Const', 'CSByte', 'CShort', 'CSng', 'CStr', 'CType', 'Date', 'Decimal',
                        'Declare', 'Default', 'Delegate', 'Dim', 'DirectCast', 'Double', 'Enum', "End Class", "End Sub",
                        "End Function", "Public", "Private", "Handles", "MyBase", 'False', 'True', 'Friend', 'Implements',
                        "New", "Integer", "String","Imports", "Function", "Sub", "End Sub", "End Function", 'Await', 'Async']

        list_blue_document_options = [DocumentOptions(word, Styles.Color.blue.QColor) for word in list_blue]

        list_lilac = ['Case', 'Catch', 'Continue', 'Do', 'Each', 'For', 'If', 'Else', 'elif', 'ElseIf', "Then", "Try", "End Try",
                        "While", 'Return', 'Exit', 'Finally', 'Next', 'Exit Select', 'End Select', 'Select Case', 'End If', 'Finally', "Throw", "Catch"]
        list_lilac_document_options = [DocumentOptions(word, Styles.Color.lilac.QColor) for word in list_lilac]

        list_document_options = []
        list_document_options.extend(list_blue_document_options)
        list_document_options.extend(list_lilac_document_options)
        return list_document_options 

    @classmethod
    def words_py(cls):
        list_words = [DocumentOptions(option.word.lower(), option.color) for option in cls.words()]
        list_blue = ['self', 'cls', 'return', 'def', 'None', "True", 'False', 'from', 'import']
        list_blue_document_options = [DocumentOptions(word, Styles.Color.blue.QColor) for word in list_blue]
        list_words.extend(list_blue_document_options)
        list_dark_green = ['str', 'int', 'enumerate', 'list', 'tuple'] # type da erro
        list_dark_green_document_options = [DocumentOptions(word, Styles.Color.dark_green.QColor) for word in list_dark_green]
        list_words.extend(list_dark_green_document_options)
        return list_words

    @classmethod
    def words_cs(cls):
        list_words = [DocumentOptions(option.word.lower(), option.color) for option in cls.words()]
        list_blue = ['int', 'using', 'string', 'except', 'namespace', 'async', 'await', 'var', 'static', 'readonly', 'const',
                    'private', 'public']
        list_blue_document_options = [DocumentOptions(word, Styles.Color.blue.QColor) for word in list_blue]
        
        list_dark_green = ['Task', 'Console', 'Stopwatch', 'list', 'tuple']
        list_dark_green_document_options = [DocumentOptions(word, Styles.Color.dark_green.QColor) for word in list_dark_green]
        list_words.extend(list_dark_green_document_options)
        list_words.extend(list_blue_document_options)
        list_words.append(DocumentOptions('/*', Styles.Color.light_green.QColor))
        list_words.append(DocumentOptions('*/', Styles.Color.light_green.QColor))
        return list_words

class Browser(QTextBrowser):
    def __init__(self, adjust_height = False, adjust_font_size = False, 
                    update_list_widget = False,  font_size = 12, min_height = 0, objectName : str = None, parent : QWidget = None):
        super().__init__()

        self.adjust_height = adjust_height
        self.adjust_font_size = adjust_font_size
        self.min_height = min_height
        self.min_font_size = 8
        self.max_font_size = 30
        self.update_list_widget = update_list_widget
        self.loaded_with = None
        self.setOpenExternalLinks(True)
        Text.update_wheel_event_size(self, font_size, False)
       
        if self.adjust_height:
            #window = QCoreApplication.instance().activeWindow()
            #if window:
            #    window.resizeConnect(self.adjustWidgetHeight)
            self.textChanged.connect(self.adjustWidgetHeight)
            self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
            self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        if objectName:
            self.setObjectName(objectName)

        if parent:
            try:
                parent.layout().addWidget(self)
            except:
                layout = QHBoxLayout()
                layout.setContentsMargins(0, 0, 0, 0)
                layout.addWidget(self)
                parent.setLayout(layout)
                

    def adjustWidgetHeight(self, max_height = 0):
        Text.adjust_height(self, self.min_height, max_height)
        
    def setHtml(self, text: str, use_format = False) -> None:
        self.loaded_with = "setHtml"
        if use_format:
            return super().setHtml(Text.format_html(text))
        else:
            return super().setHtml(text)
        
    def setHtmlByText(self, text: str, use_format = True):
        TextBrowser = QTextBrowser()
        match = re.search(r'font:\s*(\d+)pt', self.styleSheet())
        if match:
            size = match.group(1)
        else:
            size = 12
        TextBrowser.setPlainText(text)
        text_html = Text.alter_font_size(TextBrowser.toHtml() , size)
        TextBrowser.deleteLater()
        self.setHtml(text_html, use_format)

    def setPlainText(self, text: str) -> None:
        self.loaded_with = "setPlainText"
        return super().setPlainText(text)

    def wheelEvent(self, e: QWheelEvent):
        if e.modifiers() & Qt.KeyboardModifier.ControlModifier and self.adjust_font_size:
            Text.update_widgets_size(self, e)
        else:
            return super().wheelEvent(e)


class Edit(QTextEdit):

    def __init__(self, adjust_height = False, adjust_font_size = False,
                    update_list_widget = False, font_size = 12, min_height = 0, objectName : str = None, parent : QWidget = None):
        super().__init__()
    
        self.adjust_height = adjust_height
        self.adjust_font_size = adjust_font_size
        self.min_height = min_height
        self.min_font_size = 8
        self.max_font_size = 30
        self.update_list_widget = update_list_widget
        self.loaded_with = None 
        Text.update_wheel_event_size(self, font_size, False)
        
        if self.adjust_height:
            #window = QCoreApplication.instance().activeWindow()
            #if window:
            #    window.resizeConnect(self.adjustWidgetHeight)
    
            self.textChanged.connect(self.adjustWidgetHeight)
            self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
            self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        if objectName:
            self.setObjectName(objectName)

        if parent:
            try:
                parent.layout().addWidget(self)
            except:
                layout = QHBoxLayout()
                layout.setContentsMargins(0, 0, 0, 0)
                layout.addWidget(self)
                parent.setLayout(layout)

    def adjustWidgetHeight(self, max_height = 0):
        Text.adjust_height(self, self.min_height, max_height)
   
    def setHtml(self, text: str, use_format = False) -> None:
        
        self.loaded_with = "setHtml"
        if use_format:
            super().setHtml(Text.format_html(text))
        else:
            super().setHtml(text)
        
    def setHtmlByText(self, text: str, use_format = True):
        TextBrowser = QTextBrowser()
        match = re.search(r'font:\s*(\d+)pt', self.styleSheet())
        if match:
            size = match.group(1)
        else:
            size = 12
        TextBrowser.setPlainText(text)
        text_html = Text.alter_font_size(TextBrowser.toHtml() , size)
        TextBrowser.deleteLater()
        self.setHtml(text_html, use_format)
    
    def setPlainText(self, text: str) -> None:
        self.loaded_with = "setPlainText"
        super().setPlainText(text)

    def wheelEvent(self, e: QWheelEvent):
        if e.modifiers() & Qt.KeyboardModifier.ControlModifier and self.adjust_font_size:
            Text.update_widgets_size(self, e)
        else:
            return super().wheelEvent(e)
        

class OnWheelEvent(object):
    list_widget_on_wheel_event : list[Browser | Edit] = []
    font_size = 12
        
class Text(object):

    class Edit(Edit):
        ...

    class Browser(Browser):
        ...
 
    class DocumentOptions(DocumentOptions):
        ...

    class DocumentTypeFile(Enum):
        VB = 0
        CSharp = 1
        Python = 2
        Json = 3

    def set_list_widget_on_wheel_event(list_text_widget : list[Browser | Edit]):
        OnWheelEvent.list_widget_on_wheel_event = list_text_widget

    def get_current_font_size():
        return OnWheelEvent.font_size

    def set_initial_font_size(font_size : int):
        OnWheelEvent.font_size = font_size

    @classmethod
    def update_style_font_size(cls, widget : Browser | Edit , new_size : int):
        widget.clearFocus()
        type_widget = None
        if widget.__class__.__name__ == 'Edit':
            type_widget = 'QTextEdit'
        elif widget.__class__.__name__ == 'Browser':
            type_widget = 'QTextBrowser'
        else:
            return

        widget.setStyleSheet(type_widget +'''{
                font: ''' + str(new_size) + '''pt "Segoe UI";
            }
            ''')
        
        if widget.loaded_with == 'setHtml':
            text_html = cls.alter_font_size(widget.toHtml() , new_size)
            widget.setHtml(text_html, True)

    def alter_font_size(html_text, new_size):
        # Analise o HTML
        soup = BeautifulSoup(html_text, 'html.parser')
        
        # Selecione o elemento 'body' e atualize o atributo 'style'
        body_tag = soup.find('body')
        all_tags = body_tag.find_all()
        
        if body_tag:
            if 'style' in body_tag.attrs:
                body_tag['style'] += f'font-size: {new_size};'
            else:
                body_tag['style'] = f'font-size: {new_size};'

        for tag in all_tags:
            if 'style' in tag.attrs:
                tag['style'] += f'font-size: {new_size}pt;'

        # Retorne o HTML modificado
        return str(soup)

    def format_html(html_text : str):
        # Use expressões regulares para encontrar o texto em negrito e o link e substituir pelas tags HTML correspondentes
        html_text = re.sub(r'\*\*(.*?)\*\* \[(.*?)\]\((.*?)\)', r'<b>\1</b> (<a href="\3" style="color: rgba(66, 114, 219, 0.7)" >\3</a>)', html_text)

        # div com o codigo
        #html_text = re.sub(r'```(.*?)```', r'<div>\1</div>', html_text, flags=re.DOTALL)

        # Substitua texto em negrito
        html_text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', html_text)
        partes = re.split(r'(```.*?```)', html_text, flags=re.DOTALL)
        for i, parte in enumerate(partes):
            if i % 2 == 0:
                partes[i] = re.sub(r'`([^`]+)`', r'`<b>\1</b>`', parte)
        html_text = ''.join(partes)

        # Substitua texto em itálico
        #html_text = re.sub(r'_([^_]+)_', r'<i>\1</i>', html_text)
        
        # Substitua links
        html_text = re.sub(r'\[([^]]+)\]\(([^)]+)\)', r'<a href="\2" style="color: rgba(66, 114, 219, 0.7)" >\1</a>', html_text)
        
         # Trata títulos 
        html_text = re.sub(r'##### (.*?)\n', r'<h5>\1</h5>', html_text)
        html_text = re.sub(r'#### (.*?)\n', r'<h4>\1</h4>', html_text)
        html_text = re.sub(r'### (.*?)\n', r'<h3>\1</h3>', html_text)
        html_text = re.sub(r'## (.*?)\n', r'<h2>\1</h2>', html_text)

        # Particiona o texto em blocos de código e outros textos
        partes = re.split(r'(```.*?```)', html_text, flags=re.DOTALL)
        for i, parte in enumerate(partes):
            if i % 2 == 0:  # Não é um bloco de código
                # Substitui texto em negrito dentro de blocos de texto
                partes[i] = re.sub(r'`([^`]+)`', r'<code>\1</code>', parte)
            else:  # É um bloco de código, envolve com <pre><code>...</code></pre>
                partes[i] = f'<pre><code>{parte[3:-3]}</code></pre>'
        html_text = ''.join(partes)

        return html_text

    def get_text_code(text: str, pattern=r'```(.*?)```'):
        # Encontra todas as correspondências no texto
        matches = re.finditer(pattern, text, flags=re.DOTALL)

        # Lista para armazenar os dicionários de resultados
        results = []

        # Itera sobre as correspondências
        for match in matches:
            # Obtém o texto correspondente
            code_text = match.group(1)

            # Obtém a posição inicial e final no texto completo
            start_pos = match.start()
            end_pos = match.end()

            # Adiciona os resultados à lista
            results.append({"text": code_text, "start": start_pos, "end": end_pos})

        # Retorna a lista de dicionários
        return results


    def adjust_height(widget : Browser | Edit , min_height = 0, max_height = 0):

        widget.document().adjustSize()
        document_height = widget.document().size().height()
        widget_height = document_height + widget.contentsMargins().top() + widget.contentsMargins().bottom()
    
        if widget.horizontalScrollBar().isVisible():
            widget_height += widget.horizontalScrollBar().height()

        new_height = int(widget_height)
    
        if new_height < min_height:
            new_height = min_height
        if new_height > max_height and max_height > 0:
            new_height = max_height

        widget.setFixedHeight(new_height)


    @classmethod
    def update_wheel_event_size(cls, widget : Browser | Edit, new_size : int, adjust_height = True):
        cls.update_style_font_size(widget, new_size)
        if widget.adjust_height and adjust_height:
            widget.adjustWidgetHeight()


    @classmethod
    def update_widgets_size(cls, widget : Browser | Edit, y : QWheelEvent | int):
        
        if widget.toPlainText().strip():
            if type(y) == QWheelEvent:
               y = y.angleDelta().y()

            font = widget.font()
            current_size = font.pointSize()
            new_size = current_size + y // 120  # Altera o tamanho da fonte com base na roda de rolagem
            new_size = max(widget.min_font_size, new_size)  # Garante que o tamanho da fonte seja pelo menos 1
            if new_size > widget.max_font_size :
                new_size = widget.max_font_size 

            cls.update_wheel_event_size(widget, new_size)

            if widget.update_list_widget:
                if OnWheelEvent.list_widget_on_wheel_event: 
                    OnWheelEvent.font_size = new_size

                    for w in OnWheelEvent.list_widget_on_wheel_event:
                        cls.update_wheel_event_size(w, new_size)

    @classmethod
    def wheel_event_size(cls, widget : Browser | Edit , angle_delta_y : int,  nim_size = 8, max_size = 50):
        if widget.hasFocus():
            if widget.toPlainText().strip():
                font = widget.font()
                current_size = font.pointSize()
                new_size = current_size + angle_delta_y // 120  # Altera o tamanho da fonte com base na roda de rolagem
                new_size = max(nim_size, new_size)  # Garante que o tamanho da fonte seja pelo menos 1
                if new_size > max_size:
                    new_size = max_size

                cls.update_style_font_size(widget, new_size)
                

    @staticmethod
    def copy(widget : Browser | Edit | QTextBrowser | QTextEdit):
        cursor = widget.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.Start)
        cursor.select(QTextCursor.SelectionType.Document)
        selected_text = cursor.selectedText()
        clipboard = QApplication.clipboard()
        clipboard.setText(selected_text)

    class BracesHighlighter(QSyntaxHighlighter):

        # Enum para definir os diferentes tipos de braces (delimitadores)
        class BracesType(Enum):
            CURLY = r'\{(.*?)\}'  # Para {}
            SQUARE = r'\[(.*?)\]'  # Para []
            ROUND = r'\((.*?)\)'  # Para ()
            ANGLE = r'\<(.*?)\>'  # Para <>

        def __init__(self, document, braces_types=[], validate_word_list=False, validate_identifier=False):
            super().__init__(document)

            # Parâmetros e variáveis de controle
            self.validate_word_list = validate_word_list
            self.validate_identifier = validate_identifier
            self.list_words = []  # Lista de palavras para validar
            self.color_word_in_list = Styles.Color.blue.QColor  # Cor para palavras dentro da lista
            self.color_word_outside_list = QColor("red")  # Cor para palavras fora da lista
            self.block_signals = False

            # Se nenhum tipo de brace for passado, usa CURLY por padrão
            if not braces_types:
                braces_types = [self.BracesType.CURLY]

            # Constrói a lista de padrões de acordo com os tipos de braces escolhidos
            self.patterns = [re.compile(brace_type.value) for brace_type in braces_types]

            # Define as cores padrão para o formato
            self.brace_format_in_list = QTextCharFormat()
            self.brace_format_in_list.setForeground(self.color_word_in_list)

            self.brace_format_outside_list = QTextCharFormat()
            self.brace_format_outside_list.setForeground(self.color_word_outside_list)

        def update_list_words(self, new_list_words: list[str]):
            """Atualiza a lista de palavras permitidas e refaz o destaque."""
            self.list_words = new_list_words
            self.rehighlight()

        def highlightBlock(self, text: str):
            if self.block_signals:
                return  # Previne chamadas recursivas

            # Itera sobre os padrões para cada tipo de brace selecionado
            for pattern in self.patterns:
                for match in pattern.finditer(text):
                    word = match.group(1)  # Captura apenas o conteúdo dentro dos delimitadores

                    # Validação de identificador
                    if word.isidentifier() or not self.validate_identifier:
                        # Se a validação de lista de palavras estiver ativa
                        if self.validate_word_list:
                            if word in self.list_words:
                                # Aplica a cor para palavras dentro da lista
                                start_index = match.start(1)  # Captura o índice do conteúdo
                                self.setFormat(start_index, len(word), self.brace_format_in_list)
                            else:
                                # Aplica a cor para palavras fora da lista
                                start_index = match.start(1)
                                self.setFormat(start_index, len(word), self.brace_format_outside_list)
                        else:
                            # Se a validação da lista estiver desativada, aplica a cor padrão
                            start_index = match.start(1)
                            self.setFormat(start_index, len(word), self.brace_format_in_list)
                    else:
                        # Se não for um identificador válido
                        start_index = match.start(1)
                        self.setFormat(start_index, len(word), self.brace_format_outside_list)

        @classmethod
        def format_text(cls, text: str, patterns: list[re.Pattern] = [re.compile(r'{(.*?)}')], color_word_identifier = Styles.Color.blue, color_word_not_identifier = 'red'):

            def replace_word(match):
                word: str = match.group(1)
                full_match = match.group(0)
                open_delim = full_match[0] if len(full_match) > 0 else ''
                close_delim = full_match[-1] if len(full_match) > 1 else ''

                if word.isidentifier():
                    return f'{open_delim}<span style="color:{color_word_identifier};">{word}</span>{close_delim}'
                else:
                    return f'{open_delim}<span style="color:{color_word_not_identifier};">{word}</span>{close_delim}'

            formatted_text = text
            for pattern in patterns:
                formatted_text = pattern.sub(replace_word, formatted_text)

            return formatted_text

    # Função que aplica o syntax highlighter no QTextEdit
    @classmethod
    def apply_braces_highlighter(cls, text_edit: QTextEdit, braces_types : list[BracesHighlighter.BracesType]=[], validate_word_list=False, validate_identifier=False):
        highlighter = cls.BracesHighlighter(text_edit.document(), braces_types, validate_word_list, validate_identifier)
        setattr(text_edit, "highlighter", highlighter)  # Adiciona o highlighter como um atributo de text_edit
        return highlighter
    
    class Colorize:

        def __init__(self, widget : Browser | Edit | QTextBrowser | QTextEdit, plainText : str,  not_use_rgb : bool, file_type : DocumentTypeFile):

            document = widget.document()
            cursor = QTextCursor(document)

            if file_type.value == Text.DocumentTypeFile.Json.value:
                self.findall(cursor, r'(?<=:\s)("[^"]*")', Styles.Color.maron.QColor)
                return

            pattern_string = r'''(["])(.*?)\1'''
    
            exceptions = [DocumentOptions("List", Styles.Color.dark_green.QColor)]
            pattern_class_name = r'(?i)(Public|Private) (?i)Class (\w+)'
            options = ReservedWords.words()
            function_color = Styles.Color.yellow.QColor
            patterns = {}

            pattern_multi_comments = None
            starts_with = ["'", "//", "#"]
            if file_type.value == Text.DocumentTypeFile.VB.value:
                starts_with = ["'"]

            elif file_type.value == Text.DocumentTypeFile.CSharp.value:
                options = ReservedWords.words_cs()
                starts_with = ["//"]
                pattern_multi_comments = re.compile(r'/\*(.*?)\*/', re.DOTALL)

            elif file_type.value == Text.DocumentTypeFile.Python.value:
                pattern_string = r'''(["']{3}|["'])(.*?)\1'''
                pattern_class_name = r'class (\w+)'
                function_color = Styles.Color.dark_green.QColor
                options = ReservedWords.words_py()
                exceptions = [DocumentOptions("__init__", Styles.Color.blue.QColor)]
                starts_with = ["#"]

            if not not_use_rgb:

                # Agrupar palavras pela mesma cor
                color_groups = {}
                for option in options:
                    # Obtendo a cor em formato hexadecimal
                    color_hex = option.color.name(QColor.NameFormat.HexRgb)
                    if color_hex not in color_groups:
                        color_groups[color_hex] = []
                    color_groups[color_hex].append(option.word)

                for color, words in color_groups.items():
                    # Junta as palavras em um único padrão usando '|'
                    word_pattern = r'\b(' + '|'.join(re.escape(word) for word in words) + r')\b'
                    color_css = f"color: {color};"
                    replacement = f'<span style="{color_css}">\\1</span>'
                    patterns[word_pattern] = replacement

                widget.setPlainText(plainText)
                html = widget.toHtml()
                for pattern, replacement in patterns.items():
                    # Substituições são feitas no texto convertido em HTML
                    html = re.sub(pattern, replacement, html, flags=re.MULTILINE | re.DOTALL)

                widget.setHtml(html)
                
                pattern_function_names = r'(\w+)\([^)]*\)'
                unique_words = self.get_dict_options(options)[0]
                self.finditer_pattern(cursor, plainText, pattern_function_names, 1, function_color, exceptions, unique_words)

                self.finditer_pattern(cursor, plainText, pattern_class_name, 2, Styles.Color.dark_green.QColor)
                
                # string
                self.findall(cursor, pattern_string, Styles.Color.maron.QColor)

                #comentarios
                self.line(cursor, Styles.Color.light_green.QColor, starts_with)
                if pattern_multi_comments:
                    self.finditer_pattern(cursor, plainText, pattern_multi_comments, 1, Styles.Color.light_green.QColor)

                
        @staticmethod
        def __merge_char_format(cursor: QTextCursor, match: re.Match, group: int, _format: QTextCharFormat, ignore_words: list, word_exceptions_map: dict):
            
            try:
                name = match.group(group)

                # Verifica se a palavra deve ser ignorada
                if name in ignore_words:
                    return

                start = match.start(group)
          
                cursor.movePosition(QTextCursor.MoveOperation.Start)

                cursor.setPosition(cursor.selectionStart() + start, QTextCursor.MoveMode.MoveAnchor)
                cursor.setPosition(cursor.selectionStart() + len(name) , QTextCursor.MoveMode.KeepAnchor)

                # Aplica formatação específica se houver exceção para a palavra
                if word_exceptions_map and name in word_exceptions_map:
                    exception_option = word_exceptions_map[name]
                    exception_format = QTextCharFormat()
                    exception_format.setForeground(exception_option.color)
              
                    cursor.mergeCharFormat(exception_format)
                    cursor.charFormat().foreground
                else:
                    cursor.mergeCharFormat(_format)
            except Exception as e:
                ...


        @classmethod
        def finditer_pattern(cls, cursor: QTextCursor, plainText: str, pattern: str, group: int, color: QColor, exceptions=[], ignore_words=[]):
   
            word_exceptions_map = {exception.word: exception for exception in exceptions}

            matches = re.finditer(pattern, plainText)

            _format = QTextCharFormat()
            _format.setForeground(color)  # Define a cor desejada para a palavra-chave

            for match in matches:
                cls.__merge_char_format(cursor, match, group, _format, ignore_words, word_exceptions_map)


        @classmethod
        def finditer_words(cls, cursor: QTextCursor, words: list[str | list | tuple], group: int, color: QColor, exceptions=[], ignore_words=[]):
     
            # Se a posição de início foi especificada, mova o cursor para essa posição
            cursor.movePosition(QTextCursor.MoveOperation.Start)

            cursor.select(QTextCursor.SelectionType.Document)
            selected_text = cursor.selectedText()

            word_exceptions_map = {exception.word: exception for exception in exceptions}

            _format = QTextCharFormat()
            _format.setForeground(color)  # Define a cor desejada para a palavra-chave

            for word in words:
                try:
                    if isinstance(word, (list, tuple)):
                        type_of_quotes = word[0]
                        word = word[1]
                        if type_of_quotes == '"':
                            word = f'"{word}"'
                        elif type_of_quotes == '"""':
                            word = f'"""{word}"""'
                        elif type_of_quotes == "'":
                            word = f"'{word}'"
                        elif type_of_quotes == "'''":
                            word = f"'''{word}'''"

                    for match in re.finditer(re.escape(word), selected_text):
                        cls.__merge_char_format(cursor, match, group, _format, ignore_words, word_exceptions_map)
                except Exception as e:
                    ...

        @staticmethod
        def get_dict_options(options):
            unique_words = {}
            multiple_words = {}

            for option in options:
                words = option.word.split()
                if len(words) == 1:
                    unique_words[words[0]] = option
                else:
                    multiple_words[option.word] = option

            return unique_words, multiple_words

        @classmethod
        def findall(cls, cursor: QTextCursor, pattern: str, color: QColor):
 
            cursor.movePosition(QTextCursor.MoveOperation.Start)
            cursor.select(QTextCursor.SelectionType.Document)
            selected_text = cursor.selectedText()
            matches = re.findall(pattern, selected_text)

            # Encontre os valores repetidos
            valores_repetidos = [item for item in matches if matches.count(item) > 1]

            # Crie a primeira lista com valores únicos (sem repetições)
            lista_sem_repeticao = list(set(matches) - set(valores_repetidos))

            # Crie a segunda lista com os valores repetidos
            lista_repetidos = list(set(valores_repetidos))

            for match in lista_sem_repeticao:
                try:
                    if type(match) == list or type(match) == tuple:
                        type_of_quotes = match[0]
                        match = match[1]
                        if type_of_quotes == '"':
                            match = f'"{match}"'
                        elif type_of_quotes == '"""':
                            match = f'"""{match}"""'
                        elif type_of_quotes == "'":
                            match = f"'{match}'"
                        elif type_of_quotes == "'''":
                            match = f"'''{match}'''"

                    start = selected_text.find(match)
                    end = start + len(match)

                    if start != -1 and end != -1:
                        cursor.movePosition(QTextCursor.MoveOperation.Start)
                        cursor.setPosition(cursor.selectionStart() + start, QTextCursor.MoveMode.MoveAnchor)
                        cursor.setPosition(cursor.selectionStart() + len(match), QTextCursor.MoveMode.KeepAnchor)
                        _format = QTextCharFormat()
                        _format.setForeground(color)
                        cursor.mergeCharFormat(_format)
                except Exception as e:
                    ...

            # Chama a função finditer_words com a lista de valores repetidos
            cls.finditer_words(cursor, lista_repetidos, 0, color)


        @classmethod
        def line(cls, cursor: QTextCursor, color: QColor, starts_with=()):
            starts_with = tuple(starts_with)

            # Se a posição de início foi especificada, mova o cursor para essa posição
            cursor.movePosition(QTextCursor.MoveOperation.Start)

            while not cursor.atEnd():
                cursor.select(QTextCursor.SelectionType.BlockUnderCursor)
                selected_text = cursor.selectedText()
                block_text = selected_text.replace('\u2029', '').strip()
                _format = QTextCharFormat()
                _format.setForeground(color)


                if block_text.startswith(starts_with):
                    cursor.mergeCharFormat(_format)
                else:
                    for start_char in starts_with:
                        if start_char in block_text:
                            start_pos = selected_text.find(start_char)
                            start = cursor.selectionStart() + start_pos
                            end = cursor.selectionStart() + len(selected_text)

                            cursor.setPosition(start, QTextCursor.MoveMode.MoveAnchor)
                            cursor.setPosition(end, QTextCursor.MoveMode.KeepAnchor)
                            cursor.mergeCharFormat(_format)

                cursor.movePosition(QTextCursor.MoveOperation.NextBlock)

    class CompareTexts(object):
        def __init__(self, text_edit_original : QTextEdit | QTextBrowser, new_text_edit : QTextEdit | QTextBrowser, theme : str):
            self.text_edit_original = text_edit_original
            self.new_text_edit = new_text_edit
            self.rbg_comment = Styles.Color.light_green.QColor
            self.compare(theme)
          

        def compare(self, theme: str):
            
            text1 = self.text_edit_original.toPlainText()
            text2 = self.new_text_edit.toPlainText()
            text1 = text1.replace('\u2029', '').strip()
            text2 = text2.replace('\u2029', '').strip()

            min_length = min(len(text1), len(text2))
 
            for i in range(min_length):
                if text1[i] != text2[i]:
                    #if text1[i].strip():
                    #    self.highlight_difference(self.Interface.textEdit_file_original, i)
                    if  text2[i].strip():
                        self.highlight_difference(self.new_text_edit, i, theme)

        def highlight_difference(self, text_edit, index, theme : str):
            cursor = text_edit.textCursor()
            cursor.setPosition(index)
            cursor.movePosition(QTextCursor.MoveOperation.Right, QTextCursor.MoveMode.KeepAnchor, n=1)

            if self.rbg_comment == cursor.charFormat().foreground().color().rgb():
                return

            fmt = QTextCharFormat()
            color_difference = QColor(237, 237, 237) if theme == 'light' else QColor(15, 15, 15)
            fmt.setBackground(QBrush(color_difference))
            
            cursor.mergeCharFormat(fmt)

            text_edit.setTextCursor(cursor)

        #def highlight_line(self, text_edit, line_number, theme : str):
        #    cursor = text_edit.textCursor()
        #    cursor.setPosition(0)
        #    cursor.movePosition(QTextCursor.MoveOperation.Down, QTextCursor.MoveMode.KeepAnchor, n=line_number + 1)
        #    cursor.movePosition(QTextCursor.MoveOperation.EndOfLine, QTextCursor.MoveMode.KeepAnchor)
        
        #    if self.rbg_comment == cursor.charFormat().foreground().color().rgb():
        #        return

        #    fmt = QTextCharFormat()

        #    color_difference = (235, 235, 235) if theme == 'light' else (20, 20, 20)
        #    fmt.setBackground(QBrush(QColor(*color_difference)))
            
        #    cursor.mergeCharFormat(fmt)
        #    text_edit.setTextCursor(cursor)


    class ReservedWords(ReservedWords):
        ...

    @classmethod
    def noNewLine(cls, widget : Browser | Edit | QTextBrowser | QTextEdit):
        widget.setLineWrapMode(QTextEdit.LineWrapMode.NoWrap)

        # Definir uma nova função para sobrescrever o keyPressEvent
        def keyPressEvent(event):
            # Ignorar teclas de quebra de linha (Enter/Return)
            if event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
                event.ignore()  # Ignora o evento da tecla Enter/Return
            else:
                original_keyPressEvent(event)  # Chama o método original para outras teclas

        # Salva o keyPressEvent original
        original_keyPressEvent = widget.keyPressEvent
        # Substitui o keyPressEvent
        widget.keyPressEvent = keyPressEvent

    @classmethod
    def setDocument(cls, widget : Browser | Edit | QTextBrowser | QTextEdit, text : str , scroll_top = True, scroll_to_bottom = False, not_use_rgb = False, file_type : DocumentTypeFile = None, lines_index_start = -1):
        if widget.adjust_height:
            widget.textChanged.disconnect(widget.adjustWidgetHeight)

        scroll_bar_value = widget.verticalScrollBar().value()

        #text_doc = ""
        #if lines_index_start >= 0:
        #    lines = text.splitlines()
        #    max_line_num = lines_index_start + len(lines)
        #    line_num_width = len(str(max_line_num))
        #    text_doc = '\n'.join(f"{Utils.adjust_text_length(str(i + 1), line_num_width, 5)}{line}" for i, line in enumerate(lines, start=lines_index_start))
        #else:
            
        text_doc = text

        document = widget.document()
        if '!DOCTYPE HTML PUBLIC' in text_doc:
            document.setHtml(text_doc)
        else:
            document.setPlainText(text_doc)

        if file_type:
            plainText = widget.toPlainText()
            Text.Colorize(widget, plainText, not_use_rgb, file_type)
        
        if scroll_top:
            widget.setDocument(document)
        else:
            verticalScrollBar = widget.verticalScrollBar()
            widget.setDocument(document)
            if scroll_to_bottom:
                verticalScrollBar.setValue(verticalScrollBar.maximum())
            else:
                verticalScrollBar.setValue(scroll_bar_value)

        if widget.adjust_height:
            widget.textChanged.connect(widget.adjustWidgetHeight)
            widget.adjustWidgetHeight()


    @classmethod
    def setPlainText(widget : Browser | Edit ,  text : str, scroll_top = True):
        if scroll_top:
            widget.setPlainText(text)
        else:
            scroll_bar_value = widget.verticalScrollBar().value()
            widget.setPlainText(text)
            widget.ensureCursorVisible()
            widget.verticalScrollBar().setValue(scroll_bar_value)

    




