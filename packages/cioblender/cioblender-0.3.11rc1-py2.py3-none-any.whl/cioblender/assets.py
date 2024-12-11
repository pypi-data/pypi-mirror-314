import bpy
import os
import platform
import re
from ciopath.gpath_list import PathList, GLOBBABLE_REGEX
import logging
from cioblender import task, util

logger = logging.getLogger(__name__)

STARTUP_VAL = "startup.blend"

def resolve_payload(**kwargs):
    """
    Resolve the upload_paths field for the payload.

    This function gathers a list of file paths to be uploaded, including auxiliary paths,
    extra assets, and scanned assets, and returns them as a dictionary.

    :param kwargs: A dictionary of keyword arguments that may include "blender_filepath".
    :return: A dictionary containing the "upload_paths" key with a list of file paths.
    """
    path_list = PathList()

    path_list.add(*auxiliary_paths(**kwargs))
    path_list.add(*extra_paths())
    path_list.add(*scan_assets())

    return {"upload_paths": [p.fslash() for p in path_list]}


def resolve_payload_extended(**kwargs):
    """
    Resolve the upload_paths field for the payload.

    This function gathers a list of file paths to be uploaded, including auxiliary paths,
    extra assets, and scanned assets, and returns them as a dictionary.

    :param kwargs: A dictionary of keyword arguments that may include "blender_filepath".
    :return: A dictionary containing the "upload_paths" key with a list of file paths.
    """
    path_list = PathList()

    path_list.add(*auxiliary_paths(**kwargs))
    path_list.add(*extra_paths())
    path_list.add(*scan_assets())

    try:
        blender_folder = None

        output_folder = kwargs.get("output_folder", None)
        if output_folder:
            output_folder = output_folder.replace("\\", "/")
        blender_filepath = kwargs.get("blender_filepath")
        if blender_filepath:
            blender_filepath = blender_filepath.replace("\\", "/")
            blender_folder = os.path.dirname(blender_filepath)
        # print("blender_folder : {}".format(blender_folder))
        # print("output_folder : {}".format(output_folder))

        # Get the current assets
        current_assets = []
        for path in path_list:
            path = str(path)
            path = path.replace("\\", "/")
            if path not in current_assets:
                current_assets.append(str(path))

        # print("Updated current assets: {}".format(current_assets))
        # Filter out paths that are within the output folder
        # Todo: Add a validation warning for this
        filtered_paths = [path for path in current_assets if not is_within_output_folder(path, output_folder)]
        # print("filtered paths before removing the blender folder: {}".format(filtered_paths))
        # Filter out paths that are the "blender file folder"
        filtered_paths = [path for path in filtered_paths if not path == blender_folder]
        # print("filtered paths after removing the blender folder: {}".format(filtered_paths))
        return {"upload_paths": filtered_paths}

    except Exception as e:
        logger.debug("Unable to clean assets, error: {}".format(e))

    return {"upload_paths": [p.fslash() for p in path_list]}

def is_within_output_folder(path, output_folder):
    # Normalize the paths to handle different platforms and spaces
    normalized_path = os.path.normpath(str(path))  # Convert path to string
    normalized_output_folder = os.path.normpath(str(output_folder))  # Convert path to string

    # Check if the normalized path is within the normalized output folder
    result = normalized_path.startswith(normalized_output_folder)
    return result

def auxiliary_paths(**kwargs):
    """
    Get auxiliary paths.

    This function retrieves auxiliary paths, specifically the "blender_filepath" if it exists.

    :param kwargs: A dictionary of keyword arguments that may include "blender_filepath".
    :return: A PathList object containing auxiliary paths.
    """
    path_list = PathList()
    """
    try:
        blender_filepath = kwargs.get("blender_filepath")
        blender_filepath = blender_filepath.replace("\\", "/")
        if blender_filepath and STARTUP_VAL not in blender_filepath:
            # Check if blender_filepath exists
            if os.path.exists(blender_filepath):
                path_list.add(blender_filepath)
                path_list.real_files()
            else:
                logger.debug("Unable to find blender_filepath: {}".format(blender_filepath))
    except Exception as e:
        logger.debug("Unable to load blender_filepath, error: {}".format(e))
    """


    try:
        blender_filepath = kwargs.get("blender_filepath")
        blender_filepath = blender_filepath.replace("\\", "/")
        render_filepath = task.get_render_file(kwargs)
        if render_filepath:
            render_filepath = render_filepath.replace("\\", "/")
            # Check if render_filepath exists
            if os.path.exists(render_filepath):
                print("Render file path: ", render_filepath)
                render_filepath = util.resolve_path(render_filepath)
                print("Render file path: ", render_filepath)
                path_list.add(render_filepath)
                # path_list.real_files()
            else:
                logger.debug("Unable to find blender_filepath: {}".format(blender_filepath))
    except Exception as e:
        logger.debug("Unable to load blender_filepath, error: {}".format(e))

    try:
        cio_dir = os.getenv('CIO_DIR')
        if cio_dir:
            script_path = "{}/cioblender/scripts/brender.py".format(cio_dir)
            if os.path.exists(script_path):
                script_path = util.resolve_path(script_path)
                path_list.add(script_path)
    except Exception as e:
        logger.debug("Unable to load script_path, error: {}".format(e))


    return path_list

def extra_paths():
    """
    Add extra assets.

    This function retrieves extra assets from the current Blender scene and adds them to the PathList.

    :return: A PathList object containing extra asset paths.
    """
    path_list = PathList()
    scene = bpy.context.scene

    # Add extra file assets
    try:
        extra_file_assets_list = scene.extra_file_assets_list

        for asset in extra_file_assets_list:
            file_path = asset.file_path
            if file_path and STARTUP_VAL not in file_path:
                # Check if asset.file_path exists
                if os.path.exists(file_path) and not is_home_directory_or_drive(file_path):
                    file_path = util.resolve_path(file_path)
                    path_list.add(file_path)
                else:
                    logger.debug("Unable to find extra file asset: {}".format(file_path))
    except Exception as e:
        logger.debug("Unable to load extra file assets, error: {}".format(e))

    # Add extra directory assets
    try:
        extra_dir_assets_list = scene.extra_dir_assets_list

        for asset in extra_dir_assets_list:
            file_path = asset.file_path
            if file_path and STARTUP_VAL not in file_path:
                # Check if asset.file_path exists
                if os.path.exists(file_path) and not is_home_directory_or_drive(file_path):
                    file_path = util.resolve_path(file_path)
                    path_list.add(file_path)
                    path_list.real_files()
                else:
                    logger.debug("Unable to find extra directory asset: {}".format(asset.file_path))
    except Exception as e:
        logger.debug("Unable to load extra dir assets, error: {}".format(e))

    return path_list

def is_home_directory_or_drive(path):
    """
    Check if the given path is a home directory, or, if on Windows, a root drive.

    :param path: Path to check
    :return: True if the path is a home directory or a root drive (Windows only), False otherwise
    """
    try:
        scene = bpy.context.scene
        # Normalize the path for consistent comparisons
        path = os.path.normpath(path)
        # Check for home directory
        home_path = os.path.expanduser('~')
        home_path = os.path.normpath(home_path)
        # If path is a file, get its directory
        if os.path.isfile(path):
            path = os.path.dirname(path)

        # Normalize paths to remove trailing slashes for direct comparison
        path = path.rstrip("\\/")
        home_path = home_path.rstrip("\\/")

        # Check if the path is the home directory, considering extra slashes, etc
        if path.lower() == home_path.lower():
            print(f"Path {path} is home directory {home_path}")
            return True

        # For Windows, check if the path is a root drive
        if platform.system().lower().startswith('win'):
            # Check for root drives (e.g., "C:\", "E:\")
            if re.match(r"^[a-zA-Z]:\\?$", path):
                print(f"Path {path} is a root drive")
                return True

            # Checking if it's directly under a root drive (e.g., "C:\folder")
            # drive, rest = os.path.splitdrive(path)
            # if drive and (rest == "\\" or rest == "/"):
            #   return True

    except Exception as e:
        logger.debug("Unable to check if path is home directory or drive, error: {}".format(e))

    return False

def scan_assets():
    """
    Scan assets in the current Blender project and return a PathList containing their paths.

    :return: A PathList object containing the paths of scanned assets.
    """
    path_list = PathList()

    path_list.add(*scan_materials())
    path_list.add(*scan_objects())
    path_list.add(*scan_linked_libraries())
    path_list.add(*scan_objects_with_overrides())

    # Scan for Simulation Bake Directory
    path_list.add(*scan_simulation_bake_directory())

    # Scan for Alembic files
    path_list.add(*scan_for_alembic_files())
    # Scan for HDR files
    path_list.add(*scan_for_hdr_files())

    return path_list

def scan_materials():
    """
    Scan materials in the current Blender project and add their image paths to the PathList.

    :return: A PathList object containing image paths from materials with nodes.
    """
    path_list = PathList()
    try:
        if not bpy.data.materials:
            return path_list
        # Iterate through all materials in the scene
        for material in bpy.data.materials:
            if not material.use_nodes:
                continue
            for node in material.node_tree.nodes:
                if node.type == 'TEX_IMAGE' and node.image:
                    image_filepath = bpy.path.abspath(node.image.filepath)
                    # check if the image_filepath exists
                    if os.path.exists(image_filepath):
                        image_filepath = util.resolve_path(image_filepath)
                        path_list.add(image_filepath)
                        # path_list.real_files()
                    else:
                        logger.debug("Unable to find image_filepath: {}".format(image_filepath))
    except Exception as e:
        logger.debug("Unable to scan materials, error: {}".format(e))

    return path_list

def scan_objects():
    """
    Scan objects in the current Blender project and add image paths from materials with nodes to the PathList.

    :return: A PathList object containing image paths from materials in mesh objects.
    """
    path_list = PathList()

    try:
        if not bpy.data.objects:
            return path_list
        for obj in bpy.data.objects:
            if obj.type == 'MESH':
                for slot in obj.material_slots:
                    if not slot.material:
                        continue
                    if slot.material and slot.material.use_nodes:
                        for node in slot.material.node_tree.nodes:
                            if node.type == 'TEX_IMAGE' and node.image:
                                image_filepath = bpy.path.abspath(node.image.filepath)
                                # check if the image_filepath exists
                                if os.path.exists(image_filepath):
                                    image_filepath = util.resolve_path(image_filepath)
                                    path_list.add(image_filepath)
                                    # path_list.real_files()
                                else:
                                    logger.debug("Unable to find image_filepath: {}".format(image_filepath))
    except Exception as e:
        logger.debug("Unable to scan objects, error: {}".format(e))
    return path_list

def scan_linked_libraries():
    """
    Scan linked libraries in the current Blender project and add their paths to the PathList.

    :return: A PathList object containing paths of linked libraries.
    """
    path_list = PathList()

    try:
        if not bpy.data.libraries:
            return path_list
        for library in bpy.data.libraries:
            # Check if the library is linked or used in the scene
            if library.users > 0:
                library_filepath = bpy.path.abspath(library.filepath)
                # check if the library_filepath exists
                if os.path.exists(library_filepath):
                    library_filepath = util.resolve_path(library_filepath)
                    path_list.add(library_filepath)
                    # path_list.real_files()
                else:
                    logger.debug("Unable to find linked library: {}".format(library_filepath))
    except Exception as e:
        logger.debug("Unable to scan linked libraries, error: {}".format(e))
    return path_list

def scan_objects_with_overrides():
    """
    Scan objects with library overrides and add material library paths to the PathList.

    :return: A PathList object containing material library paths of objects with overrides.
    """
    path_list = PathList()

    try:
        if not bpy.context.scene.objects:
            return path_list
        for obj in bpy.context.scene.objects:
            if obj.is_library_indirect:
                for slot in obj.material_slots:
                    if not slot.material:
                        continue
                    material_filepath = bpy.path.abspath(slot.material.library.filepath)
                    # check if the material_filepath exists
                    if os.path.exists(material_filepath):
                        material_filepath = util.resolve_path(material_filepath)
                        path_list.add(material_filepath)
                        # path_list.real_files()
                    else:
                        logger.debug("Unable to find object with override: {}".format(material_filepath))
    except Exception as e:
        logger.debug("Unable to scan objects with overrides, error: {}".format(e))
    return path_list

def scan_simulation_bake_directory():
    """
    Scan for the Simulation Bake Directory in Geometry Nodes modifiers and add it to the PathList.
    Resolve relative paths to absolute paths.

    :return: A PathList object containing the Simulation Bake Directory path, if found and resolved.
    """
    path_list = PathList()
    try:
        # Iterate through all objects in the scene
        for obj in bpy.data.objects:
            # Check if the object has modifiers
            for modifier in obj.modifiers:
                # Check if the modifier is a GeometryNodes modifier and has a simulation_bake_directory attribute
                if modifier.type == 'NODES' and hasattr(modifier, 'simulation_bake_directory'):
                    # Get the directory path and resolve it to an absolute path
                    bake_directory_path = modifier.simulation_bake_directory
                    print("Bake directory path: ", bake_directory_path)
                    # Check if the bake_directory_path is a valid directory on the file system
                    if not os.path.isdir(bake_directory_path):

                        # Remove '//' from head of bake_directory_path
                        if bake_directory_path.startswith('//'):
                            bake_directory_path = bake_directory_path[2:]
                        # Remove '\' from the tail of bake_directory_path
                        if bake_directory_path.endswith('\\'):
                            bake_directory_path = bake_directory_path[:-1]
                        # Get the path where the Blender file is located
                        blend_file_path = bpy.data.filepath
                        # Resolve the bake_directory_path to an absolute path
                        bake_directory_path = os.path.join(os.path.dirname(blend_file_path), bake_directory_path)
                        print("Bake directory path after resolving: ", bake_directory_path)

                    # Check if the bake_directory_path is a valid directory
                    if os.path.isdir(bake_directory_path):
                        bake_directory_path = util.resolve_path(bake_directory_path)
                        path_list.add(bake_directory_path)
    except Exception as e:
        logger.debug(f"Unable to scan for Simulation Bake Directory, error: {e}")

    return path_list

def scan_for_alembic_files():
    """
        Scans the current Blender project for objects utilizing Alembic (.abc) files, particularly through the Mesh Sequence Cache modifier, which is commonly used for importing complex animations and simulations from external software.

        This function iterates over all objects in the project, checks each object for the presence of a Mesh Sequence Cache modifier, and extracts the file path of the Alembic file if present. It ensures that the file path is absolute and valid before adding it to the returned list of paths.

        Note:
        - The function assumes Alembic files are primarily used with the Mesh Sequence Cache modifier.
        - Paths are cleaned and normalized using `util.resolve_path` to ensure consistency.

        Returns:
            PathList: A collection of cleaned and absolute paths to Alembic (.abc) files used in the project. The PathList object facilitates further operations on these paths.
        """
    path_list = PathList()
    try:
        for obj in bpy.data.objects:
            # Assuming Alembic files could be referenced in object modifiers, for example, as a Mesh Sequence Cache
            for modifier in obj.modifiers:
                if modifier.type == 'MESH_SEQUENCE_CACHE':
                    abc_file_path = bpy.path.abspath(modifier.cache_file.filepath)
                    if os.path.exists(abc_file_path):
                        abc_file_path = util.resolve_path(abc_file_path)
                        path_list.add(abc_file_path)
    except Exception as e:
        logger.debug(f"Unable to scan for Alembic files, error: {e}")
    return path_list

def scan_for_hdr_files():
    """
    Scans the current Blender project for HDR (High Dynamic Range) image files used as environment textures. Environment textures are typically used for lighting and background in renders and are found in the world's node tree as environment textures.

    This function searches through the nodes in the world's node tree for the 'TEX_ENVIRONMENT' node type, which is indicative of an environment texture. When an HDR image is found, its file path is extracted, verified for existence, and then added to a list of paths.

    Note:
    - The function specifically looks for 'TEX_ENVIRONMENT' nodes within the world's node tree and checks if the associated image's file format is HDR.
    - Paths are cleaned and normalized using `util.resolve_path` to ensure consistency and prevent issues with relative paths.

    Returns:
        PathList: A collection of cleaned and absolute paths to HDR files used as environment textures in the project. The PathList object enables efficient management and utilization of these paths.
    """
    path_list = PathList()
    try:
        if bpy.context.scene.world and bpy.context.scene.world.node_tree:
            for node in bpy.context.scene.world.node_tree.nodes:
                if node.type == 'TEX_ENVIRONMENT' and node.image and node.image.file_format in ['HDR']:
                    hdr_file_path = bpy.path.abspath(node.image.filepath)
                    if os.path.exists(hdr_file_path):
                        hdr_file_path = util.resolve_path(hdr_file_path)
                        path_list.add(hdr_file_path)
    except Exception as e:
        logger.debug(f"Unable to scan for HDR files, error: {e}")
    return path_list