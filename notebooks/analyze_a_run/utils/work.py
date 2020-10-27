from datetime import datetime
# from google.colab import files

from pathlib import Path
from collections import namedtuple
from io import BytesIO
from pprint import pprint

# import psycopg2 as ps
import matplotlib.pyplot as plt
# plt.style.use('dark_background')
import seaborn as sns
# sns.set_theme(style="whitegrid")
import ipywidgets as widgets
# back end of ipywidgets
from IPython.display import display

import io
from googleapiclient.http import MediaIoBaseDownload
import zipfile

import collections
import itertools
import functools
import glob
import operator
import os
import re
import yaml
import numpy as np
import pandas as pd

from PIL import Image

# skimage
import skimage
import skimage.metrics as skmetrics
from skimage.metrics import peak_signal_noise_ratio as psnr
from skimage.metrics import structural_similarity as ssim
from skimage.metrics import mean_squared_error

from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures

from utils.handle_server_connection import get_data_from_db, get_data_from_db_by_status, get_data_from_db_by_constraints
from utils.functions import read_conf_file, load_target_image, get_dict_dataframes, get_dataframe

def get_new_targets(target, size):
    offset = target // 2
    if target % 2 == 0:
        extreme_1 = size // 2
        residual = 0
    else:
        extreme_1 = size // 2 - 1
        residual = 1
        pass
    extreme_2 = size // 2
    return extreme_1 - offset + residual, extreme_2 + offset + residual

def get_cropped_by_center_image(im, target = 25):
    width, height = im.size

    if isinstance(target, int):
        target = (target, target)
        pass

    left, right = get_new_targets(target[0], width)
    top, bottom = get_new_targets(target[1], height)

    # print(im.crop((left, top, right, bottom)).size)
    # print((left, top, right, bottom))

    im_cropped = im.crop((left, top, right, bottom))
    return im_cropped

def calculate_several_jpeg_compression(image, image_dim_bits, qualities):
    # Named tuple for creating a record related to
    # a trial for compressing the target image.
    typename = 'WeightsPsnr'
    fields_name = ['psnr', 'ssim', 'quality', 'file_size_bits', 'bpp', 'width', 'heigth', 'CR']
    WeightsPsnr = collections.namedtuple(typename, fields_name) 

    # List used to save results and keep trace of failures, if any.
    result_tuples = []
    failure_qualities = []

    # Then test the effect of several different quality values
    # used in compression transform.
    for quality in qualities:
        try:
            # Convert to JPEG specifying quality of compression.
            with BytesIO() as f:
                # im_tmp.save(f'myimg.jpg', quality = int(quality))
                # im_jpeg = Image.open('myimg.jpg')
                
                image.save(f, format='JPEG', quality = int(quality))
                f.seek(0)
                compressed_file_size_bits = f.getbuffer().nbytes * 8
                im_jpeg = Image.open(f)
                assert im_jpeg.size == image.size, "im_jpeg.size != image.size"
    
                # Calculate quantities to be stored for this trial
            
                # data used for deriving scores
                width, height = im_jpeg.size[0], im_jpeg.size[1]
                pixels = width * height
                # compressed_file_size_bits = Path('myimg.jpg').stat().st_size * 8
                compressed_file_size_bits = f.getbuffer().nbytes * 8
            
                # Scores
                bpp = compressed_file_size_bits / pixels    
                psnr_score = psnr(np.asarray(image), np.asarray(im_jpeg), data_range=255)
                ssim_score = ssim(np.asarray(image), np.asarray(im_jpeg), data_range=255)
                CR = image_dim_bits / compressed_file_size_bits
            
                # Store results into a list
                values = [psnr_score, ssim_score, quality, compressed_file_size_bits, bpp, width, height, CR]
                result_tuples.append(WeightsPsnr._make(values))
        except Exception as err:
            # Keep track of unaccepted quality values for compressing the image
            print(str(err))
            failure_qualities.append(quality)
            pass
        pass
    return result_tuples, failure_qualities


def calculate_several_jpeg_compression_with_crops(image, qualities, cropping_list):
    # Named tuple for creating a record related to
    # a trial for compressing the target image.
    typename = 'WeightsPsnr'
    fields_name = ['psnr', 'ssim', 'quality', 'file_size_bits', 'bpp', 'width', 'heigth', 'CR']
    WeightsPsnr = collections.namedtuple(typename, fields_name) 

    # List used to save results and keep trace of failures, if any.
    result_tuples = []
    failure_qualities = []

    # Gather results.
    for edges in cropping_list: # for edges in edges_list:
    
        # Firstly crop image to desired shape.    
        left, top, right, bottom = list(map(int, edges))
        im_tmp = image.crop((left, top, right, bottom))
    
        # Get size cropped image
        cropped_file_size_bits = None
        with BytesIO() as f:
            im_tmp.save(f, format='PNG')
            cropped_file_size_bits = f.getbuffer().nbytes * 8
            pass
    
        # Then test the effect of several different quality values
        # used in compression transform.
        for quality in qualities:
            try:
                # Convert to JPEG specifying quality of compression.
                with BytesIO() as f:
                    # im_tmp.save(f'myimg.jpg', quality = int(quality))
                    # im_jpeg = Image.open('myimg.jpg')
                
                    im_tmp.save(f, format='JPEG', quality = int(quality))
                    f.seek(0)
                    im_jpeg = Image.open(f)
                    assert im_jpeg.size == im_tmp.size, "im_jpeg.size != im_tmp.size"
    
                    # Calculate quantities to be stored for this trial
            
                    # data used for deriving scores
                    width, height = im_jpeg.size[0], im_jpeg.size[1]
                    pixels = width * height
                    # compressed_file_size_bits = Path('myimg.jpg').stat().st_size * 8
                    compressed_file_size_bits = f.getbuffer().nbytes * 8
            
                    # Scores
                    bpp = compressed_file_size_bits / pixels    
                    psnr_score = psnr(np.asarray(im_tmp), np.asarray(im_jpeg), data_range=255)
                    ssim_score = ssim(np.asarray(im_tmp), np.asarray(im_jpeg), data_range=255)
                    CR = cropped_file_size_bits / compressed_file_size_bits
            
                    # Store results into a list
                    values = [psnr_score, ssim_score, quality, compressed_file_size_bits, bpp, width, height, CR]
                    result_tuples.append(WeightsPsnr._make(values))
                    pass
            except Exception as err:
                # Keep track of unaccepted quality values for compressing the image
                print(err)
                failure_qualities.append(quality)
            pass
        pass
    return result_tuples, failure_qualities


def fetch_data(conf_data):
    records_list = None
    if not conf_data['data_fetch_strategy']['fetch_from_db']:
        if conf_data['is_single_run']:
            train_df = get_dataframe(conf_data)
        else:
            ts_list = '1603410154-248962,1603421693-497763'.split(",")
            # ts_list = '1603421693-497763'.split(",")
            result_dict_df = get_dict_dataframes(conf_data)
                # train_df: pd.DataFrame = result_dict_df['1603410154-248962'] # train_df: pd.DataFrame = result_dict_df['1603478755-305517']
    
            data = list(map(operator.itemgetter(1), filter(lambda item: item[0] in ts_list, result_dict_df.items())))
            train_df = pd.concat(data)
            print(collections.Counter(train_df['hl']))
            pass
    else:
        result_dict_df, records_list = get_data_from_db(conf_data)
        # data = list(map(operator.itemgetter(1), filter(lambda item: item[0] in ts_list, result_dict_df.items())))
        data = list(map(operator.itemgetter(1), result_dict_df.items()))
        train_df = pd.concat(data)
        print(collections.Counter(train_df['hl']))
        pass
    return train_df, result_dict_df, records_list

def fetch_data_by_status(conf_data, status = '*'):
    records_list = None
    if not conf_data['data_fetch_strategy']['fetch_from_db']:
        return None
    else:
        records_list = get_data_from_db_by_status(conf_data, status = status)
        pass
    return records_list

def chain_constraints_as_str(constraints, fetch_data_downloaded = False):
        def map_constraint(item):
            # pprint(item)
            attr_name = item[0]
            attr_type = item[1]['type']
            attr_vals = item[1]['val']
            """
            if len(attr_vals) == 0: return ''
            if len(attr_vals) == 1:
                if len(attr_vals[0]) == 0: return ''
            """
            
            def reduce_func(a, b, attr_type = attr_type):
                if attr_type is int:
                    return f'{attr_name} = {b}' if a == '' else f" {a} OR {attr_name} = {b} "
                elif attr_type is str:
                    b_ = f"'{b}'"
                    return f"{attr_name} = {b_}" if a == '' else f" {a} OR {attr_name} = {b_} "
                else:
                    raise Exception(f'Error {str(attr_type)} not allowed!')
            res = functools.reduce(reduce_func, attr_vals, f'')# f'{attr_name} = ')
            # print(res)
            return res
        
        
        def filter_unecessary_constraints(item):
            vals = operator.itemgetter(1)(item)
            if vals != None:
                if len(vals['val']) == 1:
                    if len(vals['val'][0]) == 0:
                        # print('zero')
                        return False
                    pass
                return True
            return False
         
        chained_constraints = str(functools.reduce(lambda a,b: f'({b})' if a == '' else f" {a} AND ({b}) ",
            list(map(map_constraint, 
                     # filter(lambda item: operator.itemgetter(1)(item) != None, constraints._asdict().items())
                     filter(filter_unecessary_constraints, constraints._asdict().items())
            )), f''
        ))
        return chained_constraints

def fetch_data_by_constraints(conf_data, constraints, fetch_data_downloaded = False):
    records_list, res = None, None
    
    typename = 'QueryConstraints2'
    field_names = "image;date;timestamp;hidden_features;image_size;status".split(";")
    
    QueryConstraints2 = collections.namedtuple(typename, field_names)
    chained_constraints = chain_constraints_as_str(constraints)
    
    records_list, result_dict_df, query_str = get_data_from_db_by_constraints(conf_data, chained_constraints, fetch_data_downloaded=fetch_data_downloaded)
    
    return records_list, result_dict_df, query_str, chained_constraints
    