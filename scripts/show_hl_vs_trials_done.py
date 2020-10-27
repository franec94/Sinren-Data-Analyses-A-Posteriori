import csv
import argparse
import os
import sys
import tabulate

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Process CSV file.')
    parser.add_argument('--csv_filename', dest='csv_filename',
                    help='Path csv file')

    args = parser.parse_args()

    with open(args.csv_filename, "r") as f:
        csv_reader = csv.reader(f)
        data = []
        for row in csv_reader:
            data.append(row)
        print(tabulate.tabulate(data, headers=["hidden features", "trials done"]))
    pass