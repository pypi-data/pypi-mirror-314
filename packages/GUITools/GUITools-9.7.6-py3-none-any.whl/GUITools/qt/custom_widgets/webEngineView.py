# -*- coding: latin -*-
from PyQt6.QtWidgets import QWidget, QVBoxLayout
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEngineSettings
from PyQt6.QtWebEngineCore import QWebEngineDownloadRequest
from PyQt6.QtCore import QUrl, QFileInfo, QCoreApplication
from ..dialog import Dialog
from ..notification import Notification
import os

class WebEngineView(QWebEngineView):
    def __init__(self, parent : QWidget = None):
        super().__init__(parent=parent)
        self.isLoaded = False
        self._file_name = ""
        self.settings().setAttribute(QWebEngineSettings.WebAttribute.PluginsEnabled, True)
        self.settings().setAttribute(QWebEngineSettings.WebAttribute.PdfViewerEnabled, True)

        ## Connect the downloadRequested signal
        profile = self.page().profile()
        profile.downloadRequested.connect(self.on_downloadRequested)
      
        self.setUrl(QUrl("https://example.com"))
        self.close()
        self.loadFinished.connect(self.on_loadFinished)
        ##self.webView.urlChanged

    def on_loadFinished(self):
        if not self.isLoaded:
            self.show()
            self.isLoaded = True

    def on_downloadRequested(self, download_request: QWebEngineDownloadRequest):
        old_path = download_request.url().path() 
        suffix = QFileInfo(old_path).suffix()

        path, _ = Dialog.saveFileName(QCoreApplication.instance().activeWindow(), "Save File", "*." + suffix, self._file_name)

        if path:
            download_request.stateChanged.connect(lambda : self.on_downloadStateChanged(download_request))
            download_request.setDownloadDirectory(os.path.dirname(path))
            download_request.setDownloadFileName(os.path.basename(path))
            download_request.accept()

    def on_downloadStateChanged(self, download_request: QWebEngineDownloadRequest):
        if download_request.state() == QWebEngineDownloadRequest.DownloadState.DownloadCompleted:
            Notification.success('Download',f"Download finished: {os.path.normpath(os.path.join(download_request.downloadDirectory(), download_request.downloadFileName()))}")
        elif download_request.state() == QWebEngineDownloadRequest.DownloadState.DownloadInterrupted:
            Notification.error('Download', "Download interrupted")
        elif download_request.state() == QWebEngineDownloadRequest.DownloadState.DownloadCancelled:
            Notification.error('Download', "Download cancelled")

class CustomWebEngineView(QWidget):
    def __init__(self, parent=None):
        super(CustomWebEngineView, self).__init__(parent)

        self.vlayout = QVBoxLayout(self)
        self.vlayout.setContentsMargins(0,0,0,0)
        self.wiew = WebEngineView()
   
        self.vlayout.addWidget(self.wiew)

    def setUrlFromLocalFile(self, url: str) -> None:
        self.wiew._file_name = os.path.basename(url)
        return self.wiew.setUrl(QUrl.fromLocalFile(url))

    def setUrl(self, url: str) -> None:
        self.wiew._file_name = ""
        return self.wiew.setUrl(QUrl(url))

