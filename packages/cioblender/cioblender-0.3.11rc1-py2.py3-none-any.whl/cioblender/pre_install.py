import os
import sys
import importlib.util

def fslash(path):
    """
    Replace backslashes with forward slashes in the given path.

    :param path: A string representing a file path.
    :return: A string with backslashes replaced by forward slashes.
    """
    return path.replace("\\", "/")

PLATFORM = sys.platform
# PLUGIN_FILE_NAME = "conductor_submitter_plugin.py"  # Name of the plugin file
PLUGIN_FILE_NAME = "conductor.py"  # Name of the plugin file

def remove_plugin_from_blender_folders(platform):
    """
    Remove and unregister the Conductor Blender plugin from Blender addon folders based on the platform.

    :param platform: The platform identifier (e.g., "win", "linux", "darwin").
    """
    user_home = os.path.expanduser("~")
    blender_versions_folder = None
    try:
        if platform.startswith("win"):
            blender_versions_folder = os.path.join(user_home, "AppData/Roaming/Blender Foundation/Blender")
        elif platform.startswith("linux"):
            blender_versions_folder = os.path.join(user_home, ".config/blender")
        elif platform.startswith("darwin"):
            blender_versions_folder = os.path.join(user_home, "Library/Application Support/Blender")

        if blender_versions_folder:
            for version_folder in os.listdir(blender_versions_folder):
                addon_folder = os.path.join(blender_versions_folder, version_folder, "scripts/addons")
                plugin_path = os.path.join(addon_folder, PLUGIN_FILE_NAME)
                if os.path.exists(plugin_path):
                    # Attempt to unregister the plugin
                    spec = importlib.util.spec_from_file_location("module.name", plugin_path)
                    plugin_module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(plugin_module)
                    if hasattr(plugin_module, 'unregister'):
                        plugin_module.unregister()
                        print(f"Unregistered plugin at {plugin_path}")
                    # Remove the plugin file
                    try:
                        os.remove(plugin_path)
                        print(f"Removed plugin file from {plugin_path}")
                    except Exception as e:
                        print(f"Unable to remove plugin file at {plugin_path}, error: {e}")
                else:
                    print(f"No plugin file found at {plugin_path}")
    except Exception as e:
        print(f"Error during plugin removal: {e}")

def main():
    """
    Main function for removing the Conductor Blender addon.

    This function attempts to unregister and remove the addon from Blender's addon folders based on the platform.
    """
    if not PLATFORM.startswith(("win", "linux", "darwin")):
        sys.stderr.write("Unsupported platform: {}".format(PLATFORM))
        sys.exit(1)

    remove_plugin_from_blender_folders(PLATFORM)
    print("Completed Blender addon removal process.")

if __name__ == "__main__":
    main()
