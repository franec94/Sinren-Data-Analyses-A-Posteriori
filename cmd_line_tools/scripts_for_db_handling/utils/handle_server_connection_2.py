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
import tqdm
import tabulate
import yaml

from collections import namedtuple
from io import BytesIO
from typing import NamedTuple

import numpy as np
import pandas as pd

import copy
import sys

def get_sql_statement_insert_jpeg_compressions_table():
    table_name = "compressions_table"
    attr_names = "width,height,crop_width,crop_heigth,image,quality,bpp,mse_score,psnr_score,ssim_score,cr_score,is_cropped"
    n = len(attr_names.split(","))
    place_holders = ','.join(p for p in ["?"] * n)
    sql_statement = f"INSERT INTO {table_name} ({attr_names}) VALUES ({place_holders})"
    return sql_statement

def get_sql_statement_insert_table(table_name, attr_names):
    # table_name = "compressions_table"
    # attr_names = "width,height,crop_width,crop_heigth,image,quality,bpp,mse_score,psnr_score,ssim_score,cr_score,is_cropped"
    n = len(attr_names)
    place_holders = ','.join(p for p in ["?"] * n)
    attr_names_q = ','.join(p for p in attr_names)
    sql_statement = f"INSERT INTO {table_name} ({attr_names_q}) VALUES ({place_holders});"
    return sql_statement

def get_sql_statement_check_in_table(table_name, attr_names, is_symbols):
    # table_name = "compressions_table"
    # attr_names = "width,height,crop_width,crop_heigth,image,quality,bpp,mse_score,psnr_score,ssim_score,cr_score,is_cropped"
    n = len(attr_names[0:13])
    place_holders = [p for p in ["?"] * n]# ','.join(p for p in ["?"] * n)
    attr_names_q = attr_names[:13] # ','.join(p for p in attr_names)
    # attr_names_q = ','.join(p for p in attr_names)
    # attr_names_q = list(filter(lambda xx: 'seed,using_quantization'.find(xx) == -1, attr_names_q))

    constraints = list(map(lambda item: f"{item[0]} {item[1]} {item[2]}", zip(attr_names_q, is_symbols, place_holders)))
    constraints = ' AND '.join([a_constraint for a_constraint in constraints])
    # sql_statement = f"select {attr_names_q} FROM {table_name} " # WHERE {constraints}"
    sql_statement = f"select  COUNT(*) FROM {table_name} WHERE {constraints};"
    return sql_statement


def insert_data_by_sql_statement(data, db_resource, table_name, attr_names):

    sql_statement = get_sql_statement_insert_table(table_name, attr_names)
    inserted_list, skipped_list = [], []
    for ii in tqdm.tqdm(range(len(data))):
        with contextlib.closing(sqlite3.connect(f"{db_resource}")) as connection:
            
            to_insert = True; a_record = data[ii]
            a_record_tuple = tuple(a_record)
            with contextlib.closing(connection.cursor()) as cursor:
                is_symbols = list(map(lambda item: 'IS' if item is None else '=', a_record))
                sql_statement_check_in = get_sql_statement_check_in_table(table_name, attr_names, is_symbols)
                if sql_statement_check_in is not None:
                    a_tuple = tuple(map(lambda item: item[1], filter(lambda xx: str(xx[0]) not in "".split(","), enumerate(a_record_tuple[:13]))))
                    rows = cursor.execute(sql_statement_check_in, a_tuple).fetchall()
                    if rows[0] == (0,):
                        inserted_list.append(a_record_tuple)
                    else:
                        to_insert = False
                        skipped_list.append(a_record_tuple)
                        pass
                pass
            with contextlib.closing(connection.cursor()) as cursor:
                if to_insert:
                    rows = cursor.execute(sql_statement, a_record_tuple).fetchall()
                    connection.commit()
                pass
            pass
        pass
    print(f'SKIPPED: {len(skipped_list)} | INSERTED: {len(inserted_list)} | TOT: {len(data)}')
    return inserted_list, skipped_list