from __future__ import print_function

SHOW_VISDOM_RESULTS = False

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
import json
import operator
import os
import sqlite3
import re
import sys
import time
import yaml

import numpy as np
import pandas as pd

from utils.functions import check_file_exists

def _get_dict_dataframes(records_list, columns):
    
    if records_list is None or len(records_list) == 0: return None
    
    index_ts = list(records_list[0]._asdict().keys()).index('timestamp')
    index_fp = list(records_list[0]._asdict().keys()).index('full_path')
    
    ts_list = list(map(operator.itemgetter(index_ts), records_list))
    files_list = list(map(operator.itemgetter(index_fp), records_list))
    result_dict_df = dict()
    for a_file, a_ts in zip(files_list, ts_list):
        # print(a_file, a_ts)
        try:
            check_file_exists(a_file, raise_exception=True)
            train_arr = np.loadtxt(a_file)
            indeces = [a_ts] * len(train_arr)
            train_df = pd.DataFrame(data = train_arr, columns = columns, index=indeces)
            result_dict_df[a_ts] = train_df
        except Exception as err:
            print(str(err))
            pass
        pass
    return result_dict_df

def _filter_data(records_list, target_status = 'Done'):
    
    if records_list is None or len(records_list) == 0: return None
    
    def filter_dones(item, attribute_name = 'status', target = f'{target_status}'):
        return getattr(item, attribute_name).lower() == target.lower()
    # records_list_filtered = list(filter(filter_dones, records_list))
    
    index = list(records_list[0]._asdict().keys()).index('status')
    records_list_filtered = list(filter(lambda item: operator.itemgetter(index)(item) == f'{target_status}', records_list))
    
    return records_list_filtered

def _map_data(records_list, root_data_dir):
    
    if records_list is None or len(records_list) == 0: return None
    
    typename = 'RunsLogged2'
    field_names = "image,date,timestamp,hidden_features,image_size,status,full_path"
    RunsLogged2 = collections.namedtuple(typename, field_names)
    
    def map_to_full_path(item, root_data_dir = f'{root_data_dir}', filename = 'result_comb_train.txt'):
        image_name_r = str(getattr(item, 'image'))
        date_r = str(re.sub('/', '-', getattr(item, 'date')))
        date_r = datetime.datetime.strptime(date_r, '%d-%m-%y').strftime("%d-%m-%Y")
        timestamp_r = str(getattr(item, 'timestamp'))
        full_path_list = [root_data_dir, image_name_r, date_r, timestamp_r, 'train', filename]
        full_path = functools.reduce(lambda a,b : os.path.join(a, b), full_path_list)
        # full_path = os.path.join(root_data_dir, image_name_r, date_r, timestamp_r, 'train', filename)
        # print(full_path)
        return RunsLogged2._make(list(item._asdict().values()) + [full_path])
    
    records_mapped_list = list(map(map_to_full_path, records_list))
    return records_mapped_list
    

def _get_data_from_db(conf_data, sql_statement):
    if conf_data['db_infos']['is_local_db']:
        db_resource = os.path.join(
            conf_data['db_infos']['db_location'],
            conf_data['db_infos']['db_name'])
    else:
        db_resource = conf_data['db_infos']['db_url']
    
    
    
    typename = 'RunsLogged'
    field_names = "image,date,timestamp,hidden_features,image_size,status"
    RunsLogged = collections.namedtuple(typename, field_names)
    
    records_list = None
    with contextlib.closing(sqlite3.connect(f"{db_resource}")) as connection:
        with contextlib.closing(connection.cursor()) as cursor:
            # Test code snippet:
            # rows = cursor.execute("SELECT 1").fetchall()
            # print(rows)
        
            # Code snippet:
            rows = cursor.execute(f'{sql_statement}').fetchall()
            # pprint(rows)
            records_list = list(map(RunsLogged._make, rows))
            pass
        pass
    # pprint(records_list)
    return records_list
    
def get_data_from_db(conf_data):
    table_name = 'table_runs_logged'
    table_attributes = "image,date,timestamp,hidden_features,image_size,status"
    
    sql_statement = f"SELECT {table_attributes} FROM {table_name}"
    if conf_data['cropped_image']['flag']:
        crop_size = conf_data['cropped_image']['crop_size']
        if isinstance(crop_size, str):
            # print(crop_size)
            crop_size = re.sub('\)', ']"', crop_size)
            crop_size = re.sub('\(', '"[', crop_size)
            crop_size = re.sub(' ', '', crop_size)
        elif isinstance(crop_size, int):
            crop_size = f'"[{crop_size},{crop_size}]"'
            pass
        sql_statement += f" WHERE image_size = {crop_size};"
        pass

    print(sql_statement)
        
        
    
    records_list = _get_data_from_db(conf_data, sql_statement)
    
    records_list_filtered = _filter_data(records_list, target_status = 'Done')
    records_list_mapped = _map_data(records_list_filtered, root_data_dir = conf_data['db_infos']['root_data_dir'])
    
    # pprint(records_list_mapped)
    
    columns = conf_data['columns_df_str'].split(";")
    result_dict_df = _get_dict_dataframes(records_list_mapped, columns)
    return result_dict_df, records_list_mapped