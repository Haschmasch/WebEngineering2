import json
import shutil
from fastapi import UploadFile
from os import listdir
from os.path import isfile, join


def read_json(path):
    with open(path, 'r', encoding='utf-8') as json_file:
        return json.load(json_file)


def write_json(path, json_dict):
    with open(path, 'w', encoding='utf-8') as json_file:
        json.dump(json_dict, json_file, ensure_ascii=False)


def write_text_file(path, text):
    with open(path, 'w', encoding='utf-8') as file:
        file.write(text)


def read_text_file(path):
    with open(path, 'r', encoding='utf-8') as file:
        return file.readlines()


def write_uploaded_file(path, uploaded_file: UploadFile):
    try:
        with open(path, "wb+") as buffer:
            shutil.copyfileobj(uploaded_file.file, buffer)
    finally:
        uploaded_file.file.close()


def remove_directory(path):
    if path.isdir(path):
        shutil.rmtree(path)



def get_file_paths(directory):
    return [f for f in listdir(directory) if isfile(join(directory, f))]
