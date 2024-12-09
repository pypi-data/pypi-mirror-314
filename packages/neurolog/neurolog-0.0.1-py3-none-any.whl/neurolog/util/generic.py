import shutil
from pathlib import Path

import tqdm
import colorama
from colorama import Fore, Back, Style


def load_toml(config_path):
    return toml.load(Path(config_path).open('rb'))

def deep_update(mapping: dict, *updating_mappings: dict) -> dict:
    '''Code adapted from pydantic'''
    updated_mapping = mapping.copy()
    for updating_mapping in updating_mappings:
        for k, v in updating_mapping.items():
            if k in updated_mapping and isinstance(updated_mapping[k], dict) and isinstance(v, dict):
                updated_mapping[k] = deep_update(updated_mapping[k], v)
            else:
                updated_mapping[k] = v
    return updated_mapping

def copy_file(ipath, opath):
    shutil.copy2(ipath, opath)

def color_str(str, fore_color):
    return fore_color + str + Fore.RESET

def bs(arr, t):
    if len(arr) == 0: return 0
    if len(arr) == 1:
        if t > arr[0]: return 1
        else: return 0

    mid = len(arr) // 2
    if arr[mid] == t:
        return mid
    elif t > arr[mid]:
        return mid+bs(arr[mid:],t)
    else:
        return bs(arr[:mid],t)
