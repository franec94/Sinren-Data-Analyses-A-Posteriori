# ---------------------------- #
# Generic Imports
# ---------------------------- #

from pprint import pprint
from PIL import Image
from tqdm import tqdm
from typing import Union, Tuple

from functools import partial

import collections
import copy
import datetime
import functools
import h5py
import math
import logging
import operator
import os
import random
import shutil
import sys
import re
import time

import numpy as np
import pandas as pd

# ---------------------------- #
# Custom Imports
# ---------------------------- #

from utils.functions import check_dir_exists, check_file_exists, create_dir

def work(opt):
    logging.info(f"Doing work...")

    train_path: str = os.path.join(opt.data_path, 'train')
    check_dir_exists(train_path)


    file_train_path: str = os.path.join(opt.data_path, 'train', 'result_comb_train.txt')
    check_file_exists(file_train_path)

    columns: list = "#params;seed;hl;hf;mse;psnr;ssim;eta".split(";")
    train_arr: np.ndarray = np.loadtxt(file_train_path)

    train_df: pd.DataFrame = pd.DataFrame(data = train_arr, columns = columns)
    
    logging.info(train_df.head(5))
    train_df.info()
    logging.info(train_df.describe())

    pass