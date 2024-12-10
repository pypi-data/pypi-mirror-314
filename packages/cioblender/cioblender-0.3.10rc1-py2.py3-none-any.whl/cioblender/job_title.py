

def resolve_payload(**kwargs):
    """
    Resolve a job title by stripping leading and trailing whitespace.

    Args:
        **kwargs: Keyword arguments.

    Keyword Args:
        job_title (str): The job title to be resolved.

    Returns:
        dict: A dictionary containing the Blender resolved job title.

    Example:
        {'job_title': 'Blender Linux Render'}

    """
    title = kwargs.get("job_title").strip()
    return {"job_title": title}
