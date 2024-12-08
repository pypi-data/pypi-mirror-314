import os
import shutil

def get_file_list(directory):
    file_list = []
    for root, _, files in os.walk(directory):
        for file in files:
            files.append(os.path.join(root, file))
    return file_list

def get_dir_list(directory, relative=False):
    dir_list = []
    for root, dirs, _ in os.walk(directory):
        for dir in dirs:
            if relative:
                relative_root = root.replace(directory, '')
                dir_list.append(os.path.join(relative_root, dir))
            else:
                dir_list.append(os.path.join(root, dir))
    return dir_list


def get_files_by_extension(directory, extensions, relative=False):
    file_list = []
    for root, _, files in os.walk(directory):
        for file in files:
            file_ext = os.path.splitext(file)[1].lower()

            for ext in extensions:
                if ext.casefold() == file_ext.casefold():
                    if relative:
                        relative_root = root.replace(directory, '')
                        file_list.append(os.path.join(relative_root, file))
                    else:
                        file_list.append(os.path.join(root, file))

    return file_list

def get_files_containing_string(directory, string, relative=False):
    file_list = []
    for root, _, files in os.walk(directory):
        for file in files:
            if string.casefold() in file.casefold():
                if relative:
                    relative_root = root.replace(directory, '')
                    file_list.append(os.path.join(relative_root, file))
                else:
                    file_list.append(os.path.join(root, file))

    return file_list


def get_dirs_containing_string(directory, string, relative=False):
    dir_list = []
    for root, dirs, files in os.walk(directory):
        for dir in dirs:
            if string.casefold() in dir.casefold():
                if relative:
                    relative_root = root.replace(directory, '')
                    dir_list.append(os.path.join(relative_root, dir))
                else:
                    dir_list.append(os.path.join(root, dir))

    return dir_list

def directory_contains_directory(directory, subdirectory):
    for _, dirs, _ in os.walk(directory):
        for dir in dirs:
            if subdirectory.casefold() in dir.casefold():
                return True
    return False

def directory_contains_file(directory, filename):
    for _, _, files in os.walk(directory):
        for file in files:
            if filename.casefold() in file.casefold():
                return True
    return False

def directory_contains_file_with_extension(directory, extension):
    for _, _, files in os.walk(directory):
        for file in files:
            if extension.casefold() in os.path.splitext(file)[1].casefold():
                return True
    return False

def create_directory(directory_path):
    os.makedirs(directory_path, exist_ok=True)

def create_subdirectory(parent_dir, subdirectory_name):
    subdirectory_path = os.path.join(parent_dir, subdirectory_name)
    os.makedirs(subdirectory_path, exist_ok=True)

def copy_file(src_file_path, dest_file_path):
    shutil.copy2(src_file_path, dest_file_path)

def move_file(src_file_path, dest_file_path):
    shutil.move(src_file_path, dest_file_path)

def directory_exists(directory_path):
    return os.path.exists(directory_path) and os.path.isdir(directory_path)

def delete_directory(directory_path):
    if os.path.exists(directory_path):
        if os.path.isdir(directory_path):
            shutil.rmtree(directory_path)

def get_file_extension(file_path):
    return os.path.splitext(file_path)[1].lower()

def get_file_name(file_path):
    return os.path.basename(file_path)

def get_file_directory(file_path):
    return os.path.dirname(file_path)

def recreate_directory(directory_path):
    delete_directory(directory_path)
    create_directory(directory_path)
