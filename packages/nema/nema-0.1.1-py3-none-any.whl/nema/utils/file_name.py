import uuid


def generate_random_file_name(extension: str):

    return f"{uuid.uuid4()}.{extension}"
