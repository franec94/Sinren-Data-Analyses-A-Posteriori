import glob
import logging
import os
import sys

import numpy as np
import pandas as pd

def  get_root_level_logger(root_path, loggger_name='train.log'):
    log_filename = os.path.join(root_path, f'{loggger_name}')
    log_filename_exists = check_file_exists(log_filename, raise_exception=False)
    if log_filename_exists:
        os.remove(log_filename)
        pass

    logging.basicConfig(filename=f'{log_filename}', level=logging.INFO)
    pass


def check_file_exists(file_path, raise_exception=True):
    if not os.path.isfile(file_path):
        if raise_exception:
            raise Exception(f"Error: file '{file_path}' does not exists!")
        return False
    return True

def check_dir_exists(dir_path):
    if not os.path.isdir(dir_path):
        raise Exception(f"Error: directory '{dir_path}' does not exists!")
    pass


def create_dir(dir_path):
    if not os.path.isdir(dir_path):
        try:
            os.makedirs(dir_path)
        except PermissionError as err:
            print(f"Error raised when dealing with dir '{dir_path}' creation!", file=sys.stderr)
            print(str(err))
            sys.exit(-1)
            pass
        except:
            pass
        pass
    pass
