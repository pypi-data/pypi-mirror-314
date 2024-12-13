from PyQt6.QtWidgets import QSizePolicy, QLabel, QFrame, QVBoxLayout, QApplication
from PyQt6.QtGui import QTextDocument
from PyQt6.QtCore import Qt
import markdown
import webbrowser

class ResizeLabel(QFrame):

    def __init__(self, text = "", use_markdown = False, wordWrap = True, textBrowserInteraction = True, margins = [0,0,0,0]):
        super().__init__()
        self.label = QLabel("", self)
        self.label.linkActivated.connect(self.open_link)
        self._document = QTextDocument()
        
        if wordWrap:
            self.label.setWordWrap(True)

        if textBrowserInteraction:
            self.label.setTextInteractionFlags(
                Qt.TextInteractionFlag.TextBrowserInteraction |
                Qt.TextInteractionFlag.LinksAccessibleByMouse
            )
            
        layout = QVBoxLayout(self)
        layout.setContentsMargins(*margins)
        layout.setSpacing(0)
        layout.addWidget(self.label)
        self.setText(text, use_markdown)
        self.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed))

    def open_link(self, url : str):
        webbrowser.open(url)

    def copy(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self._document.toPlainText())
      
    def setText(self,  text : str, use_markdown = False):
        if use_markdown:
            html = markdown.markdown(text.strip())
            self._document.setHtml(html)
            self.label.setText(html)
        else:
            self._document.setPlainText(text)
            self.label.setText(text)
        self.adjustSize()

    def adjustSize(self):
        self.label.adjustSize() 
        return super().adjustSize()