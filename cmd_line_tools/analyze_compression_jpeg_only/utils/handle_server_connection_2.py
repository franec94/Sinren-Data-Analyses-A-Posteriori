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

import copy
import sys

def get_sql_statement_insert_jpeg_compressions_table():
    table_name = "compressions_table"
    attr_names = "width,height,crop_width,crop_heigth,image,quality,bpp,mse_score,psnr_score,ssim_score,cr_score,is_cropped"
    n = len(attr_names.split(","))
    place_holders = ','.join(p for p in ["?"] * n)
    sql_statement = f"INSERT INTO {table_name} ({attr_names}) VALUES ({place_holders})"
    return sql_statement

def insert_data_by_sql_statement(data, db_resource, sql_statement):
    def map_attr(attr):
        if isinstance(attr, str):
            if attr.upper() != "NULL":
                return f"'{attr}'"
            else:
                return "NULL"
        elif isinstance(attr, bool):
            if attr is True:
                return "true"
            else:
                return "false"
        return f"{attr}"

    with contextlib.closing(sqlite3.connect(f"{db_resource}")) as connection:
        with contextlib.closing(connection.cursor()) as cursor:
            for a_record in data:
                # a_record_tmp = list(map(map_attr, a_record._asdict().values()))
                a_record_tmp = a_record
                pprint(a_record_tmp)
                
                # rows = cursor.execute(sql_statement.format(a_record_tmp) + ';').fetchall()
                rows = cursor.execute(sql_statement, a_record_tmp).fetchall()
                print(rows)
                pass
            pass
        connection.commit()
        pass
    pass