from pprint import pprint
import csv
import argparse
import os
import sys
import tabulate

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Process CSV file.')
    parser.add_argument('--csv_filename', dest='csv_filename',
                    help=f'Path input file which can have one of the following allowed extensions {".csv,.txt".split(",")}.')

    args = parser.parse_args()

    if not os.path.isfile(args.csv_filename):
        print(f"Error: input resource '{args.csv_filename}' is not a file!", file=sys.stderr)
        sys.exit(-1)
        pass
    file_name, file_extension = os.path.splitext(f'{args.csv_filename}')
    if file_extension not in ".csv,.txt".split(","):
        print(f"Error: input file extension '{file_extension}'", file=sys.stderr)
        print(f"Error: input resource '{args.csv_filename}' has not one of the following allowed extensions:", file=sys.stderr)
        print(f"{'.csv,.txt'.split(',')}", file=sys.stderr)
        sys.exit(-1)
        pass

    with open(args.csv_filename, "r") as f:
        """
        csv_reader = csv.reader(f)
        data = []
        for row in csv_reader:
            data.append(row)
            pass
        """
        """
        data = list(csv.reader(f))
        print(tabulate.tabulate(data, headers=["hidden layers", "trials done"]))
        """

        data = dict(
            tabular_data=list(csv.reader(f)),
            headers=["hidden features", "hidden layers", "trials done"],
            # tablefmt='fancy_grid'
            )
        print(tabulate.tabulate(**data))
        pass
    pass