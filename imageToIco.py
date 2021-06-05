import os
from typing import Tuple, List
from PIL import Image


ICO_SIZES = [
    (256, 256),
    (128, 128),
    (64, 64),
    (32, 32),
    (16, 16),
]


def strip_extension(filename) -> str:
    try:
        ext_dot_index = filename.rindex('.')
    except ValueError:
        ext_dot_index = len(filename)
    return filename[:ext_dot_index]


def get_ico_sizes(image_size: Tuple[int, int]) -> List[Tuple[int, int]]:
    width = image_size[0]
    i = -1
    for i in range(len(ICO_SIZES)):
        if ICO_SIZES[i][0] <= width:
            break
    return ICO_SIZES[i:]


def convert_file(full_name: str, name_to_save: str, directory_to_save: str) -> Tuple[str, List[Tuple[int, int]]]:
    """ -> (full name of written file, ico sizes) """
    img = Image.open(full_name)
    new_full_name = os.path.join(
        directory_to_save,
        name_to_save + '.ico'
    )
    ico_sizes = get_ico_sizes(img.size)
    img.save(new_full_name, 'ico', sizes=ico_sizes)
    img.close()
    return new_full_name, ico_sizes


def handle_single_file(filepath: str):
    directory, filename = os.path.split(filepath)
    try:
        full_name_of_result_file, ico_sizes = convert_file(
            full_name=filepath, 
            name_to_save=strip_extension(filename),
            directory_to_save=directory
        )
        print(f"File converted successfully! (converted file: {full_name_of_result_file}, ico sizes: {ico_sizes})")
    except Exception as e:
        print(f"File conversion ERROR: {e}")        


def handle_folder(folder_path: str):
    target_ext = input("Input target extension: ").strip()
    if not target_ext:
        print(f"Extension is incorrect!")
        return

    if not target_ext.startswith('.'):
        target_ext = '.' + target_ext
    
    result_folder_path = os.path.join(folder_path, "_ICO")
    count = 0
    while os.path.exists(result_folder_path):
        count += 1
        result_folder_path = os.path.join(folder_path, "_ICO" + str(count))
    
    try:
        os.mkdir(result_folder_path)
    except Exception as e:
        print(f"Error occurred while creating result directory! ('{result_folder_path}')", e)
        return

    all_ext_ok = (target_ext == ".*")
    success_count = 0
    errors_count = 0
    
    for name in os.listdir(folder_path):
        full_name = os.path.join(folder_path, name)
        if os.path.isfile(full_name):
            if name.lower().endswith(target_ext) or all_ext_ok:
                try:
                    _, ico_sizes = convert_file(
                        full_name=full_name,
                        name_to_save=strip_extension(name),
                        directory_to_save=result_folder_path
                    )
                    success_count += 1
                    print(f"'{full_name}' ------ OK   {ico_sizes}")
                except Exception as e:
                    errors_count += 1
                    print(f"'{full_name}' ------ ERROR:   {e}")
    
    print(f"Result folder: {result_folder_path}")
    print(f"Success: {success_count}")
    print(f"Errors: {errors_count}")


def main():
    path = input("Input folder or file path: ").strip().strip("\"\'")

    if path[0] == '\'' and path[-1] == '\'':
        path = path[1:-1]

    elif path[0] == '"' and path[-1] == '"':
        path = path[1:-1]

    if os.path.isfile(path):
        handle_single_file(path)

    elif os.path.isdir(path):
        handle_folder(path)

    else:
        print(f"Path '{path}' is incorrect or does not exist!")


if __name__ == '__main__':
    main()
    input("Press ENTER to finish the program...")