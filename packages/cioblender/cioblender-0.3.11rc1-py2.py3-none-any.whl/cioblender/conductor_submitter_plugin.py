
import bpy
import traceback
import time
from bpy.utils import register_class, unregister_class
from bpy.types import Operator, Panel, PropertyGroup
from bpy.props import StringProperty, CollectionProperty
import json
import sys
import subprocess
import webbrowser


import os

from ciocore import conductor_submit
import ciocore.config
import ciocore.api_client

import cioblender.const as k

ciocore.api_client.ApiClient.register_client(client_name="cioblender", client_version=k.VERSION)

job_msg = "Job submitted."

from cioblender import (
    payload,
    project,
    instances,
    controller,
    software,
    submit,
    frames,
    task,
    json_viewer
)

bl_info = {
    "name": "Conductor Render Submitter",
    "author": "Your Name",
    "version": (0, 1, 7, 21),
    "blender": (3, 6, 1),
    "location": "Render > Properties",
    "description": "Conductor Render submitter UI for Blender",
    "category": "Render",
}

bpy.types.Object.my_int_property = bpy.props.IntProperty(
    name="My Int Property",
    description="This is a custom integer property for the object",
    default=70,    # Default initial value
    min=0,        # Minimum value for the slider
    max=100,       # Maximum value for the slider
)

class ObjPanel(Panel):
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "render"
    bl_category = "Conductor Render Submitter"

    def draw(self, context):
        layout = self.layout
        scene = context.scene

class RenderSubmitterPanel(ObjPanel):
    bl_label = "Conductor Render Submitter"
    bl_idname = "RENDER_PT_RenderSubmitterPanel"

class ConductorJobPanel(ObjPanel):
    bl_label = "Conductor Job"
    bl_idname = "RENDER_PT_ConductorJobPanel"
    bl_parent_id = "RENDER_PT_RenderSubmitterPanel"

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        # Connect button
        layout.operator("render_submitter.connect", text="Connect")
        # Export Script button
        layout.operator("render_submitter.export_script", text="Preview Script")
        # Submit button
        layout.operator("render_submitter.submit", text="Submit")


class ConfigurationPanel(ObjPanel):
    bl_label = "Configuration"
    bl_idname = "RENDER_PT_ConfigurationPanel"
    bl_parent_id = "RENDER_PT_RenderSubmitterPanel"

class GeneralPanel(ObjPanel):
    bl_label = "General"
    bl_idname = "RENDER_PT_GeneralPanel"
    bl_parent_id = "RENDER_PT_ConfigurationPanel"

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        layout.label(text="Job Title:")
        layout.prop(scene, "job_title", text="")

        layout.label(text="Project:")
        layout.prop(scene, "project", text="")

        layout.label(text="Instance Type:")
        layout.prop(scene, "instance_type", text="")

        layout.label(text="Machine Type:")
        layout.prop(scene, "machine_type", text="")

        layout.prop(scene, "preemptible", text="Preemptible")

        layout.label(text="Preemptible Retries:")
        layout.prop(scene, "preemptible_retries", text="")

        layout.label(text="Blender Version:")
        layout.prop(scene, "blender_version", text="")

        layout.label(text="Render Software:")
        #layout.prop(scene, "render_software", text="")
        # Row layout for render software and version
        row = layout.row()
        row.prop(scene, "render_software", text="")
        row.prop(scene, "render_version", text="")

        # Todo: Add a button to add a plugin
        # layout.operator("render_submitter.add_plugin", text="Add Plugin")

class RenderSettingsPanel(ObjPanel):
    bl_label = "Render Settings"
    bl_idname = "RENDER_PT_RenderSettingsPanel"
    bl_parent_id = "RENDER_PT_ConfigurationPanel"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        render = scene.render

        # Resolution settings

        row = layout.row(align=True)
        row.prop(scene, "resolution_x_override", text="Resolution X")

        row = layout.row(align=True)
        row.prop(scene, "resolution_y_override", text="Resolution Y")

        row = layout.row(align=True)
        row.prop(scene, "resolution_percentage_override", text="Resolution %")

        # Camera selection menu
        layout.label(text="Camera:")
        layout.prop(scene, "camera_override", text="")

        #layout.label(text="Samples:")
        #layout.prop(scene, "samples_override", text="")

        row = layout.row(align=True)
        row.prop(scene, "samples_override", text="Samples")

class FramesPanel(ObjPanel):
    bl_label = "Frames"
    bl_idname = "RENDER_PT_Conductor_Frames_Panel"
    bl_parent_id = "RENDER_PT_ConfigurationPanel"

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        row = layout.row(align=True)
        row.prop(scene, "chunk_size", text="Chunk Size")

        layout.prop(scene, "use_custom_range", text="Use Custom Range")

        if scene.use_custom_range:
            row = layout.row(align=True)
            row.prop(scene, "frame_range", text="Custom Range")

        # Display the option to use scout frames
        layout.prop(scene, "use_scout_frames", text="Use Scout Frames")

        row = layout.row(align=True)
        row.prop(scene, "scout_frames", text="Scout Frames")

class FrameInfoPanel(ObjPanel):
    bl_label = "Frame Info"
    bl_idname = "RENDER_PT_FrameInfoPanel"
    bl_parent_id = "RENDER_PT_ConfigurationPanel"
    bl_options = {'DEFAULT_CLOSED'}  # Set the panel to be closed by default

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        row = layout.row(align=True)
        row.active = False
        row.prop(scene, "frame_spec", text="Frame Spec")

        row = layout.row(align=True)
        row.active = False
        row.prop(scene, "scout_spec", text="Scout Spec")

        row = layout.row(align=True)
        row.active = False
        row.prop(scene, "frame_count", text="Frame Count")

        row = layout.row(align=True)
        row.active = False
        row.prop(scene, "task_count", text="Task Count")

        row = layout.row(align=True)
        row.active = False
        row.prop(scene, "scout_frame_count", text="Scout Frame Count")

        row = layout.row(align=True)
        row.active = False
        row.prop(scene, "scout_task_count", text="Scout Task Count")

        row = layout.row(align=True)
        row.active = False
        row.prop(scene, "resolved_chunk_size", text="Resolved Chunk Size")

class AddonsPanel(ObjPanel):
    bl_label = "Add-ons"
    bl_idname = "RENDER_PT_AddonsPanel"
    bl_parent_id = "RENDER_PT_RenderSubmitterPanel"
    bl_description = "Choose from the list of Blender add-ons compatible with your selected Blender version. Be aware that changing the Blender version will update the available add-ons and their respective versions. Ensure you select the add-on and its version that best suits your needs"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        addon_properties = scene.addon_properties

        for addon in addon_properties:
            row = layout.row()
            row.prop(addon, "enabled", text=addon.name)
            # show the version as a menu
            row.prop(addon, "menu_option", text="")


class AdvancedPanel(ObjPanel):
    bl_label = "Advanced"
    bl_idname = "RENDER_PT_Conductor_Advanced_Panel"
    bl_parent_id = "RENDER_PT_RenderSubmitterPanel"
    def draw(self, context):
        layout = self.layout
        scene = context.scene

        layout.row().label(text="") # blank line
        layout.prop(scene, "output_folder", text="Output Folder")
# -------------------------------------------------------------------
# Define a custom panel class
class ExtraFileAssetProperty(PropertyGroup):
    file_path: StringProperty(
        name="File Path",
        description="Path to extra asset file",
        subtype='FILE_PATH',
    )

class ExtraFileAssetsPanel(Panel):
    bl_label = "Extra File Assets"
    bl_idname = "RENDER_PT_ExtraFileAssetsPanel"
    bl_parent_id = "RENDER_PT_Conductor_Advanced_Panel"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_description = "Add extra file assets"

    def draw(self, context):
        layout = self.layout

        # Add a button to open the file browser
        layout.operator("object.open_file_browser")

        # Access the extra_file_assets_list from the scene
        scene = context.scene
        extra_file_assets_list = scene.extra_file_assets_list

        for i, extra_asset in enumerate(extra_file_assets_list):
            row = layout.row(align=True)
            row.prop(extra_asset, "file_path", text="File Path", slider=True)
            remove_op = row.operator("custom.remove_extra_file_asset", text="", icon='X')
            remove_op.index = i

class RemoveExtraFileAssetOperator(Operator):
    bl_idname = "custom.remove_extra_file_asset"
    bl_label = "Remove Extra File Asset"
    index: bpy.props.IntProperty()

    def execute(self, context):
        scene = context.scene
        extra_file_assets_list = scene.extra_file_assets_list
        extra_file_assets_list.remove(self.index)
        return {'FINISHED'}

class OpenFileBrowserOperator(Operator):
    bl_idname = "object.open_file_browser"
    bl_label = "Add Extra File Assets"
    bl_description = "Search and upload files missed by the automatic asset scan. For an overview of detected assets, check the 'upload_paths' listed in the preview panel, ready for upload. Utilize this functionality to incorporate special elements such as custom scripts, textures, or crucial files into your render job. It's important to note that this feature should not be used for assets already integrated within the Blender scene; for those, please rely on the 'Linked Assets' functionality"

    filepath: bpy.props.StringProperty(subtype='FILE_PATH')

    def invoke(self, context, event):
        wm = context.window_manager
        wm.fileselect_add(self)
        return {'RUNNING_MODAL'}

    def draw(self, context):
        layout = self.layout
        layout.label(text="Select a file:")

    def execute(self, context):
        # Check if the selected file path is not empty
        if self.filepath:
            # Add the selected file as an instance of ExtraFileAssetProperty
            scene = context.scene
            if not hasattr(scene, "extra_file_assets_list"):
                scene.extra_file_assets_list = []

            extra_asset = scene.extra_file_assets_list.add()
            extra_asset.file_path = self.filepath

            # Refresh the UI
            refresh_ui()

        return {'FINISHED'}
# -------------------------------------------------------------------
# Define a custom panel class
class ExtraDirAssetProperty(PropertyGroup):
    file_path: StringProperty(
        name="Dir Path",
        description="Path to extra asset dir",
        subtype='DIR_PATH',
    )

class ExtraDirAssetsPanel(Panel):
    bl_label = "Extra Directory Assets"
    bl_idname = "RENDER_PT_ExtraDirAssetsPanel"
    bl_parent_id = "RENDER_PT_Conductor_Advanced_Panel"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_description = "Add extra dir assets"

    def draw(self, context):
        layout = self.layout

        # Add a button to open the file browser
        layout.operator("object.open_dir_browser")

        # Access the extra_file_assets_list from the scene
        scene = context.scene
        extra_dir_assets_list = scene.extra_dir_assets_list

        for i, extra_asset in enumerate(extra_dir_assets_list):
            row = layout.row(align=True)
            row.prop(extra_asset, "file_path", text="Dir Path", slider=True)
            remove_op = row.operator("custom.remove_extra_dir_asset", text="", icon='X')
            remove_op.index = i

class RemoveExtraDirAssetOperator(Operator):
    bl_idname = "custom.remove_extra_dir_asset"
    bl_label = "Remove Extra Dir Asset"
    index: bpy.props.IntProperty()

    def execute(self, context):
        scene = context.scene
        extra_dir_assets_list = scene.extra_dir_assets_list
        extra_dir_assets_list.remove(self.index)
        return {'FINISHED'}

class OpenDirBrowserOperator(Operator):
    bl_idname = "object.open_dir_browser"
    bl_label = "Add Extra Directory Assets"
    bl_description = "Search and upload entire folders missed by the automatic asset scan. For an overview of detected assets, check the 'upload_paths' listed in the preview panel, ready for upload. Utilize this functionality to incorporate special elements such as custom scripts, textures, or crucial files into your render job. It's important to note that this feature should not be used for assets already integrated within the Blender scene; for those, please rely on the 'Linked Assets' functionality"

    filepath: bpy.props.StringProperty(subtype='DIR_PATH')

    def invoke(self, context, event):
        wm = context.window_manager
        self.filepath = ""
        wm.fileselect_add(self)
        return {'RUNNING_MODAL'}

    def draw(self, context):
        layout = self.layout
        layout.label(text="Select a directory:")

    def execute(self, context):
        # Check if the selected file path is not empty
        if self.filepath:
            # Add the selected file as an instance of ExtraFileAssetProperty
            scene = context.scene
            if not hasattr(scene, "extra_dir_assets_list"):
                scene.extra_dir_assets_list = []


            extra_asset = scene.extra_dir_assets_list.add()
            extra_asset.file_path = self.filepath

            # Refresh the UI
            refresh_ui()

        return {'FINISHED'}
# -------------------------------------------------------------------
class PreviewPanel(ObjPanel):
    bl_label = "Preview"
    bl_idname = "RENDER_PT_PreviewPanel"
    bl_parent_id = "RENDER_PT_RenderSubmitterPanel"
    bl_description = "Generate and inspect a JSON script tailored for offline job submission by clicking this button. The script dynamically updates in response to changes made within the submitter panels. Revisit this section at any time to verify that your submission data is accurately captured."

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        # Add the integer slider
        # layout.prop(scene, "display_tasks", slider=True)

        # Get all item values as JSON format
        values = create_json_data(True)

        # Convert values to JSON format
        json_data = json.dumps(values, indent=4)

        # Display the JSON format line by line in the preview panel
        lines = json_data.split("\n")
        for line in lines:
            layout.label(text=line)



class AddonProperty(bpy.types.PropertyGroup):
    enabled: bpy.props.BoolProperty(name="Enabled", default=False)
    name: bpy.props.StringProperty(name="Name")
    version_items: bpy.props.StringProperty()  # Store versions as a string

    def get_version_items(self, context):
        # Decode the versions from the stored string
        versions = self.version_items.split(',') if self.version_items else []
        return [(v, v, "") for v in versions]

    # Dynamic callback for EnumProperty items
    def version_items_callback(self, context):
        return self.get_version_items(context)

    # EnumProperty for versions
    menu_option: bpy.props.EnumProperty(
        name="Version",
        description="Choose a version",
        items=version_items_callback
    )
def save_plugin_settings(context):
    """
    Save the current settings of the plugin from the given scene.

    This function iterates through predefined properties in the scene and saves their current values.
    If a property does not have a value, `None` is saved for that property.

    Args:
    scene (bpy.types.Scene): The Blender scene from which to save the settings.

    Returns:
    dict: A dictionary containing the saved values of the properties.
    """
    scene = context.scene
    saved_settings = {}
    try:
        properties_to_save = [
                              ]

        for prop in properties_to_save:
            saved_settings[prop] = getattr(scene, prop, None)

        print("Saved settings: {}".format(saved_settings))
    except Exception as e:
        print("Unable to save settings: {}".format(e))

    return saved_settings

def save_env_settings(context):
    """
    Save the current settings of the extra env variables

    This function iterates through predefined properties in the scene and saves their current values.
    If a property does not have a value, `None` is saved for that property.

    Args:
    context: The Blender context

    Returns:
    dict: A dictionary containing the saved values of the properties.
    """
    scene = context.scene
    saved_env = {}
    try:
        for var in scene.custom_variables.variables:
            saved_env[var.variable_name] = var.variable_value
        print("Saved settings: {}".format(saved_env))
    except Exception as e:
        print("Unable to save settings: {}".format(e))

    return saved_env

def apply_saved_plugin_settings(context, saved_settings):
    """
    Apply the previously saved settings to the given scene.

    This function iterates through the saved settings and applies them back to the scene properties.
    Only properties with non-None values are set.

    Args:
    scene (bpy.types.Scene): The Blender scene to which the settings will be applied.
    saved_settings (dict): A dictionary containing the saved settings.
    """
    scene = context.scene
    try:
        for prop, value in saved_settings.items():
            if prop not in ["extra_variables"]:
                print("Applying {} to {}".format(value, prop))
                if value is not None:
                    setattr(scene, prop, value)


    except Exception as e:
        print("Unable to apply settings: {}".format(e))



# Connect Operator
class ConnectOperator(Operator):
    bl_idname = "render_submitter.connect"
    bl_label = "Connect"
    bl_description = "Click to force a connection with Conductor's backend. This will fetch the list of projects,software packages, and instance types, and then refresh the UI. "  # Tooltip text

    def execute(self, context):
        """
        Execute the connection operation for the plugin.

        This method first saves the current plugin settings, performs the connection operations,
        and then restores the saved settings to the scene.

        Args:
        context (bpy.types.Context): The current Blender context.

        Returns:
        set: A set containing the finishing status.
        """
        scene = context.scene
        # saved_settings = save_plugin_settings(context)
        saved_env = save_env_settings(context)

        print("Connecting to Conductor...")
        controller.connect()

        # Update other property menus here if needed
        populate_project_menu(context)

        populate_blender_version_menu(context)

        populate_machine_type_menu(context)
        populate_addons(context)
        populate_render_version_menu(context)
        populate_output_folder(context)
        populate_camera_override_menu(context)
        # populate_render_software_menu(context)

        set_resolution(context)

        # Get blender filename
        filename = bpy.path.basename(bpy.context.blend_data.filepath)
        # print("Filename: ", filename)
        filename = filename.split(".")[0]
        # Get blender version
        blender_version = bpy.app.version_string.split(" ")[0]
        print("Blender Version: ", blender_version)

        # Set the job title
        software_version = bpy.app.version
        software_version = f"{software_version[0]}.{software_version[1]}.{software_version[2]}"
        job_title = "Blender {} Linux Render {}".format(software_version, filename)

        # Set bpy.types.Scene.job_title to job_title
        context.scene.job_title = job_title  # Update the job_title property

        set_frames(context)
        populate_frame_info_panel()

        populate_extra_env(context, saved_env)

        # Apply the saved settings for other properties
        # apply_saved_plugin_settings(context, saved_settings)

        # Refresh the UI
        refresh_ui()
        refresh_properties()

        return {'FINISHED'}

def set_frames(context):
    try:
        scene = context.scene
        current_chunk_size = scene.chunk_size
        current_use_custom_range = scene.use_custom_range
        current_frame_range = scene.frame_range
        current_use_scout_frames = scene.use_scout_frames
        current_scout_frames = scene.scout_frames

        if not current_use_custom_range:
            scene.frame_range = get_scene_frame_range()
        else:
            if not current_frame_range or current_frame_range == "":
                scene.frame_range = get_scene_frame_range()

    except Exception as e:
        print("Error while setting frames: ", e)

# Submit Operator
class ExportScriptOperator(Operator):
    """
    Blender Operator to export rendering script data as a JSON file.

    This operator is responsible for gathering data intended for rendering,
    storing it in a JSON format within the Blender project directory, and
    then attempting to open the exported file with the system's default
    application for previewing JSON content. The JSON file is named after
    the Blender project file and saved in the same directory.

    Attributes:
        bl_idname (str): Blender identifier name for the operator.
        bl_label (str): Label for the operator in the UI.
        bl_description (str): Description of the operator's purpose and functionality.

    Methods:
        execute(context): Executes the operator's logic, exporting the JSON data to a file
                          and then attempting to open that file for preview. If the system's
                          default application fails to open the file, it tries to open the file
                          within Blender using a custom JSON viewer if available. In case of any
                          failures, appropriate error messages are logged and shown to the user.
    """
    bl_idname = "render_submitter.export_script"
    bl_label = "Export Script"
    bl_description = "Store the script intended for rendering within the Blender directory as a JSON file, and subsequently open it for a preview."

    def execute(self, context):
        """
        Execute the operation of exporting the script as JSON and opening it.

        This method gathers rendering script data, saves it as a JSON file in the
        same directory as the Blender project file, and attempts to open the exported
        file with the system's default application. If unable to open with the system's
        default application, it falls back to a custom JSON viewer within Blender.

        Args:
            context: The context in which the operator is executed. Provides access to
                     Blender's data and operations.

        Returns:
            A set containing 'FINISHED' to indicate successful completion of the operation.
        """
        # print("Export Script clicked")

        # Get all item values as JSON data
        payload = create_json_data(False)
        json_data = json.dumps(payload, indent=4)
        filepath = ""

        try:
            # Save JSON data to a file
            filename = bpy.path.basename(bpy.context.blend_data.filepath)
            filename = filename.split(".")[0]
            filepath = os.path.join(bpy.path.abspath("//"), f"{filename}.json")
            with open(filepath, "w") as file:
                print("Writing JSON file: ", filepath)
                file.write(json_data)
        except Exception as e:
            print(f"Failed to save JSON file: {filepath} {e}")
        else:
            try:
                # Open the JSON file with the system default application
                print(f"Opening file: {filepath}...")
                platform = sys.platform
                if platform.lower().startswith("win"):
                    os.startfile(filepath)
                    # json_viewer.invoke_json_viewer(payload)
                    # webbrowser.open(filepath)

                elif platform == "darwin":
                    subprocess.call(["open", filepath])
                elif platform == "linux":
                    subprocess.call(["xdg-open", filepath])

            except Exception as e:
                try:
                    # Show the Submission dialog
                    json_viewer.invoke_json_viewer(payload)

                except Exception as e:
                    print(f"Failed to open file: {filepath} {e}")
                    self.report({'ERROR'}, f"Could not open JSON file {filepath}. Please open it manually.")


        return {'FINISHED'}

# Submit Operator
class SubmitOperator(Operator):
    bl_idname = "render_submitter.submit"
    bl_label = "Submit"
    bl_description = "Submit the job to Conductor for processing."  # Tooltip text

    def execute(self, context):
        print("Submit clicked ...")

        kwargs = create_raw_data()

        blender_payload = payload.resolve_payload(**kwargs)

        # Show the Submission dialog
        submit.invoke_submission_dialog(kwargs, blender_payload)

        # Open the Submission Window instead of invoking the submission dialog
        #bpy.ops.screen.userpref_show('INVOKE_DEFAULT')
        #context.area.ui_type = 'RENDER'
        #bpy.context.scene.submission_tab = 'VALIDATION'  # Set default tab

        # Redirect to the Properties editor and your custom panel
        # Find an area to switch to the Properties editor
        # This is where you can add code to open the widget or perform other actions
        #bpy.ops.wm.call_panel(name=SubmissionWindowPanel.bl_idname)
        return {'FINISHED'}

# Define the panel for the custom widget
class SubmissionWindowPanel(bpy.types.Panel):
    bl_label = "Submission Window"
    bl_idname = "RENDER_PT_SubmissionWindow"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "render"
    bl_category = "Conductor Render Submitter"

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        # Tabs
        row = layout.row()
        row.prop(scene, "submission_tab", expand=True)

        if scene.submission_tab == 'VALIDATION':
            self.draw_validation_tab(layout)
        elif scene.submission_tab == 'PROGRESS':
            self.draw_progress_tab(layout)
        elif scene.submission_tab == 'RESPONSE':
            self.draw_response_tab(layout)

    def draw_validation_tab(self, layout):
        layout.label(text="Validation Tab Content")
        # Add more UI elements for Validation tab here

    def draw_progress_tab(self, layout):
        layout.label(text="Progress Tab Content")
        # Add more UI elements for Progress tab here

    def draw_response_tab(self, layout):
        layout.label(text="Response Tab Content")
        # Add more UI elements for Response tab here



# Define the class for the SimpleOperator
class SimpleOperator(bpy.types.Operator):
    bl_idname = "custom.simple_operator"
    bl_label = "Custom Notification Operator"

    success = bpy.props.BoolProperty(default=False)
    job_number = bpy.props.StringProperty(default="")

    def execute(self, context):
        if self.success:
            self.report({'INFO'}, f"Job {self.job_number} was successful.")
        else:
            self.report({'ERROR'}, f"Job {self.job_number} failed.")
        return {'FINISHED'}

class ExtraEnvironmentPanel(bpy.types.Panel):

    bl_label = "Extra Environment Panel"
    bl_idname = "RENDER_PT_ExtraEnvironment"
    bl_parent_id = "RENDER_PT_Conductor_Advanced_Panel"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'

    def draw(self, context):
        layout = self.layout

        # Add a button to add a new variable row
        layout.operator("custom.add_variable")

        # Draw existing variables
        scene = context.scene
        variables = scene.custom_variables.variables
        for i, variable in enumerate(variables):
            row = layout.row()
            row.prop(variable, "variable_name", text="Variable")
            row.prop(variable, "variable_value", text="Value")
            row.operator("custom.remove_variable", text="", icon='X').index = i

class AdditionalRenderingOptionsPanel(bpy.types.Panel):
    bl_label = "Additional Rendering Options"
    bl_idname = "RENDER_PT_AdditionalRenderingOptions"
    bl_parent_id = "RENDER_PT_Conductor_Advanced_Panel"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_description = "A list of additional rendering options is available for advanced control over the rendering process"

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        # layout.prop(scene, "factory_startup")
        layout.prop(scene, "disable_audio")
        layout.prop(scene, "update_camera_checkbox")
        layout.prop(scene, "view_layers_checkbox")


class UploadDaemonPanel(bpy.types.Panel):
    bl_label = "Upload Daemon"
    bl_idname = "RENDER_PT_UploadDaemon"
    bl_parent_id = "RENDER_PT_Conductor_Advanced_Panel"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_description = "Configure settings for using the Upload Daemon"

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        # Checkbox for "Use Upload Daemon"
        layout.prop(scene, "use_upload_daemon", text="Use Upload Daemon")

        # String entry for "Location Tag"
        layout.prop(scene, "location_tag", text="Location Tag")

# Define an operator to add a new variable row
class AddVariableOperator(bpy.types.Operator):
    bl_idname = "custom.add_variable"
    bl_label = "Add Extra Environment Variables"
    bl_description = "Define environment variables and their values for your job submission. This is especially useful if you're using custom shell scripts that require modifications to the PATH variable for detection. Should you need to include such scripts, ensure they are selected in the extra assets section. When submitting from Windows, remember to omit the drive letter from the script's path when setting up the environment variable. Environment variables can be set to be either exclusive or to append to existing values."

    def execute(self, context):
        scene = context.scene
        variables = scene.custom_variables.variables
        variables_dict = scene.variables_dict
        new_variable = variables.add()
        new_variable.variable_name = ""
        new_variable.variable_value = ""
        variables_dict[new_variable.variable_name] = new_variable.variable_value
        return {'FINISHED'}


# Define an operator to remove a variable row
class RemoveVariableOperator(bpy.types.Operator):
    bl_idname = "custom.remove_variable"
    bl_label = "Remove Variable"
    index: bpy.props.IntProperty()

    def execute(self, context):
        scene = context.scene
        variables = scene.custom_variables.variables
        variables_dict = scene.variables_dict
        variable = variables[self.index]
        key = variable.variable_name
        if key in variables_dict:
            del variables_dict[key]
        variables.remove(self.index)
        return {'FINISHED'}

# Define a custom property for storing variable data
class CustomVariableProperty(bpy.types.PropertyGroup):
    variable_name: bpy.props.StringProperty(name="Variable Name")
    variable_value: bpy.props.StringProperty(name="Variable Value")

# Define a custom property to store the list of variables
class CustomVariableListProperty(bpy.types.PropertyGroup):
    variables: bpy.props.CollectionProperty(type=CustomVariableProperty)

def populate_extra_env(context, saved_env):
    # Todo: review these hard coded env variables
    # Populate extra env variables
    env_dict = {
        "CONDUCTOR_PATHHELPER": "0",
        "HDF5_USE_FILE_LOCKING": "FALSE",
        "__conductor_letter_drives__": "1",
        "CONDUCTOR_MD5_CACHING": "TRUE",
    }
    scene = context.scene
    variables = scene.custom_variables.variables

    # Clear existing variables
    variables.clear()
    scene.variables_dict.clear()  # Clearing the variables_dict as well
    variables_dict = scene.variables_dict

    for key, value in env_dict.items():
        if key not in saved_env:
            new_variable = variables.add()
            new_variable.variable_name = key
            new_variable.variable_value = value
            variables_dict[key] = value

    for key, value in saved_env.items():
        new_variable = variables.add()
        new_variable.variable_name = key
        new_variable.variable_value = value
        variables_dict[key] = value


def refresh_ui():
    """Refresh the UI"""
    bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)

def refresh_properties():
    """Refresh the UI"""
    for area in bpy.context.screen.areas:
        if area.type == 'PROPERTIES':
            area.tag_redraw()

def submit_job(payload):
    """Submit a job to Conductor."""
    try:
        remote_job = conductor_submit.Submit(payload)
        response, response_code = remote_job.main()

    except:
        response = traceback.format_exc()
        response_code = 500

    print("response is: ", response)

    return {"response": response, "response_code": response_code}

def get_job_message(self, context):
    if job_msg:
        self.layout.label(text=job_msg)

# Update the Machine Type Menu based on the value of the Instance Type Menu
def update_instance_type_menu(self, context):

    # Update the Machine Type Menu based on the value of the Instance Type Menu
    instance_list = instances.populate_menu(context.scene.instance_type)
    # print("instance_list: ", instance_list)
    # Update the items of the Machine Type Menu
    bpy.types.Scene.machine_type = bpy.props.EnumProperty(
        name="Machine Type",
        description="Choose a machine type on which to run this job.",
        items=instance_list,
    )
    # select_first_machine_type(context)

def render_software_update(self, context):
    # Reset render_version when changing render software
    # context.scene.render_version = 'NONE'  # Set to 'NONE' or your defined default value
    populate_render_version_menu(context)

def get_render_resolution(scene):
    """Update the resolution percentage"""

    resolution_percentage_override = scene.resolution_percentage_override
    # get resolution_x_override amd resolution_y_override
    resolution_x_override = scene.resolution_x_override
    resolution_y_override = scene.resolution_y_override
    # Calculate the new resolution_x_override and resolution_y_override
    # print("resolution_x_override: ", resolution_x_override)
    # print("resolution_y_override: ", resolution_y_override)
    # print("resolution_percentage_override: ", resolution_percentage_override)
    if resolution_percentage_override == 100:
        return resolution_x_override, resolution_y_override

    else:
        new_resolution_x = int(resolution_x_override * resolution_percentage_override / 100)
        new_resolution_y = int(resolution_y_override * resolution_percentage_override / 100)
        # print("new_resolution_x: ", new_resolution_x)
        # print("new_resolution_y: ", new_resolution_y)
        return new_resolution_x, new_resolution_y


def populate_blender_version_menu(context):
    """Populate the Blender Version Menu """
    prev_blender_version = context.scene.blender_version
    # print("original blender version ", context.scene.blender_version)

    blender_versions = software.populate_host_menu()
    # Reverse the list
    blender_versions.reverse()

    bpy.types.Scene.blender_version = bpy.props.EnumProperty(
        name="Blender Version",
        description="Choose the specific Blender version for job submission. This version may vary from the one installed locally. Be aware of any feature variations between versions that might affect your render. Note that changing this setting will modify the lists of accessible renders and add-ons accordingly.",
        items=blender_versions,
        update=blender_version_update_callback  # Assign the callback function here

    )
    # print("Current blender version ", context.scene.blender_version)
    try:
        if not prev_blender_version:
            blender_name = software.get_blender_name()
            print("Blender name: ", blender_name)
            context.scene.blender_version = blender_name
        # print("Final blender version ", context.scene.blender_version)
    except:
        pass



def populate_camera_override_menu(context):
    """Populate the Camera Selection Menu"""
    scene = context.scene

    # Create a list of tuples for each camera in the scene
    camera_list = [(cam.name, cam.name, "") for cam in scene.objects if cam.type == 'CAMERA']

    # Define the update function for the EnumProperty
    def update_camera_checkbox(self, context):
        scene = context.scene
        scene.camera = scene.objects.get(self.camera_override)

    # Create an EnumProperty for camera selection
    bpy.types.Scene.camera_override = bpy.props.EnumProperty(
        name="Camera Selection",
        description="Set a specific camera for job submission, distinct from the active camera in your Blender scene. Modifying this selection will not alter the active camera within your Blender scene. Ensure you choose the desired camera for your final rendered image",
        items=camera_list,
        update=update_camera_checkbox
    )

    # Set the default value for the camera_override property
    if scene.camera:
        scene.camera_override = scene.camera.name


def blender_version_update_callback(self, context):
    populate_addons(context)


def set_resolution(context):
    """Set resolution and samples override properties based on the current scene."""
    scene = context.scene
    render = scene.render
    try:

        if scene.resolution_x_override <= 0:
            scene.resolution_x_override = render.resolution_x
        if scene.resolution_y_override <= 0:
            scene.resolution_y_override = render.resolution_y
        if scene.resolution_percentage_override <= 0:
            scene.resolution_percentage_override = render.resolution_percentage
        if scene.samples_override <= 0:
            scene.samples_override = scene.cycles.samples if scene.render.engine == 'CYCLES' else 0

    except Exception as e:
        print("Error setting resolution: ", e)


def populate_machine_type_menu(context):
    instance_type = context.scene.instance_type
    if not instance_type:
        instance_type = "GPU"
    instance_list = instances.populate_menu(instance_type)
    # print("instance_list: ", instance_list)
    bpy.types.Scene.machine_type = bpy.props.EnumProperty(
        name="Machine Type",
        description="Select the optimal machine setup for your job by evaluating critical elements. For GPU-based machines, consider the number of cores, memory size, type of graphics card, and its memory capacity. In contrast, for CPU-focused machines, assess the number of cores and the available memory.",
        items=instance_list,
    )
    # Set the value Machine Type to be the first index in the Menu
    # select_first_machine_type(context)

def select_first_machine_type(context):
    # Check if the EnumProperty 'machine_type' exists on bpy.types.Scene
    try:
        if hasattr(bpy.types.Scene, 'machine_type'):
            # Attempt to set the value of 'machine_type' to the first item

                scene = context.scene
                first_item = scene.bl_rna.properties['machine_type'].enum_items[0].identifier
                scene.machine_type = first_item
    except Exception as e:
        print("Unable to find default value for machine_type: ", e)

def populate_project_menu(context):
    """Populate the Project Menu"""
    project_items = project.populate_menu(bpy.types.Scene)
    # Reverse the list
    project_items.reverse()
    # print("project_items: ", project_items)
    bpy.types.Scene.project = bpy.props.EnumProperty(
        name="project",
        description="Conductor project in which to run the job.",
        items=project_items
    )


def populate_addon_properties(addon_names, addon_properties):
    """Populate addon_properties with the given addon names and versions, excluding 'Redshift'."""
    addon_properties.clear()
    for addon_name, versions in addon_names.items():
        if addon_name not in ["Redshift"]:
            addon_prop = addon_properties.add()
            addon_prop.name = addon_name
            addon_prop.enabled = False  # Default state
            addon_prop.version_items = ','.join(versions)


def set_enabled_addons(enabled_addon_versions, addon_properties, context):
    """Set enabled state and version for addons in addon_properties based on enabled_addon_versions."""
    for addon_prop in addon_properties:
        addon_name = addon_prop.name.replace(' ', '_').lower()
        if addon_name in enabled_addon_versions:
            addon_prop.enabled = True
            current_version = enabled_addon_versions.get(addon_name)
            if current_version:
                current_version_tuple = (current_version, current_version, '')
                if current_version_tuple in addon_prop.get_version_items(context):
                    addon_prop.menu_option = current_version


def update_render_software_menu(addon_packages):
    """Update render software menu based on available addon packages."""
    items_list = [("Cycles", "Cycles", ""), ("Eevee", "Eevee", "")]
    if "redshift-blender" in addon_packages:
        items_list.append(("Redshift", "Redshift", ""))
    bpy.types.Scene.render_software = bpy.props.EnumProperty(
        name="Render Software",
        description="Select the rendering software. If you choose Eevee, you must select a GPU instance type.",
        items=items_list,
        update=render_software_update
    )

def save_current_addon_settings(context):
    scene = context.scene
    saved_addon_settings = {}
    for addon in scene.addon_properties:
        saved_addon_settings[addon.name] = {
            "enabled": addon.enabled,
            "version": addon.menu_option
        }
    return saved_addon_settings

def apply_saved_addon_settings(context, saved_addon_settings):
    try:
        scene = context.scene
        for addon_name, settings in saved_addon_settings.items():
            for addon in scene.addon_properties:
                if addon.name == addon_name:
                    addon.enabled = settings["enabled"]
                    if settings["version"] in addon.version_items.split(','):
                        addon.menu_option = settings["version"]
    except Exception as e:
        print("Unable to apply saved addon.", e)


def populate_addons(context):
    """
    Populate the Addons Panel with a list of add-ons.
    It involves populating addon properties, setting enabled addons based on the software,
    and updating the render software menu.
    """
    saved_addon_settings = save_current_addon_settings(context)

    kwargs = create_raw_data()
    addon_names = software.get_add_on_names(**kwargs)
    # addon_names["conductor"] = ["0.3.0", "0.2.0", "0.4.0", "0.5"]
    addon_properties = context.scene.addon_properties

    populate_addon_properties(addon_names, addon_properties)
    enabled_addon_versions = software.get_addon_versions_dict()
    if enabled_addon_versions:
        set_enabled_addons(enabled_addon_versions, addon_properties, context)

    render_software_selection = context.scene.render_software
    addon_packages = software.get_package_dict()
    update_render_software_menu(addon_packages)

    apply_saved_addon_settings(context, saved_addon_settings)


def populate_render_version_menu(context):
    version_items = []
    render_software = context.scene.render_software
    kwargs = create_raw_data()
    addon_names = software.get_add_on_names(**kwargs)
    print("render software: {}".format(render_software))

    if render_software.lower() in ["cycles", "eevee"]:
        print("Resetting render software")
        bpy.types.Scene.render_version = bpy.props.EnumProperty(
            name="Render Version",
            description="Select the version of the rendering software.",
            items=[('NONE', 'None', '')]
        )
    elif render_software.lower() in ["redshift"]:
        if "Redshift" in addon_names.keys():
            version_items = addon_names["Redshift"]
            # version_items.append(('NONE', 'None', ''))
            print("Setting render software to {}".format(render_software))
            bpy.types.Scene.render_version = bpy.props.EnumProperty(
                name="Render Version",
                description="Choose the specific version of your rendering software. Note that for Cycles and Eevee renders, version selection is not applicable as these renderers do not have distinct version options.",
                items=[(v, v, "") for v in version_items]
            )

    # Refresh the UI
    refresh_ui()



def populate_output_folder(context):
    scene = bpy.context.scene
    current_output_folder = scene.output_folder
    if not current_output_folder or current_output_folder == "":
        blender_filepath = bpy.context.blend_data.filepath
        blender_folder = os.path.dirname(blender_filepath)
        output_folder = get_output_folder(blender_folder)
        scene.output_folder = output_folder


# Todo: Add additional renderers
def populate_render_software_menu(context):
    """Populate the Render Software Menu """
    print("Populate the Render Software Menu ...")
    kwargs = create_raw_data()
    render_software = software.populate_driver_menu(**kwargs)
    print("render_software: ", render_software)
    bpy.types.Scene.render_software = bpy.props.EnumProperty(
        name="Render Software",
        items=render_software,
        desscritpion="Choose the appropriate rendering software based on your requirements. For Cycles, it's highly recommended to use a GPU instance type to ensure maximum performance and efficiency. In the case of Eevee or Redshift, selecting a GPU instance type is essential, as these renderers exclusively support GPU processing.",
        update=render_software_update  # Add the update callback
    )

def create_raw_data():
    #
    scene = bpy.context.scene
    software_version = bpy.app.version
    software_version = f"{software_version[0]}.{software_version[1]}.{software_version[2]}"

    start_frame = scene.frame_start
    end_frame = scene.frame_end
    # frame_range = "{}-{}".format(start_frame, end_frame)

    # Get the full path to the Blender file
    blender_filepath = bpy.context.blend_data.filepath
    # Get the Blender filename from the full path
    blender_filename = bpy.path.basename(blender_filepath)
    # Get the folder containing the Blender file
    blender_folder = os.path.dirname(blender_filepath)

    new_resolution_x, new_resolution_y = get_render_resolution(scene)
    scene_frame_range = get_scene_frame_range()

    kwargs = {
        "software_version": software_version,
        "job_title": scene.job_title,
        "project": scene.project,
        "instance_type": scene.instance_type,
        "machine_type": scene.machine_type,
        "preemptible": scene.preemptible,
        "preemptible_retries": scene.preemptible_retries,
        "blender_version": scene.blender_version,
        "render_software": scene.render_software,
        "render_version": scene.render_version,
        "chunk_size": scene.chunk_size,
        "scene_frame_start": scene.frame_start,
        "scene_frame_end": scene.frame_end,
        "use_custom_range": scene.use_custom_range,
        "frame_range": scene.frame_range,
        "scene_frame_range": scene_frame_range,
        "use_scout_frames": scene.use_scout_frames,
        "scout_frames": scene.scout_frames,
        "frame_spec": scene.frame_spec,
        "scout_spec": scene.scout_spec,
        "output_folder": scene.output_folder,
        "resolved_chunk_size": scene.resolved_chunk_size,
        "blender_filename": blender_filename,
        "blender_filepath": blender_filepath,
        "blender_folder": blender_folder,
        "extra_variables": scene.custom_variables.variables,
        "resolution_x_override": scene.resolution_x_override,
        "resolution_y_override": scene.resolution_y_override,
        "resolution_percentage_override": scene.resolution_percentage_override,
        "new_resolution_x": new_resolution_x,
        "new_resolution_y": new_resolution_y,
        "camera_override": scene.camera_override,
        "samples_override": scene.samples_override,
        # "factory_startup": scene.factory_startup,
        "disable_audio": scene.disable_audio,
        "update_camera_checkbox": scene.update_camera_checkbox,
        "view_layers_checkbox": scene.view_layers_checkbox,

        # "display_tasks": scene.display_tasks,

    }
    return kwargs

def get_output_folder(blender_folder):
    """Get the output folder"""
    output_folder = "~/render"
    try:
        if not blender_folder:
            blender_folder = os.path.expanduser("~")
            output_folder = os.path.join(blender_folder, "render")

        else:
            output_folder = os.path.join(blender_folder, "render")

    except Exception as e:
        print("Error creating output folder: ", e)

    # create the output folder if it doesn't exist
    if output_folder and not os.path.exists(output_folder):
        os.makedirs(output_folder)
    return output_folder


def create_json_data(task_display_limit):
    """Create JSON data from the scene properties"""
    kwargs = create_raw_data()
    kwargs["task_display_limit"] = task_display_limit
    # print("kwargs: ", kwargs)
    json_data = payload.resolve_payload(**kwargs)
    return json_data

def get_scene_frame_range():
    """Get the frame range from the scene"""
    scene = bpy.context.scene
    start_frame = scene.frame_start
    end_frame = scene.frame_end
    frame_range = "{}-{}".format(start_frame, end_frame)
    return frame_range

def populate_frame_info_panel():
    """Populate the Frame Info Panel"""
    scene = bpy.context.scene
    frame_range = get_scene_frame_range()
    kwargs = create_raw_data()
    frame_info_dict = frames.set_frame_info_panel(**kwargs)

    scene.frame_spec = scene.frame_range
    scene.scout_spec = str(frame_info_dict.get("scout_frame_spec", 0))
    scene.frame_count = str(frame_info_dict.get("frame_count", 0))
    scene.task_count = str(frame_info_dict.get("task_count", 0))
    scene.scout_frame_count = str(frame_info_dict.get("scout_frame_count", 0))
    scene.scout_task_count = str(frame_info_dict.get("scout_task_count", 0))
    scene.resolved_chunk_size = str(frame_info_dict.get("resolved_chunk_size", scene.chunk_size))


def on_chunk_size_updated(self, context):
    populate_frame_info_panel()

def on_custom_range_updated(self, context):
    populate_frame_info_panel()


class WaitSaveFinishOperator(bpy.types.Operator):
    """Operator which runs in modal mode and waits for the file to be saved."""
    bl_idname = "wm.wait_save_finish"
    bl_label = "Wait for Save to Finish"

    timer = None
    filepath_before = ""

    def modal(self, context, event):
        if event.type == 'TIMER':
            # Check if the file has been saved by comparing the current filepath with the initial one
            if bpy.data.filepath != self.filepath_before and bpy.data.is_saved:
                self.finish(context)
                return {'FINISHED'}

        return {'PASS_THROUGH'}

    def execute(self, context):
        # Store the initial filepath to detect when it changes
        self.filepath_before = bpy.data.filepath

        # Add a timer to check periodically if the file has been saved
        self.timer = context.window_manager.event_timer_add(0.1, window=context.window)
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    def finish(self, context):
        # Remove the timer and perform the continuation action
        context.window_manager.event_timer_remove(self.timer)
        print("File has been saved. Continuing the process...")
        # Here you would call your continuation method, e.g., self.on_continue()
        # For this example, we're just printing to the console.

# List of classes to register
classes = [
    RenderSubmitterPanel, # Grandparent panel
    ConductorJobPanel, # Parent panel
    ConfigurationPanel, # Parent panel
    AddonsPanel, # Parent panel
    AdvancedPanel, # Parent panel
    # PreviewPanel, # Parent panel
    GeneralPanel, # Child panel
    RenderSettingsPanel, # Child panel
    FramesPanel, # Child panel
    FrameInfoPanel, # Child panel
    AddonProperty,
    ExtraFileAssetsPanel,# Child panel
    OpenFileBrowserOperator,# Child panel
    RemoveExtraFileAssetOperator,
    ExtraDirAssetsPanel,# Child panel
    OpenDirBrowserOperator,# Child panel
    RemoveExtraDirAssetOperator,
    ExtraEnvironmentPanel,# Child panel
    AdditionalRenderingOptionsPanel, # Child panel
    UploadDaemonPanel, # Child panel
    ExtraFileAssetProperty,
    ExtraDirAssetProperty,
    AddVariableOperator,
    RemoveVariableOperator,
    CustomVariableProperty,
    CustomVariableListProperty,
    ConnectOperator,
    ExportScriptOperator,
    SubmitOperator,
    # RenderAddPluginOperator,
    SimpleOperator,
    WaitSaveFinishOperator,
    # SubmissionWindowPanel,
]

# Register the add-on
def register():
    try:
        # First, unregister any previous versions of the plugin if they are active
        if "Conductor Render Submitter" in bpy.context.preferences.addons:
            bpy.ops.wm.addon_disable(module="Conductor Render Submitter")
    except Exception as e:
        print("Error disabling previous version of the plugin: ", e)


    # Now register the new version of the plugin
    for cls in classes:
        register_class(cls)

    # Create custom properties for the scene

    # Job Title
    bpy.types.Scene.job_title = bpy.props.StringProperty(
        name="Job Title",
        description="This title will appear in the Conductor dashboard. You may overwrite the default expression.",
        default="Blender Linux Render"
    )

    # Project
    bpy.types.Scene.project = bpy.props.StringProperty(
        name="Project",
        description="Conductor project in which to run the job.",
        # default="default"
        # default="None"
        # default=[('NONE', 'None', '')]

    )

    # Instance Type
    bpy.types.Scene.instance_type = bpy.props.EnumProperty(
        name="Instance Type",
        description="Choose from machines either with or without graphics cards. Utilizing a GPU is highly recommended for enhanced speed and efficiency, particularly when rendering with Cycles software. However, if you're using Eevee or Redshift rendering software, selecting a GPU-equipped machine is essential, as these renderers exclusively support GPU-based operations.",
        items=[("GPU", "GPU", ""),("CPU", "CPU", "")],
        update=update_instance_type_menu
    )

    # Machine Type
    bpy.types.Scene.machine_type = bpy.props.EnumProperty(
        name="Machine Type",
        description="Select the optimal machine setup for your job by evaluating critical elements. For GPU-based machines, consider the number of cores, memory size, type of graphics card, and its memory capacity. In contrast, for CPU-focused machines, assess the number of cores and the available memory.",
        items=[]
    )

    # Preemptible
    bpy.types.Scene.preemptible = bpy.props.BoolProperty(
        name="Preemptible",
        description="Choose whether this machine can be preempted by the cloud provider. Preemptible machines are less expensive and are nearly always the best choice for short to medium render jobs.",
        default=True
    )
    bpy.types.Scene.preemptible_retries = bpy.props.IntProperty(
        name="Preempted Retries",
        description="Preempted Retries: Determine the automatic retry count for tasks that get preempted. This setting is applicable and significant only when the 'Preemptible' option is active.",
        default=1,
        min=1,
        max=100
    )

    # Blender Version
    bpy.types.Scene.blender_version = bpy.props.EnumProperty(
        name="Blender Version",
        description="Choose the specific Blender version for job submission. This version may vary from the one installed locally. Be aware of any feature variations between versions that might affect your render. Note that changing this setting will modify the lists of accessible renders and add-ons accordingly.",
        items=[]
    )

    # Render Software
    bpy.types.Scene.render_software = bpy.props.EnumProperty(
        name="Render Software",
        description="Choose the appropriate rendering software based on your requirements. For Cycles, it's highly recommended to use a GPU instance type to ensure maximum performance and efficiency. In the case of Eevee or Redshift, selecting a GPU instance type is essential, as these renderers exclusively support GPU processing.",
        #items=[],
        items=[("Cycles", "Cycles", ""), ("Eevee", "Eevee", "")],
        ###items=[("Cycles", "Cycles", ""), ("Eevee", "Eevee", ""), ("Redshift", "Redshift", "")]
        update=render_software_update  # Add the update callback
    )

    # Render version
    bpy.types.Scene.render_version = bpy.props.EnumProperty(
        name="Render Version",
        description="Choose the specific version of your rendering software. Note that for Cycles and Eevee renders, version selection is not applicable as these renderers do not have distinct version options.",
        items=[('NONE', 'None', '')]
    )

    # Resolution X

    bpy.types.Scene.resolution_x_override = bpy.props.IntProperty(
        name="Resolution X",
        description="Customize the X resolution for job submission, independently from the Blender scene's setting. This option specifies the number of horizontal pixels in the rendered image. Note that altering this value here will not affect the Resolution X in your Blender scene.",
        # default=1920,
        min=1,
        max=16384,
    )

    # Resolution Y
    bpy.types.Scene.resolution_y_override = bpy.props.IntProperty(
        name="Y",
        description="Customize the Y resolution for job submission, independently from the Blender scene's setting. This option specifies the number of vertical pixels in the rendered image. Note that altering this value here will not affect the Resolution Y in your Blender scene.",
        # default=1080,
        min=1,
        max=16384,
    )
    # Resolution percentage
    bpy.types.Scene.resolution_percentage_override = bpy.props.IntProperty(
        name="%",
        description="Adjust the resolution scale percentage specifically for job submission, without affecting the Blender scene's settings. This parameter determines the proportion of the render resolution. Changing this value here won't impact the Resolution Percentage in your Blender scene. To see the final rendering resolution for the job submission, click on the 'Preview Script' button above.",
        # default=100,
        min=1,
        max=1000,
    )
    # Camera
    bpy.types.Scene.camera_override = bpy.props.EnumProperty(
        name="Camera",
        description="Set a specific camera for job submission, distinct from the active camera in your Blender scene. Modifying this selection will not alter the active camera within your Blender scene. Ensure you choose the desired camera for your final rendered image. This seelection is ignored if 'Update active camera every frame' is checked",
        items=[]
    )
    # Samples
    bpy.types.Scene.samples_override = bpy.props.IntProperty(
        name="Samples",
        description="Specify a custom number of render samples for job submission, which may differ from the setting in your Blender scene. Render samples represent the count of samples per pixel, crucial for defining the detail and quality of your rendered image. Choose a samples value that suits your scene's needs; note that while higher render samples can enhance image detail, they also increase rendering time without significant improvement beyond a certain point. For optimal performance and speed, especially with high sample rates using the Cycles renderer, opting for a GPU rendering instance is highly recommended",
        # default=512,
        min=1,
        max=10000,
    )

    # Chunk Size
    bpy.types.Scene.chunk_size = bpy.props.IntProperty(
        name="Chunk Size",
        description="Set the frame quantity per chunk, with a chunk constituting a batch of frames rendered collectively. Opt for a chunk size of 1-5 for intricate scenes to maintain detail and manage complexity effectively. For simpler scenes, a larger chunk size of 10-20 is recommended, and consider deactivating scout frames for efficiency. Treating task frames as part of a continuous animation sequence, rather than as distinct frames, optimizes the rendering workflow. This approach significantly reduces computational load, leading to quicker rendering outcomes",
        default=1,
        min=1,
        max=800,
        update=on_chunk_size_updated
    )


    bpy.types.Scene.use_custom_range = bpy.props.BoolProperty(
        name="Use Custom Range",
        description="If enabled, this option permits the alteration of the frame range defined in the Blender scene settings",
        default=True
    )

    # Frame Spec
    bpy.types.Scene.frame_range = bpy.props.StringProperty(
        name="Custom Range",
        description="Customize the frame range independent of the Blender scene settings, such as using a range of 1-100. This field is editable for manual input or can be auto-filled using an expression. Valid frame ranges include comma-separated lists of arithmetic sequences, denoted as individual numbers or hyphenated ranges with an optional step value (e.g., x for intervals), like 1,7,10-20,30-60x3,1001. While spaces and trailing commas are permissible, letters and non-numeric symbols are not. Both negative and mixed ranges are accepted, such as -50--10x2,-3-6",
        # default="1-100",
        update=on_custom_range_updated
    )


    # Use Scout Frames
    bpy.types.Scene.use_scout_frames = bpy.props.BoolProperty(
        name="Use Scout Frames",
        description="Activate the Scout Frames feature. Further details provided below",
        default=True
    )

    # Scout Frames
    bpy.types.Scene.scout_frames = bpy.props.StringProperty(
        name="Scout Frames",
        description="Set 'fml:3' for scout frames at the start, middle, and end (e.g., '1, 51, 100' for a range of 1-100) or 'auto:3' for evenly spaced frames (e.g., '17, 51, 84'). This feature is crucial for previewing render quality before processing the entire job. However, when using chunk sizes larger than one, be cautious with scout frames to avoid unnecessary rendering. Refer to the frames info panel for more specifics",
        default="fml:3"
    )

    bpy.types.Scene.frame_spec = bpy.props.StringProperty(
        name="Frame Spec:",
        description="Read-only parameter to show the frame range",
        default="1-100"
    )
    bpy.types.Scene.scout_spec = bpy.props.StringProperty(
        name="Scout Spec:",
        description="Read-only parameter to show the resolved scout frame spec",
        default=""
    )
    bpy.types.Scene.frame_count = bpy.props.StringProperty(
        name="Frame Count:",
        description="Read-only parameter to show the number of frames to render",
        default=""
    )
    bpy.types.Scene.task_count = bpy.props.StringProperty(
        name="Task Count:",
        description="A read-only field that displays the total number of tasks. For instance, setting the chunk size to 2 results in the creation of half the number of tasks compared to the total frames",
        default=""
    )
    bpy.types.Scene.scout_frame_count = bpy.props.StringProperty(
        name="Scout Frame Count:",
        description="This read-only field indicates the quantity of scout frames. Should the chunk size exceed one, the actual number of frames rendered could surpass the designated scout frames, as tasks are rendered in full without partial execution",
        default=""
    )
    bpy.types.Scene.scout_task_count = bpy.props.StringProperty(
        name="Scout Task Count:",
        description="A read-only attribute displaying the count of tasks encompassing the chosen scout frames",
        default=""
    )

    bpy.types.Scene.resolved_chunk_size = bpy.props.StringProperty(
        name="Resolved Chunk Size:",
        description="Resolved Chunk Size",
        default=""
    )

    # Addon properties
    bpy.types.Scene.addon_properties = bpy.props.CollectionProperty(type=AddonProperty)

    # Extra File Assets List
    bpy.types.Scene.extra_file_assets_list = CollectionProperty(type=ExtraFileAssetProperty)

    # Extra Directory Assets List
    bpy.types.Scene.extra_dir_assets_list = CollectionProperty(type=ExtraDirAssetProperty)

    # Custom Variables
    bpy.types.Scene.custom_variables = bpy.props.PointerProperty(type=CustomVariableListProperty)
    bpy.types.Scene.variables_dict = {}

    # Output Folder
    bpy.types.Scene.output_folder = bpy.props.StringProperty(
        name="Output Folder",
        description="This is the destination folder for downloading rendered images. Ensure this folder and its subfolders are not used to store assets required for scene rendering to avoid any conflicts",
        default="",
        subtype='DIR_PATH'
    )
    bpy.types.Scene.submission_tab = bpy.props.EnumProperty(
        name="Submission Tab",
        items=[
            ('VALIDATION', "Validation", ""),
            ('PROGRESS', "Progress", ""),
            ('RESPONSE', "Response", "")
        ],
        default='VALIDATION'
    )
    """
    bpy.types.Scene.factory_startup = bpy.props.BoolProperty(
        name="Factory Startup",
        description="Skip reading the startup.blend in the users home directory.",
        default=False
    )
    """
    bpy.types.Scene.disable_audio = bpy.props.BoolProperty(
        name="Disable Audio",
        description="Force sound system to None, disabling audio in Blender for rendering tasks",
        default=True
    )
    bpy.types.Scene.update_camera_checkbox = bpy.props.BoolProperty(
        name="Update active camera every frame",
        description="Continuously update the active camera for each frame from the Blender scene, overriding any previously selected camera settings.",
        default=False
    )
    bpy.types.Scene.view_layers_checkbox = bpy.props.BoolProperty(
        name="Render all active view layers",
        description="Render all active view layers",
        default=False
    )
    bpy.types.Scene.use_upload_daemon = bpy.props.BoolProperty(
        name="Use Upload Daemon",
        description="The upload daemon operates as an independent background process initiated via the command line. When the 'use_upload_daemon' option is selected, assets are not uploaded during the Blender session, allowing you to continue working without interruption during file uploads. Upon submission, a list of required assets is sent to Conductor. The upload daemon then periodically queries the server for any assets that need uploading. As soon as your submission reaches the server, the upload daemon retrieves the list and begins the upload process. You have the flexibility to activate the upload daemon either before or after job submission. Once activated, it monitors your entire account, enabling you to submit multiple jobs seamlessly.",
        default=False
    )
    bpy.types.Scene.location_tag = bpy.props.StringProperty(
        name="Location Tag",
        description="For this submission, please specify a location to align it with the corresponding uploader process. If your organization operates across multiple sites, you can assign a specific location to this submission, such as 'London'. This allows you to streamline your downloads by using the location option with a downloader daemon, ensuring you only download submissions associated with 'London'.",
        default=""
    )
    """
    # Display Tasks
    bpy.types.Scene.display_tasks = bpy.props.IntProperty(
        name="Display Tasks",
        description="On the preview Panel, set the number of tasks to show. This is for display purposes only and does not affect the tasks that are submitted to Conductor.",
        default=3,
        min=1,
        max=10
    )
    """
    # Triggers reloading of all scripts
    # bpy.ops.script.reload()

# Unregister the add-on
def unregister():
    try:
        # Remove classes from Blender
        for cls in reversed(classes):
           bpy.utils.unregister_class(cls)

        # Remove custom properties from bpy.types.Scene
        props_to_remove = [
            'job_title', 'project', 'instance_type', 'machine_type',
            'preemptible', 'preemptible_retries', 'blender_version',
            'render_software', 'render_version', 'resolution_x_override', 'resolution_y_override', 'resolution_percentage_override',
            'camera_override', 'samples_override',
            'chunk_size', 'use_custom_range',
            'frame_range', 'use_scout_frames', 'scout_frames',
            'frame_spec', 'scout_spec', 'frame_count', 'task_count',
            'scout_frame_count', 'scout_task_count', 'resolved_chunk_size',
            'addon_properties',
            'extra_file_assets_list', 'custom_variables', 'variables_dict', 'output_folder',
            'preview_panel_collapsed', 'display_tasks',
            'submission_tab', 'disable_audio', 'update_camera_checkbox', 'view_layers_checkbox',
            'use_upload_daemon', 'location_tag',
            #'factory_startup',
        ]

        for prop in props_to_remove:
            if hasattr(bpy.types.Scene, prop):
                delattr(bpy.types.Scene, prop)
    except Exception as e:
        print("Failed to unregister one or more properties: {}".format(e))



# Run the register function when the add-on is enabled
if __name__ == "__main__":
    # Register the add-on
    register()
    # Switch to the rendering workspace to show the UI
    bpy.context.window.workspace = bpy.data.workspaces["Render"]
