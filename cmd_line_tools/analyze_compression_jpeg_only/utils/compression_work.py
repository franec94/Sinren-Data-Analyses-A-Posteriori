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
import operator
import os
import re
import sqlite3
import sys
import time
import tqdm
import tabulate
import yaml

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


from utils.classes import JpegCompressionResult, BenfordResult

def _get_images(a_image_path, args, quality):
    if args.crop_width != None and args.crop_heigth != None:
        kwargs = dict(crop_width=args.crop_width , crop_heigth=args.crop_heigth)
            
        a_image_gt = JpegCompressionResult.get_cropped_image_as_arr(a_image_path, **kwargs)
        a_image = JpegCompressionResult.get_cropped_image(a_image_path, **kwargs)

        kwargs = dict(crop_width=args.crop_width , crop_heigth=args.crop_heigth, quality=quality)
        a_image_compressed = JpegCompressionResult.get_cropped_image_as_arr(a_image_path, **kwargs).astype(dtype = np.uint8)

        assert a_image.size == (args.crop_width, args.crop_heigth), "Error width and heigth are not correctly updated."
    elif args.sidelength:
        kwargs = dict(sidelength=args.sidelength)
        a_image_gt = JpegCompressionResult.get_cropped_image_as_arr(a_image_path, **kwargs)
        a_image = JpegCompressionResult.get_cropped_image(a_image_path, **kwargs)

        kwargs = dict(sidelength=args.sidelength, quality=quality)
        a_image_compressed = JpegCompressionResult.get_cropped_image_as_arr(a_image_path, **kwargs).astype(dtype = np.uint8)
        
        assert a_image.size == (args.sidelength, args.sidelength), "Error width and heigth are not correctly updated (via sidelength)."
    else:
        a_image = JpegCompressionResult.get_cropped_image(a_image_path)
        a_image_gt = JpegCompressionResult.get_image_as_arr(a_image_path, quality = quality).astype(dtype = np.uint8)
        a_image_compressed = JpegCompressionResult.get_image_as_arr(a_image_path, quality = quality).astype(dtype = np.uint8)
        pass
    return a_image, a_image_gt, a_image_compressed

def _get_images_and_bpp(a_image_path, args, quality):
    if args.crop_width != None and args.crop_heigth != None:
        kwargs = dict(crop_width=args.crop_width , crop_heigth=args.crop_heigth)
            
        a_image_gt = JpegCompressionResult.get_cropped_image_as_arr(a_image_path, **kwargs)
        a_image = JpegCompressionResult.get_cropped_image(a_image_path, **kwargs)
        bpp_score = JpegCompressionResult.calculate_bpp(a_image_path, **kwargs)

        kwargs = dict(crop_width=args.crop_width , crop_heigth=args.crop_heigth, quality=quality)
        a_image_compressed = JpegCompressionResult.get_cropped_image_as_arr(a_image_path, **kwargs).astype(dtype = np.uint8)

        assert a_image.size == (args.crop_width, args.crop_heigth), "Error width and heigth are not correctly updated."
    elif args.sidelength:
        kwargs = dict(sidelength=args.sidelength)
        a_image_gt = JpegCompressionResult.get_cropped_image_as_arr(a_image_path, **kwargs)
        a_image = JpegCompressionResult.get_cropped_image(a_image_path, **kwargs)
        bpp_score = JpegCompressionResult.calculate_bpp(a_image_path, **kwargs)

        kwargs = dict(sidelength=args.sidelength, quality=quality)
        a_image_compressed = JpegCompressionResult.get_cropped_image_as_arr(a_image_path, **kwargs).astype(dtype = np.uint8)
        
        assert a_image.size == (args.sidelength, args.sidelength), "Error width and heigth are not correctly updated (via sidelength)."
    else:
        a_image = JpegCompressionResult.get_cropped_image(a_image_path)
        a_image_compressed = JpegCompressionResult.get_image_as_arr(a_image_path, quality = quality).astype(dtype = np.uint8)
        bpp_score = JpegCompressionResult.calculate_bpp(a_image_path, quality = quality)
        pass

    return a_image, a_image_gt, a_image_compressed, bpp_score


def _calculate_occurences_for_benford_law(images_list, quality, args):

    data_tuples, cnt_gt, cnt_compressed = [], None, None
    for a_image_path in images_list:

        filename, _  = os.path.splitext(os.path.basename(a_image_path))
        a_image = JpegCompressionResult.get_image(a_image_path)
        width, height = a_image.size

        a_image, a_image_arr, a_image_compressed_arr = \
            _get_images(a_image_path, args, quality)
        crop_width, crop_heigth = a_image.size

        if cnt_gt == None and cnt_compressed == None:
            # print('first case')
            cnt_gt = collections.Counter(map(lambda item: str(item)[0], a_image_arr.flatten()))
            cnt_compressed = collections.Counter(map(lambda item: str(item)[0], a_image_compressed_arr.flatten()))
            
            values_list = [width, height, crop_width, crop_heigth, quality, filename, copy.deepcopy(cnt_gt), copy.deepcopy(cnt_compressed)]
            a_record = BenfordResult(*values_list)
            # pprint(a_record)
        else:
            # print('no first case')
            # pprint(cnt_gt)
            # pprint(cnt_compressed)
            cnt_gt_tmp = collections.Counter(map(lambda item: str(item)[0], a_image_arr.flatten()))
            cnt_compressed_tmp = collections.Counter(map(lambda item: str(item)[0], a_image_compressed_arr.flatten()))

            cnt_gt += cnt_gt_tmp
            cnt_compressed += cnt_compressed_tmp

            values_list = [width, height, crop_width, crop_heigth, quality, filename, cnt_gt_tmp, cnt_compressed_tmp]
            a_record = BenfordResult(*values_list)
            pass
        
        data_tuples.append(a_record)
        pass
    return cnt_gt, cnt_compressed, data_tuples

def _calculate_compressions_by_quality(images_list, quality, args):
    data_tuples = []
    for a_image_path in images_list:

        # a_image_gt = JpegCompressionResult.get_image_as_arr(a_image_path).astype(dtype = np.uint8)
        a_image = JpegCompressionResult.get_image(a_image_path)
        width, height = a_image.size

        a_image, a_image_arr, a_image_compressed_arr, bpp_score = \
            _get_images_and_bpp(a_image_path, args, quality)
        crop_width, crop_heigth = a_image.size

        if width != crop_width or height != crop_heigth:
            is_cropped = True
        else:
            is_cropped = False

        filename, _  = os.path.splitext(os.path.basename(a_image_path))

        mse_score = JpegCompressionResult.calculate_mse(a_image_arr, a_image_compressed_arr)
        psnr_score = JpegCompressionResult.calculate_psnr(a_image_arr, a_image_compressed_arr)
        ssim_score = JpegCompressionResult.calculate_ssim(a_image_arr, a_image_compressed_arr)

        cr_score = JpegCompressionResult.calculate_cr_score(a_image, quality = quality)
        val_list = [width, height, crop_width, crop_heigth, filename, quality, bpp_score, mse_score, psnr_score, ssim_score, cr_score, is_cropped]

        jcr = JpegCompressionResult(*val_list)
        # print(jcr._asdict())
        # print(jcr)
        data_tuples.append(jcr)
        pass
    return data_tuples

def calculate_compressions_by_quality(args):
    data_list = []
    images_list = args.image_files
    # for a_quality in np.arange(args.min_quality, args.max_quality+1).astype(dtype = np.int):
    # for a_quality in range(args.min_quality, args.max_quality+1):
    for a_quality in tqdm.tqdm(range(args.min_quality, args.max_quality+1)):
        # print(a_quality)
        data_tuples_tmp = _calculate_compressions_by_quality(images_list, a_quality, args)
        data_list.extend(data_tuples_tmp)
        pass
    return data_list

def get_benfords_from_cntrs(counter_arr):
    def sort_elem(elem):
        return dict(sorted(elem.items(), key=operator.itemgetter(0)))
    counter_arr = list(map(sort_elem, counter_arr))

    res_df = pd.DataFrame(counter_arr)
    # result_df = pd.concat([result_df, res_df], axis = 0)
    return res_df

def calculate_occurences_for_benford_law(args):
    data_list = []
    images_list = args.image_files
    # for a_quality in np.arange(args.min_quality, args.max_quality+1).astype(dtype = np.int):
    result_dict = {}
    cnt_gt, cnt_compressed  = None, None
    data_tuples = []
    # for a_quality in range(args.min_quality, args.max_quality+1):
    for a_quality in tqdm.tqdm(range(args.min_quality, args.max_quality+1)):
        # print(a_quality)
        
        if cnt_gt is None and cnt_compressed is None:
            cnt_gt, cnt_compressed, data_tuples_tmp = _calculate_occurences_for_benford_law(images_list, a_quality, args)
        else:
            _, cnt_compressed_tmp, data_tuples_tmp = _calculate_occurences_for_benford_law(images_list, a_quality, args)
            cnt_compressed  += cnt_compressed_tmp
            pass

        data_tuples.extend(data_tuples_tmp)
        pass
    return cnt_gt, cnt_compressed, data_tuples
