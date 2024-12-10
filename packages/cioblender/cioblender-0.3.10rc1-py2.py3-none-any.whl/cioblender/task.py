import os
from cioblender import frames, util

RENDER_DICT = {
    "Cycles": "CYCLES",
    "Eevee": "BLENDER_EEVEE",
    "Redshift": "REDSHIFT",
}


def get_task_template(**kwargs):
    """
    Constructs a command string to render a project using Blender, based on various rendering settings and system configurations.
    The command includes parameters for file paths, output settings, render engine, and additional optional flags such as resolution and sampling.

    Args:
        **kwargs (dict): A dictionary of keyword arguments containing rendering and system settings. Relevant keys include:
            - first (int): The starting frame for rendering.
            - last (int): The ending frame for rendering.
            - step (int): The step count between frames to render.
            - output_folder (str): The directory path where the rendered files will be stored.
            - blender_filename (str): The name of the Blender file to render.
            - render_software (str): The rendering engine to use, defaults to 'CYCLES' if not specified.
            - instance_type (str): The type of instance to render on, if applicable.
            - machine_type (str): The machine type designation for rendering.
            - new_resolution_x (int): The horizontal resolution for rendering.
            - new_resolution_y (int): The vertical resolution for rendering.
            - camera_override (str): Specific camera to use for rendering.
            - update_camera_checkbox (bool): Flag to update camera settings, defaults to False.
            - view_layers_checkbox (bool): Flag to toggle view layers, defaults to False.
            - samples_override (int): Override for the number of samples per pixel.
            - factory_startup (bool): Whether to start Blender with factory settings.
            - disable_audio (bool): Whether to disable audio during rendering.

    Returns:
        str: A fully formed Blender command ready to be executed for rendering tasks, incorporating the provided configurations.

    Note:
        The function handles path normalization and error checking internally, logging any issues encountered during the command construction.
    """
    first = kwargs.get("first", 1)
    last = kwargs.get("last", 1)
    step = kwargs.get("step", 1)

    render_filepath = get_render_file(kwargs)
    render_filepath = util.clean_and_strip_path(render_filepath)
    render_filepath = f'"{render_filepath}"'

    command_scene_path = render_filepath

    output_folder = kwargs.get("output_folder", None)
    output_folder = util.clean_and_strip_path(output_folder)
    blender_filename = kwargs.get("blender_filename", None)
    if blender_filename:
        blender_filename = blender_filename.split(".")[0]

    output_path = os.path.join(output_folder, blender_filename + "_").replace("\\", "/")
    output_path = f'"{output_path}"'

    render_software = kwargs.get("render_software", None)
    render_software = RENDER_DICT.get(render_software, "CYCLES")
    render_software = f'"{render_software}"'

    cioblender_path = os.path.dirname(__file__)

    script_path = "{}/scripts/brender.py".format(cioblender_path)
    cio_dir = os.getenv('CIO_DIR')
    if cio_dir:
        script_path = "{}/cioblender/scripts/brender.py".format(cio_dir)

    script_path = util.clean_and_strip_path(script_path)
    script_path = f'"{script_path}"'

    instance_type = kwargs.get("instance_type", None)
    machine_type = kwargs.get("machine_type", None)

    resolution_x = kwargs.get("new_resolution_x", None)
    resolution_y = kwargs.get("new_resolution_y", None)

    camera = kwargs.get("camera_override", None)
    camera = f'"{camera}"'
    update_camera_checkbox = kwargs.get("update_camera_checkbox", False)
    view_layers_checkbox = kwargs.get("view_layers_checkbox", False)

    samples = kwargs.get("samples_override", None)
    extra_args = ""
    if resolution_x:
        extra_args += f" --resolution_x={resolution_x}"
    if resolution_y:
        extra_args += f" --resolution_y={resolution_y}"
    if camera:
        extra_args += f" --camera={camera}"
    if samples:
        extra_args += f" --samples={samples}"
    if update_camera_checkbox:
        extra_args += " --update_camera_checkbox=UPDATE_CAMERA_ON"
    else:
        extra_args += " --update_camera_checkbox=UPDATE_CAMERA_OFF"
    if view_layers_checkbox:
        extra_args += " --view_layers_checkbox=VIEW_LAYERS_ON"
    else:
        extra_args += " --view_layers_checkbox=VIEW_LAYERS_OFF"

    factory_startup = kwargs.get("factory_startup", False)
    disable_audio = kwargs.get("disable_audio", False)

    # Additional command options for background_mode, factory_startup, and disable_audio
    additional_cmds = "-b"

    if factory_startup:
        additional_cmds += " --factory-startup"
    if disable_audio:
        additional_cmds += " -noaudio"

    # Constructing the command using the modern format style
    cmd = f"blender {additional_cmds} {command_scene_path} -P {script_path} -E {render_software} --render-output {output_path} -s {first} -e {last} -- render_device={instance_type} --machine_type={machine_type} {extra_args}"

    return cmd


def get_render_file(kwargs):
    """
    Save the current Blender file.

    Args:
        kwargs (dict): A dictionary of keyword arguments for task configuration.
    """
    render_filepath = None
    try:
        blender_filepath = kwargs.get("blender_filepath", None)
        render_filepath = blender_filepath

    except Exception as e:
        print("Error in saving render file {}, error: {}".format(render_filepath, e))
    return render_filepath


def resolve_payload(**kwargs):
    """
    Resolve the task_data field for the payload.

    If we are in sim mode, we emit one task.

    Args:
        kwargs (dict): A dictionary of keyword arguments for payload resolution.

    Returns:
        dict: A dictionary containing the task_data field for the payload.
    """

    tasks = []
    frame_info_dict = frames.set_frame_info_panel(**kwargs)
    kwargs["chunk_size"] = frame_info_dict.get("resolved_chunk_size")

    sequence = frames.main_frame_sequence(**kwargs)
    chunks = sequence.chunks()

    task_display_limit = kwargs.get("task_display_limit", False)
    display_tasks_count = len(chunks)
    if task_display_limit:
        display_tasks_count = kwargs.get("display_tasks", 1)
    # print("task_display_limit: {}".format(task_display_limit))
    # print("display_tasks_count: {}".format(display_tasks_count))
    # Get the scout sequence, if any.
    for i, chunk in enumerate(chunks):
        if task_display_limit:
            if i >= display_tasks_count:
                break
        # Get the frame range for this chunk.
        kwargs["first"] = chunk.start
        kwargs["last"] = chunk.end
        kwargs["step"] = chunk.step
        # Get the task template.
        cmd = get_task_template(**kwargs)

        tasks.append({"command": cmd, "frames": str(chunk)})


    return {"tasks_data": tasks}