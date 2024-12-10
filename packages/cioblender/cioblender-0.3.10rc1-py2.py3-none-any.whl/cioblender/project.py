"""Manage project menu selection."""


from ciocore import data as coredata


def populate_menu(node):
    """Populate project menu.

    Get a list of items from the shared data_block where they have been cached. The menu needs a list in the format:
    [(key, value, ""), ...]

    Since projects are simply a list of names, the key (k) and value (v) can be the same.

    Args:
        node: The current node.

    Returns:
        list: A list of project items in the format [(key, value, ""), ...].
    """

    # if not connected, return a default value

    if not coredata.valid():
        return [("not_connected", "-- Not Connected --", "")]

    # if connected, get the list of projects
    project_data = coredata.data()["projects"]

    # if there are no projects, return a default value
    if not project_data:
        return [("no_projects", "-- No Projects --", "")]
    else:
        # Create a dictionary of projects
        blender_projects = {}
        # For each project in the project_data, if the project is not in the blender_projects dictionary,
        # add it to the dictionary
        for project in project_data:
            if project not in blender_projects:
                blender_projects[project] = (project, project, "")
        # Return the list of projects in reverse order, as Blender sorts the list in reverse order
        return list(blender_projects.values())[::-1]


def resolve_payload(**kwargs):
    """
        Resolve the payload for the project selection.

        Args:
            kwargs: A dictionary of keyword arguments.

        Returns:
            dict: A dictionary containing the selected project in the "project" field.
        """
    return {"project": kwargs.get("project")}
