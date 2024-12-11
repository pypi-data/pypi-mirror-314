from pathlib import Path as MyPath


def clean_and_strip_path(current_path):
    """
    Cleans and normalizes the given path string by resolving to an absolute path and stripping
    any drive letters if present. It converts all backslashes to forward slashes for consistency.

    Args:
    current_path (str): The path string that needs to be cleaned and normalized.

    Returns:
    str: The cleaned and normalized path as a string.

    Raises:
    Exception: If the path resolution fails, it catches the exception and prints an error message.
    """
    cleaned_path = current_path
    # convert the path to a PathList
    try:
        if current_path:
            current_path = current_path.replace("\\", "/")
            current_path = MyPath(current_path).resolve(strict=True)
            current_path = str(current_path)
            if ":" in current_path:
                current_path = current_path.split(":")[1]
            cleaned_path = current_path.replace("\\", "/")
    except Exception as e:
        print("Unable to clean and strip path: {} error: {}", current_path, e)
    return cleaned_path

def resolve_path(filepath):
    """
    Resolves the given file path to its absolute form and ensures the path exists.
    It converts all backslashes to forward slashes for consistency.

    Args:
    filepath (str): The file path that needs to be resolved.

    Returns:
    str: The resolved file path as a string.

    Raises:
    Exception: If the path resolution fails, it catches the exception and prints an error message.
    """
    try:
        filepath = MyPath(filepath).resolve(strict=True)
        filepath = str(filepath)
        filepath = filepath.replace("\\", "/")
    except Exception as e:
        print("Unable to resolve path: {} error: {}", filepath, e)
    return filepath
