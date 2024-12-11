import uuid
import os


__all__ = [
    "get_support_file_upload_path",
]


def get_unique_filename(filename: str):
    extension = os.path.splitext(filename)[1]
    return f"{str(uuid.uuid4())}{extension}"


def get_file_upload_path(
    filename: str,
    instance=None,
    filename_prefix: str = None,
    dir_name: str = None,
    unique: bool = True,
    user_file: bool = False,
):
    if unique:
        path = get_unique_filename(filename)
    else:
        path = filename

    if filename_prefix:
        path = filename_prefix + "_" + path

    if dir_name:
        if user_file and getattr(instance, "user", None):
            dir_name += f"/{instance.user.id}"
        path = f"{dir_name}/{path}"

    return path


def get_support_file_upload_path(instance, filename: str) -> str:
    return get_file_upload_path(filename=filename, dir_name="base_support")


def get_email_notification_file_upload_path(instance, filename):
    return get_file_upload_path(
        instance=instance, filename=filename, dir_name="email_notification_files", user_file=True
    )
