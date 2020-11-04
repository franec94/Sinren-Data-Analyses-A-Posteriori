import argparse
import logging
import os
import pickle
import sys
from utils.functions import check_file_exists, check_dir_exists

def preprocess_cmd_line_args_for_jpeg_compression(args):
    if not check_dir_exists(args.output_location, raise_exception=False):
        os.makedirs(args.output_location)
        pass

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    # if args.enable_logging:
    filename = os.path.join(args.output_location, 'root.log')
    output_file_handler = logging.FileHandler(f"{filename}", mode="w")
    logger.addHandler(output_file_handler)    
    # pass
    # stdout_handler = # logging.StreamHandler(sys.stdout)
    # logger.addHandler(stdout_handler)

    if args.enable_pickling:
        print("Pickling cmd line arguments...")
        logger.info("Pickling cmd line arguments...")
        with open("cmd_line_args_dict.pickle", "w") as f:
            pickle.dump(dict(args), f)
            pass
        pass

    def filter_not_existing_files(a_file):
        res_exists = check_file_exists(a_file, raise_exception=False)
        logger.info(f"{os.path.basename(a_file)} exists? {res_exists}")
        return res_exists
    def filter_is_jmage(a_file):
        _, file_extension = os.path.splitext(a_file)
        is_jpeg = file_extension in ".jpeg,.jpg,.png".split(",")
        logger.info(f"{os.path.basename(a_file)} is image? {is_jpeg}")
        return is_jpeg
    def filter_is_dir(a_dir):
        res_exists = check_dir_exists(a_dir, raise_exception=False)
        logger.info(f"{a_dir} exists? {res_exists}")
        return res_exists
    
    if args.image_files != None:
        args.image_files = list(set(args.image_files))
        logger.info("Filter out what is not a file...")
        n_before = len(args.image_files)
        args.image_files = list(filter(filter_not_existing_files, args.image_files))
        n_after = len(args.image_files)
        logger.info(f"Filtered out {n_before-n_after}/{n_before}")

        logger.info("Filter out what is not a jpeg file...")
        n_before = len(args.image_files)
        args.image_files = list(filter(filter_is_jmage, args.image_files))
        n_after = len(args.image_files)
        logger.info(f"Filtered out {n_before-n_after}/{n_before}")
        pass

    if args.dirs != None:
        logger.info("Filter out what is not a dir file...")
        n_before = len(args.dirs)
        args.jpeg_dirsfiles = list(filter(filter_is_dir, args.dirs))
        n_after = len(args.dirs)
        logger.info(f"Filtered out {n_before-n_after}/{n_before}")

        for a_dir in args.dirs:
            res = list(filter(
                filter_is_jmage,
                filter(
                    filter_not_existing_files,
                    map(lambda entry: os.path.join(a_dir, entry), os.listdir(a_dir))
                    )
                )
            )
            if res != None and len(res) != 0:
                if args.image_files == None:
                    args.image_files = res
                else:
                    args.image_files.extend(res)
                    pass
                pass
            pass
        pass

    args.image_files = list(set(args.image_files))
    return args, logger

def get_argparser_for_jpeg_compression():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--image_files", default=None, type=str, nargs='+', dest="image_files", help="List of input jpeg files to process."
    )

    parser.add_argument(
        "--dirs", default=None, type=str, nargs='+', dest="dirs", help="List of input dirs with jpeg files to process."
    )
    parser.add_argument(
        "--output_location", type=str, default=".", dest="output_location", help="Local path where results will be put."
    )
    parser.add_argument(
        "--min_quality", type=int, default=20, dest="min_quality", help="Minimum quality value from which beginning jpeg compression (default: 20)."
    )
    parser.add_argument(
        "--max_quality", type=int, default=95, dest="max_quality", help="Maximum quality value from which beginning jpeg compression (default: 95)."
    )
    parser.add_argument(
        "--enable_logging",default=False, action='store_true', dest="enable_logging", help="Maximum quality value from which beginning jpeg compression (default: False)."
    )
    parser.add_argument(
        "--enable_pickling",default=False, action='store_true', dest="enable_pickling", help="Pickel logger and others, if any (default: False)."
    )
    parser.add_argument(
        "--sidelength",default=None, type=int, dest="sidelength", help="Sidelength for cropping to a squared image (default: None)."
    )
    parser.add_argument(
        "--crop_width",default=None, type=int, dest="crop_width", help="Width size for cropping to a squared/rectangle image (default: None)."
    )
    parser.add_argument(
        "--crop_heigth",default=None, type=int, dest="crop_heigth", help="Height size for cropping to a squared/rectangle image (default: None)."
    )
    parser.add_argument(
        "--show_results_via_table",default=False, action='store_true', dest="show_results_via_table", help="Show results inside a table (default: False)."
    )
    parser.add_argument(
        "--db_resource",default=None, type=str, dest="db_resource", help="DB resource (default: None)."
    )
    return parser