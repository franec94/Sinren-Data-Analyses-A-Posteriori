from __future__ import print_function

SHOW_VISDOM_RESULTS = False

import warnings
warnings.filterwarnings("ignore", message="Numerical issues were encountered ")

from fastcore.foundation import *
from fastcore.meta import *
from fastcore.utils import *
from fastcore.test import *
from nbdev.showdoc import *
from fastcore.dispatch import typedispatch
from functools import partial
import inspect

from fastcore.imports import in_notebook, in_colab, in_ipython

from io import BytesIO
from PIL import Image
from pprint import pprint
if in_colab():
    from google.colab import files
    pass

# import psycopg2 as ps
import matplotlib.pyplot as plt
# plt.style.use('dark_background')
import seaborn as sns
# sns.set_theme(style="whitegrid")
if in_colab() or in_notebook():
    # back end of ipywidgets
    from IPython.display import display    
    import ipywidgets as widgets
    pass

import collections
import datetime
import functools
import glob
import json
import operator
import os
import sys
import time
import yaml

import scipy
import numpy as np
import pandas as pd

if  (in_notebook() or in_ipython()) and SHOW_VISDOM_RESULTS:
    import visdom
    pass

# skimage
import skimage
import skimage.metrics as skmetrics
from skimage.metrics import peak_signal_noise_ratio as psnr
from skimage.metrics import structural_similarity as ssim
from skimage.metrics import mean_squared_error

from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures

from utils.functions import read_conf_file, load_target_image, get_dict_dataframes, get_dataframe
from utils.make_graphics import compare_compressions
from utils.work import calculate_several_jpeg_compression, get_cropped_by_center_image
