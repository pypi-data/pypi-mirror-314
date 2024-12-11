
from cioblender import (
    job_title,
    project,
    instances,
    software,
    environment,
    driver,
    frames,
    task,
    assets,
    miscellaneous,
)


def resolve_payload(task_display_limit=False, **kwargs):
    """
    Resolve the payload for various components of a Blender job.

    This function combines payloads from different modules responsible for job components.
    The individual payloads for job title, project, software, miscellaneous data, instances, driver, environment,
    assets, frames, and task are collected and merged into a single payload dictionary.

    :param kwargs: A dictionary of keyword arguments that may be required for resolving payloads.
    :return: A dictionary containing the merged payload for all components.
    """

    payload = {}
    payload.update(job_title.resolve_payload(**kwargs))
    payload.update(project.resolve_payload(**kwargs))
    payload.update(software.resolve_payload(**kwargs))
    payload.update(miscellaneous.resolve_payload(**kwargs))
    payload.update(instances.resolve_payload(**kwargs))
    payload.update(driver.resolve_payload(**kwargs))
    payload.update(environment.resolve_payload(**kwargs))
    payload.update(assets.resolve_payload(**kwargs))
    payload.update(frames.resolve_payload(**kwargs))
    payload.update(task.resolve_payload(**kwargs))

    return payload
