import sys
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QImage, QPainter
from PyQt5.QtWidgets import QApplication, QMainWindow, QToolBar, QLineEdit, QAction, QFileDialog, QMessageBox
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage

class WebBrowser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Web Browser")
        self.setGeometry(100, 100, 800, 600)

        self.web_view = QWebEngineView(self)
        self.web_view.loadFinished.connect(self.set_title)
        self.web_view.urlChanged.connect(self.update_address_bar)
        self.setCentralWidget(self.web_view)

        self.toolbar = QToolBar()
        self.addToolBar(self.toolbar)

        self.back_btn = QAction('Back', self)
        self.toolbar.addAction(self.back_btn)

        self.forward_btn = QAction('Forward', self)
        self.toolbar.addAction(self.forward_btn)

        self.reload_btn = QAction('Reload', self)
        self.toolbar.addAction(self.reload_btn)

        self.screenshot_btn = QAction('Take Screenshot', self)
        self.toolbar.addAction(self.screenshot_btn)

        self.address_bar = QLineEdit()
        self.address_bar.returnPressed.connect(self.load_url)
        self.toolbar.addWidget(self.address_bar)

        self.web_view.createWindow = self.create_window
        self.web_view.page().featurePermissionRequestCanceled.connect(self.permission_request_canceled)

        self.back_btn.triggered.connect(self.web_view.back)
        self.forward_btn.triggered.connect(self.web_view.forward)
        self.reload_btn.triggered.connect(self.web_view.reload)
        self.screenshot_btn.triggered.connect(self.take_screenshot)

    def load_url(self):
        url = self.address_bar.text()
        self.web_view.setUrl(QUrl.fromUserInput(url))

    def set_title(self):
        title = self.web_view.page().title()
        self.setWindowTitle(f"Web Browser - {title if title else 'Untitled'}")

    def take_screenshot(self):
        image = QImage(self.web_view.size(), QImage.Format_ARGB32)
        painter = QPainter(image)
        self.web_view.render(painter)
        painter.end()

        file_path, _ = QFileDialog.getSaveFileName(self, "Save Screenshot", "", "PNG (*.png);;JPEG (*.jpg *.jpeg)")

        if file_path:
            if image.save(file_path):
                QMessageBox.information(self, "Screenshot Saved", "Screenshot saved successfully!")
            else:
                QMessageBox.warning(self, "Error", "Failed to save the screenshot.")

    def create_window(self, window_type):
        # Handle link clicks in the same window
        new_web_view = QWebEngineView(self)
        new_web_view.urlChanged.connect(self.update_address_bar)
        self.setCentralWidget(new_web_view)
        return new_web_view

    def permission_request_canceled(self, frame, feature):
        if feature == QWebEnginePage.Feature.CloseWindowCFrame:
            self.close_window(frame)

    def close_window(self, frame):
        if isinstance(frame, QWebEngineView):
            frame.deleteLater()

    def update_address_bar(self, url):
        self.address_bar.setText(url.toString())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    browser = WebBrowser()
    browser.show()
    sys.exit(app.exec_())
