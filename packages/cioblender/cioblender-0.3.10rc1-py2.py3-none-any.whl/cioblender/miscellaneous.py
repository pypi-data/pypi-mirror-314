import bpy
def resolve_payload(**kwargs):
    """
    Resolve the notifications field for the payload.

    This function sets the 'local_upload' field to True, indicating that local uploads are enabled.

    :param kwargs: A dictionary of keyword arguments (not used).
    :return: A dictionary containing the resolved payload with 'local_upload' set to True.
    """
    local_upload = True
    result = {}
    try:
        scene = bpy.context.scene
        use_upload_daemon = scene.use_upload_daemon
        local_upload = not use_upload_daemon
        result["local_upload"] = local_upload
        location = scene.location_tag
        if location:
            result["location"] = location
    except Exception as e:
        print(f"Error in resolve_payload: {e}")

    return result