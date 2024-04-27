import os
import shutil


def copy_recursive(source, target):
    if not os.path.exists(target):
        os.mkdir(target)

    for element in os.listdir(source):
        source_element_path = os.path.join(source, element)
        target_element_path = os.path.join(target, element)

        if os.path.isfile(source_element_path):
            shutil.copy(source_element_path, target)
        else:
            copy_recursive(source_element_path, target_element_path)
