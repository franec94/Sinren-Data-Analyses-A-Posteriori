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

from utils.functions import check_dir_exists, create_dir

def work(opt):
    logging.info(f"Doing work...")

    train_path = os.path.join(opt.data_path, 'train')
    check_dir_exists(train_path)


    file_train_path = os.path.join(opt.data_path, 'train', 'result_comb_train.txt')
    check_dir_exists(file_train_path)

    columns = "#params;seed;hl;hf;mse;psnr;ssim;eta".split(";")
    train_arr = np.loadtxt(file_train_path)

    train_df = pd.DataFrame(data = train_arr, columns = columns)
    print(train_df.head(5))

    pass