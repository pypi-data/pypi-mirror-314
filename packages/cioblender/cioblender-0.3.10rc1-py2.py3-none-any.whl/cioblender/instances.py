"""Manage instance_type menu."""

from ciocore import data as coredata

def populate_menu(family):
    """
    Populate the instance type menu.

    This function populates the menu with instance types based on the provided family.

    :param family: The family of instance types (e.g., 'cpu' or 'gpu').
    :return: A list of tuples containing instance type names and descriptions.
    """

    if not coredata.valid():
        return [("not_connected", "-- Not Connected --", "")]

    # if connected, get the list of instance types
    instance_data = get_instance_types(family)

    # if there are no instance types, return a default value
    if not instance_data:
        return [("no_instances", "-- No instances --", "")]
    else:
        instance_list = []
        # For each item in the instance_data, add it to the instance_list as a tuple
        for item in sorted(instance_data, key=lambda k: (k['cores'], k['memory'])):
            instance_list.append((item["name"], item["description"], ""))
        # Return the instance_list
        return instance_list


def get_instance_types(family):
    """
    Get a list of instance types based on the provided family.

    :param family: The family of instance types (e.g., 'cpu' or 'gpu').
    :return: A list of instance types.
    """

    instance_type = str(family).lower() if family else "gpu"  # Set default family to "cpu"
    instances = coredata.data()["instance_types"]
    if instances:
        instances = instances.instance_types.values()
        return [item for item in instances if is_family(item, instance_type)]
    else:
        return []


def is_family(item, family):
    """
    Check if an instance type belongs to the specified family.

    :param item: The instance type item.
    :param family: The family of instance types (e.g., 'cpu' or 'gpu').
    :return: True if the instance type belongs to the specified family, otherwise False.
    """
    return ((family == "gpu") and item.get("gpu")) or ((family == "cpu") and not item.get("gpu"))


def resolve_payload(**kwargs):
    """
    Resolve the payload for instance type selection.

    This function prepares the payload for the selected instance type, preemptible status, and retries.

    :param kwargs: A dictionary of keyword arguments that may include 'machine_type', 'preemptible', and 'preemptible_retries'.
    :return: A dictionary containing the resolved payload.
    """

    instance_type = kwargs.get("machine_type")
    preemptible = kwargs.get("preemptible")
    retries = kwargs.get("preemptible_retries")
    result = {
        "instance_type": instance_type,
        "force": False,
        "preemptible": [False, True][preemptible]
    }

    if retries > 0 and preemptible:
        result["autoretry_policy"] = {"preempted": {"max_retries": retries}}

    return result

