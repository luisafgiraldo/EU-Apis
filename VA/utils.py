import base64
import os


def transformer(image_path):
    """
    Transforms a file into its Base64 representation if it is in an allowed format.

    Args:
        image_path (str): Path to the file to be transformed.

    Returns:
        str: Base64-encoded string of the file.
        None: If the file format is not allowed or the file does not exist.
    """

    # Formatos permitidos
    allowed_file_formats = [
        ".jpg",
        ".jpeg",
        ".png",
        ".heic",
        ".webp",
        ".avif",
        ".mp4",
        ".mov",
    ]

    # Verificar si el archivo existe
    if not os.path.isfile(image_path):
        print("Error: File does not exist.")
        return None

    # Verificar formato de imagen
    if not any(image_path.lower().endswith(ext) for ext in allowed_file_formats):
        print(
            f"Invalid file format. Allowed formats are: {', '.join(allowed_file_formats)}"
        )
        return None

    # Codificar la imagen en Base64
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")
    except Exception as e:
        print(f"Error while reading the file: {e}")
        return None


def first_file_finder(image_dir, allowed_extensions=None):
    """
    Finds the first file in the specified directory matching allowed extensions.

    Args:
        image_dir (str): The path to the directory.
        allowed_extensions (list, optional): List of allowed file extensions.

    Returns:
        str: The full path to the first valid file found.
    """
    if allowed_extensions is None:
        allowed_extensions = [".jpg", ".jpeg", ".png", "mp4", "mov"]

    try:
        image_files = [
            f for f in os.listdir(image_dir)
            if os.path.isfile(os.path.join(image_dir, f))
            and not f.startswith(".")
            and any(f.lower().endswith(ext) for ext in allowed_extensions)
        ]
        if not image_files:
            print(f"No valid files found in {image_dir} with extensions: {allowed_extensions}")
            return None
        return os.path.join(image_dir, image_files[0])
    except FileNotFoundError:
        print(f"Directory not found: {image_dir}")
        return None




def union_path(param1, param2):
    """
    Joins two path components into a single path.

    Args:
        param1 (str): The first part of the path.
        param2 (str): The second part of the path.

    Returns:
        str: The joined path.
        None: If any of the parameters is invalid.
    """
    if not isinstance(param1, str) or not isinstance(param2, str):
        print("Both parameters must be strings.")
        return None

    return os.path.join(param1, param2)
