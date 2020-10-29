from __future__ import print_function

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

# Data Scienc & Machine Learning main imports.
# ----------------------------------------------- #
import scipy
import numpy as np
import pandas as pd

def get_ready_siren_df_to_merge(siren_df, image):
    with BytesIO() as f:
        image.save(f, format='PNG')
        file_size_bits = f.getbuffer().nbytes * 8
        pass
    # Define "BPP attribute" and add it to existing df.
    siren_df['bpp'] = siren_df['#params'].values * 32 / (image.size[0] * image.size[1])
    
    # Define "file_size_bits attribute" and add it to existing df.
    siren_df['file_size_bits'] = siren_df['#params'].values * 32
    # Define "CR attribute" and add it to existing df.
    siren_df['CR'] = file_size_bits / (siren_df['#params'].values * 32)
    
    # Define "Compression Label" and add it to existing df.
    hf_arr = siren_df['hf'].values.astype(dtype = np.int)
    create_label_lambda = lambda hf: f'siren-{hf}'
    siren_df['compression'] = list(map(create_label_lambda, hf_arr))
    
    return siren_df

def get_ready_jpeg_df_to_merge(jpeg_df):
    # Define "Compression Label" and add it to existing df.
    jpeg_df['compression'] = ['jpeg'] * jpeg_df.shape[0]
    return jpeg_df

def prepare_and_merge_target_dfs(siren_df, jpeg_df, *args, **kwargs):
    # pprint(kwargs)
    
    # Target image, either cropped or not, depending on the kind of run.
    image = kwargs['image']
    
    # Prepare siren_df for merging.
    siren_df = get_ready_siren_df_to_merge(siren_df, image=image)
    
    # Prepare jpeg_df for merging.
    jpeg_df = get_ready_jpeg_df_to_merge(jpeg_df)
    
    # Get columns to be merged and new columsn for
    # rename them after merging.
    siren_columns_for_merge = kwargs['siren_columns_for_merge']
    jpeg_columns_for_merge = kwargs['jpeg_columns_for_merge']
    columns_names_merge = kwargs['columns_names_merge']
    
    # Performe merging.
    data_frames_list = [
        siren_df[siren_columns_for_merge],
        jpeg_df[jpeg_columns_for_merge],
    ]
    merged_df = pd.concat(data_frames_list, names = columns_names_merge)
    return merged_df, siren_df, jpeg_df