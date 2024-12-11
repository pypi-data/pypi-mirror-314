from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QLabel,
    QProgressBar,
    QFrame,
)
from PySide6.QtCore import Qt

from cioblender import const as k

CHIP_HEIGHT = 30

ROUNDED_LEFT = (
    "border-radius: 0; border-top-left-radius: 3px; border-bottom-left-radius: 3px"
)
ROUNDED_RIGHT = (
    "border-radius: 0; border-top-right-radius: 3px; border-bottom-right-radius: 3px"
)

RIBBON_STYLESHEET = {
    "OFF": f"background-color: {k.OFF_GRADIENT};{ROUNDED_LEFT};",
    "MD5_COMPLETE": f"background-color: {k.MD5_GRADIENT};{ROUNDED_LEFT};",
    "MD5_CACHED": f"background-color: {k.MD5_CACHE_GRADIENT};{ROUNDED_LEFT};",
}

PROGRESS_BAR_STYLESHEETOLD = f"""
QProgressBar {{
    background-color: {k.OFF_GRADIENT};
    font-size: 8px;
    text-align: center;
    {ROUNDED_RIGHT};
}} 
QProgressBar::chunk {{
    background-color: {k.UPLOAD_GRADIENT};
}}
"""

PROGRESS_BAR_STYLESHEET_ALREADY_UPLOADEDOLD = f"""
QProgressBar {{
    background-color: {k.OFF_GRADIENT};
    font-size: 8px;
    text-align: center;
    {ROUNDED_RIGHT};
}}
QProgressBar::chunk {{
    background-color: {k.UPLOAD_CACHE_GRADIENT};
}}
"""


class MyProgressBar(QProgressBar):
    def __init__(self, *args, **kwargs):
        super(MyProgressBar, self).__init__(*args, **kwargs)
        self.setAlignment(Qt.AlignCenter)
        self._text = None

    def setText(self, text):
        self._text = text

    def text(self):
        return self._text

class FileStatusRow(QWidget):
    def __init__(self, filename, *args, **kwargs):
        super(FileStatusRow, self).__init__(*args, **kwargs)

        self.layout = QHBoxLayout()

        self.layout.setContentsMargins(10, 0, 10, 0)
        self.layout.setSpacing(0)

        self.setLayout(self.layout)
        self.filename_label = QLabel(filename)
        self.filename_label.setContentsMargins(0, 0, 10, 0)
        self.status_chip = StatusChip()

        self.layout.addWidget(self.filename_label)
        self.layout.addStretch()
        self.layout.addWidget(self.status_chip)


class StatusChip(QFrame):
    def __init__(self, *args, **kwargs):
        super(StatusChip, self).__init__(*args, **kwargs)

        self.setFixedHeight(CHIP_HEIGHT)
        self.setFixedWidth(80)

        layout = QHBoxLayout()
        layout.setSpacing(0)
        self.setLayout(layout)

        self.md5_ribbon = QFrame()
        self.md5_ribbon.setFixedWidth(14)
        self.md5_ribbon.setFixedHeight(CHIP_HEIGHT)
        self.md5_ribbon.setStyleSheet(RIBBON_STYLESHEET["OFF"])

        self.upload_progress_bar = QProgressBar()
        self.upload_progress_bar.setFixedWidth(64)
        self.upload_progress_bar.setFixedHeight(CHIP_HEIGHT)
        # self.upload_progress_bar.setRange(0, 100)
        self.upload_progress_bar.setAlignment(Qt.AlignCenter)

        self.set_bar_stylesheet("PROGRESS_BAR_STYLESHEET")
        self.upload_progress_bar.setAlignment(Qt.AlignCenter)

        layout.addWidget(self.md5_ribbon)
        layout.addWidget(self.upload_progress_bar)

        self.progress = {
            "bytes_to_upload": 0,
            "bytes_uploaded": 0,
            "already_uploaded": False,
            "md5": "",
            "md5_was_cached": False,
        }
    def set_bar_stylesheet(self, stylesheet):
        if stylesheet == "PROGRESS_BAR_STYLESHEET":
            self.upload_progress_bar.setStyleSheet(
                '''
                QProgressBar
                {
                    background-color: {k.OFF_GRADIENT};
                    font-size: 10px;
                    border: 2px solid grey;
                    border-radius: 5px;
                    text-align: center;
                    
                }
                QProgressBar::chunk
                {
                    background-color: {k.UPLOAD_CACHE_GRADIENT};
                    width: 2.15px;
                    margin: 0.5px;
                }
                '''
            )
        elif stylesheet == "PROGRESS_BAR_STYLESHEET_ALREADY_UPLOADED":
            self.upload_progress_bar.setStyleSheet(
                '''
            QProgressBar
            {
                background-color: {k.OFF_GRADIENT};
                font-size: 10px;
                border: 2px solid grey;
                border-radius: 5px;
                text-align: center;
                
            }
            QProgressBar::chunk
            {
                background-color: {k.UPLOAD_CACHE_GRADIENT};
                width: 2.15px;
                margin: 0.5px;
            }
            '''
        )

    def update_status(self, progress):
        self.progress.update(progress)

        if self.progress["md5_was_cached"]:
            md5_stylesheet = RIBBON_STYLESHEET["MD5_CACHED"]
        elif self.progress["md5"]:
            md5_stylesheet = RIBBON_STYLESHEET["MD5_COMPLETE"]
        else:
            md5_stylesheet = RIBBON_STYLESHEET["OFF"]

        self.md5_ribbon.setStyleSheet(md5_stylesheet)

        if self.progress["already_uploaded"]:
            percentage = 100
            self.set_bar_stylesheet("PROGRESS_BAR_STYLESHEET_ALREADY_UPLOADED")
            # self.upload_progress_bar.setFormat("Cached")
        elif self.progress["bytes_to_upload"] == 0:
            percentage = 0
            self.set_bar_stylesheet("PROGRESS_BAR_STYLESHEET")
        else:
            percentage = int(
                self.progress["bytes_uploaded"] * 100 / self.progress["bytes_to_upload"]
            )
            self.set_bar_stylesheet("PROGRESS_BAR_STYLESHEET")

        self.set_bar_stylesheet("PROGRESS_BAR_STYLESHEET")
        self.upload_progress_bar.setValue(percentage)

    def update_progress(self, value):
        # Update the progress bar
        if value <= 100 and value > 0:
            self.upload_progress_bar.setFormat(f"{value}%")

            self.upload_progress_bar.setValue(value)
            self.set_bar_stylesheet("PROGRESS_BAR_STYLESHEET")
            self.upload_progress_bar.setVisible(True)
        else:
            self.upload_progress_bar.setVisible(False)
