from __future__ import print_function

SHOW_VISDOM_RESULTS = False
DARK_BACKGROUND_PLT = True

# ----------------------------------------------- #
# Python's Imports
# ----------------------------------------------- #

# Std Lib and others.
# ----------------------------------------------- #
import warnings
warnings.filterwarnings("ignore", message="Numerical issues were encountered ")
# from contextlib import closing
from io import BytesIO
from PIL import Image
from pprint import pprint

# import psycopg2 as ps
import contextlib
import collections
import datetime
import functools
import glob
import itertools
import json
import operator
import os
import re
import sqlite3
import sys
import time
import yaml


# FastAi imports.
# ----------------------------------------------- #
from fastcore.foundation import *
from fastcore.meta import *
from fastcore.utils import *
from fastcore.test import *
from nbdev.showdoc import *
from fastcore.dispatch import typedispatch
from functools import partial
import inspect

from fastcore.imports import in_notebook, in_colab, in_ipython

# Constraint imports.
# ----------------------------------------------- #
if in_colab():
    from google.colab import files
    pass

if  (in_notebook() or in_ipython()) and SHOW_VISDOM_RESULTS:
    import visdom
    pass

if in_colab() or in_notebook():
    # back end of ipywidgets
    from IPython.display import display    
    import ipywidgets as widgets
    pass

# Data Scienc & Machine Learning main imports.
# ----------------------------------------------- #
import scipy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
if DARK_BACKGROUND_PLT:
    plt.style.use('dark_background')
    pass
import seaborn as sns # sns.set_theme(style="white") # sns.set(style="whitegrid", color_codes=True)
# sns.set(style="darkgrid", color_codes=True)

# skimage
# ----------------------------------------------- #
import skimage
import skimage.metrics as skmetrics
from skimage.metrics import peak_signal_noise_ratio as psnr
from skimage.metrics import structural_similarity as ssim
from skimage.metrics import mean_squared_error

# sklearn
# ----------------------------------------------- #
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures


# ----------------------------------------------- #
# Custom Imports
# ----------------------------------------------- #

from utils.functions import read_conf_file, load_target_image, get_dict_dataframes, get_dataframe
from utils.make_graphics import compare_compressions
from utils.work import calculate_several_jpeg_compression, get_cropped_by_center_image, fetch_data, fetch_data_by_status, fetch_data_by_constraints, get_info_from_logged_parser, insert_data_read_from_logs
from utils.handle_server_connection import get_data_from_db, get_data_from_db_by_status
from utils.db_tables import TableRunsDetailsClass, TableRunsDetailsTupleClass
