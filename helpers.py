import os

def read_file(file_path):
    with open(file_path, "r") as file:
        lines = file.readlines()
    return lines

def update_file(file_path, lines):
    with open(file_path, "w") as file:
        file.writelines(lines)