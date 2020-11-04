import argparse
import logging
import os
import pickle
import sys
from utils.functions import check_file_exists, check_dir_exists, read_conf_file
import utils

def setup_logger(filename):
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    
    output_file_handler = logging.FileHandler(f"{filename}", mode="w")
    logger.addHandler(output_file_handler)   
    return logger


def preprocess_cmd_line_args_for_jpeg_compression(args):

    if not check_dir_exists(args.output_location, raise_exception=False):
        os.makedirs(args.output_location)
        pass

    filename = os.path.join(args.output_location, 'root.log')
    logger = setup_logger(filename)

    if args.enable_pickling:
        print("Pickling cmd line arguments...")
        logger.info("Pickling cmd line arguments...")
        with open("cmd_line_args_dict.pickle", "w") as f:
            pickle.dump(dict(args), f)
            pass
        pass

    
    print(f"Checking config file '{args.path_conf_combs}' exists...")
    logger.info(f"Checking config file '{args.path_conf_combs}' exists...")
    conf_data = read_conf_file(conf_file_path = f'{args.path_conf_combs}', raise_exception = True)

    def map_vals_to_list(item):
        item[1]['type'] = eval(item[1]['type'] )
        def map_val(a_val, a_type = item[1]['type']):
            if a_val == "NULL":
                return None
            return a_type(a_val)

        item[1]['vals'] = list(map(map_val, item[1]['vals'].split(",")))
        return item
    conf_data = dict(map(map_vals_to_list, conf_data.items())) 
    return args, conf_data, logger

def get_argparser_for_generating_data():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--path_conf_combs", default=None, type=str, dest="path_conf_combs", help="List of input jpeg files to process."
    )
    parser.add_argument(
        "--output_location", type=str, default=".", dest="output_location", help="Local path where results will be put."
    )
    parser.add_argument(
        "--enable_pickling",default=False, action='store_true', dest="enable_pickling", help="Pickel logger and others, if any (default: False)."
    )
    parser.add_argument(
        "--show_results_via_table",default=False, action='store_true', dest="show_results_via_table", help="Show results inside a table (default: False)."
    )
    parser.add_argument(
        "--db_resource",default=None, type=str, dest="db_resource", help="DB resource (default: None)."
    )
    parser.add_argument(
        "--save_intermediate_results_as_csv", default=False, action='store_true', dest="save_df_as_csv", help="Set to save intermediate results into csv files (default: False)."
    )
    parser.add_argument(
        "--save_data_to_db", default=False, action='store_true', dest="save_data_to_db", help="Set to save final data to db (default: False)."
    )
    return parser