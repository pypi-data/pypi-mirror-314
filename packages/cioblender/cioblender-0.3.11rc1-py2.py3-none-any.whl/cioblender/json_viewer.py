"""
This script creates a Qt dialog for Conductor job submission in Blender.

It includes three tabs: Validation, Progress, and Response.

The script defines a custom stylesheet that mimics the Blender interface style.
"""

import sys
import bpy
from PySide6 import QtWidgets, QtCore
import json


# Define the Blender-inspired stylesheet
blender_stylesheet = """
QMainWindow {
    background-color: #333333;
    color: #FFFFFF;
    border: 1px solid #555555;
}

QWidget {
    background-color: #333333;
    color: #FFFFFF;
}

QMenuBar {
    background-color: #444444;
    color: #FFFFFF;
    border: 1px solid #555555;
}

QMenuBar::item {
    background-color: #444444;
    color: #FFFFFF;
    padding: 4px 10px;
    border-radius: 2px;
}

QMenuBar::item:selected {
    background-color: #555555;
    color: #FFFFFF;
}

QMenu {
    background-color: #444444;
    color: #FFFFFF;
    border: 1px solid #555555;
}

QMenu::item {
    background-color: #444444;
    color: #FFFFFF;
    padding: 4px 10px;
    border-radius: 2px;
}

QMenu::item:selected {
    background-color: #555555;
    color: #FFFFFF;
}

QPushButton {
    background-color: #555555;
    color: #FFFFFF;
    padding: 8px 10px;
    border: 1px solid #666666;
    border-radius: 2px;
}

QPushButton:hover {
    background-color: #666666;
    border: 1px solid #777777;
}

QLineEdit {
    background-color: #444444;
    color: #FFFFFF;
    padding: 3px;
    border: 1px solid #555555;
    border-radius: 2px;
}

QLineEdit:hover {
    background-color: #555555;
}

QTextEdit {
    background-color: #444444;
    color: #FFFFFF;
    border: 1px solid #555555;
    border-radius: 2px;
}

QTextEdit:hover {
    background-color: #555555;
}

QTabWidget {
    background-color: #444444;
    color: #FFFFFF;
    border: 1px solid #555555;
    border-top-left-radius: 4px;
    border-top-right-radius: 4px;
}

QTabWidget::tab-bar {
    alignment: center;
}

QTabBar::tab {
    background-color: #555555;
    color: #FFFFFF;
    padding: 4px 10px;
    border-top-left-radius: 4px;
    border-top-right-radius: 4px;
}

QTabBar::tab:selected {
    background-color: #666666;
}
"""


class JsonViewer(QtWidgets.QDialog):
    """
    A QDialog subclass for displaying JSON data in a read-only plain text editor.
    This dialog is designed to be non-modal, allowing users to interact with
    other windows while it is open. It mimics the Blender interface style and
    provides a user-friendly way to view formatted JSON data.

    Attributes:
        json_data (dict, list, str, int, float, bool, None): The JSON data to display.
            This can be any data type that is serializable to a JSON string.
        parent (QWidget, optional): The parent widget of this dialog. Defaults to None.

    Args:
        json_data (dict, list, str, int, float, bool, None): The JSON data to be displayed.
        parent (QWidget, optional): The parent widget. Defaults to None.
    """

    def __init__(self, json_data, parent=None):
        super(JsonViewer, self).__init__(parent, QtCore.Qt.Window)
        self.setWindowTitle("JSON Viewer")
        self.setGeometry(100, 100, 900, 594)
        self.setStyleSheet(blender_stylesheet)

        layout = QtWidgets.QVBoxLayout(self)

        self.text_edit = QtWidgets.QPlainTextEdit()
        self.text_edit.setReadOnly(True)
        self.text_edit.setPlainText(json.dumps(json_data, indent=4))
        layout.addWidget(self.text_edit)

        close_button = QtWidgets.QPushButton("Close")
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)


# Maintain a list of open JsonViewer instances to prevent them from being garbage collected.
open_json_viewers = []


def invoke_json_viewer(json_data):
    """
    Initializes and displays a JsonViewer dialog with the provided JSON data.
    Multiple instances of the JsonViewer can be opened and will remain responsive.
    This function ensures that each opened JsonViewer is kept in memory to prevent
    them from being hidden or closed prematurely.

    Args:
        json_data (dict, list, str, int, float, bool, None): The JSON data to be displayed in
            the JsonViewer dialog. This can be any data type that is serializable to a JSON string.
    """
    print("Call JSON Dialog ...")
    app = QtWidgets.QApplication.instance()
    if app is None:
        app = QtWidgets.QApplication(sys.argv)
        app.setQuitOnLastWindowClosed(False)  # Prevent app from exiting when dialog is closed

    print("JSON Dialog ...")
    json_window = None
    try:
        json_window = next(iter(app.topLevelWidgets()), None)
    except Exception as e:
        print(f"Unable to get the main Blender window due to: {e}")

    dialog = JsonViewer(json_data, parent=json_window)
    dialog.show()

    # Add the new dialog to the list of open viewers to keep it referenced
    open_json_viewers.append(dialog)


if __name__ == "__main__":
    payload = None  # Replace None with your JSON data as needed
    invoke_json_viewer(payload)