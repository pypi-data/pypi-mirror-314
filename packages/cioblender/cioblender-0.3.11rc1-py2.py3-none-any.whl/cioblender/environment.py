import re
from cioblender import software, util

from ciocore import data as coredata
from ciocore.package_environment import PackageEnvironment


def resolve_payload(**kwargs):
    """
    Resolve the payload for the environment.

    This function retrieves and processes environment information, including the 'PATH' variable and additional
    environment variables, based on the provided keyword arguments. It compiles the relevant environment variables
    into a dictionary and returns it as part of the payload.

    :param kwargs: A dictionary of keyword arguments that may include 'extra_variables'.
    :return: A dictionary containing the 'environment' key with the environment variables.
    """

    pkg_env = get_main_env(**kwargs)
    pkg_env = get_addons_env(pkg_env)
    pkg_env = get_render_software_env(pkg_env, **kwargs)

    return {"environment": dict(pkg_env)}


def get_main_env(**kwargs):
    """
    Resolve the payload for the environment.

    This function retrieves and processes environment information, including the 'PATH' variable and additional
    environment variables, based on the provided keyword arguments. It compiles the relevant environment variables
    into a dictionary and returns it as part of the payload.

    :param kwargs: A dictionary of keyword arguments that may include 'extra_variables'.
    :return: A dictionary containing the 'environment' key with the environment variables.

    Todo:
    You can initialize PackageEnvironment() with the package, and it will then contain all the environment variables for that package.
    env_pack = PackageEnvironment(package)
    And then you can extend it with the environments from other packages:
    env_pack.extend(another_package)
    And you can then add entries from the extra-env section.
    env_pack.extend({"environment": [...] })
    """
    env_pack = PackageEnvironment()

    # Get unique paths from packages with non-empty 'path' attribute
    paths = list({package.get("path") for package in software.packages_in_use(**kwargs) if package.get("path")})

    # Join the unique paths with ":"
    blender_path = ":".join(paths)

    main_env = {
        "environment": [
            {"name": "PATH", "value": blender_path, "merge_policy": "append"}
        ]
    }

    env_pack.extend(main_env)
    try:
        extra_variables = kwargs.get("extra_variables", None)

        if extra_variables:
            for variable in extra_variables:
                key, value = variable.variable_name, variable.variable_value
                if key and value:
                    env_item = {
                        "environment": [
                            {"name": key, "value": value, "merge_policy": "append"}
                        ]
                    }
                    env_pack.extend(env_item)
    except Exception as e:
        print("Unable to get extra environment variables. Error: {}".format(e))

    return env_pack

def get_addons_env(pkg_env):
    ids_list, env_list = software.get_ids_env()
    if env_list:
        for env in env_list:
            if env:
                pkg_env.extend(env)
    return pkg_env

def get_render_software_env(pkg_env, **kwargs):
    ids_list, env_list = software.get_render_software_ids_env(**kwargs)
    if env_list:
        for env in env_list:
            if env:
                pkg_env.extend(env)
    return pkg_env

def get_render_software_env_old(pkg_env, **kwargs):
    render_software = kwargs.get("render_software", None)
    if render_software and render_software.lower().startswith("redshift"):
        # print("Getting Redshift env")
        pkg_env = get_redshift_env(pkg_env, **kwargs)

    return pkg_env

def get_redshift_env(pkg_env, **kwargs):
    package_host, package_renderer = get_redshift_package_renderer(**kwargs)
    # print("Redshift package host {}".format(package_host))
    # print("Redshift package renderer {}".format(package_renderer))

    if package_host:
        pkg_env.extend(package_host)

    if package_renderer:
        pkg_env.extend(package_renderer)
    return pkg_env

def get_redshift_package_renderer(**kwargs):
    """
    Get the package renderer.
    """
    package_host, package_renderer = None, None
    package_host_env, package_renderer_env = None, None
    tree_data = coredata.data().get("software")
    try:
        rs_version = "3.5.17"
        redshift_name_template = "redshift-blender {version} linux"
        blender_name = kwargs.get("blender_version", None)
        redshift_blender_name = redshift_name_template.format(version=rs_version)
        package_host = tree_data.find_by_name(blender_name)
        package_renderer = tree_data.find_by_path(blender_name + "/" + redshift_blender_name)
        # print(">package_host: {}".format(package_host))
        # print(">package_renderer: {}".format(package_renderer))
        if package_host and "environment" in package_host:
            package_host_env = package_host
            #print("package_host_env: {}".format(package_host_env))
        if package_renderer and "environment" in package_renderer:
            package_renderer_env = package_renderer
            # print ("package_renderer_env: {}".format(package_renderer_env))

    except Exception as e:
        print("Unable to get package renderer. Error: {}".format(e))
    return package_host_env, package_renderer_env

def extend_env(env_pack, other_pack):
    """
    Extend the environment package with another package.
    Assuming that "merge_policy" the other_pack is "append"
    """
    for key, value in other_pack.items():
        if key in env_pack:
            existing_value = env_pack[key]
            env_pack[key] = "{}:{}".format(existing_value, value)
    return env_pack

def format_env(env_pack):
    formatted_env = {}
    for key, value in env_pack:
        if isinstance(value, list):
            # Process each dict in the list to extract the name and value
            for var in value:
                if var['merge_policy'] == 'exclusive' or var['name'] not in formatted_env:
                    formatted_env[var['name']] = var['value']
                elif var['merge_policy'] == 'append':
                    # Append the value if merge_policy is 'append'
                    existing_value = formatted_env[var['name']]
                    formatted_env[var['name']] = existing_value + ':' + var['value']
        else:
            # Directly assign the value if it's not a list
            formatted_env[key] = value
    return formatted_env



def get_blender_version(**kwargs):
    version = "3.5.1"
    blender_version_name = kwargs.get("blender_version", None)
    if blender_version_name:
        version_match = re.search(r"\b(\d+\.\d+\.\d+)", blender_version_name)

        if version_match:
            version = version_match.group(1)
            print("Extracted version:", version)
        else:
            print("Version match not found.")
    else:
        print("Blender version string is empty.")

    return version

