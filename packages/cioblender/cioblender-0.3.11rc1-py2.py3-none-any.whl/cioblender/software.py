
import bpy
import addon_utils
import json
from ciocore import data as coredata
from cioblender import driver


def populate_host_menu():
    """
    Populate Blender version menu.

    This function is called by the UI whenever the user clicks the Blender Version button.

    Returns:
        list of str: A list of supported Blender versions.
    """
    if not coredata.valid():
        return ["not_connected", "-- Not connected --"]

    software_data = coredata.data()["software"]
    host_names = software_data.supported_host_names()
    if not host_names:
        return [("no_host_names", "-- No hostnames --", "")]
    else:
        # Create a dictionary of projects
        blender_host_names = {}
        # For each host in the host_names, if the host is not in the blender_host_names dictionary,
        # add it to the dictionary
        for s in host_names:
            if s not in blender_host_names:
                blender_host_names[s] = (s, s, "")
        # Return the list of hosts
        return list(blender_host_names.values())


def populate_driver_menu(**kwargs):
    """
    Populate the renderer/driver type menu.

    Args:
        **kwargs: Additional keyword arguments.

    Returns:
        list of str: A list of driver types.
    """
    if not coredata.valid():
        return ["not_connected", "-- Not connected --"]
    # print("Driver menu: ")
    # print ([el for i in _get_compatible_plugin_versions(**kwargs) for el in (i,i)])

    return [el for i in _get_compatible_plugin_versions(**kwargs) for el in (i,i)]

def _get_compatible_plugin_versions(**kwargs):
    """
    Get compatible plugin versions.

    Args:
        **kwargs: Additional keyword arguments.

    Returns:
        list of str: A list of compatible plugin versions.
    """
    driver_data = driver.get_driver_data(**kwargs)
    if driver_data["conductor_product"].lower().startswith(("built-in", "unknown")):
        return [driver_data["conductor_product"]]

    if not coredata.valid():
        return []
    software_data = coredata.data().get("software")
    # print("software_data: {}".format(software_data))
    selected_host = kwargs.get("blender_version")
    # print("selected_host: {}".format(selected_host))
    plugins = software_data.supported_plugins(selected_host)
    # print("plugins: {}".format(plugins))
    plugin_names = [plugin["plugin"] for plugin in plugins]
    # print("plugin_names: {}".format(plugin_names))

    if driver_data["conductor_product"] not in plugin_names:
        return ["No plugins available for {}".format(driver_data["conductor_product"])]

    plugin_versions = []
    for plugin in plugins:
        if plugin["plugin"] == driver_data["conductor_product"]:
            for version in plugin["versions"]:
                plugin_versions.append("{} {}".format(
                    plugin["plugin"], version))
            break
    # print("plugin_versions: {}".format(plugin_versions))
    
    return plugin_versions


def resolve_payload(**kwargs):
    """
    Resolve the package IDs section of the payload for the given node.

    Args:
        **kwargs: Additional keyword arguments.

    Returns:
        dict: A dictionary containing the resolved package IDs.
    """
    ids = set()

    for package in packages_in_use(**kwargs):
        ids.add(package["package_id"])
        # print("ids: {}".format(ids))

    ids_list, env_list = get_ids_env()
    for package_id in ids_list:
        # print("package: {}".format(package_id))
        ids.add(package_id)


    ids_list, env_list = get_render_software_ids_env(**kwargs)
    for package_id in ids_list:
        # print("package: {}".format(package_id))
        ids.add(package_id)


    return {"software_package_ids": list(ids)}

def get_ids_env():
    """
    Retrieves package IDs and environment settings for selected add-ons and their versions.

    This function iterates over the selected add-ons and their versions, matches them with available
    packages, and then extracts the corresponding package IDs and environment settings.

    Returns:
        tuple: A tuple containing two lists - the first list contains package IDs, and the second list
        contains environment settings.
    """
    ids_list = []
    env_list = []

    selected_addons_versions = get_selected_addons_names_versions()
    addon_packages = get_package_dict()
    for addon, version in selected_addons_versions:
        if addon in addon_packages:
            if version in addon_packages[addon]:
                package = addon_packages[addon][version]
                package_id = package.get("package_id", None)
                if package_id and package_id not in ids_list:
                    ids_list.append(package_id)
                env = package.get("environment", None)
                if env and env not in env_list:
                    env_list.append(env)

    # print("ids_list: {}".format(ids_list))
    # print("env_list: {}".format(env_list))

    return ids_list, env_list
def get_render_software_ids_env(**kwargs):
    """
    Retrieves package IDs and environment settings for a specific render software based on provided parameters.

    Args:
        **kwargs: Keyword arguments that specify details about the render software, like its name and version.

    Returns:
        tuple: A tuple containing two lists - the first list contains package IDs, and the second list
        contains environment settings for the render software.
    """
    ids_list = []
    env_list = []

    addon_packages = get_package_dict()
    render_software = kwargs.get("render_software", None)
    # print(">>>>render_software: {}".format(render_software))
    if render_software:
        if render_software.lower().startswith("redshift"):
            redshift_package = addon_packages.get("redshift-blender", None)
            if redshift_package:
                render_version = kwargs.get("render_version", None)
                if render_version and render_version in redshift_package:
                    package = redshift_package.get(render_version, None)
                    if package:

                        # print(">>>>>> redshift: package: {}".format(package))
                        package_id = package.get("package_id", None)
                        if package_id and package_id not in ids_list:
                            ids_list.append(package_id)
                        env = package.get("environment", None)
                        if env and env not in env_list:
                            env_list.append(env)
    return ids_list, env_list


def get_add_on_names(**kwargs):
    """
    Retrieves a dictionary of add-on names available for a specific Blender version.

    Args:
        **kwargs: Keyword arguments that may contain the Blender version to query.

    Returns:
        dict: A dictionary where keys are add-on names and values are lists of versions available for those add-ons.
    """
    package_dict, sorted_addons_dict = get_blender_addons_list(**kwargs)
    return sorted_addons_dict


def rename_blender_addon(name):
    """
    Renames a Blender add-on from its system name to a more readable format.

    Args:
        name (str): The original system name of the Blender add-on.

    Returns:
        str: The reformatted, more readable name of the add-on.
    """
    # Split the name by '-'
    parts = name.split('-')
    # Remove the last part (assuming it's 'blender' or similar)
    meaningful_parts = parts[:-1]
    # Join the remaining parts (in case there were multiple '-')
    joined_parts = ' '.join(meaningful_parts)
    # Replace underscores with spaces and capitalize each word
    formatted_name = ' '.join(word.capitalize() for word in joined_parts.split('_'))

    return formatted_name


def get_blender_addons_list(**kwargs):
    """
    Retrieves a list of available add-ons for a specified version of Blender, along with their package information.

    Args:
        **kwargs: Keyword arguments that may contain the Blender version to query.

    Returns:
        tuple: A tuple containing a dictionary of package information and a dictionary of formatted add-on names.
    """
    package_dict = {}
    formatted_dict = {}
    coredata.init(product="blender")
    sw = coredata.data()["software"]
    blender_name = kwargs.get("blender_version", None)
    add_ons = sw.supported_plugins(blender_name)
    for add_on in add_ons:
        add_on_name = add_on.get("plugin", None)
        add_on_versions = add_on.get("versions")
        if add_on_name and add_on_versions:
            if add_on_name not in package_dict:
                package_dict[add_on_name] = {}
            for version in add_on_versions:
                add_on_path = "{} {} linux".format(add_on_name, version)
                query = "{}/{}".format(blender_name, add_on_path)
                add_on_package = sw.find_by_path(query)
                if add_on_package:
                    product = add_on_package.get("product")
                    package_id = add_on_package.get("package_id")
                    env = add_on_package.get("environment")
                    if product and package_id:
                        if version not in package_dict[add_on_name]:
                            package_dict[add_on_name][version] = {}
                        package_dict[add_on_name][version]["package_id"] = package_id
                        package_dict[add_on_name][version]["environment"] = env

            formatted_name = rename_blender_addon(add_on_name)
            if formatted_name and formatted_name not in formatted_dict:
                formatted_dict[formatted_name] = list(reversed(add_on_versions))

            # Sort the formatted_dict by keys:
            sorted_addons_dict = {k: formatted_dict[k] for k in sorted(formatted_dict)}


            # print(">>> Package dict:", package_dict)
            # print(">>> formatted_dict: ", formatted_dict)

    # Convert the addons_list to a JSON string
    addons_dict_json = json.dumps(sorted_addons_dict)
    # Store the JSON string in a custom property in the Blender scene
    bpy.context.scene['addons_dict_json'] = addons_dict_json

    package_dict_json = json.dumps(package_dict)
    bpy.context.scene['package_dict_json'] = package_dict_json

    return package_dict, sorted_addons_dict

def get_addons_dict():
    """
    Retrieves a dictionary of add-ons stored as a JSON string in the Blender scene.

    Returns:
        dict: A dictionary of add-ons extracted from the JSON string.
    """
    # Retrieve the JSON string from the Blender scene
    addons_dict_json = bpy.context.scene.get('addons_dict_json', '[]')

    # Convert the JSON string back to a Python list
    addons_dict = json.loads(addons_dict_json)

    return addons_dict

def get_package_dict():
    """
   Retrieves a dictionary of package information stored as a JSON string in the Blender scene.

   Returns:
       dict: A dictionary of package information extracted from the JSON string.
   """
    # Retrieve the JSON string from the Blender scene
    package_dict_json = bpy.context.scene.get('package_dict_json', '[]')

    # Convert the JSON string back to a Python list
    package_dict = json.loads(package_dict_json)

    return package_dict

def original_blender_addon_name(formatted_name):
    """
    Converts a formatted add-on name back to its original system name.

    Args:
        formatted_name (str): The formatted name of the Blender add-on.

    Returns:
        str: The original system name of the add-on.
    """
    name_with_underscores = formatted_name.replace(' ', '_').lower()

    # Add the suffix '-blender' to the name
    original_name = "{}-blender".format(name_with_underscores)

    return original_name


def get_selected_addons_names_versions():
    """
    Get the names and versions of the selected (enabled) add-ons from the add-ons panel and convert them to the
    original system name format.

    Returns:
        list of tuples: A list of tuples, where each tuple contains the original system name of
        an enabled add-on and its selected version.
    """
    selected_addons_versions = []

    # Ensure that the addon_properties attribute exists in the scene
    if hasattr(bpy.context.scene, "addon_properties"):
        # Loop through the addon_properties and check if the add-on is enabled
        for addon in bpy.context.scene.addon_properties:
            if addon.enabled:
                # Convert the formatted name to the original system name
                original_name = original_blender_addon_name(addon.name)
                # Append the original name and selected version to the list
                selected_addons_versions.append((original_name, addon.menu_option))

    # print("Selected addons and versions: {}".format(selected_addons_versions))

    return selected_addons_versions


def parse_version(version_str):
    """
    Extracts the numeric part of the version string and returns a tuple of integers for comparison.
    Handles cases with two or three version numbers (e.g., '2.80' or '4.0.1').
    For example, 'blender 2.80.glibc217 linux' becomes (2, 80, 0),
    and 'blender 4.0.1.glibc217 linux' becomes (4, 0, 1).
    Non-numeric parts are ignored/discarded.
    """
    parts = version_str.split(' ')
    if len(parts) > 1:
        version_part = parts[1]
        numeric_parts = version_part.split('.')  # Split the version part into individual numbers
        version_numbers = []
        for part in numeric_parts:
            if part.isdigit():
                version_numbers.append(int(part))
            else:
                version_numbers.append(0)  # Non-numeric parts are treated as 0

        # Ensure the version is always a tuple of three numbers (major, minor, patch)
        # If there are less than 3 parts, fill the remaining parts with 0
        return tuple(version_numbers + [0] * (3 - len(version_numbers)))
    return (0, 0, 0)  # Default version if parsing fails




def version_difference(version1, version2):
    """
    Calculates a weighted difference between two version tuples.

    The difference considers the major, minor, and patch versions with different weights,
    giving more importance to higher version levels.

    Args:
        version1 (tuple): The first version tuple.
        version2 (tuple): The second version tuple.

    Returns:
        int: A weighted difference between the two versions.
    """
    # We have to decide if we want the closest version overall or closest version below current version
    major_weight = 1000
    minor_weight = 100
    patch_weight = 10
    # Calculate the weighted difference
    diff = (major_weight * abs(version1[0] - version2[0]) +
            minor_weight * abs(version1[1] - version2[1]) +
            patch_weight * abs(version1[2] - version2[2]))
    return diff


def find_closest_version(available_versions, current_version_tuple):
    """
    Finds the closest version to the current_version from the list of available_versions.
    If two versions have the same difference from the current version, the older version is selected.
    """
    closest_version = None
    minimum_difference = float('inf')
    current_closest_tuple = None

    for version_str in available_versions:
        version_tuple = parse_version(version_str)

        difference = version_difference(version_tuple, current_version_tuple)
        if difference < minimum_difference:
            minimum_difference = difference
            closest_version = version_str
        elif difference == minimum_difference:
            # If the difference is the same, choose the older version
            current_closest_tuple = parse_version(closest_version)
            if version_tuple < current_closest_tuple:  # Compare tuples, this will choose the older version
                closest_version = version_str
        # print("closest_version: {}".format(closest_version))

    return closest_version

def get_blender_name(**kwargs):
    coredata.init(product="blender")
    sw = coredata.data()["software"]
    host_versions = sw.supported_host_names()

    # Get the current Blender version as a string
    current_version_tuple = bpy.data.version
    # current_blender_version_str = f"{version[0]}.{version[1]}.{version[2]}"
    # current_version_tuple = (4, 0, 5)

    # Find the closest version
    closest_version = find_closest_version(host_versions, current_version_tuple)
    # print(f"Closest version to the current scene's Blender version ({current_version_tuple}): {closest_version}")

    # Use the closest version for further processing
    blender_name = closest_version
    return blender_name

# --------------------
import bpy
import addon_utils


def get_enabled_addons():
    """
    Retrieves a list of currently enabled addons in Blender.

    This function collects the names of all enabled addons from the user's preferences,
    gathers detailed information about each addon from the addon utilities, and then
    filters the addons to only include those that are enabled.

    Returns:
        list: A list of tuples, each containing (module, info) for each enabled addon.
    """
    prefs = bpy.context.preferences
    addon_names = set()  # Initialize an empty set for addon names
    for addon in prefs.addons:
        addon_names.add(addon.module)  # Add each addon name to the set

    addons = []
    for mod in addon_utils.modules(refresh=False):
        addon_info = addon_utils.module_bl_info(mod)
        addons.append((mod, addon_info))  # Append the module-info pair to the addons list

    addon_list = []
    for mod, info in addons:
        if mod.__name__ in addon_names:
            addon_list.append((mod, info))

    return addon_list


def get_addon_versions(addon_tuple):
    """
    Extracts the version information of a given addon.

    Args:
        addon_tuple (tuple): A tuple containing the module and info of an addon.

    Returns:
        tuple: The version of the addon as a tuple (major, minor, patch).
    """
    info = addon_tuple[1]
    version = info.get('version', (0, 0, 0))  # Use get with default value
    return version


def get_addon_versions_dict():
    """
    Constructs a dictionary of the enabled addons and their version numbers.

    This function utilizes `get_enabled_addons` to retrieve a list of enabled addons,
    then iterates over these addons, fetching their version numbers and storing
    them in a dictionary with the addon name as the key and the version number as the value.

    The function also prints each addon name followed by its version number.
    """
    addon_versions = {}
    enabled_addons = get_enabled_addons()
    for addon_tuple in enabled_addons:
        addon_name = addon_tuple[0].__name__
        version = get_addon_versions(addon_tuple)
        version_str = '.'.join(map(str, version))  # Convert version tuple to string
        if addon_name not in addon_versions:
            addon_versions[addon_name] = version_str
        # print(f"{addon_name} {version_str}")

    return addon_versions




# --------------------------------------------------------------------
def get_redshift_package_renderer(**kwargs):
    """
    Get the package renderer.
    """
    package_renderer_id = None
    tree_data = coredata.data().get("software")
    try:
        rs_version = "3.5.17"
        redshift_name_template = "redshift-blender {version} linux"
        blender_name = kwargs.get("blender_version", None)
        redshift_blender_name = redshift_name_template.format(version=rs_version)
        package_renderer = tree_data.find_by_path(blender_name + "/" + redshift_blender_name)
        # print(">>package_renderer: {}".format(package_renderer))
        if package_renderer:
            package_renderer_id = package_renderer["package_id"]
            # print("package_renderer_id: {}".format(package_renderer_id))

    except Exception as e:
        print("Unable to get package renderer. Error: {}".format(e))
    return package_renderer_id



def packages_in_use(**kwargs):
    """
    Return a list of packages as specified by names in the software dropdowns.

    Args:
        **kwargs: Additional keyword arguments.

    Returns:
        list of dict: A list of packages.
    """
    if not coredata.valid():
        return []
    tree_data = coredata.data().get("software")
    #print("tree_data: {}".format(tree_data))
    if not tree_data:
        return []

    platform = list(coredata.platforms())[0]
    host = kwargs.get("blender_version")
    blender_version = kwargs.get("blender_version")
    driver = "{}/{} {}".format(host, blender_version, platform)
    paths = [host, driver]
    num_plugins = kwargs.get("extra_plugins", 0)
    for i in range(1, num_plugins+1):
        parm_val = kwargs["extra_plugin_{}".format(i)]
        paths.append("{}/{} {}".format(host, parm_val, platform))

    return list(filter(None, [tree_data.find_by_path(path) for path in paths if path]))





