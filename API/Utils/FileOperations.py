import json
import os
import shutil
from fastapi import UploadFile
from os import listdir
from os.path import isfile, join, isabs, abspath
from pathlib import Path


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


def remove_directory(path):
    resolved_path = try_resolve_relative_path(path)
    if path.isdir(resolved_path):
        shutil.rmtree(resolved_path)


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


