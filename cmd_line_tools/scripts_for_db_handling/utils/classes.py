from __future__ import print_function


from utils.libs import DARK_BACKGROUND_PLT

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
import copy
import datetime
import functools
import glob
import itertools
import json
import logging
import operator
import os
import re
import sqlite3
import sys
import time
import tabulate
import yaml

from collections import namedtuple
from io import BytesIO
from typing import NamedTuple

import numpy as np
import pandas as pd

import skimage
import skimage.metrics as skmetrics
from skimage.metrics import peak_signal_noise_ratio
from skimage.metrics import structural_similarity
from skimage.metrics import mean_squared_error

import copy
import sys

class BenfordResult(NamedTuple):
    width: int
    height: int
    crop_width: int
    crop_heigth: int
    quality: int
    name: str
    counter_gt: collections.Counter
    counter_compressed: collections.Counter
    pass

class JpegCompressionResult(NamedTuple):
    width: int
    height: int
    crop_width: int
    crop_heigth: int
    name: str
    quality: int
    bpp: float
    mse_score: float
    psnr_score: float
    ssim_score: float
    cr_score: float
    is_cropped: bool

    @staticmethod
    def calculate_bpp(img_gt, *args, **kwargs):
        image = JpegCompressionResult.get_image(img_gt, *args, **kwargs)
        file_size_bits, width, heigth = None, None, None
        with BytesIO() as f:
            logging.getLogger()
            image.save(f, format='JPEG')
            f.seek(0)
            file_size_bits = f.getbuffer().nbytes * 8
            width, heigth = image.size
            pass
        return file_size_bits / (width * heigth)

    @staticmethod
    def calculate_mse(arr_gt, arr, *args, **kwargs):
        return mean_squared_error(arr_gt, arr)
    
    @staticmethod
    def calculate_psnr(arr_gt, arr, *args, **kwargs):
        return peak_signal_noise_ratio(arr_gt, arr, **kwargs)
    
    @staticmethod
    def calculate_ssim(arr_gt, arr, *args, **kwargs):
        return structural_similarity(arr_gt, arr, **kwargs)
    
    @staticmethod
    def calculate_cr_score(img_gt, *args, **kwargs):
        with BytesIO() as f:    
            img_gt.save(f, format='JPEG')
            f.seek(0)
            file_size_bits = f.getbuffer().nbytes * 8
            pass
        with BytesIO() as f:    
            img_gt.save(f, format='JPEG', quality = kwargs['quality'])
            f.seek(0)
            compressed_file_size_bits = f.getbuffer().nbytes * 8
            pass
        return file_size_bits / compressed_file_size_bits
    
    @staticmethod
    def get_image(image_file_path, *args, **kwargs):
        im = None
        if 'quality' in kwargs.keys():
            with BytesIO() as f:
                image_file = Image.open(image_file_path)
                image_file.save(f, format='JPEG', quality = kwargs['quality'])
                f.seek(0)
                im = Image.open(f)
                im = copy.deepcopy(im)
                pass
        else:
            im = Image.open(image_file_path)
        return im
    
    @staticmethod
    def get_image_as_arr(image_file_path, *args, **kwargs):
        if 'quality' in kwargs.keys():
            with BytesIO() as f:
                image_file = Image.open(image_file_path)
                image_file.save(f, format='JPEG', quality = kwargs['quality'])
                f.seek(0)
                return np.asarray(Image.open(f))
        return np.asarray(Image.open(image_file_path))
    
    @staticmethod
    def _get_new_targets(target, size):
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
    
    @staticmethod
    def get_cropped_image_as_arr(image_file_path, *args, **kwargs):
        image = JpegCompressionResult.get_cropped_image(image_file_path, **kwargs)
        return np.asarray(image)

    @staticmethod
    def _get_cropped_by_center_image(im, target = 25):
        width, height = im.size

        if isinstance(target, int):
            target = (target, target)
            pass

        left, right = JpegCompressionResult._get_new_targets(target[0], width)
        top, bottom = JpegCompressionResult._get_new_targets(target[1], height)

        # print(im.crop((left, top, right, bottom)).size)
        # print((left, top, right, bottom))
        # print(im)
        # sys.exit(0)

        im_cropped = im.crop((left, top, right, bottom))
        return im_cropped
    
    @staticmethod
    def get_cropped_image(image_file_path, *args, **kwargs):
        if 'crop_width' in kwargs.keys() and 'crop_heigth' in kwargs.keys():
            target = (kwargs['crop_width'], kwargs['crop_heigth'])
        elif 'sidelength' in kwargs.keys():
            target = kwargs['sidelength']
        else:
            raise Exception("Crop failed due to missing input variables.")
        
        # pprint(target)
        # raise Exception(str(target))
        image = JpegCompressionResult.get_image(image_file_path, *args, **kwargs)
        # pprint(image)
        image = JpegCompressionResult._get_cropped_by_center_image(image, target)
        return image

    pass



