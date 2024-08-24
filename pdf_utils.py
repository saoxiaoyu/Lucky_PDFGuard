import os
from os.path import isdir, join

def create_directory(directory_path):
    if not isdir(directory_path):
        os.mkdir(directory_path)

def get_pdf_files_in_directory(directory_path):
    return [join(directory_path, file) for file in os.listdir(directory_path) if file.endswith('.pdf')]

def remove_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)
