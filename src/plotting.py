import os


def output_file(output_dir, *path_parts):
    """
    Build an output file path and ensure its parent directory exists.
    """
    filename = os.path.join(output_dir, *path_parts)
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    return filename
