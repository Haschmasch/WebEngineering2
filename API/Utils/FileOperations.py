"""
Helper file for basic file operations.
"""

import json
import os
import shutil
from fastapi import UploadFile
from os.path import isfile, isabs, abspath
from pathlib import Path
from PIL import Image, ImageOps


def read_json(path):
    """
    Reads a json file from the specified path.
    :param path: The path including the file name.
    :return: The json as a dict
    """
    path = try_resolve_relative_path(path)
    with open(path, 'r', encoding='utf-8') as json_file:
        return json.load(json_file)


def write_json(path, json_dict):
    """
    Writes a json file to the specified path.
    :param path: The path including the file name.
    :param json_dict: The dict that should be written.
    """
    resolved_path = mkdir_and_resolve_relative_path(path)
    with open(resolved_path, 'w', encoding='utf-8') as json_file:
        json.dump(json_dict, json_file, ensure_ascii=False)


def write_text_file(path, text):
    """
    Writes a text file to the specified path.
    :param path: The path including the file name.
    :param text: The text that should be written.
    """
    resolved_path = mkdir_and_resolve_relative_path(path)
    with open(resolved_path, 'w', encoding='utf-8') as file:
        file.write(text)


def read_text_file(path):
    """
    Reads a text file from the specified path.
    :param path: The path including the file name.
    :return: The text as string.
    """
    resolved_path = try_resolve_relative_path(path)
    with open(resolved_path, 'r', encoding='utf-8') as file:
        return file.readlines()


def write_uploaded_file(path, uploaded_file: UploadFile):
    """
    Writes an uploaded file from the specified path.
    :param path: The path including the file name.
    :param uploaded_file: The file to be written. This is a fastapi class.
    """
    resolved_path = mkdir_and_resolve_relative_path(path)
    try:
        with open(resolved_path, "wb+") as buffer:
            shutil.copyfileobj(uploaded_file.file, buffer)
    finally:
        uploaded_file.file.close()


def remove_file(path):
    """
    Deletes a file from the specified path.
    Throws an error if the path was not found.
    :param path: The path including the file name.
    """
    resolved_path = try_resolve_relative_path(path)
    if isfile(resolved_path):
        os.remove(resolved_path)
    else:
        raise FileNotFoundError(f"File to delete not found")


# TODO: Maybe remove parent dir, when the specified dir is the only dir under the parent. This can lead to
#  emtpy directories otherwise.
def remove_directory(directory):
    """
    Deletes a directory including all files in that directory.
    Throws an error if the directory was not found.
    :param directory: The directory to be deleted.
    """
    resolved_path = try_resolve_relative_path(directory)
    if os.path.isdir(resolved_path):
        shutil.rmtree(resolved_path)
    else:
        raise FileNotFoundError(f"Directory to delete not found")


def create_thumbnail(path):
    """
    Creates a thumbnail image from the specified image path
    :param path: The path including the file name.
    """
    resolved_path = mkdir_and_resolve_relative_path(path)
    thumbnail_path = get_thumbnail_path(resolved_path)
    # Create thumbnail if the source file exists, and it does not exist
    if isfile(resolved_path) and not isfile(thumbnail_path):
        image = Image.open(resolved_path)
        image.thumbnail((256, 256))
        transposed_img = ImageOps.exif_transpose(image)
        transposed_img.save(thumbnail_path)

    # Delete all other thumbnails in the directory
    files = get_file_paths(os.path.dirname(resolved_path))
    for file in files:
        if file != thumbnail_path and "_thumbnail" in file:
            remove_file(file)


def get_thumbnail_path(directory):
    """
    Gets the thumbnail image from a path.
    :param directory: The directory of the image.
    :return: The full path with the name og the image.
    """
    resolved_path = try_resolve_relative_path(directory)
    filename, file_extension = os.path.splitext(resolved_path)
    return f"{filename}_thumbnail{file_extension}"


def get_file_paths(directory):
    """
    Get the paths of all files from a directory.
    :param directory: The directory of the files.
    :return: A list of strings for all image paths.
    """
    resolved_dir = try_resolve_relative_path(directory)
    return [os.path.join(dirpath, f) for (dirpath, dirnames, filenames) in os.walk(resolved_dir) for f in filenames]


def mkdir_and_resolve_relative_path(path):
    """
    This creates the directories that leads to the path and resolves relative paths.
    :param path: The path to be created and resolved.
    :return: The resolved path.
    """
    resolved_path = try_resolve_relative_path(path)
    Path(Path(resolved_path).parent).mkdir(parents=True, exist_ok=True)
    return resolved_path


def try_resolve_relative_path(path):
    """
    Tries go get the absolute path from a relative path.
    :param path: The path to be resolved.
    :return: The resolved path.
    """
    resolved_path = path
    if not isabs(path):
        resolved_path = abspath(path)
    return resolved_path


def get_chat_file_path(chat_id, chat_root_directory):
    """
    Gets the path to a chat file (json).
    :param chat_id: The id of the chat.
    :param chat_root_directory: The root directory of the chat.
    :return: The complete path with the name of the chat file.
    """
    filename = f"{chat_id}.json"
    filepath = os.path.join(chat_root_directory, filename)
    return filepath
