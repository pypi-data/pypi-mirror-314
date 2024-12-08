import os
from pathlib import Path

from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QIcon, QAction
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import QMessageBox, QMenu

from frontengine.utils.multi_language.language_wrapper import language_wrapper


class WebWidget(QWebEngineView):

    def __init__(self, url: str, is_file: bool = False):
        super().__init__()
        self.menu = None
        self.close_action = None
        self.opacity: float = 0.2
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        if not is_file:
            self.load(url)
        else:
            self.web_url = Path(url)
            if self.web_url.exists() and self.web_url.is_file():
                # QUrl non ascii path encode, Avoid read wrong path and file name
                source = QUrl.fromLocalFile(str(self.web_url))
                print(f"Origin file {str(self.web_url)}")
                self.load(source)
            else:
                message_box = QMessageBox(self)
                message_box.setText(
                    language_wrapper.language_word_dict.get("webview_message_box_text")
                )
                message_box.show()
        # Set Icon
        self.icon_path = Path(os.getcwd() + "/je_driver_icon.ico")
        if self.icon_path.exists() and self.icon_path.is_file():
            self.setWindowIcon(QIcon(str(self.icon_path)))

    def contextMenuEvent(self, event):
        if self.close_action is None:
            self.close_action = QAction("Close")
            self.close_action.triggered.connect(self.close)
        if self.menu is None:
            self.menu = QMenu(self)
            self.menu.addAction(self.close_action)
        self.menu.popup(event.globalPos())

    def set_ui_variable(self, opacity: float = 0.2) -> None:
        self.opacity = opacity
        self.setWindowOpacity(opacity)

    def set_ui_window_flag(self, enable_input: bool = False, show_on_bottom: bool = False) -> None:
        if not enable_input:
            self.setWindowFlag(
                Qt.WindowType.WindowTransparentForInput
            )
            self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        if show_on_bottom:
            self.setWindowFlag(Qt.WindowType.WindowStaysOnBottomHint)
        else:
            self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)
        self.setWindowFlag(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowType_Mask |
            Qt.WindowType.Tool
        )

    def mousePressEvent(self, event) -> None:
        # if event.button() == Qt.MouseButton.MiddleButton:
        print(event.button())
        super().mousePressEvent(event)

    def mouseDoubleClickEvent(self, event) -> None:
        super().mouseDoubleClickEvent(event)

    def mouseGrabber(self) -> None:
        super().mouseGrabber()
