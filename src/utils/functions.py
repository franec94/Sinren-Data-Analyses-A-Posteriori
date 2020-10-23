import os
import sys

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