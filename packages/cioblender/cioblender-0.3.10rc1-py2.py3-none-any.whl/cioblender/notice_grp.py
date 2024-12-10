import os
from PySide6 import QtWidgets, QtCore, QtGui
from cioblender.const import PLUGIN_DIR
import webbrowser


class NoticeGrp(QtWidgets.QFrame):
    def __init__(self, text, severity="info", url=None):
        """
        Initialize a Notice Group widget.

        This widget is used to display a notice or message with optional severity and a clickable link.

        :param text: The text message to display.
        :param severity: The severity level of the notice (options: "info", "warning", "error", "success").
        :param url: The URL to open when the notice is clicked (optional).
        """
        super(NoticeGrp, self).__init__()

        self.url = url
        if severity not in ["info", "warning", "error", "success"]:
            severity = "error"

        self.scale_factor = self.logicalDpiX() / 96.0
        icon_size = 24 if self.logicalDpiX() < 150 else 48

        self.setFrameStyle(QtWidgets.QFrame.Panel | QtWidgets.QFrame.Sunken)
        self.setLineWidth(2)

        layout = QtWidgets.QHBoxLayout()
        self.setLayout(layout)

        icon_filename = "Conductor{0}_{1}x{1}.png".format(severity.capitalize(), icon_size)
        iconPath = os.path.join(PLUGIN_DIR, "icons", icon_filename)

        img_label = QtWidgets.QLabel(self)
        pixmap = QtGui.QPixmap(iconPath)
        img_label.setPixmap(pixmap)
        img_label.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        img_label.setFixedWidth(40 * self.scale_factor)
        layout.addWidget(img_label)

        if self.url:
            widget = QtWidgets.QPushButton(text)
            widget.setAutoDefault(False)
            widget.clicked.connect(self.on_click)
        else:
            widget = QtWidgets.QLabel()
            widget.setMargin(10)
            widget.setWordWrap(True)
            widget.setText(text)

        layout.addWidget(widget)

    def on_click(self):
        webbrowser.open(self.url)
