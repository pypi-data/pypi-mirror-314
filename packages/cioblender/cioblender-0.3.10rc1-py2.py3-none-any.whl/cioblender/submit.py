import traceback
import sys
import os
import bpy
from ciocore import conductor_submit
from PySide6 import QtWidgets, QtCore
from cioblender import validation
from cioblender.submission_dialog import SubmissionDialog

def invoke_submission_dialog(kwargs, payload):
    """
    Display the Conductor submission dialog.

    Args:
        payload: The payload data for job submission.
    """
    try:
        print("Call SubmissionDialog ...")
        app = QtWidgets.QApplication.instance()
        if app is None:
            app = QtWidgets.QApplication(sys.argv)

        print("loading SubmissionDialog ...")
        # Get the main Blender window as the parent for the dialog
        blender_window = None
        try:
            blender_window = next(iter(app.topLevelWidgets()), None)
        except:
            print("Unable to get the main Blender window")

        dialog = SubmissionDialog(payload=payload, parent=blender_window)
        errors, warnings, notices = validation.run(kwargs)
        dialog.validation_tab.populate(errors, warnings, notices)

        dialog.show()
        # Embed the QtWidget dialog within a Blender panel
        bpy.types.WindowManager.dialog = dialog

        # Removed app.exec_() to avoid blocking the Blender UI

        # Add a Blender timer to intermittently process Qt events
        def process_qt_events():
            app.processEvents()
            return 0.1  # Adjust the timer interval as needed

        bpy.app.timers.register(process_qt_events)

    except Exception as e:
        print("Error in calling SubmissionDialog: {}".format(e))

def invoke_submission_dialog_original(kwargs, payload):
    """
    Display the Conductor submission dialog.

    Args:
        payload: The payload data for job submission.
    """
    try:
        print("Call SubmissionDialog ...")
        app = QtWidgets.QApplication.instance()
        if app is None:
            app = QtWidgets.QApplication(sys.argv)

        print("loading SubmissionDialog ...")
        # Get the main Blender window as the parent for the dialog
        blender_window = None
        try:
            blender_window = next(iter(app.topLevelWidgets()), None)
        except:
            print("Unable to get the main Blender window")

        dialog = SubmissionDialog(payload=payload, parent=blender_window)
        errors, warnings, notices = validation.run(kwargs)
        dialog.validation_tab.populate(errors, warnings, notices)

        dialog.show()
        # Embed the QtWidget dialog within a Blender panel
        bpy.types.WindowManager.dialog = dialog

        app.exec_()

        # Explicitly delete the dialog and quit the application
        del dialog
        app.quit()

    except Exception as e:
        print("Error in calling SubmissionDialog: {}".format(e))


def submit_job(payload):
    """
    Submit a job to Conductor and return the response.

    Args:
        payload: The payload data for job submission.

    Returns:
        dict: A dictionary containing the job submission response and response code.
    """

    try:
        print("upload_paths: ", payload.get("upload_paths"))
        remote_job = conductor_submit.Submit(payload)
        response, response_code = remote_job.main()
    except:
        response = traceback.format_exc()
        response_code = 500
    # return {"response": response, "response_code": response_code}
    return response
