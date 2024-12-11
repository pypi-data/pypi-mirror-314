import bpy
from cioblender.buttoned_scroll_panel import ButtonedScrollPanel
from cioblender.notice_grp import NoticeGrp
from cioblender import submit
from pathlib import Path


class ValidationTab(ButtonedScrollPanel):

    def __init__(self, payload, dialog):
        """
       Initialize the ValidationTab.

       Args:
           payload: The payload containing submission data.
           dialog: The parent dialog to which this tab belongs.
       """
        super(ValidationTab, self).__init__(
            dialog,
            buttons=[("close", "Close"), ("save", "Save Scene and Continue Submission"), ("continue", "Continue Submission")])
        self.dialog = dialog
        self.payload = payload
        self.configure_signals()
        self.buttons["close"].setFixedHeight(30)
        self.buttons["save"].setFixedHeight(30)
        self.buttons["continue"].setFixedHeight(30)

    def configure_signals(self):
        """
        Configure signals for the buttons in the tab.
        """
        self.buttons["close"].clicked.connect(self.dialog.on_close)
        self.buttons["save"].clicked.connect(self.on_save)
        self.buttons["continue"].clicked.connect(self.on_continue)

    def populate(self, errors, warnings, infos):
        """
        Populate the ValidationTab with validation results.

        Args:
            errors (list): A list of error messages.
            warnings (list): A list of warning messages.
            infos (list): A list of informational messages.
        """
        
        obj = {
            "error": errors,
            "warning": warnings,
            "info": infos
        }
        has_issues = False
        for severity in ["error", "warning", "info"]:
            for entry in obj[severity]:
                has_issues = True
                widget = NoticeGrp(entry, severity)
                self.layout.addWidget(widget)

        if not has_issues:
            widget = NoticeGrp("No issues found", "success")
            self.layout.addWidget(widget)

        self.layout.addStretch()

        if errors:
            self.buttons["continue"].setEnabled(False)
        else:
            self.buttons["continue"].setEnabled(True)

    def on_save(self):
        """
        Handle the "Save Scene and Continue Submission" button click event.

        Trigger the submission process and show the progress tab.
        """
        print("Save Scene and Continue Submission...")
        try:
            if bpy.data.is_dirty:
                if bpy.data.filepath:
                    # If the file has been saved before, just save it
                    bpy.ops.wm.save_mainfile()
                else:
                    # Define the save path using pathlib for easy path handling
                    save_path = Path("~/blender_files/blender_file.blend").expanduser()

                    # Ensure the directory exists
                    save_path.parent.mkdir(parents=True, exist_ok=True)

                    # Save the file
                    bpy.ops.wm.save_as_mainfile(filepath=str(save_path))
        except Exception as e:
            print(f"Failed to save the scene: {e}")

        self.on_continue()

    def on_continue(self):
        """
        Handle the "Continue Submission" button click event.

        Trigger the submission process and show the progress tab.
        """
        print("Continue Submission...")
        response_list = []
        if self.payload:
            scene = bpy.context.scene
            use_upload_daemon = scene.use_upload_daemon

            if not use_upload_daemon:
                # Show the progress tab
                self.dialog.show_progress_tab()

                print("Submitting jobs...")
                # print ("payload: ", self.payload)
                self.dialog.progress_tab.submit(self.payload)
            else:
                response = submit.submit_job(self.payload)

                # Enable response tab and disable validation and progress tabs
                self.dialog.show_response_tab()

                print("Showing the response ...")
                if response and response not in response_list:
                    response_list.append(response)
                print("response list: ", response_list)
                self.dialog.response_tab.hydrate(response_list)



        
 