import json
import os
import shutil
from fastapi import UploadFile
from os import listdir
from os.path import isfile, join, isabs, abspath
from pathlib import Path
from PIL import Image


def read_json(file_name):
    path = get_file_path(file_name)
    with open(path, 'r', encoding='utf-8') as json_file:
        return json.load(json_file)


def write_json(path, json_dict):
    resolved_path = mkdir_and_resolve_relative_path(path)
    with open(resolved_path, 'w', encoding='utf-8') as json_file:
        json.dump(json_dict, json_file, ensure_ascii=False)


def write_text_file(path, text):
    resolved_path = mkdir_and_resolve_relative_path(path)
    with open(resolved_path, 'w', encoding='utf-8') as file:
        file.write(text)


def read_text_file(path):
    resolved_path = try_resolve_relative_path(path)
    with open(resolved_path, 'r', encoding='utf-8') as file:
        return file.readlines()


def write_uploaded_file(path, uploaded_file: UploadFile):
    resolved_path = mkdir_and_resolve_relative_path(path)
    try:
        with open(resolved_path, "wb+") as buffer:
            shutil.copyfileobj(uploaded_file.file, buffer)
    finally:
        uploaded_file.file.close()


def remove_file(path):
    resolved_path = try_resolve_relative_path(path)
    if isfile(resolved_path):
        os.remove(resolved_path)


# TODO: Maybe remove parent dir, when the specified dir is the only dir under the parent. This can lead to
#  emtpy directories otherwise.
def remove_directory(path):
    resolved_path = try_resolve_relative_path(path)
    if os.path.isdir(resolved_path):
        shutil.rmtree(resolved_path)


def create_thumbnail(path):
    resolved_path = mkdir_and_resolve_relative_path(path)
    thumbnail_path = get_thumbnail_path(resolved_path)
    # Create thumbnail if the source file exists, and it does not exist
    if isfile(resolved_path) and not isfile(thumbnail_path):
        image = Image.open(resolved_path)
        image.thumbnail((256, 256))
        image.save(thumbnail_path)

    # Delete all other thumbnails in the directory
    files = get_file_paths(os.path.dirname(path))
    t_name, t_directory = os.path.split(thumbnail_path)
    for file in files:
        name, directory = os.path.split(file)
        if name is not t_name and "_thumbnail" in file:
            remove_file(file)


def get_thumbnail_path(path):
    resolved_path = try_resolve_relative_path(path)
    filename, file_extension = os.path.splitext(resolved_path)
    return f"{filename}_thumbnail.{file_extension}"


def get_file_paths(directory):
    resolved_dir = try_resolve_relative_path(directory)
    return [f for f in listdir(resolved_dir) if isfile(join(resolved_dir, f))]


def mkdir_and_resolve_relative_path(path):
    resolved_path = try_resolve_relative_path(path)
    Path(Path(resolved_path).parent).mkdir(parents=True, exist_ok=True)
    return resolved_path


def try_resolve_relative_path(path):
    resolved_path = path
    if not isabs(path):
        resolved_path = abspath(path)
    return resolved_path

def get_file_path(file_name):
    dir_path = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(dir_path, file_name)
    return path


