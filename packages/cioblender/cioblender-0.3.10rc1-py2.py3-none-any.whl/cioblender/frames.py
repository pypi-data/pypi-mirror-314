
import re

from cioseq.sequence import Sequence
import math

AUTO_RX = re.compile(r"^auto[, :]+(\d+)$")
FML_RX = re.compile(r"^fml[, :]+(\d+)$")

MAX_TASKS = 800


def main_frame_sequence(**kwargs):
    """
    Generate a Sequence containing the current chosen frames.

    This function generates a sequence of frames based on the provided frame specification and chunk size.

    :param kwargs: A dictionary of keyword arguments that may include 'frame_range' and 'chunk_size'.
    :return: A Sequence containing the chosen frames.
    """
    chunk_size = kwargs.get("chunk_size")
    use_custom_range = kwargs.get("use_custom_range")
    if use_custom_range:
        spec = kwargs.get("frame_range")
    else:
        spec = kwargs.get("scene_frame_range")
    if not spec:
        return Sequence.create(1, 1)
    else:
        return Sequence.create(spec, chunk_size=chunk_size, chunk_strategy="progressions")


def scout_frame_sequence(main_sequence, **kwargs):
    """
    Generate a Sequence containing scout frames.

    This function generates a sequence of scout frames, which can be generated from a specified pattern
    or by subsampling the main frame sequence.

    :param main_sequence: The main frame sequence.
    :param kwargs: A dictionary of keyword arguments that may include 'scout_frames' and 'use_scout_frames'.
    :return: A Sequence containing the scout frames or None.
    """
    if not kwargs.get("use_scout_frames"):
        return

    scout_spec = kwargs.get("scout_frames")

    match = AUTO_RX.match(scout_spec)
    if match:
        samples = int(match.group(1))
        return main_sequence.subsample(samples)
    else:
        match = FML_RX.match(scout_spec)
        if match:
            samples = int(match.group(1))
            return main_sequence.calc_fml(samples)

    try:
        return Sequence.create(scout_spec).intersection(main_sequence)

    except:
        pass


def resolve_payload(**kwargs):
    """
    Resolve the payload for scout frames.

    This function calculates and returns the scout frames if the 'use_scout_frames' option is enabled.

    :param kwargs: A dictionary of keyword arguments that may include 'use_scout_frames'.
    :return: A dictionary containing the scout frames or an empty dictionary.
    """
    use_scout_frames = kwargs.get("use_scout_frames")
    if not use_scout_frames:
        return {}

    main_seq = main_frame_sequence(**kwargs)
    scout_sequence = scout_frame_sequence(main_seq, **kwargs)
    if scout_sequence:
        return {"scout_frames": ",".join([str(f) for f in scout_sequence])}
    return {}

def set_frame_info_panel(**kwargs):
    """
    Update fields in the Frames Info panel that are driven by frames related settings.
    """
    frame_info_dict = {}

    chunk_size = kwargs.get("chunk_size")
    frame_range = kwargs.get("frame_range")
    main_seq = main_frame_sequence(**kwargs)

    task_count = main_seq.chunk_count()
    frame_count = len(main_seq)
    frame_info_dict["resolved_chunk_size"] = chunk_size
    resolved_chunk_size = cap_chunk_count(task_count, frame_count, chunk_size)
    if resolved_chunk_size > chunk_size:
        frame_info_dict["resolved_chunk_size"] = resolved_chunk_size
        kwargs["chunk_size"] = resolved_chunk_size
        main_seq = main_frame_sequence(**kwargs)
        task_count = main_seq.chunk_count()
        frame_count = len(main_seq)

    scout_seq = scout_frame_sequence(main_seq, **kwargs)

    frame_info_dict["frame_count"] = frame_count
    frame_info_dict["task_count"] = task_count
    frame_info_dict["scout_frame_spec"] = "No scout frames. All frames will be started."

    if scout_seq:
        scout_chunks = main_seq.intersecting_chunks(scout_seq)
        # if there are no intersecting chunks, there are no scout frames, which means all frames will start.
        if scout_chunks:
            scout_tasks_sequence = Sequence.create(",".join(str(chunk) for chunk in scout_chunks))
            frame_info_dict["scout_frame_count"] = len(scout_tasks_sequence)
            frame_info_dict["scout_task_count"] = len(scout_chunks)
            frame_info_dict["scout_frame_spec"] = str(scout_seq)

    return frame_info_dict


def cap_chunk_count(task_count, frame_count, chunk_size):
    """Cap the number of chunks to a max value.

    This is useful for limiting the number of chunks to a reasonable
    number, e.g. for a render farm.
    """
    if task_count > MAX_TASKS:
        return math.ceil(frame_count / MAX_TASKS)

    return chunk_size

def get_resolved_chunk_size(**kwargs):
    """
    Get the resolved chunk size for the current node.
    """
    chunk_size = kwargs.get("chunk_size")
    main_seq = main_frame_sequence(**kwargs)
    frame_count = len(main_seq)
    task_count = main_seq.chunk_count()

    resolved_chunk_size = cap_chunk_count(task_count, frame_count, chunk_size)
    if resolved_chunk_size >= chunk_size:
        return resolved_chunk_size

    return chunk_size



