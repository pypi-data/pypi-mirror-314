import os
import sys
import subprocess
import re


def fslash(path):
    """
    Replace backslashes with forward slashes in the given path.

    :param path: A string representing a file path.
    :return: A string with backslashes replaced by forward slashes.

    """
    return path.replace("\\", "/")

# Todo: use get_version_number() to get 'version'

PLATFORM = sys.platform
PWD = os.path.dirname(os.path.abspath(__file__))
CIO_DIR = fslash(os.path.dirname(PWD))
print("CIO_DIR", CIO_DIR)

ADDOON_FILE = os.path.join(PWD, "conductor_submitter_plugin.py")
INIT_CONTENT = """
import sys
import os
CIO_DIR = '{}'
sys.path.append(CIO_DIR)
os.environ['CIO_DIR'] = CIO_DIR
                       
from cioblender import conductor_submitter_plugin

bl_info = {{
    'name': 'Conductor Render Submitter',
    'author': 'Conductor Technologies, CoreWeave',
    'version': (0, 3, 10, 0),
    'blender': (4, 0, 2),
    'location': 'Render > Properties',
    'description': 'Conductor Render submitter UI',
    'category': 'Render',
}}

def register():
    conductor_submitter_plugin.register()

def unregister():
    conductor_submitter_plugin.unregister()

if __name__ == '__main__':
    register()
""".format(CIO_DIR)


def create_plugin_at_blender_folders(platform):
    """
    Copy the Conductor Blender plugin to Blender addon folders based on the platform.

    :param platform: The platform identifier (e.g., "win", "linux", "darwin").
    :return: A list of folders where the plugin was copied to.
    """
    user_home = os.path.expanduser("~")
    blender_versions_folder = None
    copied_folders = []
    addon_destination = ""

    if platform.startswith("win"):
        blender_versions_folder = os.path.join(user_home, "AppData/Roaming/Blender Foundation/Blender")
    elif platform.startswith("linux"):
        blender_versions_folder = os.path.join(user_home, ".config/blender")
    elif platform.startswith("darwin"):
        blender_versions_folder = os.path.join(user_home, "Library/Application Support/Blender")

    msg = "Source plugin: %s\n" % ADDOON_FILE
    sys.stdout.write(msg)
    if blender_versions_folder:
        for version_folder in os.listdir(blender_versions_folder):
            addon_folder = os.path.join(blender_versions_folder, version_folder, "scripts/addons")
            if not os.path.exists(addon_folder):
                try:
                    os.makedirs(addon_folder)
                except:
                    continue
            # Todo: Do we need to remove existing plugin file?
            """
            # Check and remove existing plugin file
            existing_plugin_path = os.path.join(addon_folder, "conductor.py")
            if os.path.exists(existing_plugin_path):
                try:
                    os.remove(existing_plugin_path)
                except Exception as e:
                    msg = "Unable to remove existing plugin at %s, error: %s\n" % (existing_plugin_path, e)
                    sys.stdout.write(msg)
            """
            # Write the new plugin
            try:
                addon_destination = os.path.join(addon_folder, "conductor.py")
                with open(addon_destination, "w", encoding="utf-8") as f:
                    f.write(INIT_CONTENT + "\n")

                copied_folders.append(addon_folder)
                msg = "Created Conductor Blender plugin %s\n" % addon_destination
                sys.stdout.write(msg)
            except Exception as e:
                sys.stderr.write(f"Unable to copy plugin {ADDOON_FILE} to folder {addon_destination}, error: {e}\n")

    return copied_folders

def remove_quarantine_attr(dir_path):
    """
    Remove the quarantine attribute from all files in the given directory recursively.

    :param dir_path: A string representing the path to the directory.
    """
    try:
        # Running the xattr command to remove the quarantine attribute
        subprocess.run(["xattr", "-dr", "com.apple.quarantine", dir_path], check=True)
        print(f"Quarantine removed from all files in {dir_path}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to remove quarantine from {dir_path}: {e}")

def get_version_number():
    """
    Extracts and returns the version number from a "VERSION" file located in the same directory as this script.

    This function reads the version number from a file named "VERSION" expected to be found in the package directory.
    It then uses regular expressions to find all numeric sequences in the version string, converting them to integers.

    The function assumes the version string is formatted in a standard versioning format (e.g., "1.0.0"), where the
    numbers represent major, minor, and patch versions, respectively. These numbers are extracted, converted to integers,
    and returned as a list.

    Returns:
        list of int: A list containing the version numbers found in the "VERSION" file. Each element of the list is
        an integer corresponding to a part of the version number (e.g., major, minor, patch).

    Raises:
        FileNotFoundError: If the "VERSION" file does not exist in the package directory.
        ValueError: If the version string does not contain any numbers.

    Example:
        If the "VERSION" file contains the string "2.4.1", this function will return [2, 4, 1].
    """
    PKG_DIR = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(PKG_DIR, "VERSION")) as version_file:
        version_str = version_file.read().strip()
    numbers = re.findall(r'\d+', version_string)
    numbers = [int(num) for num in numbers]
    return numbers

def remove_all_quarantine():
    """
    This function is designed to remove the quarantine attribute from the shiboken6 and PySide6 directories,
    which are commonly subject to this attribute on macOS systems. Removing the quarantine attribute is necessary
    to avoid potential security restrictions that can prevent these directories from being accessed or executed
    properly.

    The function locates the shiboken6 and PySide6 directories within the parent directory specified by the global
    variable `CIO_DIR`. It then attempts to remove the quarantine attribute from these directories using the
    `remove_quarantine_attr` function, which must be defined elsewhere in the codebase.

    Exceptions:
        In case of any errors during the process, such as failure to find the directories, lack of permissions,
        or issues executing the attribute removal command, the function catches the exception and prints a message
        indicating the failure along with the error message returned by the system.

    Note:
        This function is specifically tailored for use on macOS systems where the quarantine attribute is a common
        issue. It assumes that the `remove_quarantine_attr` function is capable of interacting with the system's
        attributes and that `CIO_DIR` is a predefined global variable pointing to the parent directory of the
        shiboken6 and PySide6 directories.
    """
    try:

        # Paths to the shiboken6 and PySide6 directories in the parent directory
        shiboken6_dir = os.path.join(CIO_DIR, "shiboken6")
        pyside6_dir = os.path.join(CIO_DIR, "PySide6")

        # Remove quarantine from the directories
        remove_quarantine_attr(shiboken6_dir)
        remove_quarantine_attr(pyside6_dir)

    except Exception as e:
        print(f"Failed to remove quarantine from shiboken6 and PySide6 on the MacOS {e}")

def main():
    """
    Main function for setting up the Conductor Blender addon.

    This function adds the CIO_DIR path to the beginning of the addon file and copies the addon to Blender's
    addon folders based on the platform.
    """
    if not PLATFORM.startswith(("win", "linux", "darwin")):
        sys.stderr.write("Unsupported platform: {}\n".format(PLATFORM))
        sys.exit(1)

    # Remove all quarantine only if the platform is macOS
    if PLATFORM.startswith("darwin"):
        remove_all_quarantine()

    copied_folders = create_plugin_at_blender_folders(PLATFORM)

    if copied_folders:
        sys.stdout.write(f"Blender add-on setup successfully completed!\n")

    else:
        sys.stdout.write(f"Unable to locate any Blender add-on directories.\n")

if __name__ == "__main__":
    main()
