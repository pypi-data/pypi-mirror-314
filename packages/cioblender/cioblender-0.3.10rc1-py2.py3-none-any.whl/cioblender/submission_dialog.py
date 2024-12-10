"""
This script creates a Qt dialog for Conductor job submission in Blender.

It includes three tabs: Validation, Progress, and Response.

The script defines a custom stylesheet that mimics the Blender interface style.
"""

import sys
import time
import bpy
from PySide6 import QtWidgets, QtCore

from cioblender.validation_tab import ValidationTab
from cioblender.progress_tab import ProgressTab
from cioblender.response_tab import ResponseTab
from cioblender import validation

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

class SubmissionDialog(QtWidgets.QDialog):
    """
    A Qt dialog for Conductor job submission in Blender.

    This dialog includes three tabs: Validation, Progress, and Response.

    Args:
        payload: The payload data for job submission.
        parent: The parent widget (default is None).
    """
    def __init__(self, payload=None, parent=None):
        """
        Initialize the SubmissionDialog.

        Args:
            payload: The payload data for job submission.
            parent: The parent widget (default is None).
        """
        # super(SubmissionDialog, self).__init__(parent, QtCore.Qt.WindowStaysOnTopHint)
        super(SubmissionDialog, self).__init__(parent)

        # super(SubmissionDialog, self).__init__()
        self.setWindowTitle("Conductor Submission")

        # Apply the Blender-inspired stylesheet to the dialog
        self.setStyleSheet(blender_stylesheet)

        # Create a widget
        self.payload = payload
        self.parent = parent

        self.layout = QtWidgets.QVBoxLayout()
        self.tab_widget = QtWidgets.QTabWidget()
        self.setLayout(self.layout)
        self.layout.addWidget(self.tab_widget)
        self.setGeometry(200, 200, 1000, 694)

        self.validation_tab = ValidationTab(self.payload, self)
        self.tab_widget.addTab(self.validation_tab, "Validation")

        self.progress_tab = ProgressTab(self.payload, self)
        self.tab_widget.addTab(self.progress_tab, "Progress")

        self.response_tab = ResponseTab(self.payload, self)
        self.tab_widget.addTab(self.response_tab, "Response")

        self.tab_widget.setTabEnabled(1, False)
        self.tab_widget.setTabEnabled(2, False)

        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        # Release the widget when done with it
        #self.widget.deleteLater()

    def on_close(self):
        """Close the dialog when the "Close" button is clicked."""
        self.accept()

    def show_progress_tab(self):
        """Show the Progress tab and enable it."""
        self.tab_widget.setTabEnabled(1, True)
        self.tab_widget.setCurrentWidget(self.progress_tab)
        QtCore.QCoreApplication.processEvents()
        time.sleep(1)

    def show_response_tab(self):
        """Show the Response tab and enable it, while disabling the Validation tab."""
        self.tab_widget.setTabEnabled(2, True)
        self.tab_widget.setCurrentWidget(self.response_tab)
        self.tab_widget.setTabEnabled(0, False)
        QtCore.QCoreApplication.processEvents()
        time.sleep(1)


def run(payload):

    #Run the Conductor job submission dialog.

    #Args:
    #    payload: The payload data for job submission.
 

    app = QtWidgets.QApplication.instance()
    if app is None:
        app = QtWidgets.QApplication(sys.argv)

    dialog = SubmissionDialog(payload)
    errors, warnings, notices = validation.run(payload)
    dialog.validation_tab.populate(errors, warnings, notices)

    dialog.show()
    # Embed the QtWidget dialog within a Blender panel
    bpy.types.WindowManager.dialog = dialog

    app.exec_()

    # Explicitly delete the dialog and quit the application
    del dialog
    app.quit()

if __name__ == "__main__":
    payload = None  # Replace with your payload data
    run(payload)
